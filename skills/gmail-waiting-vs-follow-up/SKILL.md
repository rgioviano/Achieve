---
name: Gmail Waiting vs Follow-Up
description: >-
  Use when filing Gmail for Ryne or drafting Achieve email: Waiting only if last
  send asked a question; quiet ~3+ days → Follow-Up; no Waiting on
  confirm/FYI/close; archive wins; chase only if last send asked a question;
  archive Lead Form / WP plugin-fail / password-reset noise; no website URL in
  connector signatures.
---
# Gmail Waiting vs Follow-Up

Use these labels correctly. They are not the same folder.

## Meanings

- **Waiting** — ball is on them. Ryne’s last send **asked a question** (or he is waiting to hear back before anything further).
- **Follow-Up** — chase pile. Quiet ~3+ days after a question send. Keep Follow-Up until he clears them or says otherwise.
- **Inbox** — reply pile (needs him this week). Do not recreate Action.
- **Later** — real but not this week, with a named future date.
- **Reference** — keep forever, no next step.
- **Archive** — done / noise. Archive alone wins as done even if Waiting / Follow-Up / Later / Reactivate remain. Never restore Inbox or re-list archived threads. Never archive client, parent, or other human threads that still need a reply; if unsure, leave in Inbox. Newsletters, Zapier, Meta, MindBody receipts, calendar noise → archive.

## Always archive as noise (locked 2026-10-07)

Archive and do **not** keep in Inbox or list under Email Triage:

1. Subjects starting with **Lead Form -** (form submissions). CRM owns the sheet row; PA does not need these emails saved for Ryne.
2. WordPress **update plugins failed** notices.
3. WordPress / site **password reset** request emails ("someone is requesting a password reset" and similar).

## After send (locked 2026-09-19)

1. **Asked a question** → apply **Waiting**, remove **Inbox**.
2. Quiet ~3+ days on that question send → apply **Follow-Up** (chase), restore Inbox if needed for the chase list.
3. **Confirm / answer / FYI / close with no ask** → do **not** apply Waiting. Archive or leave labeled done.
4. Do **not** auto-strip **Follow-Up** from chase threads.
5. Do **not** dual-file Follow-Up on every send.
6. Do **not** sweep Follow-Up off Sent or Waiting just to clear a folder.

Supersedes the old blunt rule “after any send apply Waiting.”

## Chase threads / follow-up list

Only **suggest a chase** when Ryne’s last outbound **asked a question** (ball still on them) and the thread is quiet ~3+ days. Do not chase when he only confirmed something or answered their question. Default: short list with one-sentence “where we left off”; full draft only when he asks.

## Signature (Achieve connector / API sends)

Plain text only. No hyperlinks, no `https://`, no `www.`, no markdown links. Gmail wraps any URL into `google.com/url?…`.

```
Ryne Gioviano, MSEd, CSCS
Owner, Achieve Sports Performance & Personal Training

For scheduling or account questions:
Contact@achieve-personaltraining.com | Text: 630.340.4114
```

Omit the website line on connector sends. Site stays on the live web signature only.

## Ownership

PA / CoS / CRM all follow this. CRM owns Lead Form sheet filing; PA archives the Lead Form emails as noise. Never auto-strip Follow-Up.
