---
name: Achieve mail
description: >-
  Use when Ryne runs /achieve-mail or asks about Achieve/IronBlueprint inbox,
  triage, leads, or drafting client email. Gmail only (work + contact +
  IronBlueprint connectors); never Spark.
---
# Achieve mail (Gmail)

Mailbox access is **Gmail** via the connected Gmail connectors. Keep this skill named **`/achieve-mail`**. Do not use Spark, the Spark CLI, or Spark Desktop.

Look up current Gmail tool schemas before calling them. Do not assume frozen argument names.

## Achieve client/lead replies (required)

Ryne uses **`/achieve-mail` alone**. Do not ask him to also run `/achieve-writing-style`.

Whenever this skill is used to review, triage, or reply to Achieve / IronBlueprint mail (`ryne@achievesportsperformance.com`, `contact@achieve-personaltraining.com`, `ryne@ironblueprint.app`) - including "get my emails," "inbox," "what needs a reply," leads, Gmail, or drafting responses:

1. **Immediately read and follow** the achieve-writing-style skill (do not ask Ryne to run it). If that skill is missing, use the saved gym-voice + Achieve policy facts (Hi FirstName, answer first, Thanks, plus his gym signature; 24-hour cancel, 12-hour book, 3-month min, extra 5th week, etc.). Never draft Achieve client/lead replies from this mailbox skill alone or with generic wording.
2. Use **this** skill for mailbox work (Gmail search/read/draft). Filing labels follow the gmail-waiting-vs-follow-up skill.

**Do not send email** unless Ryne explicitly asks you to send. Default: draft in chat (and create a Gmail draft).

**Signature (required on Gmail connector/API draft/send):** The connector does **not** append the web-client signature. Include this plain-text block after `Thanks,` (no hyperlinks, no `https://`, no `www.`, no website line):

```
Ryne Gioviano, MSEd, CSCS
Owner, Achieve Sports Performance & Personal Training

For scheduling or account questions:
Contact@achieve-personaltraining.com | Text: 630.340.4114
```

## Accounts

Sweep these Gmail accounts (separate connectors):

- `ryne@achievesportsperformance.com` - work (primary)
- `contact@achieve-personaltraining.com` - contact
- `ryne@ironblueprint.app` - ironblueprint
- Personal `[email kept out of repo]` - personal (only when the ask includes personal mail / PA brief triage)

Do not search personal Gmail for Achieve client/lead work unless he asks.

## Tool map

| Need | How | Notes |
|------|-----|--------|
| Inbox / people mail | search threads on the right account. Query: `in:inbox newer_than:3d` | Add `is:unread` when useful. |
| Search | search with Gmail operators | Then get thread for full bodies. |
| Read a conversation | get thread | Always read before drafting. |
| Sent / unreplied | `in:sent newer_than:14d` | Open threads; check whether latest is from Ryne with no later inbound. |
| Drafts in Gmail | create draft as a reply | Also deliver the body in chat. |
| Send | send message / sending a draft | **Forbidden unless he says send.** |

Log Gmail **thread IDs**. Do not invent Spark integer IDs.

## Typical `/achieve-mail` run

1. Load achieve-writing-style.
2. Sweep Inbox people/priority mail (skip Zapier, Google security, waitlist receipts, newsletters unless he asks).
3. Draft per writing style. Deliver bodies in chat. Create Gmail drafts.
4. File per Waiting vs Follow-Up (question send → Waiting; confirm/FYI/close → no Waiting).

## Standing rules

- Never send or delete without Ryne's explicit yes.
- Never archive client/parent/human threads that still need a reply.
- Numa SMS is a different register; this skill is email only.
- Always include the gym signature in the connector draft/send body.

## Policies and pricing
Before drafting anything about pricing, cancels, holds, booking, packages or evals, read the achieve-policies skill (/home/box/agent-data/workflows/achieve-policies/SKILL.md) and follow it.
