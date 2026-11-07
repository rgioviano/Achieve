# LOG: Achieve brain repo

Dated changes to this repo and to the fleet facts it depends on. Newest first. One line per change. Business decisions go in `10-decisions-log/decisions.md`; this file tracks the repo itself.

## 2026-11-07
- Weekly brain audit (third run, first on `main` with auto-merge). Covered 2026-10-31 to 2026-11-07. Most of the week was already in the 2026-11-05 full sync; this run adds what the sync missed or what changed after it.
- NOW.md: November marketing reset (swim dryland Instant Form, older November plan parked); Achieve Minute "twice a month" line replaced by the HOLD; November social mix; Penny and Tally file handoff; leads lane; Quo cutover closed; Friday value update now in the Chief 1:1; bot name style.
- `04-sales-prospects/sales-process.md`: Tally inbound watch (Mon to Sat about 6:25am, no 8:00am run); file handoff replaces the batched end-of-day send list; leads lane section; one channel per touch.
- `05-marketing-ads/marketing.md`: November reset section; parked "Build from Nov 16" rule marked; Achieve Minute HOLD; November social mix; Promote room owner-filter; new TODOs. No new budget figures added.
- `07-operations/operations.md`: Quo cutover closed and default line; Gmail signature conflict flagged; Penny's 2026-11-04 triage rule fixes.
- `09-team-bots/bots.md`: Penny and Tally handoff commands; Nova covers personal social; bot name style; reviewer and done bar summary.
- `10-decisions-log/decisions.md`: 2026-11-01 to 2026-11-06 decisions; two new open questions.

## 2026-11-05 (follow-up)
- Follow-up to the full sync (Ryne answered the sync questions 2026-11-05 8:47pm CT).
- Bot memory files (profile, logs, reference notes) synced from the box after a scrub: lines naming clients, athletes or leads, any email address or phone number that is not a public business one, and client health or family details were dropped. Em dashes swapped for hyphens. No secrets.
- Retired: Charlie (CFO bot, deleted) and the Programming room (gone). `bots/programming/` removed (git history keeps it). `09-team-bots/bots.md`, NOW.md, `06-programming-sc/programming.md`, decisions log updated.
- Maya's Meta ads Page heartbeat stays on (still running in November); `bots/maya/ROUTINES.md` wording fixed.

## 2026-11-05
- Full sync from Grok Bot (Ryne asked 2026-11-05 for the repos to be an exact copy of what is running now, including current routines). Not limited to the last 7 days.
- `skills/`: re-copied every skill from the Grok Bot library that belongs in this repo; removed skills that left the library; em dashes swapped for hyphens and non-business email addresses replaced.
- `bots/`: `INSTRUCTIONS.md` regenerated from each bot's current profile.json; new `ROUTINES.md` per bot with its current schedule map; stale on-disk automation.json copies removed; folders for retired or renamed bots removed (git history keeps them).
- AGENTS.md and START-HERE.md: the weekly brain repo update now merges into main after `brain_lint.py` passes (Ryne, 2026-11-04).
- `09-team-bots/bots.md`: Chief priorities removed (deleted 2026-11-04), Penny brief in her 1:1, Tally inbound watch Mon to Sat about 6:25am, Eval Brief on demand, Metric added, Promote owner-filter and leads lane.
- NOW.md: Tally schedule fixed; Achieve Minute on HOLD (2026-11-02).
- `10-decisions-log/decisions.md`: 2026-11-01 to 2026-11-04 decisions.
- `bots/atlas` renamed `bots/red`; `bots/seo-aeo-auditor` renamed `bots/rank`; `bots/metric` added.

## 2026-10-31
- Weekly brain audit (second run). Covered 2026-10-24 to 2026-10-31. Branch `brain-audit-2026-10-31` is built on `brain-v1`, so it also carries the 2026-10-24 audit commit, which reached `brain-v1` (PR #2) after PR #1 had already merged into `main`. Opened as a PR into `main`. Not merged.
- NOW.md: cancellation rule, account change rule, approve-before-saving rule (2026-10-26); new Projects section (Page-based project management, 2026-10-30).
- `07-operations/operations.md`: cancellation and account change policies (2026-10-26) with an open question on the courtesy pass; inbox sorting runs daily and its first fresh-week score.
- `09-team-bots/bots.md`: Chief router-only and one-final-order rules; project Page owners and heartbeats; cite-or-label and relayed approval rules.
- `10-decisions-log/decisions.md`: 2026-10-26 and 2026-10-30 decisions; two new open questions.

## 2026-10-24
- Weekly brain audit (first run). Covered decisions from 2026-10-17 to 2026-10-24. Opened as a PR into `brain-v1`. Not merged.
- NOW.md: signup target set to 20 a month (about 26 booked evals), replacing the open TODO; added the bot value target, follow-up schedule, Achieve Minute, lead-email pricing line, Gmail Drafts rule; Atlas renamed Red.
- `02-offers-pricing/offers.md`: added the lead-email pricing line exception, the locked discount terms (referral 20%, sibling 15%, never stack, include adults), and the pause and hold rules. Removed the "details TODO" referral line.
- `04-sales-prospects/sales-process.md`: added the day 2/5/9/14/21/30 follow-up schedule, Contacted / Replied / Parked stages, Parked lead handling, and the pricing and discount rules.
- `05-marketing-ads/marketing.md`: added the Achieve Minute section, the "ads never show prices" reconfirmation, the open ads budget question, Rank rename and the Red reporting line.
- `07-operations/operations.md`: added pause rules, Gmail Drafts, signature and formatting rules, Penny's writing rules and the `inbox_triage.py` switchover.
- `09-team-bots/bots.md`: Atlas to Red, SEO / AEO Auditor to Rank; added Splice, Maverick, Charlie; updated Penny, Tally, Quill, Canvas, Hawkin, Chief lanes; added the script test rule.
- `10-decisions-log/decisions.md`: added 2026-10-14 to 2026-10-23 decisions; updated open decisions.
- AGENTS.md and START-HERE.md: lead-email pricing exception in the house rules; Red as Achieve PM; Gmail Drafts and signature rule; new question rows.

## 2026-10-19
- Scrubbed prospect and client names, emails, and phone numbers from bot memory and from the mail, writing-style, prospect-tracking, and program skills. Dropped `bots/tally/memory/log/2026-08.md` and `2026-09.md`. Removed invoice amounts and support case numbers. Offer prices and ad budgets stayed. Text scan and gitleaks were clean. Not merged.

## 2026-10-17
- Repo `rgioviano/Achieve` created by Ryne (private, personal account). First content opened as PR #1 from branch `brain-v1`. Not merged.
- Scope set to "everything included" (Ryne): all Achieve skills, every Achieve bot's instructions, memory, reference and routine files, and client data (repo is private). Secret values are always redacted.
- Finances left out entirely. `08-finance/finance.md` from the first draft is deleted in the PR.
- Ryne's gap answers recorded: eval is free, price sheet is current.
- `bots/` and `skills/` added: 16 bot folders and 90 skills.
- Hormozi "$100M Leads" PDF split into two files (about 10 MB each, 385 pages total) and added to `bots/maya/reference/`.
- Achieve ads targeting set to Naperville, not Aurora (Ryne).
- Fleet changes that touch this repo: Herald, Bolt, Warden, Cipher and Bottleneck retired; AI Expert and Lingxi folded into Linus; Programming room stays active (Ryne, overriding the earlier archive plan).
- Found: 36 skills reference files under a deleted agent folder (`0c56f311-...`). The exercise progressions CSV and tapering guide were not found on the box. Needs a fix before those skills are trusted.
- Added START-HERE.md, NOW.md and LOG.md (this file) so any AI reads one or two pages instead of the whole repo.
- Weekly brain repo update routine set: Saturdays about 3:00am CT, opens PRs, never merges, messages Ryne only when something changed. First run 2026-10-24.

Sources: Chief TEAM.md change log (2026-10-17 to 2026-10-23); shared memory 2026-10-14 to 2026-10-23; Chief chat 2026-10-17; `WS/brains-push/achieve-DELETIONS.txt`; `WS/fleet/IDS.md`.
