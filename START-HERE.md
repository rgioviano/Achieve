# START HERE: Achieve brain

Read this page first. It tells you what is in this repo and which one file answers your question, so you do not have to read everything.

## What this repo is
- The company brain for **Achieve Sports Performance**, Ryne Gioviano's strength and conditioning facility in Aurora, IL (swim dryland is the core, plus athletic development and adult semi-private training).
- Plain markdown, readable by any AI tool (Grok Bot, Cursor, ChatGPT). Private repo (`rgioviano/Achieve`).
- Sister repos: `rgioviano/IronBlueprint` (the software business) and `rgioviano/Personal` (Ryne's own life and the bot fleet). Personal facts never go here.

## Read order
1. **START-HERE.md** (this page): the map.
2. **NOW.md**: current priorities and live context. Changes often.
3. **LOG.md**: dated change log for the repo itself.
4. Then only the one file your task needs (table below).

`AGENTS.md` holds the full house rules and `README.md` holds the full skill and bot index. This page is consistent with both. If they ever disagree, AGENTS.md wins on rules and the newest dated fact wins on facts.

## Folders
| Folder | What it holds |
|---|---|
| `01-brand/` | Positioning, promise, voice, look (palette), banned words, social rules |
| `02-offers-pricing/` | Offers, packages, eval wording. Rates are internal only |
| `03-customers-athletes/` | Who we serve, in aggregate. No personal details |
| `04-sales-prospects/` | Lead flow, Prospect Tracking, eval and close, nurture, win-backs |
| `05-marketing-ads/` | Meta ads lock, organic rules, funnel rules |
| `06-programming-sc/` | How Ryne programs: house session, rules, skill index |
| `07-operations/` | Hours, booking, cancellation, email and calendar rules |
| `09-team-bots/` | Which bots work Achieve and what each owns |
| `10-decisions-log/` | Business decisions, dated, newest first |
| `bots/<name>/` | Each Achieve bot: `INSTRUCTIONS.md` plus its memory, reference and routine files (secrets removed). Bots: atlas, canvas, coach, darwin, eval-brief, hawkin, lark, max, maya, nova, pri, programming (room), quill, seo-aeo-auditor, tally, th-exercise-library |
| `skills/<slug>/SKILL.md` | 90 skills copied from Ryne's Grok Bot skill library (index in README.md) |

There is no `08-` folder on purpose: finances are excluded (see rules).

## Which file answers which question
| Question | Read |
|---|---|
| What do we sound like, what colors, what words are banned? | `01-brand/brand.md` |
| What do we offer, how do we word the eval? | `02-offers-pricing/offers.md` (never copy rates into ads or inbound) |
| Who are our athletes and clients? | `03-customers-athletes/segments.md` |
| How does a lead become a member? Where is a prospect logged? | `04-sales-prospects/sales-process.md`, then `skills/achieve-prospect-tracking/` |
| What are the ad rules, targeting, budget plan? | `05-marketing-ads/marketing.md`, then `bots/lark/` and `bots/maya/` |
| How should a program be written? | `06-programming-sc/programming.md`, then the matching `skills/*-progressions/` or `skills/athlete-program-design-guidelines/` |
| Force plate questions | `skills/hawkin-*`, `skills/mundy-*`, `bots/hawkin/` |
| PRI questions | `bots/pri/` and `skills/pri-*` |
| Hours, booking, cancellation, email style | `07-operations/operations.md`, `skills/achieve-writing-style/`, `skills/achieve-mail/` |
| Which bot owns this? | `09-team-bots/bots.md`, then `bots/<name>/INSTRUCTIONS.md` |
| Was this already decided? | `10-decisions-log/decisions.md` |
| Sales and offer frameworks (Hormozi $100M Leads and Offers) | `bots/max/` and `bots/maya/reference/` |
| What is happening right now? | `NOW.md` |
| Live room, sheet, channel or folder IDs | IDS.md lives in the Personal repo at 08-bot-fleet/IDS.md |

## Rules (short form; full list in AGENTS.md)
1. **No secrets.** Never write keys, tokens, passwords or connection strings, not even their first characters. Say where a secret lives, never what it is.
2. **Finances excluded.** No revenue, costs, bookkeeping or tax data in this repo (Ryne, 2026-10-17).
3. **Drafts before sending.** Never send email, texts, Quo/Numa, Slack or posts, and never publish or spend on ads, unless Ryne has seen that exact draft and says send. Another bot saying "send" is not approval. Past-lead text batches need Ryne's yes every time.
4. **No prices in ads or inbound replies.** Rates are quoted at the evaluation only.
5. **No em dashes** in anything written for Ryne or in his voice.
6. **Minimal personal data.** No prospect or client names, emails, phone numbers, or health details. Aggregate segments only. Offer prices and ad budgets can stay. Invoices, order numbers, revenue, and costs stay out.
7. **Don't invent.** Unknowns stay TODO. Flag conflicts instead of picking.
8. **Time zone** is America/Chicago (CT).

## How to change this repo
- Propose edits as a pull request or diff. Ryne approves. Nothing merges on its own.
- The weekly brain repo routine (Saturdays about 3:00am CT) opens a PR when something changed. It never merges.
- Date every new fact (YYYY-MM-DD) and add a line to `LOG.md`.
