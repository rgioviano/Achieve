# Achieve export checkpoint completeness

privacy_ready: true
semantic_review: full re-scan of memories, user_facts, instructions, routine instructions;
known client/athlete identifiers and personal-health clinical content removed when present;
brain_lint secrets/pii/emdash exit 0; scan.py empty.
skills: non-Chief incomplete/unverified; only full-text skills after Chief fill kept.

## Bots
- canvas
- coach
- eval-brief
- metric
- nova
- penny
- tally

## Files
- `bots/canvas/export/grok-bot-export-canvas.json` bytes=10174073
- `bots/coach/export/grok-bot-export-coach.json` bytes=10313714
- `bots/eval-brief/export/grok-bot-export-eval-brief.json` bytes=18487
- `bots/metric/export/grok-bot-export-metric.json` bytes=9447666
- `bots/nova/export/grok-bot-export-nova.json` bytes=9666502
- `bots/penny/export/grok-bot-export-penny.json` bytes=9471071
- `bots/tally/export/grok-bot-export-tally.json` bytes=9690644
- `scripts/brain_lint.py` bytes=9117
