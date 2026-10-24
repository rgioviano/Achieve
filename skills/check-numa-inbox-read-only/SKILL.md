---
name: Check Numa inbox (read-only)
description: >-
  Use when checking the Numa business-texting inbox (inbox.numa.com) for new or
  unanswered customer texts — for a brief, a triage pass, or a specific thread.
  Read-only: read and report, draft replies in chat, never send or type into
  Numa.
---
# Check Numa inbox (read-only)

Numa is the business texting inbox at `inbox.numa.com`. There is no connector or public API — access is the signed-in Chrome on your own computer.

**Hard rule: this is a READ pass.** Never click Send, never type into the reply/compose box, never close, assign, snooze, or resolve a conversation. Anything that would go out is written as a draft in chat and waits for the owner to say send on that exact draft. Two past sends leaked stray links because text was typed into the composer early — do not put anything in a send box, not even to "have it ready."

## 1. Open the inbox

Delegate to a `browserUse` subagent (page-level, faster and it does not grab the desktop). Give it the exact URL:

```
https://inbox.numa.com/inboxes/all
```

If the session is live, that loads straight into the list. Login is Auth0: `inbox.numa.com/login` redirects to `login.numa.com/u/login/identifier` (email) then `/u/login/password`.

**If it lands on a sign-in page:** stop the subagent and hand the desktop over with `request_box_help` and one short instruction like "Sign in to Numa". Never ask for, type, or store the password. Once handed back, dispatch the subagent again at the same URL. Sessions persist between checks, so this is occasional, not every run.

## 2. Read the list

Layout when it loads:

- Left rail: **Inbox**, Payments, Reports, Set up, Help, Me
- Folders: **Dashboard**, **All** (unread badge), **You**, **Unassigned**, **@ Mentions**
- Tabs across the top: **Open** (default), **Overdue**, **Reminders**, **Closed**
- Filters: **Assigned to** (All users), **All Labels**, **Sort by** (Newest)

Default read is **All + Open, Assigned to All users**. Each row shows the customer phone number, a one-line summary, the assignee, and a timestamp. Check **Overdue** too when doing a full triage pass — that is where a dropped thread hides.

## 3. Open the threads that matter

Click a row to open it (`/inboxes/all/c/<conversation-id>`). Inside:

- Center: the message history, newest at the bottom. **Scroll up** — the useful context (what was already promised, who last replied) is above the fold, and Numa's automated greeting can sit between real messages.
- Right panel: phone number, **Assigned to**, sentiment, and any **Task** attached to the thread.

Note per thread: who texted, their number, what they actually asked, the last outbound message and who sent it, and how long it has been quiet. Distinguish real inbound questions from Numa's automated greeting and from teammate replies that already answered it.

Use the **Back arrow** at the top left of the conversation panel to return to the list. Repeat for each thread that needs a human.

## 4. Report

Bring back, per thread that needs a reply:

- Name (or number if unnamed) and phone
- What they asked, in one line
- Current assignee and how long it has been quiet
- Whether it is already handled by someone else — if so, say so and do not draft

Then write the reply as a **draft in chat**, in the owner's texting voice, not email voice:

- Always greet: `Hi, FirstName.` — comma after Hi, period after the name. Never skip it, even mid-thread.
- 1–3 sentences. Lead with the answer, not an apology.
- "We" for the business. No email signature, no subject-line structure, no emojis.
- Do not invent prices, availability, or commitments. If a fact is missing (a class has to be checked first), flag it outside the draft rather than guessing.

Apply the same 3-day rule as email: a thread quiet 3 days after an outbound reply gets a follow-up draft surfaced, not a send.

## Never

- Send, reply, close, assign, or snooze anything in Numa
- Type any text, link, or URL into the composer
- Transcribe or store a password or one-time code
- Drive Chrome from the shell (DevTools, Playwright, cookie scraping) — use `browserUse`, or `computerUse` only if the page defeats it
