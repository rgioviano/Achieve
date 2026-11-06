# Achieve 2026-11-06 wave2 export completeness

privacy_ready: true after this review. The archive flag was false and was not treated as proof.
wave: 2026-11-06-wave2
archive_sha256: c62cd2f43038619e64fdec3da998b36a27c6e222e543ec0d3cd6ca206f5ad633
review: memories, user_facts, instructions, routines, and custom skill bodies were read. Public skill texts were kept in full. Private entries were removed whole. Private urls and file ids were removed as sections. Removed text is not quoted here.
brain_lint.py from this archive was not copied. Main already reads every file in full. Rules were not weakened.

## Bots
- hawkin
- lark
- max
- maya
- quill
- rank
- red

Wave1 exports (canvas, coach, eval-brief, metric, nova, penny, tally) were not overwritten.

## Files (committed bytes)
- `bots/hawkin/export/grok-bot-export-hawkin.json` bytes=9532952
- `bots/lark/export/grok-bot-export-lark.json` bytes=9811757
- `bots/max/export/grok-bot-export-max.json` bytes=9750364
- `bots/maya/export/grok-bot-export-maya.json` bytes=9420697
- `bots/quill/export/grok-bot-export-quill.json` bytes=9683191
- `bots/rank/export/grok-bot-export-rank.json` bytes=9476731
- `bots/red/export/grok-bot-export-red.json` bytes=9536964

## Whole entries removed (original indexes)

hawkin memories: 13, 22, 23, 31, 48, 53, 54, 61, 62, 66, 67, 68, 70, 79, 90, 91, 94
hawkin user_facts: 9, 10
Reasons: athlete names, plate reads tied to named athletes, a clinical case, a family death.

max memories: 9, 62, 92, 96, 104, 110, 113, 115, 116, 120, 122, 125, 126, 127, 128, 129, 130, 131, 132, 133, 136, 139, 140, 141, 142
Reason: lead and athlete names in follow-up logs.

maya memories: 49, 50, 56
maya user_facts: 6
Reasons: athlete names, a studio payment link, a family death.

quill memories: 55
quill user_facts: 8
Reasons: a named health record, a family death.

red memories: 22, 39, 44, 46, 51, 54, 58, 65, 108, 109, 110, 111, 116, 139, 142, 174, 175, 180, 181, 182, 183, 184
red user_facts: 10, 11, 15
Reasons: athlete and parent names, clinical notes, a Drive folder id, a family death.

lark and rank: no whole entries removed.

## Sections removed, entry kept

- hawkin memories 5: private Cursor project url
- lark memories 6: private Cursor project url
- rank memories 2 and 3: private Cursor project urls
- max memories 26: pay-page url with a studio id
- max memories 35: Google Doc url
- max memories 36: private tunnel url
- max user_facts 13: Cursor project ids
- maya memories 54: Google Doc url
- maya memories 61 and 63: private tunnel urls
- quill memories 16: Google Doc url
- quill memories 17: studio id and pay-page url
- quill memories 20 and 21: private tunnel urls
- red memories 20: Drive folder id inside a rule
- red memories 97: nutrition Doc url
- red memories 105: private tunnel url
- red memories 130: form urls
- red memories 164: Drive folder id inside a standing don'ts note
- red routines 0: one sentence that named people

Custom skill bodies had no remaining client or athlete names, so no skill text was deleted. Course wording about rib depression, inhale, and shoulder mechanics stayed.
