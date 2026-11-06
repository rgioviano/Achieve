#!/usr/bin/env python3
"""Lead follow-up due list for the Prospect Tracking 2026 tab (Tally).

Read-only. Python 3 standard library only. Never sends, drafts or writes anything.

Schedule (Ryne, 10/22/26 per Chief): follow-ups on day 2, 5, 9, 14, 21, 30 after the FIRST
outreach send date. After the day-30 touch with no reply the lead is parked. Any reply,
booking or sign-up stops the schedule.

A row is DUE when Next Follow-Up <= --today and Stage is not replied / booked / signed / parked
(case-insensitive substring match, so "Eval booked", "Signed", "PARKED" all stop it).
Rows whose Stage is lost/dead are also skipped (closed). The summary table (first row with a
cell saying AVERAGES, any column/case) and everything below it, plus blank rows, are ignored.

Stage meanings (10/23/26): "Contacted" = Achieve has sent outreach, no reply from the lead (stays in
the schedule). "Replied" = the LEAD replied (stops the schedule). Rows that are due by date but stopped
only by a Replied stage are still printed in a short HELD section as a cross-check, not in the due list.

Parked is never due. A reply, booking or sign-up takes a lead off Parked (stage_after_event); any
newer Stage overrides Parked. Only leads WITH an email address may be parked; --park-candidates lists
them (and no-email rows separately) read-only.
Parked: the script never writes. A row whose Contact Count is past the day-30 step is flagged with a
NOTE only; whether to park (or newsletter) leads after day 30 is Ryne's call, so nothing sets Parked.

Input: an export of the live 2026 tab (header row first). Accepted formats:
  * CSV file
  * Sheets values JSON {"values": [[...], ...]}
  * the Google-sheets connector read_range output {"ranges": [{"content": "<csv>"}]}
    (any wrapper text before the first "{" / after the last "}" is ignored)

Get the export (Tally, user-Google-sheets--achieve):
  read_range spreadsheetId=1x8KurT1AJOPYLca6Jz9f_zBqZ3yBUGv8-isf8pctv4g
             ranges=[{"sheet":"2026","cells":"A1:P400"}] maxChars=250000 write_to_file=true
Then:
  python3 followup_due.py --sheet <export file> [--today 2026-10-22] [--json]

Helper (also importable):
  python3 followup_due.py --next 10/21/26 --step 0     # step just completed -> next date or parked
  step 0 = first outreach sent; step 1..6 = day 2,5,9,14,21,30 follow-up sent.

Exit codes: 0 ran (due list may be empty), 2 script error (bad/empty export, missing column).
"""
import argparse, csv, datetime as dt, io, json, re, sys, zoneinfo

SCHEDULE = [2, 5, 9, 14, 21, 30]
STOP_WORDS = ("replied", "reply", "booked", "signed", "sign-up", "signup", "parked")
CLOSED_WORDS = ("lost", "dead")
NEEDED = ["Last Name", "First Name", "Stage", "Contact Count", "Email Address",
          "Phone Number", "Service Type", "Comments", "Next Follow-Up"]
CT = zoneinfo.ZoneInfo("America/Chicago")


class InputError(Exception):
    pass


def parse_date(s):
    """m/d/yy, m/d/yyyy or yyyy-mm-dd -> date; '' / unparseable -> None."""
    if s is None:
        return None
    if isinstance(s, (dt.date, dt.datetime)):
        return s if isinstance(s, dt.date) and not isinstance(s, dt.datetime) else s.date()
    s = str(s).strip()
    if not s:
        return None
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{2}|\d{4})", s)
    if m:
        mo, d, y = int(m[1]), int(m[2]), int(m[3])
        if y < 100:
            y += 2000
        try:
            return dt.date(y, mo, d)
        except ValueError:
            return None
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        try:
            return dt.date(int(m[1]), int(m[2]), int(m[3]))
        except ValueError:
            return None
    return None


def fmt_date(d):
    """Sheet style: 10/21/26."""
    return f"{d.month}/{d.day}/{d.year % 100:02d}"


def next_followup(first_send, step_done):
    """Next follow-up date after `step_done`, or 'parked'.

    first_send: date or 'm/d/yy' string of the first outreach send.
    step_done: 0 = first outreach sent, 1..6 = the day 2/5/9/14/21/30 follow-up sent.
    """
    d = parse_date(first_send)
    if d is None:
        raise ValueError(f"bad first send date: {first_send!r}")
    step_done = int(step_done)
    if step_done < 0:
        raise ValueError("step_done must be >= 0")
    if step_done >= len(SCHEDULE):
        return "parked"
    return d + dt.timedelta(days=SCHEDULE[step_done])


def stage_stops(stage):
    s = (stage or "").strip().lower()
    return any(w in s for w in STOP_WORDS)


def stage_closed(stage):
    s = (stage or "").strip().lower()
    return any(w in s for w in CLOSED_WORDS)


EVENT_STAGE = {"reply": "Replied", "booked": "Eval booked", "signed": "Signed"}


def stage_after_event(stage, event):
    """Stage after an event. A reply, booking or sign-up always overrides the current Stage,
    including Parked (it takes the lead off Parked). Any other event (e.g. 'send') keeps it."""
    return EVENT_STAGE.get((event or "").strip().lower(), stage)


def is_parked(stage):
    return "parked" in (stage or "").strip().lower()


def first_send_from(row_get):
    """First outreach send date for a row: the earliest m/d date after 'Gmail: N Ryne email(s)' in Comments
    (the re-tag note format), else None. Year is taken from Contact Date (or Last Contact)."""
    c = row_get("Comments")
    m = re.search(r"Gmail:\s*(\d+)\s+Ryne emails?\s+([0-9/ ,]+)", c)
    if not m:
        return None, None
    base = parse_date(row_get("Contact Date")) or parse_date(row_get("Last Contact"))
    year = base.year if base else None
    dates = []
    for md in re.findall(r"(\d{1,2})/(\d{1,2})", m.group(2)):
        if year:
            try:
                dates.append(dt.date(year, int(md[0]), int(md[1])))
            except ValueError:
                pass
    return (min(dates) if dates else None), int(m.group(1))


def park_candidates(rows, today, first_sends=None):
    """Read-only. BY-DATE rule (Ryne via Chief/Tally 10/23): no reply on record, an email address, and
    first outreach send more than 30 days before `today`. "No reply on record" = Stage Contacted, OR
    Stage blank with an evidenced send (a first_sends entry or a 'Gmail: N Ryne emails ...' Comments note)
    and no reply flagged in first_sends (Tally 10/23). Blank-Stage rows with no evidenced send are ignored
    (never contacted, nothing to park). The normal path is still the touch-count rule in the due list.
    No-email rows are only listed, never parked.
    first_sends: optional {email_lower: date | {"first_send": date, "sends": n, "replied": bool}} from a
    Gmail export (--sends-json); otherwise read from the Comments note. A lead flagged replied goes to
    skipped_replied, never parked. Contacted rows with no known first send are listed as unknown.
    Never writes anything."""
    header, body = rows[0], rows[1:]
    h = header_map(header)
    g = lambda r, name: (r[h[name.lower()]].strip() if name.lower() in h and h[name.lower()] < len(r) else "")
    out = {"park_with_email": [], "no_email_listed": [], "already_parked_with_email": [], "unknown_first_send": [],
           "skipped_replied": []}
    for i, r in enumerate(body, start=2):
        if any(str(c).strip().upper() == "AVERAGES" for c in r):
            break
        if not (g(r, "Last Name") or g(r, "First Name")):
            continue
        stage = g(r, "Stage")
        item = {"row": i, "name": f"{g(r,'First Name')} {g(r,'Last Name')}".strip(),
                "email": g(r, "Email Address"), "stage": stage}
        if is_parked(stage):
            (out["already_parked_with_email"] if item["email"] else out["no_email_listed"]).append(item)
            continue
        st = stage.strip().lower()
        if st not in ("contacted", ""):   # only leads with no reply on record (Contacted, or blank Stage)
            continue
        fs, n, replied = (None, None, False)
        ev = first_sends.get(item["email"].lower()) if (first_sends and item["email"]) else None
        if ev is not None:
            if isinstance(ev, dict):
                fs = ev.get("first_send")
                n, replied = ev.get("sends"), bool(ev.get("replied"))
            else:
                fs = ev
            if isinstance(fs, str):
                fs = parse_date(fs)
        else:
            fs, n = first_send_from(lambda name: g(r, name))
        if st == "" and fs is None:       # blank Stage, no evidenced send: not contacted, nothing to park
            continue
        item["first_send"] = fmt_date(fs) if fs else ""
        item["sends"] = n
        if replied:
            out["skipped_replied"].append(item)
            continue
        if fs is None:
            out["unknown_first_send"].append(item)
            continue
        if (today - fs).days <= 30:
            continue
        item["days_since_first_send"] = (today - fs).days
        (out["park_with_email"] if item["email"] else out["no_email_listed"]).append(item)
    return out


def load_sends(path):
    """Read a --sends-json file: {email: date-string | {"first_send", "sends", "replied"}} -> lowercased keys."""
    with open(path) as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise InputError(f"{path}: expected a JSON object keyed by email")
    return {k.strip().lower(): v for k, v in data.items()}


def months_ago(d, n=12):
    """Same calendar day n months earlier (Feb 29 -> Feb 28)."""
    y, m = divmod(d.month - 1 - n, 12)
    y, m = d.year + y, m + 1
    for day in (d.day, 30, 29, 28):
        try:
            return dt.date(y, m, day)
        except ValueError:
            continue


def newsletter_list(rows, today):
    """Read-only. Achieve Minute list (Ryne via Chief 10/23): Parked rows WITH an email whose Contact Date
    is within the last 12 months of `today` (Contact Date >= same day 12 months ago, inclusive).
    Older Parked rows stay Parked but are left off; a missing/unreadable Contact Date is left off too
    (age unknown); Parked rows with no email are left off. Never writes anything."""
    header, body = rows[0], rows[1:]
    h = header_map(header)
    g = lambda r, name: (r[h[name.lower()]].strip() if name.lower() in h and h[name.lower()] < len(r) else "")
    cutoff = months_ago(today, 12)
    out = {"cutoff": cutoff.isoformat(), "on_list": [], "off_older": [], "off_no_contact_date": [], "off_no_email": []}
    for i, r in enumerate(body, start=2):
        if any(str(c).strip().upper() == "AVERAGES" for c in r):
            break
        if not (g(r, "Last Name") or g(r, "First Name")) or not is_parked(g(r, "Stage")):
            continue
        item = {"row": i, "name": f"{g(r,'First Name')} {g(r,'Last Name')}".strip(),
                "email": g(r, "Email Address"), "contact_date": g(r, "Contact Date")}
        if not item["email"]:
            out["off_no_email"].append(item)
            continue
        cd = parse_date(item["contact_date"])
        if cd is None:
            out["off_no_contact_date"].append(item)
        elif cd < cutoff:
            out["off_older"].append(item)
        else:
            out["on_list"].append(item)
    return out


def load_rows(path):
    if path == "-":
        raw = sys.stdin.read()
    else:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
    if not raw.strip():
        raise InputError("empty export (empty is not zero)")
    txt = raw.strip()
    rows = None
    if "{" in txt and ("\"values\"" in txt or "\"ranges\"" in txt):
        j = json.loads(txt[txt.index("{"): txt.rindex("}") + 1])
        if "values" in j:
            rows = [[("" if c is None else str(c)) for c in r] for r in j["values"]]
        elif "ranges" in j:
            content = j["ranges"][0].get("content", "")
            rows = list(csv.reader(io.StringIO(content)))
    if rows is None:
        rows = list(csv.reader(io.StringIO(raw)))
    if not rows:
        raise InputError("no rows in export")
    return rows


def header_map(header):
    h = {c.strip().lower(): i for i, c in enumerate(header)}
    missing = [n for n in NEEDED if n.lower() not in h]
    if missing:
        raise InputError("missing column(s): " + ", ".join(missing) + " (header: " + " | ".join(header) + ")")
    return h


def asked_about(comments, n=110):
    c = (comments or "").strip()
    if not c:
        return ""
    parts = [p.strip() for p in re.split(r"(?<=[.;])\s+", c) if p.strip()]
    keep = []
    for p in parts:
        if re.match(r"^(parent|contacts?:)\b", p, re.I):
            continue
        keep.append(p)
        if len(" ".join(keep)) >= 60:
            break
    s = " ".join(keep) or c
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def step_number(contact_count):
    """Follow-up step due next: Contact Count touches done -> step = count (1..6). None if blank."""
    try:
        n = int(float(str(contact_count).strip()))
    except (ValueError, TypeError):
        return None
    return n if n >= 1 else None


def build(rows, today):
    header, body = rows[0], rows[1:]
    h = header_map(header)
    g = lambda r, name: (r[h[name.lower()]].strip() if h[name.lower()] < len(r) else "")
    due, held, bad, notes = [], [], [], []
    for i, r in enumerate(body, start=2):
        if any(str(c).strip().upper() == "AVERAGES" for c in r):
            notes.append(f"stopped at sheet row {i} (AVERAGES summary table)")
            break
        if not any(str(c).strip() for c in r):
            continue
        if not (g(r, "Last Name") or g(r, "First Name")):
            continue
        nf_raw = g(r, "Next Follow-Up")
        if not nf_raw:
            continue
        stage = g(r, "Stage")
        nf = parse_date(nf_raw)
        if nf is None:
            if nf_raw.strip().lower() == "parked":
                continue
            bad.append({"row": i, "name": f"{g(r,'First Name')} {g(r,'Last Name')}".strip(), "value": nf_raw})
            continue
        if nf > today or stage_closed(stage):
            continue
        step = step_number(g(r, "Contact Count"))
        item = {
            "row": i,
            "name": f"{g(r,'First Name')} {g(r,'Last Name')}".strip(),
            "email": g(r, "Email Address"),
            "phone": g(r, "Phone Number"),
            "step": step,
            "step_day": SCHEDULE[step - 1] if step and step <= len(SCHEDULE) else None,
            "next_followup": fmt_date(nf),
            "days_overdue": (today - nf).days,
            "last_contact": g(r, "Last Contact") if "last contact" in h else "",
            "stage": stage,
            "service_type": g(r, "Service Type"),
            "asked_about": asked_about(g(r, "Comments")),
        }
        if step and step > len(SCHEDULE):
            item["note"] = "Contact Count past the day-30 step: after-day-30 handling is Ryne's call (do not park)"
        if stage_stops(stage):
            if "replied" in stage.lower() or "reply" in stage.lower():
                item["held_reason"] = f"Stage '{stage}' (lead replied) stops the schedule"
                held.append(item)
            continue
        due.append(item)
    due.sort(key=lambda x: (-x["days_overdue"], x["row"]))
    return {"today": today.isoformat(), "due": due, "held_replied": held, "bad_dates": bad, "notes": notes}


def render(res):
    out = [f"Follow-up due list for {res['today']} (America/Chicago): {len(res['due'])} due"]
    for n, x in enumerate(res["due"], 1):
        step = f"step {x['step']} (day {x['step_day']})" if x["step_day"] else (f"step {x['step']}" if x["step"] else "step ? (Contact Count blank)")
        od = "due today" if x["days_overdue"] == 0 else f"{x['days_overdue']}d overdue"
        out.append(f"{n}. {x['name']} | {x['email'] or '-'} | {x['phone'] or '-'} | {step} | "
                   f"next {x['next_followup']} ({od}) | last {x['last_contact'] or '-'} | {x['service_type'] or '-'} | "
                   f"Stage {x['stage'] or '-'} | asked: {x['asked_about'] or '-'} [row {x['row']}]"
                   + (f" | NOTE {x['note']}" if x.get("note") else ""))
    if res["held_replied"]:
        out.append(f"HELD, due by date but Stage says Replied, i.e. the lead replied ({len(res['held_replied'])}):")
        for x in res["held_replied"]:
            out.append(f"- {x['name']} | {x['email'] or '-'} | next {x['next_followup']} | Stage {x['stage']} [row {x['row']}]")
    for b in res["bad_dates"]:
        out.append(f"BAD DATE row {b['row']} {b['name']}: Next Follow-Up {b['value']!r}")
    out += [f"note: {n}" for n in res["notes"]]
    out.append("Reminder: run the 48h no-touch check (pre_draft_check.py) on each item before drafting.")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sheet", help="export of the live 2026 tab (CSV / values JSON / read_range JSON)")
    ap.add_argument("--today", help="YYYY-MM-DD or m/d/yy (default: today in America/Chicago)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--park-candidates", action="store_true",
                    help="read-only: Contacted (or blank-Stage with an evidenced send) leads with first send > 30 days before --today (by-date rule), split with/without email")
    ap.add_argument("--sends-json", metavar="FILE",
                    help='with --park-candidates: Gmail evidence {email: {"first_send": "YYYY-MM-DD", "sends": n, "replied": bool}}')
    ap.add_argument("--newsletter-list", action="store_true",
                    help="read-only: Parked rows with an email and Contact Date within 12 months of --today")
    ap.add_argument("--next", metavar="FIRST_SEND", help="helper: first send date")
    ap.add_argument("--step", type=int, help="helper: step just completed (0 = first outreach)")
    a = ap.parse_args(argv)
    try:
        if a.next is not None:
            if a.step is None:
                raise InputError("--next needs --step")
            r = next_followup(a.next, a.step)
            print(r if r == "parked" else fmt_date(r))
            return 0
        if not a.sheet:
            raise InputError("--sheet is required")
        if a.newsletter_list:
            today = parse_date(a.today) if a.today else dt.datetime.now(CT).date()
            nl = newsletter_list(load_rows(a.sheet), today)
            if a.json:
                print(json.dumps(nl, indent=1))
            else:
                print(f"Achieve Minute list ({today.isoformat()}, Contact Date on/after {nl['cutoff']}): "
                      f"{len(nl['on_list'])} on list")
                for x in nl["on_list"]:
                    print(f"{x['name']} <{x['email']}>")
                print(f"Left off, older than 12 months: {len(nl['off_older'])} | "
                      f"left off, no Contact Date: {len(nl['off_no_contact_date'])} | "
                      f"left off, no email: {len(nl['off_no_email'])}")
                for k in ("off_older", "off_no_contact_date", "off_no_email"):
                    for x in nl[k]:
                        print(f"- [{k}] row {x['row']} {x['name']} | {x['email'] or '-'} | Contact Date {x['contact_date'] or '-'}")
            return 0
        if a.park_candidates:
            today = parse_date(a.today) if a.today else dt.datetime.now(CT).date()
            pc = park_candidates(load_rows(a.sheet), today, load_sends(a.sends_json) if a.sends_json else None)
            if a.json:
                print(json.dumps(pc, indent=1))
            else:
                print(f"Park candidates WITH email (newsletter list): {len(pc['park_with_email'])}"
                      f" | already Parked with email: {len(pc['already_parked_with_email'])}"
                      f" | no-email rows (stay as they are): {len(pc['no_email_listed'])}"
                      f" | Contacted with unknown first send: {len(pc['unknown_first_send'])}"
                      f" | skipped, replied: {len(pc['skipped_replied'])}")
                for k in ("park_with_email", "already_parked_with_email", "no_email_listed", "unknown_first_send",
                          "skipped_replied"):
                    for x in pc[k]:
                        extra = f" | first send {x['first_send']}" if x.get("first_send") else ""
                        print(f"- [{k}] row {x['row']} {x['name']} | {x['email'] or '-'} | Stage {x['stage'] or '-'}{extra}")
                print("Read-only: nothing was written. Parking needs an explicit go.")
            return 0
        today = parse_date(a.today) if a.today else dt.datetime.now(CT).date()
        if today is None:
            raise InputError(f"bad --today {a.today!r}")
        res = build(load_rows(a.sheet), today)
        print(json.dumps(res, indent=1) if a.json else render(res))
        return 0
    except (InputError, ValueError, json.JSONDecodeError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
