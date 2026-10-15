---
name: structural-revision
description: Plan and stage a revision that spans chapters — cutting or adding a subplot, moving a reveal, merging characters, re-ordering scenes, changing a character's arc — by writing a cross-chapter plan and, after approval, placing scoped TODO markers in every affected chapter. Use when the author asks for a structural edit, a big-picture revision, or a change that touches more than one chapter.
---
# structural-revision
TODOs fix paragraphs. This skill handles the changes TODOs can't see.

## Phase 1 — plan (no manuscript edits)
1. Preflight. Read `plan/premise.md`, `decisions.md`, `plan/synopsis.md`, `plan/outline.md`, all `plan/summaries/`, `bible/threads.md`, the character files affected, and the premise's chosen lenses from `reference/craft-lenses.md` (usually §0 and §2). Check that the change keeps the opening's promises, that every affected scene still contributes something, and, where those lenses are in use, the threads' nesting order (MICE) and that affected arcs still turn on the characters' own choices.
2. Write the change into `plan/revision-plan.md`:
   - **Goal** — what the change is for, in terms of reader experience.
   - **Verification and stopping condition** — how the intended effect will be checked across the sequence, what strengths to preserve, and the authorized effort limit; link `plan/cycle.md` when active.
   - **Ripple map** — a table: chapter · what must change there · why · size (line / paragraph / scene / new scene / cut).
   - **Canon and thread effects** — facts, timeline entries, threads, and arc checkpoints that change.
   - **Order of work** — which chapters first (usually the one that establishes the new fact).
   - **Risks** — what could break, especially items on the "must never become" list.
   - **Out of scope** — what this pass deliberately leaves alone.
   - An empty `Author:` line under each ripple row.
3. Commit with `--pass structural-revision`. Ask the author to annotate (`approve` / `modify: …` / `skip`) and commit with `scripts/author-commit`.

## Phase 2 — stage (after the author's annotations)
4. For each approved row, insert a scoped TODO marker at the right place in the chapter (`[start]…[end]` for ranges, `[insert]` for new scenes), quoting the plan item in the directive. Inserting markers is the only manuscript change allowed in this phase.
5. Run `python3 scripts/todo.py ids`, then commit with `--pass structural-revision -m "Stage <goal> as TODOs tN–tM"`.
6. Tell the author the markers are in place. Implementation then runs through `todo-plan` / `todo-implement` as usual, chapter by chapter in the planned order, followed by `canon-update` and a `continuity-check` across the whole ripple range.
