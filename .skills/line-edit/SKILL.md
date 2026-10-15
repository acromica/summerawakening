---
name: line-edit
description: Sentence-level editing for rhythm, precision, and economy, in the author's voice. Use whenever the author asks to line edit, tighten, polish, or copy edit a passage.
---
# line-edit
1. Preflight. Read `bible/style.md` in full; the exemplar passages set the target.
2. Respect `<!-- LOCKED -->` spans and author-only rules in `decisions.md`.
3. Read `reference/craft-lenses.md` sections 5–7 and run `scripts/stats --slop` on the passage.
4. Edit for: precise verbs and nouns, cutting redundancy and filter words (saw, felt, noticed), varied rhythm, clean dialogue attribution, removal of banned phrases. Also:
   - stimulus before response in charged moments (no "she flinched as the glass shattered");
   - psychic distance that moves a step at a time unless a jump is clearly deliberate;
   - cutting needless explanation of what the scene already shows.
5. Don't change plot, facts, or characterization. Don't homogenize voice — a strange, right sentence stays. Where the style guide and a craft lens disagree, the style guide wins.
6. Keep one sentence per line so the diff shows exactly what changed.
7. Commit with `--pass line-edit`. In the body, note any pattern you fixed repeatedly (useful for style.md).
