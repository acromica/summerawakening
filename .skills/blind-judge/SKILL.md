---
name: blind-judge
description: Judge anonymised alternative versions (A, B, C…) of a chapter or scene prepared by scripts/blind-compare, without knowing which model or approach produced which. Use when the author asks to blind-judge, compare drafts blind, or pick the best of several versions.
---
# blind-judge
1. The author gives a comparison id. Read only `build/blind/<id>/A.md`, `B.md`, … plus `plan/premise.md`, `bible/style.md` (exemplar passages), and the scene card `plan/scenes/chNN.md` if one exists.
2. Don't read `build/blind/<id>/.key.json`, the `alt/*` branches, git log, or `prompts/`. Knowing the author would bias the judgement; if you learn it by accident, say so in the report.
3. Judge against the scene card and the target reader, not against your own taste:
   - Which version best delivers the scene's goal, turn, and final image? Which has the sharper crisis (a real choice) and the stronger escalation (`reference/craft-lenses.md` §1 and §4)?
   - Which is closest to the voice of the exemplar passages?
   - Which would the target reader in `premise.md` prefer, and would a literary critic agree?
   - The best moments of each loser: lines worth grafting into the winner (quote them with letter:line).
4. Give a ranked verdict with confidence (clear / slight / toss-up). A toss-up is a valid answer.
5. Write `feedback/YYYY-MM-DD-blind-<model>-<id>.md` and commit with `--pass blind-judge`. Tell the author to run `scripts/blind-compare reveal <id>` and to record the result in `models.md`.
