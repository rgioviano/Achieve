# Penny <-> Tally lead handoff (files, not chat) - 2026-11-01

Script: `lead_handoff.py` (stdlib, read/write only inside `/home/box/agent-data/shared/handoffs/penny-tally/`).
Replaces three chat handoffs (Lauren/@poteto ops item 2, Ryne approved 2026-11-01):

| Old chat handoff | New file | Writer | Reader |
|---|---|---|---|
| Penny flags new leads / first-time prospects to Tally | Penny's existing triage output `penny/triage/{work,contact}-DAY.json`, bucket `lead_form` | Penny's 6:15am inbox_triage.py (already runs) | Tally: `lead_handoff.py triage-leads` |
| Tally sends the follow-up due list to Penny | `due/DAY.md` + `.json` | Tally: `lead_handoff.py post-due --sheet EXPORT --hold KEY=REASON` | Penny: `lead_handoff.py read-due` |
| Penny sends Tally an end-of-day list of actual sends | `sends/DAY.jsonl` | Penny: `lead_handoff.py log-send ...` per real send | Tally: `lead_handoff.py read-sends --since DAY` |

Timing: Penny triage 6:15am → Tally speed-to-book ~6:25am (reads triage, posts due list) → Penny brief 6:45am (reads due list).
Missing file = exit 3 with a one-line "NO DUE LIST / NO TRIAGE FILE" message. Say that in the brief; never guess.

Rules kept: Tally still owns every Sheet write and runs pre_draft_check before marking a lead READY (failures go in as `--hold`).
Penny still never writes the Sheet, logs only sends Ryne actually made (never drafts), and never sends without Ryne's yes.
Chat between them only for exceptions (a lead that needs a human decision), not lists.

Commands
```
H=/home/box/agent-data/shared/scripts/handoff/lead_handoff.py
python3 $H triage-leads [--date YYYY-MM-DD]
python3 $H post-due --sheet <read_range export> [--today YYYY-MM-DD] [--hold jane@example.com="Quo text 10/31"] ...
python3 $H read-due [--date YYYY-MM-DD]
python3 $H log-send --name "Jane Doe" --email jane@example.com --channel email --sent-date YYYY-MM-DD --step 1 --row 2 [--draft-id r123]
python3 $H read-sends [--since YYYY-MM-DD] [--json]
```
`--hold` KEY = email, phone or sheet row number. log-send dedupes same lead + channel + day.
Smoke-tested 2026-11-01 on made-up data in a temp folder (post/read/hold/dedupe/missing-file paths) and on the real 10/31 triage files.
