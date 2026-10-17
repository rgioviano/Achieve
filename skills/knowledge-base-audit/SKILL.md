---
name: knowledge-base-audit
description: Use at the end of each working day (or when Ryne asks "audit the brain") to compare the day's work and decisions against this knowledge base and propose edits as a diff for Ryne's approval. Never auto-commits.
---

# Knowledge base audit (end of day)

Same skill in all three brains: achieve-brain, ironblueprint-brain, personal-brain.

## When to run
- End of each working day, after the evening debrief (Mon to Wed 6:45pm CT, Fri 5:45pm CT). Thu and Sat are off days: skip unless Ryne asks.
- On demand when Ryne says "audit the brain" or a big decision lands.

## Inputs (read-only)
1. Today's work: chat transcripts and bot reports from today, approved drafts, decisions Ryne stated, routine outputs, and today's entries in agent memory logs.
2. The brain: AGENTS.md, then every file in the folders the day touched.

## Steps
1. List today's facts and decisions in one line each, with the source (chat, bot, file, date).
2. Route each item to the brain and folder it belongs in (Achieve, IronBlueprint, Personal). Personal items go only to personal-brain.
3. For each item, compare with the current file and classify it:
   - NEW: not in the brain yet.
   - CHANGED: the brain says something different (quote the old line).
   - CONFLICT: two sources disagree. Do not pick a winner; flag it for Ryne.
   - STALE: the brain says something today's work showed is no longer true.
4. Write the proposal as a unified diff per file (`--- a/path` / `+++ b/path`), plus a one-line reason and source for every hunk. Add new decisions to 10-decisions-log with the date.
5. Run the safety gate on the proposed diff before showing it:
   - No API keys, tokens, passwords, connection strings, private keys, or even prefixes of them.
   - No client or athlete phone numbers, emails, health details, or anything about minors beyond aggregate counts.
   - No em dashes.
   - No invented facts: every added line has a source.
6. Present to Ryne: a short summary (counts of NEW / CHANGED / CONFLICT / STALE), then the diffs. Plain English, bulleted.

## Hard rules
- Never commit, push, merge, or edit the brain files directly. Ryne approves the diff first; then a human or an agent he names applies it.
- Never message anyone else about the audit. Output goes to Ryne only (through Chief of Staff).
- If nothing changed, say "No brain edits today" in one line.
- Keep diffs small and specific. Do not rewrite whole files for style.
