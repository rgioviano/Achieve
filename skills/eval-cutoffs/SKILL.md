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

## Added 2026-11-10 (Desktop manual deep pass)

Source: memory/reference/pri-research-digs/2026-11.md, Desktop manual deep pass 2026-11-10.

- **Posterior Mediastinum Respiratory Reach Test:** no absolute wall-to-toe cutoff. Personal baseline: stand facing a wall, step back about an inch at a time, four-second pursed-lip exhale while reaching, heels down, knees unlocked, then inhale and round the mid-back; measure wall-to-toe when the heels lift or the back straightens. Progress is a longer distance while other PRI tests are negative. (**PRI**, Postural Respiration, Aug 2019 rev., p.40). Difficulty performing or progressing this test is a printed indication for the Left Posterior Mediastinum NM list (p.77).
- **Posterior Outlet Mediastinum Expansion Test:** sidelying, hips and knees 90°, back rounded; assess fill of that side’s posterior mediastinum on inhale. **Pos** = cannot fill. Left AIC: cannot fill the **left** posterior mediastinum in **right** sidelying. PEC / Patho PEC: cannot fill left or right in bilateral sidelying. (**PRI**, Pelvis Restoration, 2024, p.64; algorithms pp.66, 77, 84).
- **Cervical axial rotation:** **Pos** = limited in one direction compared with the other. No degree cutoff is printed. (**PRI**, Postural Respiration, pp.43-44).
- **Trunk rotation:** already listed as unequal L vs R - keep. Procedure is supine, knees maximally flexed and together; compare directions (optional yardstick from mat to the superior knee). (**PRI**, Postural Respiration, p.39).

PART <45° is also in Pelvis Restoration 2024 p.45 (not only an older edition). Shoulder flexion <160° and HG IR <80-90° remain Postural Respiration pp.42 and 41.


- Left AIC also prints +L Posterior Outlet Mediastinum Expansion Test and +R Apical Expansion Test (p.66).
- PEC also prints −B PART, +B Posterior Outlet Mediastinum Expansion Test, and +B Apical Expansion Test (p.77).
- Patho PEC also prints +B or unilateral PART, +B Posterior Outlet Mediastinum Expansion Test, and +B Apical Expansion Test (p.84).

## Added 2026-11-10 (fundamentals audit)

**Gap:** The skill owns Pos cutoffs and pattern matrices, not the printed procedures. Advisor questions need both.

Add a section **“How to perform and read (PRI manuals)”** after the matrices. Keep existing cutoffs; do not change Ryne-locked numbers. Cite printed pages.

### Pelvis Restoration, 2024, pp.40-47

- **ADT (p.41):** Sidelying, bottom hip/knee flexed 90°. Passively flex, abduct, and extend the top hip to neutral, keeping 90° knee flexion. Stabilize the pelvis so it does not fall backward or allow femoral IR. Top innominate directly over the bottom (too cephalad → false +; too caudal → false −). **Positive:** the femur will not adduct (restriction from the anterior-inferior acetabular labral rim, transverse ligament, and piriformis, or posterior-inferior femoral neck on the posterior-inferior acetabular rim), often secondary to an anteriorly rotated, forward hemipelvis. Usually left in Left AIC. Reflective of an osseous restriction from the acetabular labral rim.
- **Standing Reach Test (p.42):** Shoes on, knees fully extended, feet parallel. Reach toward the floor, arms forward, hips back, back rounded, exhale; measure fingers-to-floor in inches. A with-hip-shift version reaches to the left toes while shifting the left hip back (then the other side). Left AIC inability reflects the printed inlet/outlet on/off map on that page. PEC: “off” bilateral posterior inlet and bilateral anterior outlet; “on” bilateral anterior inlet and bilateral posterior outlet. *Ability to touch toes with +ADT and +PADT = Patho PEC.*
- **PADT (p.43):** Sidelying, both hips and knees flexed to 90°. The patient actively brings the top leg back to neutral, keeping 90° knee flexion, and touches the knee to the mat = negative. **Positive:** the top leg’s pelvic diaphragm cannot ascend, because the ipsilateral outlet (ischium) cannot abduct and the ipsilateral inlet (ilium) cannot adduct. Usually left, often from overactivity of the left distal iliacus interfering with proximal iliacus / left iliococcygeus and obturator internus. Frontal-plane stance-phase test.
- **PART (p.45):** Sidelying, bottom hip/knee flexed 70-90°, top hip/knee straight (0°). Passively stabilize the innominate and passively abduct the top leg. Stop if right thoracic abduction or sidebending occurs. **Positive:** femoral abduction of the top leg <45°. If +L ADT, expect +R PART (lateral buttressing of the femoral head on the lateral superior acetabulum). If ADT is already negative bilaterally and abduction remains limited (more often right), that can reflect inability of the ipsilateral outlet to adduct and inlet to abduct (pelvic diaphragm cannot descend); right glute max facilitation is desired. Frontal-plane swing-phase test.
- **Functional Squat (p.46):** Level 1 - initiate a squat, slight knee bend, trunk stays in flexion (inability: lack of posterior pelvic rotation; hyperactive back extensors, rectus femoris, sartorius). Level 2 - bottom back, knees forward, trunk flexed (inability: lack of femoral adduction; hyperactive hip flexors and overactive FA ERs, inferior glute max, coccygeus, piriformis). Level 3 - bottom below the knees, heels down, trunk flexed (inability: tight intercostals; hyperactive anterior/posterior tibialis; lack of IO/TA with posterior mediastinum expansion). Level 4 - heels down, trunk flexed, bottom to heels (inability: hyperactive quads and gastroc-soleus; lack of IO/TA with the frontal plane of the pelvis). Level 5 - maximal squat, heels down, trunk flexed, COG through the heels (inability: lack of maximal AF IR and synchronized diaphragm / pelvic-diaphragm respiration). *Full squat with +ADT and +PADT = Patho PEC.*
- **Hruska Abduction Lift (p.47, continues after):** Named for the leg on the wall (left sidelying, right foot on wall = Right test). Procedure and step-failure grading already in `pri-myokinematic-restoration`; do not duplicate the full five steps here - point there, and keep the <3/5 pattern-matrix cutoff already in this skill.

### Postural Respiration, Aug 2019 rev., pp.37-44

(Trunk rotation p.39, Reach Test p.40, and cervical axial rotation pp.43-44 are already in this skill from the 2026-11-10 pass. Add the four missing how-tos.)

- **Apical Expansion (p.37):** Supine, knees flexed to flatten the lumbar spine. Patient inhales through the nose; on exhalation guide the left rib cage down and hold it down as the patient tries to fill the opposite chest wall; repeat on the other side. **Positive:** cannot draw air into the right thoracic chest wall as easily as the left (patient report or observation). Limited right apical expansion reflects right rib IR with left rib ER, often from thoracic cage compensation to the left as the thoracic spine orients to the right. Limited left apical expansion after a manual right Superior T4 technique reflects an upper left Superior T4 syndrome and a right BC patho-compensatory pattern at the scapula-thoracic region (clinician path, not a gym drill).
- **Shoulder Horizontal Abduction (p.38):** Supine, knees flexed to flatten the lumbar spine. Passively take the arm into horizontal abduction while securing the shoulder joint and anterior rib cage with one hand and keeping the forearm supinated with the other. **Positive:** limited on one or both sides; **<45° is limited.** This assesses ipsilateral posterior mediastinum expansion. Limited left HA reflects right sternal rotation on a vertical axis and inability to lateralize thoracic COM to the left (left rib ER, right rib IR; loss of left ZOA with limited right trunk rotation). A bilateral limitation reflects a non-rotated but forward and elevated sternum and inability to lateralize COM left or right (both ribs in ER; loss of bilateral ZOA with limited bilateral trunk rotation). **This is reflective of a bilateral BC that could also be a bilateral PEC.**
- **HG IR (p.41):** Supine, knees flexed to flatten the lumbar spine. Bent arm at shoulder level; stabilize the anterior shoulder joint; passively rotate the arm toward the mat; repeat the other side. **Positive:** limited on one or both sides; **<80-90° is limited** (already the printed cutoff). Limited right HG IR reflects the rib-cage position seen with limited right apical expansion (posterior-superior HG impingement from the glenoid’s position on the thorax). A bilateral limitation can reflect limited apical expansion on both sides (bilateral BC) or an underlying Superior T4 syndrome (left HG IR stays limited after right apical and right HG IR are restored).
- **Shoulder Flexion (p.42):** Supine, knees flexed to flatten the lumbar spine. Passively flex the arm while stabilizing the anterior rib cage and keeping the forearm in neutral supination (thumb straight up). **Positive:** limited on one or both sides; **<160° is limited** (already the printed cutoff). Limited left HG flexion reflects left rib ER (glenoid downwardly rotated and ER’d; pec minor / anterior chest wall to the left). A bilateral limitation reflects rib ER on both sides, possibly a bilateral BC.
