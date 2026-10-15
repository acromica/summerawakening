---
name: developmental-critique
description: Structural critique of a chapter, act, or whole manuscript — stakes, pacing, arcs, scene function, promises and payoffs — judged against the book's intent and audience. Use whenever the author asks for a critique, review, feedback, or editorial report. Never edits the manuscript. For a reader's reaction without the bible, use cold-read; for scored reader personas, use reader-report.
---
# developmental-critique
Output only a report: `feedback/YYYY-MM-DD-critique-<model>-<scope>.md`. Do not touch `manuscript/`.

Ideally run this with a different model than the one that drafted the text (see `models.md`).

## Before writing
1. Read `plan/premise.md` (audience, "must never become"), `plan/scenes/chNN.md` for the chapters in scope, `bible/threads.md`, and run `scripts/stats` on the chapters in scope.
2. Follow the feedback protocol in AGENTS.md: read `decisions.md` (including **Deliberate choices**) and the `rejected` rows of `feedback/INDEX.md`. Don't re-raise them unless you have a new argument, and then say so.
3. If a recent `cold-read` report covers the scope, read it: where intent and reader experience diverge is the first thing to examine.
4. Read `reference/craft-lenses.md` §0 and whichever of §1–5 the premise's "Craft lenses" field selects (empty: §0, then others only to explain a problem a reader would feel). Use them to find and name problems, not as a checklist to fill in. Write "n/a" rather than force a lens onto a scene.

## Choose the depth
Default to a focused report: what to preserve, the most consequential uncertainty, and at most three priority findings with evidence, likely reader effect, and suggested TODOs. Use the current cycle's objective when available. Stop when that question is answered; do not manufacture findings to fill a quota.

Use the comprehensive structure below when the author requests a full developmental review or when an authorized milestone review needs it. Apply only relevant craft lenses. A scene may contribute atmosphere, perception, comedy, or relationship without a conventional crisis; assess that contribution against this book's intent. Agent-generated scene cards are hypotheses, not independent proof of success.

## Comprehensive report structure
1. **What works** — specific, with line references. The author must know what to protect.
2. **Biggest problem** — the single change with the most impact on the target reader in `premise.md`.
3. **Intent vs. page** — for each scene card, did the scene deliver its goal, turn, and final image? Quote the evidence.
4. **Scene-by-scene** — for each scene, first its contribution (§0) and whether it earns its length; then, where §1 is in use: value at stake and its shift (from → to), crisis (the real choice, and whether it is a best bad choice or irreconcilable goods), outcome (yes-but / no-and / clean), tension source, verdict (keep / cut / merge / rework). End with the polarity run across the chapter's scenes.
5. **Characters** — want vs. need, the lie, and whether change comes through costly choices; arc type versus the premise's intent; are voices distinct?
6. **Promises, progress, and payoffs** — the promises the opening makes (tone, story, character, genre) and whether they're kept; the progress signpost in each chapter (flag chapters with none); payoffs checked against `bible/threads.md` (earned? surprising yet inevitable?); thread nesting by MICE type; new setups and dropped threads.
7. **Pacing and escalation** — where attention sags or rushes; beats that repeat rather than escalate; scene/sequel balance. Use the stats (sentence-length spread, dialogue share) as evidence, not as verdicts.
8. **Immersion** — abrupt psychic-distance jumps, needless explanation, and sentimentality, frigidity, or mannerism, quoted.
9. **Drift** — any movement toward an item on the "must never become" list; name the item.
10. **Suggested TODOs** — ready-to-paste markers the author can drop into the text, e.g. `<!-- TODO [next]: … -->`.

Be direct. Rank issues. Number every finding. No generic writing advice; every point cites the text.
Add each numbered finding to `feedback/INDEX.md` as `open`. Commit with `--pass critique`.
