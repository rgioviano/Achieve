# Tally scripts

## followup_due.py (lead follow-up flow, Ryne 10/22/26 via Chief)
Read-only. Python 3 stdlib. Never sends, drafts or writes.

Schedule: day 2, 5, 9, 14, 21, 30 after the FIRST outreach send. After the day-30 touch with no reply,
Stage = parked. Any reply, booking or sign-up stops it.

Daily (8am run):
1. Export the live 2026 tab with user-Google-sheets--achieve `read_range`
   (spreadsheetId 1x8KurT1AJOPYLca6Jz9f_zBqZ3yBUGv8-isf8pctv4g, ranges [{"sheet":"2026","cells":"A1:P400"}],
   maxChars 250000, write_to_file true). The saved file is accepted as-is.
2. `python3 /home/box/agent-data/shared/scripts/tally/followup_due.py --sheet <export file>`
   (`--today YYYY-MM-DD` to pin the date, `--json` for machine output). Exit 2 = bad/empty export.
3. Run the 48h no-touch check (pre_draft_check.py) on each item, then hand the list to Penny.

Due = Next Follow-Up <= today and Stage not containing replied/booked/signed/parked (any case); lost/dead
skipped; summary table (AVERAGES row and below) and blank rows ignored. Columns are found by header name.
Rows held only by a "Replied" stage are printed in a HELD section (the 2026 tab used "Replied" to mean
Achieve replied before this flow existed).

Step number = Contact Count (touches done incl. first outreach): count 1 -> step 1 (day 2), ... count 6 -> step 6 (day 30).

Next date helper: `python3 followup_due.py --next <first send m/d/yy> --step <step just completed>`
(step 0 = first outreach; prints m/d/yy or `parked` after step 6). Importable as `next_followup()`.

Tests: `python3 /home/box/agent-data/shared/scripts/tally/test_followup_due.py` (26 cases, made-up data).

Parked (10/23): Parked is never due; a reply, booking or sign-up takes a lead off Parked (`stage_after_event`).
Only leads WITH an email may be parked. `followup_due.py --sheet <export> --park-candidates` lists leads past the
day-30 touch (Contact Count >= 7), split with/without email. Read-only; parking on the sheet needs an explicit go.

Park candidates now use the BY-DATE rule (10/23): Stage Contacted, an email, first send > 30 days before --today
(first send read from the Comments "Gmail: N Ryne emails <dates>" note). The touch-count schedule stays the normal path.
Blank Stage counts too (10/23): a blank-Stage row is a candidate when it has an evidenced send (the Comments note, or an
entry in `--sends-json FILE`, format `{email: {"first_send": "YYYY-MM-DD", "sends": n, "replied": bool}}`) and no reply.
Leads flagged `"replied": true` are listed as skipped_replied, never parked. Blank-Stage rows with no evidenced send are ignored.

Newsletter (Achieve Minute): `followup_due.py --sheet <export> --newsletter-list [--today YYYY-MM-DD]` lists name and
email for Parked rows with an email and Contact Date on/after the same day 12 months earlier (inclusive); counts the
ones left off (older, no Contact Date, no email). Read-only.
