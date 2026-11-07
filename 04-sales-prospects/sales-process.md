# Sales and prospects

## Flow
1. Inquiry arrives (website lead form, Meta Instant Form, call, SMS, email).
2. **Tally** logs it in the Prospect Tracking Sheet (2026 tab, newest at top). Tally is the only CRM. Tally's inbound watch runs Mon to Sat about 6:25am CT: it reads new leads from Penny's morning triage file (`lead_handoff.py triage-leads`), with a Gmail search as the backstop. There is no separate 8:00am run (Tally, 2026-11-01). (TEAM.md, CRM ownership 2026-09-16, updated 2026-11-01)
3. First contact fast (speed to contact target 60 seconds or less; Sales owns live contact, Marketing owns the form trigger). (Max 2026-09-08)
4. If the lead does not respond, the follow-up schedule below runs until they reply, book, or are Parked.
5. Book the evaluation (Ryne books; evenings). Penny prepares a prep card about 30 minutes before each eval.
6. Eval and close. Then follow-up if they did not sign.
7. After sign-up, **Eval Brief** drafts a Slack #clients coach brief from the Drive assessment (draft-first; Ryne approves). Gate: Prospect Tracking Sign-Up = Yes.

## Lead follow-up schedule (Ryne, 2026-10-22)
- Leads who don't respond get follow-ups on **day 2, 5, 9, 14, 21 and 30** after first outreach. Then the lead is **Parked**.
- Any reply or booking stops the schedule.
- **Tally** owns the Prospect Tracking Sheet, including the Last Contact and Next Follow-Up columns, and builds the daily due list by script (`followup_due.py`, never by hand). Tally posts it as a file with `lead_handoff.py post-due`; Penny reads it with `read-due` (2026-11-01).
- **Penny** runs the pre-draft check, drafts the follow-ups, saves emails to Ryne's work Gmail Drafts (texts stay as drafts in chat), and never writes the sheet. She logs each send Ryne actually made with `lead_handoff.py log-send` (never drafts), and Tally reads them with `read-sends`. This file handoff replaced the 2026-10-22 batched end-of-day list in chat (Ryne approved 2026-11-01). Chat between Penny and Tally is for exceptions only.
- One channel per lead per touch: never a Quo text and an email for the same touch (leads lane RULES, 2026-11-03).
- Nothing sends without Ryne.

## Achieve leads lane (live 2026-11-03, Ryne approved)
- Penny, Tally and Max read three shared files before lead work: MAP (where things live), RULES (every correction Ryne has made, dated) and CHECK (the proof a job is done). Files live on the box under `shared/lanes/achieve-leads/`.
- Rule 0: when Ryne corrects a bot in this lane, that bot adds one dated line to RULES the same day and tells Chief. Done claims need CHECK proof.
- Quo Support (the public Achieve number) is the default outbound text line; the Quo SMS cutover closed 2026-11-03.

## Prospect Tracking stages
- **Follow-up stages (Ryne, 2026-10-23):** "Contacted" for leads still getting follow-ups, "Replied" only when the lead replies, and "Parked" for leads with no reply after the day-30 follow-up.
- Older full stage list (locked 2026-10-06): New inquiry > Replied > Eval booked > Eval done > Offer > Signed / Lost / Hold. Tally owns stage and contact count, using evidence from Gmail, Quo, calendar, and the sheet only.
- TODO (question for Ryne): do Contacted / Replied / Parked replace the 2026-10-06 list, or sit in front of it (Eval booked, Eval done, Offer, Signed / Lost / Hold still used after a reply)?

## Parked leads
- Parked leads stop getting personal follow-up emails, and get no personal monthly emails. (Ryne, 2026-10-23)
- Tally marks them Parked. Parked leads with an email address whose **Contact Date is within the last 12 months** go on the Achieve Minute newsletter list. Older Parked leads stay off it.
- New list members get a short welcome note first (Quill drafts it). Ryne approves it before it sends.
- See `05-marketing-ads/marketing.md` for the Achieve Minute.

## Rules
- **Prices:** an Achieve lead email may include one "Pricing starts at $X/mo" line, with the price read live that day (Ryne, 2026-10-23). Penny's draft check allows that one line and flags any other price. All other inbound replies get no prices. Full rates are quoted at the eval.
- **Discounts:** see `02-offers-pricing/offers.md`. The 15% sibling / second family member discount is mentioned only when the family asks or when it will likely help close the sale.
- Lead nurture is the **3-7-30** value sequence, not chase. Sales owns email nurture; Marketing uses it only for paid nurture. (Max, Maya 2026-09-08). TODO (question for Ryne): does the 2026-10-22 day 2/5/9/14/21/30 schedule replace 3-7-30 for non-responders?
- Do not ask to set up an eval 3 or 4 times in a row. (Max 2026-08-31)
- Cancel or drop-off replies: offer 1x/week first ("what most athletes do in-season"), not "sorry to hear that", not fees first.
- Varsity parents: open with the force-plate eval and a program written from their jumps.
- **Reactivate win-backs:** Penny finds people who stopped, labels the last thread Reactivate, sets a reach date; Sales drafts. Wait at least 2 months after a cancel; context wins (HS in-season waits until offseason); skip angry leavers. (Max 2026-09-09)
- Past-lead batches: Ryne approves final text and recipient list every time.
- Gmail filing: see `gmail-waiting-vs-follow-up`. Archived means done.

## Numbers
- Target (Ryne, 2026-10-14): 20 signups a month, about 26 booked evals a month.
- Planning assumptions: about 90% show, about 87% close. Real 2026 show/close is being measured by marking every eval Eval done or No-show; review about mid-December 2026. (Lead plan 1a, #9)

## Skills (by name)
`achieve-prospect-tracking`, `lead-contact-and-follow-up`, `sales-discovery-questions`, `sales-eval-close`, `sales-follow-up-after-eval`, `sales-objection-handling`, `sales-nurture-3-7-30`, `sales-offer-enhancers`, `sales-tonality-and-delivery`, `achieve-reactivate-win-backs`, `mozi-sales-frameworks`, `achieve-mail`, `achieve-writing-style`.

## TODO
- TODO: Link to the Prospect Tracking sheet (Tally's profile holds it; add the link here if Ryne wants it in the repo).
- TODO: Current close script version (athlete-eval-close-script-2026-10-09 is a draft on the box).

Sources: Chief TEAM.md change log 2026-10-22 and 2026-10-23 (follow-up flow, stages, Parked, Achieve Minute list, pricing line); shared memory 2026-10-14 (signup target), 2026-10-22, 2026-10-23; TEAM.md (CRM ownership, Prospect Tracking stages 2026-10-06, call prep); Max memory profile.md; Maya memory profile.md; Tally and Eval Brief profile.json; achieve-offers/2026-10-07-monthly-lead-plan.md; workflows skill list. Chief TEAM.md (Lauren ops 2026-11-01, Achieve leads triad 2026-11-03); `shared/lanes/achieve-leads/RULES.md` (2026-11-03); shared memory 2026-11-01 (lead handoff files).
