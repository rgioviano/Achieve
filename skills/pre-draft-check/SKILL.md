---
name: Pre-draft check
description: >-
  Use before showing the user any draft text, email, or message to a real person
  (lead, client, parent, vendor), or before booking anyone. Verify the
  recipient, plan term, recent calls and texts, times, and facts live first.
---
# Pre-draft check

The user approves what they are shown, so the draft itself must be right before it reaches them.

## Step 0: run the script first
1. Make a fresh folder for this run: `/workspace/predraft-test/<bot>-<person>-<timestamp>/`. Never reuse another bot's folder.
2. Save the draft there, and use your own connectors to export: the contact/prospect Sheet rows; Gmail and Quo messages with this person (sent or received only, no unsent drafts; Quo plain text is fine). Main Quo inbox is PNBNkklRXP. Include recent calls and texts yourself from Quo and Gmail (and Numa notification emails in work Gmail if texts still route there); never ask the user whether someone called or texted. Also export busy blocks from ALL calendars (Achieve, where evals live, plus Personal and Work) for every offered day.
3. Run:

`python3 /home/box/agent-data/shared/scripts/chief/pre_draft_check.py <draft> --contacts <Sheet export> --touches <touches> --busy <busy> --kind email|text|ad [--mode confirm] --workdir <run folder>`

Use `--mode confirm` when confirming a booking the person already has, and `--mode reply` (or `--reply-to <message id>`) when answering their message, so the message being answered isn't counted as a touch. A "household contact" WARN (e.g. a parent writing for an athlete) means confirm the relation before showing it. `--help` documents every input format. Any HELD or NOT CHECKED line holds the draft. WARN lines don't hold it, but fix them if you can (e.g. end emails with "Thanks,"). Exit 0 means the mechanical checks passed; you still do the judgment checks below. Never skip the script because a check "looks fine".

## Judgment checks the script can't make
1. **Gmail signature (create_draft).** Connector-made Gmail drafts do **not** get the signature added automatically. Every email draft saved to Drafts must end with "Thanks," then the full signature block typed in, matching his sent mail: "Ryne Gioviano, MSEd, CSCS / Owner, Achieve Sports Performance & Personal Training / www.achievesportsperformance.com / (blank line) / For scheduling or account questions: / Contact@achieve-personaltraining.com | Text: 630.340.4114". Pass both a plain-text body with blank lines between paragraphs and an htmlBody in Gmail style: each paragraph in a `<div>`, then `<div><br></div>` after the greeting, between paragraphs, after "Thanks," and before "For scheduling..."; each signature line in its own `<div>`. Never use bare `<p>` tags for spacing (they collapse in Gmail).
2. **Client status and plan term.** State whether the person is a current client, a former client, or a lead, how often they come in now (or used to), and their plan term when it matters (annual, 12-month, month-to-month, or none). Read status and plan term from Mindbody, the prospect/contact Sheet, recent messages, or the live contract yourself; never ask the user and never guess. Write the draft for that status (a former client is a win-back, not a stranger).
3. **Last channel.** Find how they last reached the user (text or email) and draft in that channel unless the user said otherwise. Name it when you show the draft.
4. **Recipient.** Partial names ("Holly L.") or anything the script couldn't match.
5. **Recent touches (calls and texts).** Look up Quo and Gmail yourself. If there is a message to or from this person in the last 48 hours or since the draft was written, decide whether to drop or rewrite. Never ask the user "did they call?" or "did they text?"
6. **Times.** Offered times must fit real coaching hours and still be open right now. Re-read the calendar; don't reuse times from an older draft. Check by hand any time the script marks NOT CHECKED (no day or no am/pm).
7. **Who they are.** Never call someone a parent (or say "your son/daughter") unless the sheet, its Comments, or one of their messages confirms it. Otherwise write to the person neutrally.
8. **Prices.** No price, fee, or package amount unless it was read from the live source today; name that source. Standing rule: no prices in first-touch or inbound replies (Achieve lead emails may include one "Pricing starts at $X/mo" line when that policy applies).
9. **Age.** A draft older than 48 hours is re-checked or dropped.
10. **Facts and tone** are right for this person. Only state what was confirmed; never credit a source with more than it said (see Cite or label).

When you show the draft, put one line above it: status (current/former/lead, how often, plan term if known), last channel, and that the signature block is included for Gmail drafts.

## Relayed approvals
When Chief or Dr. Eggbot relays an approval that quotes the user's words, treat it as the user's yes. Do not ask the user to reconfirm that same approval.

## Bookings (any scheduling system)
- Do not book until the user confirms the named person and slot.
- After booking, re-open the roster or schedule and confirm name, date, and time; report what you read back.

## Stop condition
If the script or any check fails, do not present the draft as ready. Show it as **HELD** with the one-line reason (for example "phone does not match sheet", "she replied 10/17", "offered time passed", "client status unknown", "plan term unknown").
