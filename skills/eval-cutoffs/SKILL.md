---
name: Eval cutoffs
description: >-
  Use when deciding Positive vs limited on Achieve eval or PRI battery tests,
  or locking Pos phrasing for program-Asana notes from measured degrees.
---
# Achieve eval Pos cutoffs

Use this when filling program-Asana notes from an Assessment. Prefer the sheet’s own Pos/Neg marks when present. When the sheet only lists degrees (or blank Pos), apply the cutoffs below.

Run the helper for batch checks:
`python3 /home/box/agent-data/shared/scripts/achieve/eval_pos_cutoffs.py --help`

## Ryne-locked degree cutoffs (2026-11-03)
These three override the “no absolute cutoff” PRI gap for Achieve Pos phrasing:
- **FA IR:** <45° = Pos
- **FA ER:** <50° = Pos
- **HG ER:** <90° = Pos

(AAOS/textbook-style house rules. PT measured seated norms for FA IR/ER are closer to ~33-38°; still use these locked thresholds for Pos.)

## PRI manual degree cutoffs (Pos = limited)
- **Passive SLR / Passive leg raise:** <75° limited; >100° excessive (both Pos). Sources: Myokinematic SLR; Pelvis Cranial Resolution form `<75° >100°`.
- **PART (Passive Abduction Raise):** <45° abduction. Source: Pelvis PART.
- **HG / Shoulder horizontal abduction:** <45°. Source: Postural Respiration BC tests.
- **HG IR:** <80-90° (use **<85°** as the single house midpoint when a binary is needed; <80 clearly Pos, 80-90 soft zone). Source: Postural Respiration HG IR.
- **Shoulder flexion (HG flexion):** <160°. Source: Postural Respiration Shoulder Flexion.

I&I “SLR at least 70°, not greater than 100°” is treatment-target language; prefer <75° / >100° for Pos/Neg.

## No absolute degree cutoff (Pos by pattern / side-to-side / can’t-do)
- **ADT:** Pos = femur will not adduct. Usually L in Left AIC; bilateral → PEC.
- **EDT:** Pos = tested LE restricted in hip extension / femur does not approach table.
- **PADT:** Neg = top knee to neutral @ 90° knee flex and touches mat; Pos = cannot.
- **Apical expansion:** Pos = cannot fill one apex as easily as the other.
- **Trunk rotation:** Pos = unequal L vs R.
- **Standing reach / toe touch:** Left AIC & PEC >0″ (can’t touch); Patho PEC 0″ with +B ADT/+B PADT.
- **Functional Squat:** Left AIC/PEC <3/5; Patho PEC >3/5.
- **ISA Wide vs Narrow:** Achieve labeling only - no PRI ° cutoff.
- **Back To Wall Flexion:** no printed cutoff; Pos when sheet says limited / can’t.

## Pattern matrices (Pelvis)
- Left AIC: +L ADT, Standing Reach >0″, +L PADT, +R PART, Functional Squat <3/5
- PEC: +B ADT, Standing Reach >0″, +B PADT, PART − bilat, Functional Squat <3/5
- Patho PEC: +B ADT, Standing Reach 0″, +B PADT, PART + uni/bilat, Functional Squat >3/5

## Achieve Assessment sheet
Template "Assessment Template 2023" prints no degree Pos/Neg cutoffs for these tests (blank R/L/Comments). Printed sheet criteria only: Beighton Hypermobile >3; Clavicular Angle 6°-20°.

## Asana Pos phrasing
Prefer sheet language (`Pos B FA IR`, `Pos toe touch - can't reach`). When degrees drive the call:
- `Pos R FA IR` / `Pos B FA IR` etc. when under cutoff on that side
- Include the degree in notes only when it helps (`R FA ER 55 vs L 65`) - still mark Pos if under cutoff
