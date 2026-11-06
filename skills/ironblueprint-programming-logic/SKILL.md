---
name: IronBlueprint Programming Logic
description: >-
  Use when Strength Coach (or any bot) designs or redesigns a program using
  IronBlueprint Nexus logic - classify athlete vs general, then apply codebase
  session order, pairings, overhead, taper, and load rules to make decisions.
---
# IronBlueprint Programming Logic

When Ryne asks Strength Coach (or any bot) to **design or redesign a program**, make decisions the way the IronBlueprint Nexus engine does in code - not generic S&C textbooks, and not TrainHeroic house style alone.

Source of truth: `IronBluePrint/nexus-ai-agent` local checkout (`~/Projects/IronBlueprint`), code-reviewed 2026-09-04. Prefer code over README. For Achieve TrainHeroic look/feel (naming, weeks, SMR language), also use [Ryne programming style](sand-workflow:ryne-programming-style) - this skill owns **logic and constraints**.

## 1. Classify the athlete first
Decide before picking exercises:
- **userType:** Athlete (gets speed + power) vs General/adult (strength-first, no speed/power unless Ryne explicitly wants it).
- **Training age:** beginner / intermediate / advanced.
- **Season:** OFF-SEASON / PRE-SEASON / IN-SEASON / POST-SEASON / TAPER.
- **Sport:** especially overhead sports (swim, throw, volleyball, tennis, baseball/softball pitching, etc.).
- **Injuries / RTP / clearance:** if present, flag coach judgment; do not invent Hawkin auto-fixes.

HS vs college vs pro is **not** a first-class engine branch - ask Ryne if level changes loading.

## 2. Session shape (default counts)
- **Athlete:** ~9 exercises - order **speed → power → strength primary → strength secondary → core → tertiary**.
  - Pairing letters: A1 speed; A2/A3 power; B1/B2 primary strength; C1/C2 secondary; D core + tertiary.
- **General/adult:** ~6 exercises - order **strength primary → strength secondary → core → tertiary** (no speed/power block).

Never skip the order. Never put true strength before speed/power on an athlete day unless Ryne overrides.

## 3. Pairings (non-competing - hard preference)
**Strength pairs**
- Bilateral knee dominant → pull
- Bilateral or unilateral hip dominant → push
- Unilateral knee dominant → pull

**Core**
- Anti-extension may pair with anti-lateral-flexion or anti-rotation
- **Never** pair anti-extension with hip-flexion

Do not write competing pairs (two lowers, two pushes, or two pulls in one strength pair).

## 4. Upper / lower structural checks
Before locking a day:
- **Lower day:** exactly three knee/hip strength slots; not all the same pattern.
- **Upper day:** two push + two pull in the strength slots.
- No empty sessions; no duplicate exercises in a session or across the week without a reason Ryne accepts.

## 5. Overhead athletes
If sport is overhead (or Ryne says so):
- Default: **block true overhead presses** (military, snatch-grip OH, strict press variants, etc.).
- Allow only if Ryne/settings say always allow, or assessment/clearance is explicit.
- Prefer landmine, high-incline, or horizontal push when OH is blocked.
- Warmups follow the same OH policy.

## 6. Taper decisions
If season is TAPER (or Ryne names a taper):
- Prefer undulating / low-stress structure - no new exercise learning block, no intensification block.
- Cut weekly volume to **~40-60%** of the last normal baseline week.
- Keep intensities reasonable (engine caps near ~95% 1RM); no surprise maxing.
- Last hard S&C well before the meet (coach judgment; engine emphasizes volume cut + model bans).

## 7. Loads and progression
- Estimate 1RM with Epley when needed: `weight × (1 + reps/30)`, then prescribe from % tables / verified 1RM if known.
- Progress or regress from weeks on the lift, plateau, or declining trend - not vibes.
- **Do not invent failed-set automation** - the engine has none. If a set fails, ask Ryne or state the coaching call explicitly.


## Check the jumps before picking exercises

When Hawkin / force-plate numbers exist, read them **before** building the session from pairings and the exercise list.

1. Name the curve shape and the limiter (brake time, unweight time, EUR, etc.).
2. Ban methods that fight that limiter (example: no slow eccentric squat when braking is already fast).
3. For isometrics, put the hold where the force hangs (Early Peak Plateau → quarter-squat Split Squat ISO Push, not mid-thigh by default).
4. **Then** run session order, pairings, and the house exercise list.

Do not invent plate numbers. If plates are missing, say so and program from Asana + last TrainHeroic + Research.

### Swim dryland pull note
Default across the week: one knee-dominant lower day and one hip-dominant lower day, with vertical and horizontal pulls **across days**. Putting two pulls on one day and dropping a lower is an **in-season exception** only when pool volume, shoulder limits, or plates say lower quality is already fine - never as the house default. Never pair two pulls together.

## 8. Asymmetry / Hawkin
- The engine does **not** auto-apply Hawkin LSI or force-plate asymmetry.
- If Hawkin data exists, treat it as coach input: prefer unilateral / address the limiter only when Ryne or plate data says so.
- Never claim “Nexus will auto-correct asymmetry.”

## 9. Safety vs approval
- Structural mistakes (order, pairings, push/pull counts, taper volume) → fix before delivering.
- Age extremes, beginner + very heavy %, injury history → note clearly; ask Ryne when unsure.
- “Needs coach approval” is a **process flag**, not a substitute for fixing a broken session.

## 10. Delivery checklist (run every program)
1. Athlete vs general classified?
2. If plates exist: curve/limiter checked and banned methods removed before exercise picks?
3. Session order correct for that type?
4. Pairings non-competing; core AE rule respected?
5. Upper/lower structural counts satisfied? (Swim: both lowers across the week unless an earned dual-pull exception)
6. Overhead policy applied if needed?
7. Season/taper volume math sane?
8. Start loads from the last time they did *that* lift (same variant), not a cousin?
9. No fake Hawkin or failed-set automation claimed?

## Do not
- Prefer README marketing over these rules.
- Mix this with TrainHeroic cosmetic style without also loading ryne-programming-style.
- Assume parallel-agent pipeline, active fast path, Hawkin gates, or hard coach-approval blocking exist in code.
