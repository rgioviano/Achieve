---
name: Ads Audit
description: >-
  Use when the user wants a Google Ads or Meta audit. Propose only. Findings
  must clear a money bar and read like a decision, not a dashboard.
---
Hunt concrete paid-ads problems. You only propose. Never apply, pause, bid, or delete in this skill.

## Connector
If the Ryze AI connector is missing, stop. Add `https://connector.get-ryze.ai/mcp` (docs: https://www.get-ryze.ai/how-to-connect-claude-to-google-meta-ads-mcp). Wait.

List connections. Use the accounts they named. None named → workspace defaults, and say which.

## Pull
Current vs prior (default last 7 vs prior 7). Slice below campaign: search terms, placements, schedule, device, geo, ads/creatives. Campaign totals are context, not findings.

Google money is micros ÷ 1,000,000. Meta Graph money is often minor units ÷ 100, except Insights `spend` (already whole). Empty or all-zero Insights is not zero spend — recheck the window. Never invent spend, CPA, or ROAS.

## The bar
An empty run is a good run. "Could be better" is not a finding.
A finding needs: exact entity name, real numbers over a real window, a from → to change, honest impact.
Skip paused, ended, zero-delivery. Skip idle cleanup.
Materiality: about $100/month measured waste, or ~3% of monthly spend, whichever is larger.
At most three findings, worst first. One root cause = one finding.

## Hunt, in order
A. Money burning — broken conversion tracking, disapproved ads, search terms/placements with spend and zero conversions, hours/geos/devices with CPA at a multiple of account average.
B. Money missed — converting search terms with no exact keyword; budget-capped campaigns losing impression share to *budget* (not rank) with strong ROAS. Small reversible step, never a double.
C. Hygiene — fatigued creatives, one ad eating all spend, overlapping audiences. Only if it clears the same money bar.

## How a finding reads
Five pieces or it is not a recommendation:
1. Thesis — one sentence, a number from THIS account
2. Evidence — two or three facts with metrics, no adjectives
3. Action — entity, field, from-value, to-value
4. Impact — magnitude + confidence, scoped to a window
5. Watch for — the metric and threshold that would prove it wrong

Title is a claim ("$2.1k/mo on search terms with 0 conversions"). One visual identity. No 20-row tables.

## After the list
Wait for a yes on those exact items. Prefer pause over delete.
