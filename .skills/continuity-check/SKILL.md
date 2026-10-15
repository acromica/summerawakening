---
name: continuity-check
description: Check manuscript chapters against canon, timeline, threads, and character files for contradictions and knowledge leaks. Use whenever the author asks about continuity, consistency, plot holes, timeline errors, or after TODOs or drafts that change facts.
---
# continuity-check
1. Read `bible/canon.md`, `bible/timeline.md`, `bible/threads.md`, the character files for everyone in the chapters under review, and the **End state** in `plan/summaries/` for the chapter before the range.
2. Read the chapters. For each factual claim (names, ages, dates, eye colour, who knows what when, distances, travel times, objects' locations), compare with canon, with the previous end state, and with earlier chapters.
3. Write `feedback/YYYY-MM-DD-continuity-<model>-<scope>.md` with a table: location (file:line) · claim · conflicts with · severity · suggested fix.
4. Also list "knowledge leaks": characters acting on information the end states say they don't have yet.
5. Follow the feedback protocol in AGENTS.md (skip rulings already made; add your findings to `feedback/INDEX.md`).
6. Do not edit the manuscript. Commit with `--pass continuity`.
