---
name: Achieve Prospect Tracking
description: >-
  Use when CRM adds Achieve prospects to Prospect Tracking, logs lead touches,
  updates Stage/Eval?/Contact Count, builds the speed-to-book due list or Friday
  scoreboard, or updates the yearly dashboard. New rows at top, never guess.
---
# Achieve Prospect Tracking

Use when adding, updating, or reporting on Achieve prospects on the Prospect Tracking spreadsheet.

## Sheet

- File: [Prospect Tracking](https://docs.google.com/spreadsheets/d/1x8KurT1AJOPYLca6Jz9f_zBqZ3yBUGv8-isf8pctv4g)
- Current year tab (2026 worksheet id `502533256`)
- Writes: Zapier Google Sheets as `ryne@achievesportsperformance.com`. Lookup/update by **Email Address**. New leads: **create row at top** immediately below the heading. Never append to the bottom of the list.
- Ryne edits the sheet too. Re-read the header and the row live before every write. Columns can move.
- After every write, follow [Sheet write read-back](sand-workflow:sheet-write-readback): read the row back by Email Address (or by row when there is no email) and compare name, email, phone, Contact Date and Stage. On a mismatch, stop and flag it. On a write error, look the row up first and retry at most once. The sheet is the source of truth over any side tracker.

## 2026 columns (live 2026-10-22; always re-read the header, columns move)

A Last Name | B First Name | C Month | D Contact Date | E Stage | F Contact Count | G Referral Source | H Eval? | I Sign-Up | J Sign-Up Date | K Email Address | L Phone Number | M Service Type | N Comments | **O Last Contact** | **P Next Follow-Up**

- O/P added 2026-10-22 for the lead follow-up flow. Dates are real dates shown M/d/yy (write with parseInput=true, e.g. 10/21/26). The monthly summary table (AVERAGES row, ~289) and the Dashboard 2026 column are hard values, not formulas on this tab.
- **Eval?** = Yes when the person actually did an eval. Ryne's rule: everyone with Sign-Up = Yes did an eval.

Older year tabs have their own consult columns (2018-2025: Set Up Consultation / Attended Consultation; 2016-2017: Consultation). Follow each tab's own header; don't force 2026's shape onto them.

## Stage - exact values only

Use only one of these, from evidence in Gmail, Quo/Numa, the calendar, or the sheet. Never invent.

- `New inquiry` - inbound only; no Achieve outreach yet
- `Contacted` - Achieve has sent outreach (email, text, call, or Yelp Biz reply) and the lead has not replied (re-tag 10/23/26)
- `Replied` - the lead replied to Achieve's outreach (no eval booked yet)
- `Parked` - no reply after the day-30 touch, or past 30 days since the first send with no reply (Ryne 10/23). Next Follow-Up blank; on the Achieve Minute newsletter list only if it has an email and its Contact Date is within the last 12 months (older Parked leads stay off the list; `followup_due.py --newsletter-list`). A reply, booking or sign-up takes the lead off Parked.
- `Eval booked` - an eval is on the Achieve calendar or confirmed in writing
- `Eval done` - evidence they attended (also set Eval? = Yes)
- `No-show` - evidence they missed a booked eval
- `Offer` - pricing, package, or MindBody/signup link sent
- `Signed` - Sign-Up is Yes
- `Lost` - Sign-Up is No, or a clear decline or disqualify
- `Hold` - they asked to pause, will be in touch later, or aren't ready yet

If Sign-Up = Yes, Stage = Signed. If Sign-Up = No, Stage = Lost (unless Comments say otherwise).

## Contact Count + touch log

- Count only real Achieve outbound touches: work emails, Quo/Numa texts, answered outreach calls, and evidenced Yelp Biz replies.
- Don't count inbound-only messages or auto-receipts, and never write an invented 0. Leave it blank when it can't be counted.
- Add a short dated note to Comments for each touch (e.g. `10/9 text day 1`).

## Speed-to-book cadence (Ryne 2026-10-09)

- Steps run from first contact: same day, then day 1, 3, 7, 14 and 30, a close-the-loop text on day 45, and a confirm the day before a booked eval. Evals are offered in the evening for everyone, adults included (the before-10am slots are only for adult 4:1 group training after sign-up).
- Personal Assistant drafts the texts and emails. Ryne approves every send. CRM never drafts or sends.
- CRM's daily due list for PA, oldest first:
  - (a) Uncontacted leads
  - (b) Leads due today: which step, last touch date, channel
  - (c) Eval confirms for tomorrow
  - (d) Past evals with no done/no-show outcome
- Give name, contact, service type, and one line of context for each.
- No past-lead re-engage batch goes out without Ryne approving that batch's text and recipient list.
- Before any due-list item is drafted, it goes through [Pre-draft check](sand-workflow:pre-draft-check) (2-field recipient match, Gmail and Quo touches in the last 48h, future open times, parent only if confirmed, no prices).

## Lead follow-up flow (Ryne 2026-10-22 via Chief)

- Schedule for leads who have not responded: day 2, 5, 9, 14, 21, 30 after the FIRST outreach send. After the day-30 touch with no reply (Ryne 10/23): Stage = Parked and clear Next Follow-Up. Parked leads get no more personal follow-ups; they go on the Achieve Minute newsletter (Quill's, twice a month). Give Quill the parked list (names + emails) when asked. Leads who replied at some point are not parked; flag them for Ryne. Any reply, booking or sign-up stops it (leave Next Follow-Up blank, note why).
- When Penny reports sends (one end-of-day batch): Contact Count +1, Last Contact = send date, Next Follow-Up = `followup_due.py --next <first send> --step <Contact Count after the send - 1>` (or parked), Stage as evidenced. Read back every write.
- Daily 8am: export the live 2026 tab and run `python3 /home/box/agent-data/shared/scripts/tally/followup_due.py --sheet <export>` (see the README there). Never build the list by reading the sheet by hand. Hand Penny name, email/phone, step, what they asked about, after the 48h no-touch check.
- Backfill only from real Gmail sends (SENT label, not DRAFT), on or after the Contact Date. No evidence, leave blank.
- Resolved 10/23 (Ryne via Chief): Contacted = mid-sequence, Replied = lead replied only, Parked allowed. Replied rows stop the schedule; the script shows them on a HELD line as a cross-check.

## Friday scoreboard (by 5pm CT, Administrative group)

- Report month to date, by Contact Date:
  - Leads
  - Booked evals
  - Leads-to-booked %
  - Evals done
  - No-shows
  - Signed
- Put raw counts next to every percentage.
- Targets: about 20 booked and 35-38 leads a month. For October 2026 only, the target is 12-15 booked counted from 10/7 to 10/31.

## Rates

- Eval rate = evals ÷ leads
- Close rate = signed ÷ evals
- Lead-to-close = signed ÷ leads
- Show rate (attended ÷ booked) needs No-show data. 2026 has little, so say so; don't impute.

## Who counts as a prospect

Add a row only when someone **inquires about training**: a WordPress Lead Form, a first-time work-inbox training ask, a named referral wanting to train, a returning client restarting, or a leftover Instant Form.

**Never add:**
- Spam, junk, phishing, vendor pitches, or solicitations
- College observation, job-shadow, or class-requirement asks
- Existing-client ops mail
- People already on the sheet (match email, then phone, then name)
- The known do-not-contact ghost lead listed in `/home/box/agent-data/shared/lanes/achieve-leads/RULES.md`: no draft, no follow-up, no new row

If a non-prospect was added by mistake, delete the row.

## Service Type - exact values only

`Semi-Private` (use instead of regular personal training), `Swim Dryland Training`, `Athletic Development`, `Remote`, `Hybrid`. Never free-text. If the evidence doesn't map cleanly, leave it blank.

## Inbound to row

1. WordPress `Lead Form -` / `form Submission` emails get a new row if the person is missing **and** it's a real training inquiry. Search all mail, including archived (Gmail `in:anywhere`, never `in:inbox`): Penny archives these emails as noise after triage, so an Inbox-only search misses them.
2. Other first-time prospect emails in work Gmail get the same treatment. PA may flag them; CRM still owns the row.
3. Fill only what the source gave. Leave blanks rather than guess.
4. **Referral Source:** Lead Form = `Website` if empty. Meta Instant Form or SCDD leftover = `Meta Ad`. Otherwise take it from the email.
5. **Contact Date** is the first inquiry date (America/Chicago). **Month** is that month's name.
6. Set Stage = `New inquiry` on add. Leave Contact Count blank until an outbound touch is evidenced.

SCDD Instant Form watch and the E1-E4 sequences are retired (2026-09-15).

## Gap fill

Scan open or incomplete rows. Pull facts from work Gmail, Numa (read-only), Quo, Lead Form bodies, and calendar evals already on the books. Write only evidenced cells. Never invent a phone, email, price, Sign-Up = Yes, Stage, or Contact Count. Sign-Up / Sign-Up Date come only from a real close.

## Dashboard

The yearly dashboard must match the year tabs. Count from the rows. Recalc after material updates. As of 2026-10-09 it was stale (2026 showed 265 prospects; the tab had 272).

## Lanes

- CRM: inbound, touch log, Stage, Eval?, Contact Count, due list, Friday scoreboard, dashboard.
- Personal Assistant: drafts, sends (after Ryne approves), calendar, Quo/Numa, Mindbody.
- Sales: copy.
- A Chief of Staff question is not send approval.

## Quiet

If nothing is new, there are no gaps you can evidence, and nothing is due, stay silent. Silent runs still follow [Silent run heartbeat](sand-workflow:silent-run-heartbeat): log the window, the searches run, emails seen and rows matched. Alert once if there are 0 Lead Form emails in 7 days, a run was missed, or Gmail or Zapier returned an error.

- Write lesson (10/23): never write scattered rows as one block range with blank spacer rows; the Sheets connector can drop empty rows and shift writes up. Write non-adjacent rows one row (or one contiguous run) at a time, then read back.
- Step lesson (10/23): `--step` is the step just COMPLETED; first outreach = `--step 0` (gives day 2). `--step 1` after the first send skips to day 5. Check the README if a brief says otherwise.
