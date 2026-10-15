---
name: todo-implement
description: Carry out the author's TODO markers in the manuscript, either directly or following an annotated plan/todo-plan.md. Use whenever the author asks to implement, do, apply, resolve, or execute the TODOs, or approves a TODO plan.
---
# todo-implement

## Mode
- **From plan:** if `plan/todo-plan.md` has `Author:` annotations, follow them. `approve` = do the Approach; `modify: …` = do the modified version; `skip` = leave the marker untouched and add nothing.
- **Direct:** no annotated plan. Interpret each directive yourself; for anything ambiguous and consequential, leave `<!-- AGENT-Q tN: … -->` next to the marker instead of guessing.

## Steps
1. `scripts/agent-preflight`. Stop if dirty. Record the base: `BASE=$(git rev-parse HEAD)`.
2. Assign ids if missing (`python3 scripts/todo.py ids`, commit as `todo-ids`).
3. For each TODO in manuscript order:
   a. Load context: the scene, characters involved (`bible/characters/`), `bible/style.md`, relevant canon and decisions for the book (AGENTS.md, Before every pass, steps 2–3).
   b. Edit only within scope: `next`/`prev` = the adjacent paragraph; `insert` = new text at the marker; `start…end` = the range; `auto` = at most the paragraph on each side of the marker, and say which in the commit.
   c. Write one sentence per line. Match the surrounding voice. Run the slop-detector checklist on new text.
   d. Remove the marker (both markers for a range).
   e. Commit: `scripts/agent-commit --pass todo-implement --todo tN --directive "<verbatim directive>" --model <model> --harness <harness> --files manuscript/chNN-….md -m "tN: <what changed>" -b "<New-canon: …>"`.
   The commit hook checks the staged text: tN must have existed at HEAD and be gone (or carry an AGENT-Q, which counts as awaiting the author, not done), and every changed line must lie inside tN's scope. A necessary continuity fix or typo outside the scope is allowed only when the body lists it under `Out-of-scope:` with the reason; otherwise revert it.
4. Run `python3 scripts/todo.py check-scope $BASE` for the whole pass. Every warning should match an `Out-of-scope:` explanation; revert anything that doesn't.
5. Run the continuity-check skill on touched chapters if any TODO changed facts.
6. Report to the author: each TODO id, one line on what you did, any AGENT-Qs left, and `scripts/review` to see the word diff.

## Finishing
After implementation, reread the changed passage in its surrounding sequence and check the directive's intended effect and preserved strengths. Record the checked revision and evidence in `plan/cycle.md` when active, or in the completion report for a small TODO. Distinguish the editor's check from an independent reader response; mark fresh reading pending when needed. Refresh affected summaries and canon before later drafting depends on them. State why no memory update is needed if facts/end states did not change. Stop at the authorized objective or effort limit; do not automatically initiate another polish pass.

Run `python3 scripts/todo.py check-resolved` at the end. Every TODO should be gone, or carry an AGENT-Q, or have been marked `skip` by the author in the plan.

## Clearing the plan
When you worked from `plan/todo-plan.md`, clear it out as the last commit of the pass, so no later agent follows annotations that have already been carried out:
- If every item is done or was marked `skip` by the author, reset the file to the empty template (the header comment only).
- If items remain (marked `modify` or carrying an AGENT-Q that is still waiting, or not reached), delete only the finished items and keep the rest with their annotations.
- Commit with `--pass todo-plan -m "Clear implemented plan"` and put the commit hash of the implemented plan in the body. The full plan stays in git history.
