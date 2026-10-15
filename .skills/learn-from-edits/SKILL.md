---
name: learn-from-edits
description: Analyse how the author edited agent-written text and propose updates to style.md, banned phrases, and character voice notes. Use when the author asks what they keep changing, to learn from their edits, or to improve future drafts.
---
# learn-from-edits
1. Run `scripts/learn-diff` (last 5 author edits) or `scripts/learn-diff --since <rev>`. It traces each prose line the author changed back to the agent pass and model that last wrote it, so you see edits to agent text, not the author revising their own prose. Attribution is approximate: blame credits the most recent line-level change.
2. Classify changes: cuts, word substitutions, rhythm changes, dialogue changes, added interiority, removed explanation, structural moves.
3. Find patterns that recur at least twice, across different scenes. One-off edits are taste in context, not rules; a run of cuts in one scene may have a local structural cause.
4. Phrase each pattern as a hypothesis for the author to confirm ("you seem to cut characters explaining their feelings — rule, or this scene only?"), with evidence (commit, before → after).
5. The summary counts (agent lines in reviewed files vs. lines changed) describe this window only. Don't rank models with them: what the author happened to review, task difficulty, and attribution all distort them. Model comparisons come from blind judging and the measures in `models.md`.
6. Write `feedback/YYYY-MM-DD-learn-from-edits.md` with proposed additions to `bible/style.md` (Do / Don't / Banned phrases) and to character Voice sections.
7. Do not edit style.md yourself. The author copies what they agree with. Commit with `--pass learn-from-edits`.
