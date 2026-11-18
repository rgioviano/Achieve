---
name: PRI question router
description: >-
  Use first on any PRI question (advisor or programming) to route it to the
  right manual pages, pattern skill, and notes before answering.
---
# PRI question router

Library (newest edition of each manual, PDF + searchable text): `/home/box/agent-data/agents/e9d0fc7f-22cc-4b14-80a6-4b8361108e36/memory/reference/manuals/`. `INDEX.md` lists editions and text quality. `ROUTER.md` maps patterns, tests, body regions/injuries, populations, and glossary aliases to manual pages and skills.

## Steps
1. Classify the question: pattern, test, technique, injury/region, population (swim/throw/lift/gait), concept/vocabulary, or research.
2. Open `ROUTER.md` for that row: note the manual + printed pages and the matching skill (left-aic, right-bc, pec, patho-pec, pri-right-bc-treatment-guidelines, pri-techniques-by-pattern, eval-cutoffs, pri-injury-presentations, pri-fundamentals-glossary, course skills).
3. Search the text live: `python3 <library>/pri_search.py "terms" [--manual NAME] [--topic] [--context N] [--max N] [--all]`. `--topic` expands PRI shorthand (ZOA, ADT, PART, etc.); `--all` also searches older `memory/reference/*.txt` extracts and articles (Swimming and Squat and Respiration live there, not in manuals/).
4. Load the matching skill, then answer: answer first, then reasoning. Tag every claim as PRI (manual + printed page), skill notes, or inference. Quote the manual line when it matters. Prescribe only named techniques found in the text.
5. If the library lacks it (no Cervical Revolution/TMJ, Vision, Advanced Integration, Interdisciplinary, or full Left BC manual), say so plainly; check `memory/reference/pri-research-digs/` or Ryne's Mac Desktop/PRI (with approval) before saying it isn't available.

## Notes
- Myokinematic and I&I text is OCR and uneven; verify headings and labels against the PDF page image (pdftoppm) before quoting.
- Cite printed page numbers, not the PDF index (the script reports both).
- Manual techniques are clinician-only; explain them if asked, never prescribe them for the gym floor.
