---
name: Achieve program Asana from eval
description: >-
  Use when filling or creating an Achieve Programs Asana Make-program task
  from a Drive Assessment after signup (or when Ryne asks to backfill an old eval).
---
# Achieve program Asana from eval

## When
After a complimentary eval is finished and the person signs up, or when asked to backfill an old eval: fill the Programs Asana task description from the Drive Assessment. Create the task if missing.

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
7. **Movement limits / scores** that matter (only if filled and non-normal): `1 on trunk stability push-up`, `2 on deep squat`, `Limited B ankle dorsiflexion` (add numbers when recorded), other clear limits on the sheet.
8. **Training age** - `Training age X months/yrs`, `Training age 0 yrs`, or `No prior training history`.
9. **Injury history** - outer bullet `Injury history` with nested items, or a single `History of …` line when there is only one short item. Copy sheet wording.
10. **Goals** / **General note** - only when written on the sheet. Skip if blank.

Do **not** put jump heights, circumference, skinfolds, or blank tests into the notes.

### HTML skeleton
```
<body>{age} yr old {sport} - {specialty}
<ul><li>{PRI pattern}</li><ul><li>Pos …</li></ul><li>Wide ISA</li><li>Scaps</li><ul><li>IR'd, protracted, ant tilted</li></ul><li>Limited scapular upward rotation</li><li>1 on trunk stability push-up</li><li>Training age …</li><li>Injury history</li><ul><li>…</li></ul></ul></body>
```
Omit any block with no data (especially Scaps).

## Due date + recurrence (every fill)
- `due_on` = fill day + 2 calendar days (America/Chicago).
- Recurrence: type `periodically`, data `days_after_completion: 25` (same as Sophia Mancilla). Pass on `update_tasks` even if the schema omits it; verify with `get_task` including `recurrence`.

## Create vs update
- Find existing `Make [Name] new program` task and update notes/due/recurrence in place.
- If missing, create in Programs project with that title. Do not change an existing assignee on backfill. Assign on create only if Ryne already said who.

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
