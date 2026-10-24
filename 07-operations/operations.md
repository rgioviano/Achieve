# Operations

## Location and hours
- 4020 Fox Valley Center Drive, Aurora, IL.
- Mon/Wed 5:30 to 10am and 3 to 8pm; Tue/Thu 8 to 10am and 3 to 8pm; Fri 5:30 to 10am and 3 to 7pm; Sat 7am to 1pm; Sun 8am to 2pm. Weekdays closed 10am to 3pm (no midday inventory). (Atlas, now Red, 2026-08-21)

## Systems
- Booking and billing: Mindbody (skill `mindbody-staff-book-cancel`). The Google calendar named Achieve syncs Mindbody appointments.
- Programs: TrainHeroic. Notes: Asana Programs board. Force plates: Hawkin Cloud. Assessments: Drive Clients folder.
- Phone and texting: Quo (preferred) and Numa (read-and-draft only until the Quo cutover). Email: Gmail (work and contact accounts).
- Slack (Achieve workspace): #clients for coach briefs.

## Policies
- 24-hour cancellation for all clients. Late cancel or no-show under 24 hours is charged after one courtesy. (Chief profile 2026-09-11)
- Pauses are capped at 1 month and keep the grandfathered rate. In-season holds can restart up to 2 weeks after the high school season ends and keep the grandfathered rate. Longer breaks pay the current rate. (Ryne, 2026-10-23; details in `02-offers-pricing/offers.md`)
- No self-booking of evals on Ryne's calendar.
- Never send email or texts without Ryne's yes on the exact draft.

## Email drafts (Ryne, 2026-10-22 and 2026-10-23)
- Email drafts for Ryne go into the Drafts folder of the right Gmail account, as threaded replies under the original email. Not draft cards in chat. The bot tells Ryne who each draft is to and its subject. Texts still come as drafts in chat. Nothing sends unless Ryne sends it himself.
- Drafts saved through the Gmail connector do NOT get Ryne's signature added automatically. Every saved draft ends with "Thanks," and then his full signature block typed in, exactly as in his sent mail (see the `achieve-mail` skill for the block). This replaces the older note to never type the signature.
- Formatting: pass both a plain-text body (blank lines between paragraphs) and an HTML body in Gmail's own style: each paragraph in its own div, an empty line div after the greeting, between paragraphs, after "Thanks," and before "For scheduling or account questions:", then one signature line per div. Paragraph tags show in Gmail with no space between paragraphs, so do not use them.
- Penny's writing rules (approved 2026-10-23): answer first and cut soft openers; use concrete specifics; end with a question; offer open time windows. Penny runs a Friday 7:00am CT review of her drafts against what Ryne sent; style rules change only when Ryne approves.

## Inbox sorting
- Penny's morning inbox sorting runs as a script (`inbox_triage.py`) at about 6:15am CT from 2026-10-24, feeding the 6:45am brief. It only sorts; it never archives or deletes mail. It was tested on 7 days of real mail first. First score on a fresh week of mail runs Thu 2026-10-29, reported before the Fri 2026-10-30 debrief. (Ryne approved 2026-10-23)

## Calendar conventions (for bots managing Ryne's calendar)
- Titles describe the work: Coaching, Programs, Admin, Meet w/ Name, Eval - FirstName LastName. Not campaign names.
- Focus floors: 1.5 hours Programs every weekday, about 1 hour Admin, 1 hour Marketing on marketing days, 1 to 1.5 hours IronBlueprint on IB days.
- Lighter days Mon, Thu, Fri, Sat. Ryne is off Thursday and Saturday.

## Staff
- TODO: Coach roster and roles (a coach named Scott covers some sessions per the 10/19 calendar; confirm roles).
- TODO: SOPs (one exists on the box: Mindbody pause-billing SOP; confirm it is current and matches the 2026-10-23 pause rules).

Sources: shared memory 2026-10-22 (Gmail Drafts) and 2026-10-23 (signature, HTML format, pauses, Penny writing rules, inbox_triage.py); Chief TEAM.md change log 2026-10-22 and 2026-10-23; Atlas (now Red) memory profile.md; Chief memory profile.md and tomorrow-priorities.md; Penny profile.json; workflows skill list; /workspace/achieve-ops file list.
