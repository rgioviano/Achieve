#!/usr/bin/env python3
"""inbox_triage.py: first-pass sort of Ryne's inbox mail into buckets for Penny. Sorts only.

Read-only. Python 3 standard library only. Calls no API: it never reads Gmail itself and never
labels, archives, marks, moves or deletes anything. Penny pulls the mail read-only with her Gmail
connectors, saves the JSON, runs this, then does the judgment work (reading, drafting) herself.

Buckets (output order comes from bucket_order in the rules file):
  lead_form         Lead Form / new inquiry (WordPress "Lead Form -", Yelp lead messages, a new person
                    asking about training, a staff forward of one). Hand to Tally.
  payment_alert     AutoPay failed / payment alert (Mindbody "Automatic Payment ... Has Failed", or a
                    personal-finance "payment will fail" warning; scope says which).
  client_reply      A parent / client / lead writing back who needs Ryne (holds, pauses, plan changes,
                    injuries, paperwork or pricing questions, plain thank-yous flagged ack_only).
  scheduling        Booking only: eval confirm / request, reschedule, switch time, waitlist, calendar
                    accept/decline. Anything more than a time goes to client_reply.
  fyi_notification  Receipts, bank/vendor notices, Mindbody copies, porting status, student requests.
  security_alert    Suspicious login, new sign-in, Takeout, password reset, MFA, codes, new app access.
  promo_junk        Newsletters, promos, cold sales pitches.
  unknown           No rule matched or needs a human read (staff notes, vendor support tickets).

Rules live in inbox_triage_rules.json next to this file (override with --rules). Rules are tried in
order; the first match wins. See README.md for the rule fields.

Input: JSON list of messages, or {"messages": [...]}, or several files (each may set "account" at the
top level). Message fields: id, threadId, from (or sender), to, subject, date, snippet and/or body
(body wins when present), labelIds (or labels), optional account (work, contact, personal,
ironblueprint). Connector wrapper text before the first "{"/"[" is ignored.

Usage:
  python3 inbox_triage.py pull_work.json pull_contact.json            # JSON grouped by bucket
  python3 inbox_triage.py --format text pull_*.json                   # readable summary
  python3 inbox_triage.py --account work pull.json                    # default account when missing
  python3 inbox_triage.py --rules my_rules.json --out result.json pull.json
Exit code: 0 nothing to act on, 1 items in an actionable bucket (actionable_buckets in the rules),
2 error (bad input or rules; report it, do not guess).
"""
import argparse, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RULES = os.path.join(HERE, "inbox_triage_rules.json")
BUCKETS = ["lead_form", "payment_alert", "client_reply", "scheduling", "fyi_notification",
           "security_alert", "promo_junk", "unknown"]
RULE_KEYS = {"id", "bucket", "why", "sender", "from_re", "from_not_re", "subject_re", "subject_not_re",
             "text_re", "text_all_re", "text_not_re", "raw_re", "raw_not_re", "is_reply", "is_forward", "labels_any",
             "account_any", "set"}
REPLY_RX = re.compile(r"^\s*(re|aw)\s*:", re.I)
FWD_RX = re.compile(r"^\s*(fw|fwd)\s*:", re.I)
PREFIX_RX = re.compile(r"^\s*((re|aw|fw|fwd)\s*:\s*)+", re.I)
ADDR_RX = re.compile(r"[\w.+'-]+@[\w-]+(?:\.[\w-]+)+")


class TriageError(Exception):
    pass


def _compile(lst, where):
    out = []
    for p in lst or []:
        try:
            out.append(re.compile(p, re.I | re.S))
        except re.error as e:
            raise TriageError(f"bad regex in {where}: {p!r}: {e}")
    return out


def load_rules(path):
    try:
        with open(path, encoding="utf-8") as fh:
            cfg = json.load(fh)
    except (OSError, ValueError) as e:
        raise TriageError(f"cannot read rules {path}: {e}")
    for k in ("rules", "self_addresses", "bucket_order", "actionable_buckets"):
        if k not in cfg:
            raise TriageError(f"rules file missing '{k}'")
    for b in cfg["bucket_order"] + cfg["actionable_buckets"]:
        if b not in BUCKETS:
            raise TriageError(f"unknown bucket '{b}' in bucket_order/actionable_buckets")
    cfg["self_addresses"] = {a.lower() for a in cfg["self_addresses"]}
    cfg["staff_addresses"] = {a.lower() for a in cfg.get("staff_addresses", [])}
    cfg["staff_domains"] = {d.lower() for d in cfg.get("staff_domains", [])}
    cfg["_automated"] = _compile(cfg.get("automated_from_re"), "automated_from_re")
    cfg["_quote"] = _compile(cfg.get("quote_markers_re"), "quote_markers_re")
    cfg["_ack"] = _compile(cfg.get("ack_re"), "ack_re")
    seen = set()
    for i, r in enumerate(cfg["rules"]):
        rid = r.get("id") or f"rule{i}"
        bad = set(r) - RULE_KEYS
        if bad:
            raise TriageError(f"rule {rid}: unknown field(s) {sorted(bad)}")
        if r.get("bucket") not in BUCKETS:
            raise TriageError(f"rule {rid}: bucket must be one of {BUCKETS}")
        if rid in seen:
            raise TriageError(f"duplicate rule id {rid}")
        seen.add(rid)
        for k in ("from_re", "from_not_re", "subject_re", "subject_not_re", "text_re", "text_all_re", "text_not_re",
                  "raw_re", "raw_not_re"):
            r["_" + k] = _compile(r.get(k), f"rule {rid}.{k}")
    return cfg


def _json_from_text(t):
    t = t.strip()
    if not t:
        return []
    starts = [i for i in (t.find("{"), t.find("[")) if i >= 0]
    if not starts:
        raise TriageError("no JSON found")
    obj, _ = json.JSONDecoder().raw_decode(t[min(starts):])
    return obj


def load_messages(paths, default_account=None):
    msgs = []
    for p in paths:
        try:
            with open(p, encoding="utf-8") as fh:
                obj = _json_from_text(fh.read())
        except (OSError, ValueError) as e:
            raise TriageError(f"cannot read {p}: {e}")
        acct = default_account
        if isinstance(obj, dict):
            acct = obj.get("account", acct)
            obj = obj.get("messages", None)
        if not isinstance(obj, list):
            raise TriageError(f"{p}: expected a list of messages or {{\"messages\": [...]}}")
        for m in obj:
            if not isinstance(m, dict) or not m.get("id"):
                raise TriageError(f"{p}: every message needs an id")
            m = dict(m)
            if not m.get("account"):
                m["account"] = acct
            msgs.append(m)
    return msgs


def address(frm):
    m = ADDR_RX.search(frm or "")
    return m.group(0).lower() if m else (frm or "").strip().lower()


def fresh_text(text, cfg):
    """The new part of a reply: cut at the first quote marker (On ... wrote:, From: Ryne ..., etc.)."""
    cut = len(text)
    for rx in cfg["_quote"]:
        m = rx.search(text)
        if m and m.start() < cut:
            cut = m.start()
    return text[:cut].strip()


def sender_type(frm, cfg):
    addr = address(frm)
    if addr in cfg["self_addresses"]:
        return "self"
    if any(rx.search(frm or "") for rx in cfg["_automated"]):
        return "automated"
    if addr in cfg["staff_addresses"] or addr.split("@")[-1] in cfg["staff_domains"]:
        return "staff"
    return "human"


def features(m, cfg):
    frm = m.get("from") or m.get("sender") or ""
    subj = html.unescape(m.get("subject") or "")
    raw = m.get("body") or m.get("text") or m.get("snippet") or ""
    raw = html.unescape(raw).replace("\u200c", " ").replace("\u034f", " ")
    raw = re.sub(r"\s+", " ", raw)
    fresh = fresh_text(raw, cfg)
    labels = m.get("labelIds") or m.get("labels") or []
    return {
        "from": frm, "from_l": frm.lower(), "subject": subj,
        "text": (PREFIX_RX.sub("", subj) + " \n " + fresh), "fresh": fresh, "raw": subj + " \n " + raw,
        "sender": sender_type(frm, cfg), "is_reply": bool(REPLY_RX.match(subj)),
        "is_forward": bool(FWD_RX.match(subj)), "labels": set(labels), "account": m.get("account"),
    }


def rule_matches(r, f):
    if "sender" in r and f["sender"] not in r["sender"]:
        return False
    if "is_reply" in r and f["is_reply"] != r["is_reply"]:
        return False
    if "is_forward" in r and f["is_forward"] != r["is_forward"]:
        return False
    if "labels_any" in r and not (f["labels"] & set(r["labels_any"])):
        return False
    if "account_any" in r and f["account"] not in r["account_any"]:
        return False
    if r["_from_re"] and not any(rx.search(f["from_l"]) for rx in r["_from_re"]):
        return False
    if any(rx.search(f["from_l"]) for rx in r["_from_not_re"]):
        return False
    if r["_subject_re"] and not any(rx.search(f["subject"]) for rx in r["_subject_re"]):
        return False
    if any(rx.search(f["subject"]) for rx in r["_subject_not_re"]):
        return False
    if r["_text_re"] and not any(rx.search(f["text"]) for rx in r["_text_re"]):
        return False
    if r["_text_all_re"] and not all(rx.search(f["text"]) for rx in r["_text_all_re"]):
        return False
    if any(rx.search(f["text"]) for rx in r["_text_not_re"]):
        return False
    if r["_raw_re"] and not any(rx.search(f["raw"]) for rx in r["_raw_re"]):
        return False
    if any(rx.search(f["raw"]) for rx in r["_raw_not_re"]):
        return False
    return True


def classify(m, cfg):
    f = features(m, cfg)
    item = {"id": m.get("id"), "threadId": m.get("threadId"), "account": f["account"], "from": f["from"],
            "subject": f["subject"], "date": m.get("date"), "sender_type": f["sender"]}
    for r in cfg["rules"]:
        if rule_matches(r, f):
            item["bucket"], item["rule"] = r["bucket"], r["id"]
            if r.get("why"):
                item["why"] = r["why"]
            item.update(r.get("set", {}))
            break
    else:
        item["bucket"], item["rule"] = "unknown", "no_rule_matched"
    if item["bucket"] == "client_reply":
        words = len(f["fresh"].split())
        if (words <= cfg.get("ack_max_words", 15) and "?" not in f["fresh"]
                and any(rx.search(f["fresh"]) for rx in cfg["_ack"])):
            item["ack_only"] = True
    return item


def triage(msgs, cfg):
    items = [classify(m, cfg) for m in msgs]
    out = {b: [] for b in cfg["bucket_order"]}
    for b in BUCKETS:
        out.setdefault(b, [])
    for it in items:
        out[it["bucket"]].append(it)
    counts = {b: len(v) for b, v in out.items()}
    by_acct = {}
    for it in items:
        by_acct[it["account"] or "unset"] = by_acct.get(it["account"] or "unset", 0) + 1
    act = sum(counts[b] for b in cfg["actionable_buckets"])
    return {"total": len(items), "by_account": by_acct, "counts": counts, "actionable": act,
            "actionable_buckets": cfg["actionable_buckets"], "buckets": out}


def as_text(res):
    lines = [f"{res['total']} messages ({', '.join(f'{k} {v}' for k, v in res['by_account'].items())}); "
             f"{res['actionable']} to act on"]
    for b, items in res["buckets"].items():
        if not items:
            continue
        lines.append(f"\n== {b} ({len(items)})")
        for it in items:
            extra = []
            if it.get("scope"):
                extra.append(it["scope"])
            if it.get("ack_only"):
                extra.append("ack only")
            ex = f" [{', '.join(extra)}]" if extra else ""
            lines.append(f"- [{it['account']}] {it['from'][:50]} | {it['subject'][:70]} | {it['rule']}{ex} | {it['id']}")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Sort exported Gmail messages into triage buckets (read-only).")
    ap.add_argument("files", nargs="+", help="message JSON file(s)")
    ap.add_argument("--rules", default=DEFAULT_RULES)
    ap.add_argument("--account", help="account for messages that do not name one (work, contact, personal, ironblueprint)")
    ap.add_argument("--format", choices=["json", "text"], default="json")
    ap.add_argument("--out", help="also write the JSON result here")
    a = ap.parse_args(argv)
    cfg = load_rules(a.rules)
    msgs = load_messages(a.files, a.account)
    if not msgs:
        print("0 messages")
        return 0
    res = triage(msgs, cfg)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1, ensure_ascii=False)
    print(as_text(res) if a.format == "text" else json.dumps(res, indent=1, ensure_ascii=False))
    return 1 if res["actionable"] else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except TriageError as e:
        print(f"inbox_triage error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:  # noqa: BLE001
        print(f"inbox_triage error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)
