---
name: Ad metrics decisions
description: >-
  Use this when auditing Meta or Google ads performance, choosing
  kill/hold/scale/refresh actions, explaining which metrics matter vs vanity, or
  updating monthly ads knowledge with metrics decision rules.
---
# Ad metrics decisions (Meta + Google)

Durable playbook for gauging effectiveness and acting. Label **[Documented]** (platform Help) vs **[Opinion]** (operating rule). Never invent account spend/CPA/ROAS/CPL. Prefer official Meta Business Help / Google Ads Help over blogs.

Source deep-dive (2026-10-01): `/workspace/ads-metrics-expertise-2026-10-01.md` - refresh that file + this skill when monthly Meta/Google knowledge routines find material metric changes.

## Unified framework

```
1. Tracking trustworthy? (primary event = business event or tight CRM proxy)
   NO → Fix tracking / CAPI / primary vs secondary. Do not scale.
   YES ↓
2. In Learning? (Meta ad set / Google Smart Bidding)
   YES → HOLD kill/scale except broken tracking, policy, brand-safety.
   NO ↓
3. Primary outcome vs target?
   CLEARLY WORSE for full decision window + enough events → KILL or restructure.
   AT/UNDER sustained → SCALE budget if delivery headroom.
   MIXED / early → HOLD ↓
4. Diagnostics: creative vs auction/offer/page?
   Meta: CTR↓ + frequency↑ + Creative limited/fatigue → REFRESH.
   Google: weak relevance / LP / bad FUE URL → fix assets/pages.
   High Lost IS (budget) + good CPA/ROAS → SCALE budget.
   High Lost IS (rank) → quality + bids/targets, not vanity CTR.
```

**Ignore early in learning [Opinion]:** day-1 CPL/CPA spikes; single-day CTR/CPM noise; QS “-” on new keywords; comparing Meta Instant Form CPL to Google CPA without the same CRM definition.

---

## Meta (lead gen)

### Hierarchy
1. Business: cost per booked / enroll (or CRM qualified stage) **[Opinion]**
2. Opt event: Instant Form lead **or** CRM qualified via CAPI **[Documented]**
3. Delivery: Learning / Learning limited; Creative limited/fatigue; frequency
4. Diagnostics only: CTR, CPM, CPC, raw CPL
5. Vanity: impressions/reach alone, engagement without downstream quality

### Learning **[Documented]**
- ~**50 optimization events** in the week after last significant edit → exit Learning.
- **Learning limited** = unlikely to hit ~50; not a penalty; fix feed of events (budget, audience, rare event, too many ads).
- Significant edits restart learning: targeting, creative, opt event, new ad in set, pause ≥7 days, bid strategy change.

### Leads vs qualified leads **[Documented]**
- **Maximize leads** = volume (contact share).
- **Maximize qualified leads** = CRM-informed quality; Instant Forms + CAPI. New campaigns need CAPI for this goal (from Apr 2026; existing impacted Aug 2026).
- Until CRM→CAPI healthy → Maximize leads + ruthless CRM QA. When healthy → Maximize qualified leads; stage within ~28 days; Meta often cites ~200 leads/mo and ~2–4 weeks training.

### Decision tables (ads)
| Action | When |
|---|---|
| HOLD | Still Learning; spend &lt; ~2–3× target cost-per-business-result; no clear fatigue |
| REFRESH | Creative limited/fatigue; CTR↓ vs this ad’s baseline + frequency↑ |
| KILL ad | Fair spend: weak CTR *and* weak booked/quality vs peers; or fatigue with replacements ready |
| Do not kill | Only because CPL is slightly high in first 2–3 learning days |

### Decision tables (ad sets)
| Action | When |
|---|---|
| HOLD | Learning / Learning limited while consolidating |
| KILL ad set | Post-learning; sustained cost per booked/enroll (or qualified) above kill for ~7+ days or ≥50 events; tracking verified |
| SCALE | Post-learning; at/under target sustained; creative not fatigued; raise budget gradually (big edits restart Learning) |

### Creative volume vs budget **[Opinion]**
If budget can’t feed ~50 events/week, fewer ad sets + rotating creatives beats many starved tests.

### Frequency **[Documented def; Opinion use]**
Impressions ÷ reach. Rising frequency + flat reach + falling CTR + rising cost/result → refresh candidate.

---

## Google (Search / AI Max)

### Hierarchy
1. Primary conversions & value (what Smart Bidding optimizes) **[Documented]**
2. CPA / ROAS vs target (ecom: also CAC vs margin) **[Opinion]**
3. Conversion rate
4. Search terms + landing pages (esp. Final URL Expansion)
5. Lost IS (budget) vs Lost IS (rank)
6. Diagnostics only: Quality Score components, Avg CPC, CTR - QS is **not a KPI / not auction input** **[Documented]**

### Primary vs secondary **[Documented]**
Primary = Conversions column + bidding. Secondary = All conversions only. Soft micros as Primary pollute Smart Bidding.

### Learning **[Documented]**
Smart Bidding ~**7–14 days** / often ≥~30 conversions to evaluate (often ~50 for tROAS). Avoid frequent budget/target/goal edits.

### AI Max **[Documented]**
- Wait **≥2 weeks** after enable before heavy negatives.
- Weak when **budget-limited**.
- FUE can pick other URLs; RSA pins ignored when FUE picks URL. Lock with URL inclusions/exclusions; check landing pages report.

### Decision tables
| Action | When |
|---|---|
| HOLD | New AI Max &lt;~2 weeks or Smart Bidding still Learning |
| NEGATE | Term consistently spends with zero/poor primary conv.; use negatives sparingly on AI Max |
| KILL keyword | Post-learning: high spend, no/poor primary conv., search terms confirm bad intent |
| SCALE budget | Healthy CPA/ROAS + high Lost IS (budget) |
| Fix rank | High Lost IS (rank) → ads/LP/relevance/targets, not vanity CPC |
| FUE exclude | Landing pages report: wrong/thin/non-converting URL |

---

## Local lead gen vs purchase (mapping)

| Business | Judge on | Platform opt |
|---|---|---|
| Local lead gen (e.g. gym Instant Form → booked eval → enroll) | Cost per booked / enroll; lead→booked % | Meta Leads; Maximize leads until CAPI, then qualified leads |
| Purchase / SaaS | Purchase ROAS; CAC vs margin | Sales / Maximize conversion value or tROAS |

Never invent account numbers. Monthly knowledge refreshes must re-check metrics decision rules, not only product UI changes.

## When running this skill
1. Confirm tracking + primary conversion definition.
2. Check Learning status before any kill/scale.
3. Decide with business metrics; use diagnostics only to explain.
4. Label advice [Documented] vs [Opinion].
5. For Achieve/IB specifics, also read current agent memory (quality-first Meta, unit econ, no spend without yes).
