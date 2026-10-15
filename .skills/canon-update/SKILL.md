---
name: canon-update
description: Update bible/canon.md, bible/timeline.md, bible/threads.md, character arc checkpoints, per-chapter summaries in plan/summaries/, and plan/synopsis.md from the manuscript after drafting or revision. Use after a chapter is merged, when the author asks to update the bible, summaries, or synopsis, or when commits carry New-canon notes.
---
# canon-update
Refresh only records affected by the changed unit. Before dependent drafting, ensure essential end states are current; a full-book reconciliation is not required after every chapter. Record the source revision in updated chapter summaries, and distinguish what the manuscript establishes from plans and character beliefs.
1. Run `scripts/memory-status` to see which summaries are stale and how many canon entries cite changed chapters. Find new facts: `git log --format=%B <since>..HEAD | grep -A20 'New-canon:'` and read changed chapters (`git diff --stat <since>`).
2. Add each fact under the right heading in `bible/canon.md`, using the entry forms in its header: established fact, a character's belief, author-only truth, or open possibility. If a fact contradicts existing canon:
   - the author rewrote or retconned it (an author-edit or a decision says so) — strike the old line through and note what superseded it; never delete it silently;
   - otherwise — don't overwrite: add it to `open-questions.md` and flag it.
   When a passage that established a fact was cut, mark the fact superseded, then search `bible/threads.md`, character files, and later summaries for anything that depended on it, and list those in the commit body.
3. Update `bible/timeline.md` and any affected character's "Arc checkpoints".
4. Update `bible/threads.md`: add setups the chapter plants, mark payoffs it delivers (`paid chNN`), and note threads that went quiet.
5. For each changed chapter, rewrite `plan/summaries/chNN.md` from `plan/summaries/_template.md`: a summary of what is on the page (not what was planned) and the **End state** (who knows what, where things and people are, physical and emotional state). Set `Source revision:` to the full commit id of the chapter text you summarised (`git log -1 --format=%H -- manuscript/chNN-*.md`); `scripts/memory-status` uses it to flag the summary when the chapter changes. Keep the summary under 150 words; it is loaded as context by every neighbouring pass. Where a later scene depends on exact wording (a promise, a clue, a line someone will quote back), cite `chNN:line` instead of paraphrasing.
6. If a chapter's events change the book's shape, refresh the part and book paragraphs in `plan/synopsis.md`.
7. In an active cycle, record which memory files were refreshed and any unresolved contradictions under `Continuity and memory`. Do not mark the reader-effect objective verified merely because canon is updated.
8. Never edit manuscript prose. Commit with `--pass canon-update`.
