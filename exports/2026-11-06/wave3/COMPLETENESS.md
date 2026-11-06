# Achieve 2026-11-06 wave3 export completeness

privacy_ready: true after this review. The archive flag was true and was not treated as proof.
wave: 2026-11-06-wave3
archive_sha256: c758a4b1b3c375bacf490d2d7d48783d91d472966c8974bd199be604bc32df22
review: memories, user_facts, instructions, routines, and custom skill bodies were read. Public skill texts were kept in full. Private entries were removed whole. Private urls and file ids were removed as sections. Removed text is not quoted here.
brain_lint.py from this archive was not copied. Main already reads every file in full. Rules were not weakened.

## Bots
- darwin
- pri
- th-exercise-library

## Files (committed bytes)
- `bots/darwin/export/grok-bot-export-darwin.json` bytes=9583450
- `bots/pri/export/grok-bot-export-pri.json` bytes=9557373
- `bots/th-exercise-library/export/grok-bot-export-th-exercise-library.json` bytes=9471956

## Whole entries removed (original indexes)

darwin memories: 13, 15, 37, 38, 51, 83, 84
Reasons: a named athlete, post-surgical and fracture cases, a named plate read.

pri memories: 5, 8, 22, 23, 34
pri user_facts: 14, 15
Reasons: personal shoulder health, a named athlete, a family death.

th-exercise-library memories: 2, 4, 8, 9
Reason: private Google Sheet file ids.

## Sections removed, entry kept

- darwin memories 7 and 8: private Cursor project urls
- darwin instructions: private Cursor project url
- pri memories 25: private Cursor project url
- th-exercise-library memories 3: stock-sheet file id
- th-exercise-library memories 5: private Cursor project url

Custom skill bodies had no remaining client or athlete names, so no skill text was deleted.
