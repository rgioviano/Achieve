# Achieve export checkpoint completeness

privacy_ready: true for the inventory below, after the 2026-11-06 scrub.
semantic_review: memories, user_facts, instructions, routines, and personal/custom skill bodies in canvas, coach, nova, penny, and tally were read in full. A whole entry was removed when it contained a client or athlete identifier, a training or health detail tied to a named person, a nonpublic phone or email, a secret, or when the reviewer was unsure. Names were not swapped for placeholders.
brain_lint: `scripts/brain_lint.py` reads each file in full. The old 5,000,000 byte cap is gone so large exports are not cut off. The secrets, pii, and emdash rules are unchanged. Full tree exit 0 on 2026-11-06 (0 hits, 224 files).

Original exporter note, kept as history: the checkpoint first said known identifiers were already removed, non-Chief skills were incomplete or unverified, and only full-text skills after Chief fill were kept. This scrub found remaining identifiers and removed the entries below.

## Bots
- canvas
- coach
- eval-brief (unchanged; no identifiers found)
- metric (unchanged; no identifiers found)
- nova
- penny
- tally

## Files
- `bots/canvas/export/grok-bot-export-canvas.json` bytes=10172939
- `bots/coach/export/grok-bot-export-coach.json` bytes=10312755
- `bots/eval-brief/export/grok-bot-export-eval-brief.json` bytes=18487
- `bots/metric/export/grok-bot-export-metric.json` bytes=9447666
- `bots/nova/export/grok-bot-export-nova.json` bytes=9664795
- `bots/penny/export/grok-bot-export-penny.json` bytes=9465987
- `bots/tally/export/grok-bot-export-tally.json` bytes=9685883
- `scripts/brain_lint.py` bytes=9181

## Omissions (original indexes)

canvas
- memories 9: athlete identifier plus training numbers
- memories 10: athlete identifier on a progress page
- user_facts 14: private family event
- skill achieve-prospect-tracking: entire appended heartbeat.log (lead names)

coach
- memories 95: named athletes in an open-items note
- skill achieve-prospect-tracking: entire appended heartbeat.log (lead names)

nova
- memories 12: athlete names inside a caption-format note
- memories 18: named athlete session
- memories 19: named athlete session
- user_facts 4: private family event
- skill achieve-prospect-tracking: entire appended heartbeat.log (lead names)

penny
- memories 30: parent and athlete
- memories 39: athlete name in a training-options note
- memories 40: possible person name in a close note (unsure, whole entry removed)
- memories 41: parent, athlete, and contract status
- memories 43: phone-only lead record
- memories 48: lead names in a scheduling note
- memories 49: nonpublic phone
- memories 50: private family event
- memories 52: nonpublic phone
- memories 55: person name in an ops note (unsure, whole entry removed)
- memories 59: outbound test to a redacted phone
- memories 64: nonpublic phone
- routines removed whole (instruction was already a redaction placeholder): 6:45am morning brief; Lead sends report to Tally; Achieve anniversary + Overachiever shirts; Speed-to-book new lead (webhook); Project heartbeat - Quo SMS cutover

tally
- memories 3: lead-stage rules plus one named prospect
- memories 22: speed-to-book log naming leads
- memories 23: project heartbeat naming leads
- memories 24: speed-to-book log naming leads and a child
- memories 25: project heartbeat naming leads
- memories 26: speed-to-book log naming leads
- memories 28: walk-in record naming people
- user_facts 8: private family event
- instructions: one prospect-name sentence removed; the rest of the job text stayed
- routines removed whole (instruction was already a redaction placeholder): Speed-to-book lead log; Friday lead scoreboard; Project heartbeat - Achieve lead pipeline
- skill achieve-prospect-tracking: entire appended heartbeat.log (lead names)

Penny does not carry the achieve-prospect-tracking skill.

## Repo files edited so lint can pass
These were already in the brain. Only the email literals were removed.
- `skills/achieve-mail/SKILL.md`: personal Gmail address literal removed. sha256=dd0a524015b38023e1a3fbea5554890eb850361cf48c66b23c861a424d165fbf bytes=3862
- `skills/achieve-writing-style/SKILL.md`: two copies of one staff address literal removed. sha256=0e63654bde626aa8c7eea7e453cf74ee0dda6751b03f3dbc321cbaaa1f5e3d2c bytes=13177

## Formatting
In canvas, nova, and tally, one JSON newline that sat directly against the allowed contact address was given a following space. Parsed text still shows that address. A raw-text scan no longer glues the newline escape to the address.
