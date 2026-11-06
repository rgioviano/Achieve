---
name: Meta and Google Ads playbook
description: >-
  Use when building, diagnosing, scaling, killing or rewriting Meta Ads or
  Google Ads for Achieve Sports Performance or IronBlueprint, when writing Meta
  ad text fields (Primary, Headline, Description, CTA), or when the monthly
  meta-ads-knowledge-refresh or google-ads-knowledge-refresh runs.
---
# Meta and Google Ads playbook (Lark owns)

Moved out of Lark's profile 2026-11-01 (Lauren/@poteto ops: long playbooks live in skills, profiles stay short). This file is the playbook the monthly refresh routines update. Lark's profile keeps job, anti-jobs, voice, wake and VERIFY.

Pair with [Ad metrics decisions](sand-workflow:ad-metrics-decisions) for kill/hold/scale metric rules and [Ads Audit](sand-workflow:ads-audit) for audit findings format.

## Monthly refresh rule
- meta-ads-knowledge-refresh (1st ~9:17am CT) edits only the Meta sections below; google-ads-knowledge-refresh (1st ~9:27am CT) edits only the Google section.
- Prefer official Meta Business Help / Google Ads Help. Flag industry practice as [Opinion].
- Before saving a change to a kill, scale or learning rule, show Ryne the before and after. Do not rewrite silently (Ryne, 2026-10-18).
- Back up this file as `SKILL.md.bak-YYYY-MM-DD` before an edit. Add one line to the changelog at the bottom.

## Benchmarks (until Ryne's economics override)
- Achieve: cost per booked eval / enrolled member, not vanity CPL.
- IronBlueprint: purchase ROAS and CAC vs margin.
- Early learning: trust delivery + creative/asset health over CPA alone. After learning: CPA/CAC/ROAS plus CRM truth (booked/showed/paid).
- Platforms are not profit. Reconcile to CRM (Prospect Tracking) / Stripe when numbers conflict.

## Meta playbook
- **Structure:** Achieve local lead gen: Leads (Instant Form / call / Messages), or website conversion only if Pixel+CAPI fires a reliable booked-eval event. Awareness only for brand bursts. IronBlueprint: Sales/purchase (or checkout if volume is thin). Instant Form = volume; website form = higher intent.
- **Advantage+/ASC** when conversion volume + creative depth support it. Manual for new accounts, tight Achieve geo, controlled tests, retargeting isolation. Do not overlap ASC + manual cold.
- **Budget:** CBO to scale similar proven ad sets; ABO for tests. Never mix prospecting + retargeting in one CBO.
- **Learning:** ~50 optimization events / ad set / ~7 days after big edits.
- **Kill:** broken tracking/LP; ~2-3x target CPA with 0 results; after learning, CPA stuck ~50%+ over target.
- **Scale:** only after ~3-7 stable profitable days; +10-20% budget every 2-3 days.
- **Audience:** broad / Advantage+ with strong creative when Pixel+CAPI are healthy.
- **Retargeting:** separate campaign; exclude members/customers from cold; refresh when frequency ~3-3.5 / 7d.
- **Creative as ads:** ~3-5 new CONCEPTS/week; UGC/native for cold; hooks in 0-3s. Compliance: no body-shame, miracle claims or disease cures.
- **Measurement:** Pixel + CAPI with matching event_name/event_id, Advanced Matching. Achieve: Lead + CRM stages. IronBlueprint: Purchase (+value).

## Meta ad text (Scout brief 2026-10-01)
- Primary text front-loads the offer (Reels ~40-44 chars visible; Feed ~125).
- Headline holds the must-know (FB Feed often ~27; Help ~40).
- Description = nonessential only (Feed may hide it).
- CTA = fixed Meta label from objective x destination. Achieve: Book now / Contact us / Sign up / Send message. IB: Learn more / Sign up / Get quote.
- Classic DR mapping: Headline = Ogilvy telegram; Primary = AIDA + Hormozi value + proof; CTA = action match.
- Multiple text options = alternate awareness entries, never contradictory claims.
- Preview Feed/Stories/Reels; respect safe zones; set Advantage+ text toggles knowingly.
- Quill (copywriter) sharpens lines only after Lark locks these constraints.

## Google Ads playbook
- **Structure:** separate Brand Search vs Non-brand Search; optional capped Competitor. Search (+ AI Max) = high-intent core. PMax complements Search: brand exclusions + negatives so PMax does not cannibalize Brand. Demand Gen = upper-mid funnel, not a Search replacement.
- **Achieve local:** Presence geo (not Presence or Interest); call + lead-form + location/GBP assets. **IronBlueprint:** high-intent + PMax after clean tracking.
- **Bidding:** Smart Bidding (Max conversions / Target CPA / Max conversion value / Target ROAS). Do not thrash during learning (~1-2 conversion cycles; ~30+ conv, ~50 for tROAS).
- **Keywords / AI Max / RSA:** Broad needs Smart Bidding; AI Max needs brand exclusions + negatives first; RSA with 2+ Good/Excellent, up to 15 headlines / 4 descriptions, pin sparingly.
- **PMax:** themed asset groups; Excellent Ad Strength; search themes; brand exclusions.
- **Tracking:** one primary conversion per true outcome; Enhanced Conversions for Leads + Data Manager API; Consent Mode Advanced when possible.
- **Kill / scale / rewrite** [Opinion, calibrate to his CPA/ROAS]: ~2-3x target CPA with 0 conversions: pause/negate. Scale up to ~20% when on target + high Search lost IS (budget). Protect brand from PMax cannibalization. Disable structural auto-apply without his yes.

## Changelog
- 2026-11-01: created from Lark's profile (META PLAYBOOK, META AD TEXT, GOOGLE ADS PLAYBOOK, Benchmarks). Content unchanged; only reformatted.
