---
name: scene-draft
description: Draft a new scene or chapter from the outline, scene card, and story bible. Use whenever the author asks to draft, write, or generate a scene, chapter, or passage of the manuscript, or to produce alternative drafts for comparison.
---
# scene-draft
Draft the requested narrative unit; do not automatically commission critique afterward. During exploration, fix blockers and preserve momentum across the sequence. The author supplies voice exemplars at book setup; never invent replacements.

1. Preflight. Read `bible/style.md` (especially exemplar passages) and the premise/decisions set (AGENTS.md, Before every pass, step 2).
2. Read the outline beats for this chapter in `plan/outline.md`, `plan/summaries/` for the two preceding chapters (including their **End state**), and the open items in `bible/threads.md`. Read the last page of the previous chapter in full to match momentum.
3. Load only characters present in the scene. Re-read their Voice sections.
4. Write or update the scene card `plan/scenes/chNN.md` (template: `plan/scenes/_template.md`): goal, turn, who wants what, value shift, threads advanced, final image. If the author already wrote one, follow it and don't change it. Mark agent-generated cards as provisional hypotheses. Leave inapplicable craft fields blank; later review judges the intended experience as well as the card.
5. Draft. One sentence per line. Enter late, leave early. Let dialogue carry subtext; don't narrate what the dialogue shows.
6. Run `scripts/stats --slop` on the chapter and the slop-detector checklist; inspect hits and fix unwanted habits while preserving intentional effects.
7. Commit with `--pass draft`, listing any `New-canon:` facts. Commit the scene card in the same commit.
8. Record essential end-state changes (facts, knowledge, objects, unresolved tensions) in the affected chapter summary before a dependent chapter is drafted; keep planned events separate from established facts. Record the source revision and commit summary updates with `--pass canon-update`. In a multi-chapter request, carry that state forward without requiring an intervening critique.
9. Tell the author the word count, liberties taken, and open questions. Invite their own reading before evaluation; do not invent their reaction. For an active cycle, record the next step without declaring the reader effect verified.

## Alternatives (for important scenes)
When the author asks for options, draft each one on its own branch (`alt/chNN-<label>`, created from the same base, one model or approach per branch) and commit each with `--pass draft`. Then tell the author to run `scripts/blind-compare prepare manuscript/chNN-… alt/chNN-a alt/chNN-b` and to ask a different model for a blind judgement (blind-judge skill).
