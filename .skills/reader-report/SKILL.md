---
name: reader-report
description: Simulate the book's target readers (a literary critic, a core genre reader, a skeptical general reader, as defined in plan/readers.md) and score chapters on a fixed rubric so quality can be tracked across revisions. Use when the author asks how readers or critics would respond, for a reader panel, for scores, or whether a revision made a chapter better.
---
# reader-report
1. Run `scripts/agent-preflight --reader`. Read `plan/premise.md` (audience) and `plan/readers.md`. If `plan/readers.md` still holds only the template, stop and offer to draft personas from the premise for the author to approve (`--pass bible`); don't score with placeholder personas.
2. Use `scripts/reader-copy` for the chapters in scope and read only the sanitized chapters and manifest. Cite original filenames/lines. Do not read the cycle note or expected revision outcome. Don't read the bible, outline, scene cards, or earlier feedback: personas read the page, not the plan.
3. For each persona, in that persona's voice and priorities:
   - Score each chapter 1–5 on the rubric in `plan/readers.md`, one line of evidence (file:line) per score.
   - Name the line where this reader would stop reading, if any, and the line they'd quote to a friend.
   - Where the story's spell broke for this reader (`reference/craft-lenses.md` §5): the critic notices sentimentality, mannerism, and needless explanation; the core reader notices broken genre promises and stalled progress (§2); the general reader notices confusion and stretches with nothing at stake.
   - Two sentences of overall verdict.
4. **Disagreements** — where the personas split, and why. Splits are often the most useful finding: the critic and the genre reader wanting opposite things marks a real design choice for the author.
5. Write `feedback/YYYY-MM-DD-readers-<model>-<scope>.md`. Append one row per persona × chapter × criterion to `feedback/scores.tsv`: `date`, `source` = `ai`, `model_or_reader` = your exact model id, `chapter`, `persona`, `criterion`, `score` (1–5 or `n/a`), `confidence` (low / medium / high), `rubric_version` from `plan/readers.md`, `input_revision` = the `revision` in the reader-copy manifest, `scope` = the chapters you read, `run_id` = the reader-copy directory name. Compare scores only within the same model, rubric version, and input scope; models score on different scales, and repeat runs vary.
6. Commit the initial report and scores with `--pass reader-report` before opening decisions or earlier feedback. Then apply the feedback protocol and index numbered findings in a second commit without rewriting the initial reactions. Don't edit the manuscript.

Scores are diagnostic judgments from one model, not independent reader votes or proof of publication quality. Quote evidence, disclose uncertainty and prior exposure, and record the input revision and scope. Use the rubric anchors in `plan/readers.md`; compare a revision with the same rubric and input conditions, preferably blind. Human target-reader responses at sequence and full-draft milestones remain a separate source of evidence.
