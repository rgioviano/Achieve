#!/usr/bin/env python3
"""Penny <-> Tally lead handoff through files on the box (no chat messages).

Folder: /home/box/agent-data/shared/handoffs/penny-tally/  (override with --dir)
  due/YYYY-MM-DD.json + .md   Tally's follow-up due list for that day (one file per day, rewritten on rerun)
  sends/YYYY-MM-DD.jsonl      Penny's actual sends (one JSON line per send, deduped)

Subcommands
  post-due     (Tally)  build today's due list from a 2026-tab export with followup_due.py and write due/<day>.*
                        --hold KEY=REASON marks a lead HELD (KEY = email, phone or sheet row) after pre-draft check.
  read-due     (Penny)  print the due list for --date (default today). Exit 3 if that day's file is missing.
  log-send     (Penny)  record one send that Ryne actually made (email sent / text sent). Never logs drafts.
  read-sends   (Tally)  print sends since --since (default yesterday), so Tally updates Last Contact / Next Follow-Up.
  triage-leads (Tally)  print lead_form items from Penny's inbox_triage output (penny/triage/*-<day>.json).

Read/write only inside the handoff folder. Never touches Gmail, Quo, the Sheet or any chat.
Python 3 stdlib only. Times are America/Chicago.
"""
import argparse, datetime as dt, glob, json, os, sys, zoneinfo

CT = zoneinfo.ZoneInfo("America/Chicago")
BASE = "/home/box/agent-data/shared/handoffs/penny-tally"
TRIAGE = "/home/box/agent-data/penny/triage"
FOLLOWUP = "/home/box/agent-data/shared/scripts/tally"


def today_ct():
    return dt.datetime.now(CT).date()


def day(s):
    if not s:
        return today_ct()
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        raise SystemExit(f"bad date {s!r} (use YYYY-MM-DD)")


def norm_phone(p):
    d = "".join(c for c in (p or "") if c.isdigit())
    return d[-10:] if len(d) >= 10 else d


def key_matches(item, key):
    k = key.strip().lower()
    if not k:
        return False
    if k.isdigit() and len(k) < 6:
        return str(item.get("row")) == k
    if "@" in k:
        return (item.get("email") or "").strip().lower() == k
    return norm_phone(item.get("phone")) == norm_phone(k) != ""


def render_due(res):
    out = [f"# Lead follow-up due list {res['today']} (CT), posted by Tally {res['posted_at']}",
           f"{len(res['due'])} ready to draft, {len(res['held'])} held. Penny: draft only the READY items; log real sends with log-send.", ""]
    out.append("## READY")
    for n, x in enumerate(res["due"], 1):
        step = f"step {x['step']} (day {x['step_day']})" if x.get("step_day") else f"step {x.get('step') or '?'}"
        out.append(f"{n}. {x['name']} | {x.get('email') or '-'} | {x.get('phone') or '-'} | {step} | "
                   f"next {x['next_followup']} | last {x.get('last_contact') or '-'} | {x.get('service_type') or '-'} | "
                   f"asked: {x.get('asked_about') or '-'} [row {x['row']}]")
    if not res["due"]:
        out.append("(none)")
    out += ["", "## HELD (do not draft)"]
    for x in res["held"]:
        out.append(f"- {x['name']} | {x.get('email') or '-'} | {x.get('phone') or '-'} | {x['held_reason']} [row {x['row']}]")
    if not res["held"]:
        out.append("(none)")
    for b in res.get("bad_dates", []):
        out.append(f"BAD DATE row {b['row']} {b['name']}: {b['value']!r} (Tally fixes on the Sheet)")
    return "\n".join(out) + "\n"


def write_atomic(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.replace(tmp, path)


def cmd_post_due(a):
    sys.path.insert(0, FOLLOWUP)
    import followup_due as fd
    d = day(a.today)
    res = fd.build(fd.load_rows(a.sheet), d)
    holds = []
    for h in a.hold or []:
        if "=" not in h:
            raise SystemExit(f"--hold needs KEY=REASON, got {h!r}")
        k, r = h.split("=", 1)
        holds.append((k, r.strip()))
    ready, held = [], []
    for x in res["due"]:
        hit = next((r for k, r in holds if key_matches(x, k)), None)
        if hit:
            held.append(dict(x, held_reason=f"pre-draft check: {hit}"))
        else:
            ready.append(x)
    held += res["held_replied"]
    unmatched = [k for k, _ in holds if not any(key_matches(x, k) for x in res["due"])]
    out = {"today": d.isoformat(), "posted_at": dt.datetime.now(CT).strftime("%Y-%m-%d %H:%M CT"),
           "due": ready, "held": held, "bad_dates": res["bad_dates"], "notes": res["notes"],
           "unmatched_holds": unmatched}
    os.makedirs(os.path.join(a.dir, "due"), exist_ok=True)
    base = os.path.join(a.dir, "due", d.isoformat())
    write_atomic(base + ".json", json.dumps(out, indent=1))
    write_atomic(base + ".md", render_due(out))
    print(f"wrote {base}.json and .md: {len(ready)} ready, {len(held)} held")
    if unmatched:
        print("WARNING --hold keys matched no due lead: " + ", ".join(unmatched))
    return 0


def cmd_read_due(a):
    d = day(a.date)
    path = os.path.join(a.dir, "due", d.isoformat() + ".md")
    if not os.path.exists(path):
        have = sorted(glob.glob(os.path.join(a.dir, "due", "*.md")))
        last = os.path.basename(have[-1])[:-3] if have else "none"
        print(f"NO DUE LIST for {d} (latest on disk: {last}). Tally's run may have missed; say so in the brief, do not guess.")
        return 3
    sys.stdout.write(open(path, encoding="utf-8").read())
    return 0


def load_sends(dirpath, since):
    out = []
    for p in sorted(glob.glob(os.path.join(dirpath, "sends", "*.jsonl"))):
        if os.path.basename(p)[:10] < since.isoformat():
            continue
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def cmd_log_send(a):
    if not (a.email or a.phone):
        raise SystemExit("log-send needs --email or --phone")
    d = day(a.sent_date)
    rec = {"name": a.name, "email": (a.email or "").strip().lower(), "phone": norm_phone(a.phone),
           "channel": a.channel, "sent_date": d.isoformat(), "step": a.step, "row": a.row,
           "draft_id": a.draft_id or "", "note": a.note or "",
           "logged_at": dt.datetime.now(CT).strftime("%Y-%m-%d %H:%M CT")}
    os.makedirs(os.path.join(a.dir, "sends"), exist_ok=True)
    path = os.path.join(a.dir, "sends", d.isoformat() + ".jsonl")
    for r in load_sends(a.dir, d):
        if r["sent_date"] == rec["sent_date"] and r["channel"] == rec["channel"] and (
                (rec["email"] and r["email"] == rec["email"]) or (rec["phone"] and r["phone"] == rec["phone"])):
            print(f"already logged: {r['name']} {r['channel']} {r['sent_date']} (no change)")
            return 0
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(f"logged send: {rec['name']} {rec['channel']} {rec['sent_date']} -> {path}")
    return 0


def cmd_read_sends(a):
    since = day(a.since) if a.since else today_ct() - dt.timedelta(days=1)
    rows = load_sends(a.dir, since)
    if a.json:
        print(json.dumps(rows, indent=1))
        return 0
    print(f"Penny sends since {since} (CT): {len(rows)}")
    for r in rows:
        print(f"- {r['sent_date']} {r['channel']} | {r['name']} | {r['email'] or '-'} | {r['phone'] or '-'} | "
              f"step {r['step'] if r['step'] is not None else '?'} | row {r['row'] or '?'}" + (f" | {r['note']}" if r['note'] else ""))
    return 0


def cmd_triage_leads(a):
    d = day(a.date)
    files = sorted(glob.glob(os.path.join(a.triage, f"*-{d.isoformat()}.json")))
    if not files:
        print(f"NO TRIAGE FILE for {d} in {a.triage} (Penny's 6:15 triage may not have run). Fall back to Gmail search.")
        return 3
    items = []
    for p in files:
        j = json.load(open(p, encoding="utf-8"))
        items += j.get("buckets", {}).get("lead_form", [])
    print(f"lead_form items in Penny triage {d}: {len(items)} (files: {', '.join(os.path.basename(f) for f in files)})")
    for x in items:
        print(f"- {x.get('account')} | {x.get('date')} | {x.get('from')} | {x.get('subject')} | thread {x.get('threadId')} | {x.get('rule')}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=BASE)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("post-due"); p.add_argument("--sheet", required=True); p.add_argument("--today")
    p.add_argument("--hold", action="append", metavar="KEY=REASON")
    p = sp.add_parser("read-due"); p.add_argument("--date")
    p = sp.add_parser("log-send"); p.add_argument("--name", required=True); p.add_argument("--email"); p.add_argument("--phone")
    p.add_argument("--channel", choices=["email", "text"], required=True); p.add_argument("--sent-date")
    p.add_argument("--step", type=int); p.add_argument("--row", type=int); p.add_argument("--draft-id"); p.add_argument("--note")
    p = sp.add_parser("read-sends"); p.add_argument("--since"); p.add_argument("--json", action="store_true")
    p = sp.add_parser("triage-leads"); p.add_argument("--date"); p.add_argument("--triage", default=TRIAGE)
    a = ap.parse_args(argv)
    return {"post-due": cmd_post_due, "read-due": cmd_read_due, "log-send": cmd_log_send,
            "read-sends": cmd_read_sends, "triage-leads": cmd_triage_leads}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
