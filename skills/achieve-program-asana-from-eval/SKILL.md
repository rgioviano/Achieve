---
name: Achieve program Asana from eval
description: >-
  Use when filling or creating an Achieve Programs Asana Make-program task from
  a Drive Assessment after signup (or when Ryne asks to backfill an old eval).
---
# Achieve program Asana from eval

## When
After a complimentary eval is finished and the person signs up (Tally sends a new-signup handoff the same day; Ryne 2026-11-14 asked that each one gets its program task built and eval results filled), or when asked to backfill an old eval: fill the Programs Asana task description from the Drive Assessment. Check first for an existing open task (Ryne often creates it himself).

## Golden rule (Ryne 2026-11-14)
The notes list only what needs fixing. Movement screen scores of 3 or 2 do NOT go in; only 1s and 0s require intervention.

## Sources
1. Drive Assessment sheet (`FirstLastAssessmentMM.DD.YY`; sometimes misnamed Program but still Assessment).
2. Asana Programs project `221539963131988`. Title: `Make [Name] new program (2x/wk)` (or signed frequency).
3. Always use the fixed notes order below. Never freestyle the bullets.

## Fixed notes order (html_notes)
Nested HTML lists matching Anika / Sophia / Reece. First line is plain text; then one outer list.

1. **First line:** `{age} yr old {sport} - {stroke/specialty}`  
   Examples: `14 yr old swimmer - sprint freestyle`, `16 yr old golfer`.  
   If the eval is old, append `(eval M/D/YY)` and use age as written on the sheet (do not guess current age).
2. **PRI pattern** as the first outer bullet (`L AIC/R BC`, `L AIC/B BC`, etc.). Nested under it: Pos findings first; Neg only when notable. Preferred order when present: toe touch/standing reach → FA IR → FA ER → HG IR → HG ER → HG horiz abduction → shoulder flexion → passive leg raise → passive abduction raise → adduction drop → other Pos screens on the sheet. Phrase like `Pos B FA IR`, `Pos toe touch - can't reach`.
3. **Wide ISA** or **Narrow ISA**.
4. **Scaps** - only if Resting Shoulder Position has data. Nested one line, comma-separated: `IR'd` (palms face backward), protracted/retracted, downwardly rotated, winged, ant tilted, depressed, prominent medial border as needed. Omit the whole Scaps block if Resting Shoulder is blank. Neutral palms → omit IR'd.
5. **Limited scapular upward rotation** (or `Limited upward rotation`) - only if the sheet notes limited upward rotation. Downward rotation alone stays under Scaps.
6. **Hypermobile** - only if Beighton / Hypermobile = Yes.
7. **Movement limits needing intervention**: screen scores of 1 or 0 only (e.g. `1 on trunk stability push-up`, `0 on deep squat`), plus clear limits like `Limited B ankle dorsiflexion` (add numbers when recorded). Never list 2s or 3s.
8. **Training age** - `Training age X months/yrs`, `Training age 0 yrs`, or `No prior training history`.
9. **Injury history** - outer bullet `Injury history` with nested items, or a single `History of …` line when there is only one short item. Copy sheet wording.
10. **Goals** / **General note** - only when written on the sheet. Skip if blank.

Do **not** put jump heights, circumference, skinfolds, blank tests, or passing scores (2s/3s) into the notes.

### HTML skeleton
```
<body>{age} yr old {sport} - {specialty}
<ul><li>{PRI pattern}</li><ul><li>Pos …</li></ul><li>Wide ISA</li><li>Scaps</li><ul><li>IR'd, protracted, ant tilted</li></ul><li>Limited scapular upward rotation</li><li>1 on trunk stability push-up</li><li>Training age …</li><li>Injury history</li><ul><li>…</li></ul></ul></body>
```
Omit any block with no data (especially Scaps).

## Every new athlete program task (Ryne 2026-11-14)
- Must have a repeating due date every 25 days: recurrence `periodically`, `days_after_completion: 25`.
- Must be in the Programs project `221539963131988`.
- Verify both with `get_task` (recurrence + projects/memberships) after writing; the connector can silently drop recurrence. If a new signup's existing task is missing either one, add it; change nothing else.

## Due date (ONLY when creating a program task)
Ryne (2026-11-08): when he only asks to fill in eval notes on an existing (non-new-signup) task, change NOTES ONLY. Never touch due date, recurrence, assignee, or anything else, even if the task has no due date.
When creating a program task (new signup handoff or Ryne asks):
- `due_on` = creation day + 2 calendar days (America/Chicago).
- Recurrence and project per the section above. The Asana MCP can't set recurrence on an existing task (update_tasks returns "Updated 0 of 1"); set it in the Asana UI via the box browser (due date picker > Repeat > Periodically > 25 days after completion) and verify.

## Create vs update
- Existing `Make [Name] new program` task: update notes in place; preserve any existing text (merge, don't delete). Check it's the open task, not a completed predecessor.
- Create a task for a new signup handoff (or when Ryne asks) only if no open one exists. Assign on create only if Ryne already said who.
- Watch for a premature next occurrence (name ending `*`, due ~25 days out) created when a task was completed then reopened; don't edit or delete it without Ryne's yes.
- Old eval only (e.g. remote athlete far away): use the old Assessment with `(eval M/D/YY)`, add `No new eval (reason) - using M/D/YY Assessment`, and when asked add a `From mom/dad (email M/D)` block with training-relevant details from the parent's latest email (skip billing/admin).

## Reference athletes (every new signup, Ryne 2026-11-13/14)
Append at the END of the notes a plain `Reference athletes:` line, then a bulleted list of 2-3 athletes from Programs Asana with similar assessments:
- Match PRI pattern, sport, stroke/event (breaststroke differs from sprint free) or position, plus ISA, scaps, key Pos findings.
- Generally OLDER and MORE EXPERIENCED than the athlete (if the athlete is already older, more experienced is enough). Judge experience by when their program task was FIRST created; a duplicated task's created date doesn't count (trace duplicated_from / stories).
- In-person athlete: never use remote or hybrid-remote athletes as references. Remote athlete: prefer other remote athletes (their programs are similar).
- Bullet format: `Name - age, sport/stroke or position, PRI pattern, then other details`.
- If nobody fits every rule, pick the best on pattern, stroke, and experience and tell Ryne the compromise.

## PRI Pos cutoffs
When the Assessment lists degrees and you must decide Pos vs Neg, use [Eval cutoffs](sand-workflow:eval-cutoffs). Key printed °: SLR <75° or >100°; PART <45°; HG horiz abd <45°; HG IR <80-90°; shoulder flexion <160°. FA IR/ER and HG ER have no absolute PRI ° cutoff. ISA Wide/Narrow is Achieve labeling, not a PRI printed cutoff. The Assessment template itself prints no PRI/ortho degree or Pos/Neg cutoffs (only Beighton >3 and Clavicular Angle 6°-20°).

## Pos cutoffs (Ryne locked 2026-11-03)
Use when deciding whether a measured degree is Pos in notes:
- **FA IR:** <45° = Pos
- **FA ER:** <50° = Pos
- **HG ER:** <90° = Pos

Other screens: use PRI manual Pos rules (SLR <75° / >100°, PART <45°, HG horiz abd <45°, HG IR <80-90°, shoulder flexion <160°, etc.).

## Cite / label
Only state what the Assessment confirms. Label guesses as guesses. Never invent Scaps, PRI pattern, or injury details.
