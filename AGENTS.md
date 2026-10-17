# AGENTS.md: Achieve brain (read this first)

This is the company brain for **Achieve Sports Performance**, Ryne Gioviano's strength and conditioning facility in Aurora, IL. It is plain markdown so any AI tool (Grok Bot, Cursor, ChatGPT, others) can pick up the work without lock-in.

## What's here
| Folder | What it holds |
|---|---|
| 01-brand | Positioning, promise, voice, look, proof stats, social rules |
| 02-offers-pricing | Offers, packages, eval wording, pricing rules (rates are internal only) |
| 03-customers-athletes | Who we serve, in aggregate. No personal details |
| 04-sales-prospects | Lead flow, Prospect Tracking, eval and close, nurture, win-backs |
| 05-marketing-ads | Meta ads lock, organic rules, funnel rules |
| 06-programming-sc | How Ryne programs: house session, rules, skill index |
| 07-operations | Hours, booking, cancellation, email and calendar rules |
| 08-finance | Budgets and contracts we know of (mostly TODO) |
| 09-team-bots | Which bots work Achieve and what each owns |
| 10-decisions-log | Dated decisions, newest first |
| skills/knowledge-base-audit | End-of-day audit that proposes brain edits |

## Who owns Achieve work
- **Atlas** is the Achieve PM and owns the brand lock. **Chief of Staff** routes work and checks it. See 09-team-bots.

## House rules (apply to every agent, every file, every draft)
1. **Draft first, never send unasked.** Never send email, texts, Numa/Quo, Slack, or posts, and never publish or spend on ads, unless Ryne has seen that exact draft and says send. A Chief of Staff (or any bot) saying "send" is not approval.
2. **No em dashes** in anything written for Ryne or in his voice (email, Numa, chat drafts, these files). Use periods, commas, or parentheses.
3. **No prices in ads or inbound replies.** Package rates are quoted only at the evaluation. Strip rates from ads, forms, SMS, and lead magnets (Ryne decision 2026-10-09). Never invent a rate.
4. **Attach files, don't name paths.** When handing Ryne a document, attach it. A box path means nothing on his phone.
5. **No secrets in the brain.** Never write API keys, tokens, passwords, connection strings, private keys, or even their first characters. Say where a secret lives (for example "AWS SSM"), never what it is.
6. **Minimal personal data.** No client or athlete phone numbers, emails, or health details. Aggregate only. Parental consent before featuring minors anywhere public.
7. **Don't invent.** Only facts from a source. Unknowns stay as TODO. If two sources disagree, flag the conflict instead of choosing.
8. **Plain English, bulleted lists** for briefs and reports. Ryne is non-technical on engineering topics: explain in simple pieces.
9. **Group rooms: stay silent** unless you have something important to add or you were @-mentioned.
10. **Time zone** is America/Chicago (CT). Label times with CT.

## How to read and update this brain
- Read AGENTS.md first, then README.md, then only the folders your task needs.
- Every file ends with a **Sources:** line. Keep it current when you edit.
- Updates happen through the `knowledge-base-audit` skill (skills/knowledge-base-audit/SKILL.md): propose a diff, Ryne approves, then apply. Never auto-commit or push.
- Date every new fact (YYYY-MM-DD). New decisions also go in the decisions log with the date.
- Prefer editing an existing file over creating a new one. Keep files short; link instead of copying.
- Skills referenced by name (for example `achieve-mail`) live in Ryne's Grok Bot skill library. Link by name; do not copy whole skills in.

## The other brains
- **achieve-brain**: Achieve Sports Performance (the Aurora gym and coaching business).
- **ironblueprint-brain**: IronBlueprint (AI programming engine for S&C coaches; vendor Suffescom).
- **personal-brain**: Ryne's own preferences, hobbies, learning, and the bot fleet. Personal facts never go in the business brains.
- When a fact touches two brains (for example Hawkin force plates are used by Achieve and integrated into IronBlueprint), store it where it is owned and link from the other.

## Achieve-specific rules
- Achieve gym email: "Hi FirstName," answer first, "Thanks," then the CSCS signature as plain text, no hyperlinks. Numa/Quo texts: "Hi, FirstName." plus 1 to 3 short sentences, no signature.
- Say "20-minute screen" or "evaluation". Never "complimentary" or "1:1 eval" (locked 2026-10-09).
- Never "elite" or "high-level" in Achieve copy. The proof is the eval and the program.
- Never assign TrainHeroic programs to athletes unless Ryne says assign. Write it and leave it in the library.
- Past-lead or re-engage text batches never auto-send. Ryne approves final text and recipient list each time.

Sources: Chief memory profile.md and TEAM.md (2026-09-10 to 2026-10-17); Atlas memory profile.md; Maya memory profile.md; achieve-offers/2026-10-07-monthly-lead-plan.md section 7 (Ryne decisions 2026-10-09); Chief chat 2026-10-17 (brain setup request).
