---
name: exercise-instruction-pass
description: >-
  Use when asked to draft, score, highlight, and source-check exercise
  instructions for one category (e.g. 'run the instruction pass on Bilateral
  Horizontal Push') in an exercise progressions Google Sheet.
---
# Exercise instruction pass (one category at a time)

Inputs: spreadsheet id, tab, category name (column B value). Default sheet: Achieve TrainHeroic Exercise Progressions (1Ccqbzmykl0Nl2x-bMbt_R30yAtOaIgBPOlMxp0Bt1N0). Never touch the IronBlueprint sheet or TrainHeroic.

## Ground rules
- Map columns by header text, never by letter (the owner moves columns). Find: Exercise Name, YouTube Link, Exercise Instructions (final), Draft Instructions, Confidence, Instruction Source, Draft Notes. If a draft column is missing, stop and ask; never add columns.
- Never overwrite the final Exercise Instructions column. Drafts go in Draft Instructions; promotion to final only when the owner says so.
- Skip any row whose final instructions are already filled, or whose draft/confidence cells were edited by the owner since your read. Re-read each batch right before writing it.
- Format: one step or cue per line inside one cell, plain sentences, no numbers, bullets, or headers.
- Show progress fast: write in batches of about 10 rows, never hold everything until the end.
- Never invent a source. Cap each video/web lookup at about 60 seconds, then move on.

## Sequence
0. Back up: export the sheet to xlsx on the box (dated filename) before any write. Pull the category's rows (start row, end row, blank separator) with the helper script `section` command if available.
1. Draft: for every eligible row, write step-by-step setup and execution instructions into Draft Instructions. Base them on, in order: the row's own linked video, an exact-name match in an approved reference sheet, the owner's approved rows for similar lifts, then general coaching knowledge. Fill Instruction Source with what you used.
2. Score: write Confidence 1-5 for each draft. 5 = verified against the row's own video or an exact approved match; 4 = matches reputable sources or approved rows (web-only caps at 4); 3 = plausible but unverified; 2 = notable doubt; 1 = likely wrong. Write all scores for the category before any fixes.
3. Highlight: color the Draft Instructions cell of every row scoring 3 or lower yellow (#FFF2CC) with format_cells. Clear the yellow when a row later scores 4 or higher.
4. Source-check every yellow row, bottom-up:
   - First the row's own YouTube link (pull transcript); else search the owner's own channel first (Achieve: "Achieve Sports Performance & Personal Training"), then reputable coaching videos or pages.
   - Rewrite the draft to match the source, update Instruction Source with the URL, rescore, and clear the yellow if it reaches 4+. If no source found within the cap, leave it yellow and note why in Draft Notes.
   - Flag (in Draft Notes, not by editing) any row whose linked video shows a different exercise than its name.
5. Verify and report: re-read the category, diff against the backup to confirm only the draft columns changed, then report counts: drafted, score breakdown, still yellow (with row numbers), wrong-video flags, and anything skipped because the owner edited it.
