---
name: todo-plan
description: Plan how to resolve the author's TODO markers in the manuscript without editing prose. Use whenever the author asks to plan, review, or think through TODOs, or says "plan mode", "plan the todos", or wants to see an approach before changes are made.
---
# todo-plan

Produce `plan/todo-plan.md`, a reviewable plan for every open TODO. Do not edit manuscript prose.

## Steps
1. `scripts/agent-preflight`. Stop if the tree is dirty.
2. If any TODO lacks an id: `python3 scripts/todo.py ids`, then `scripts/agent-commit --pass todo-ids -m "Assign TODO ids"`.
3. `python3 scripts/todo.py list` to get every marker.
4. For each TODO, read the scoped text plus enough surrounding context (usually the whole scene), the characters involved, and relevant canon.
5. Write `plan/todo-plan.md` using the format below, in manuscript order.
6. Add a final section **Cross-cutting effects**: TODOs that interact, canon/timeline/outline changes needed, other chapters affected.
7. Commit: `scripts/agent-commit --pass todo-plan -m "Plan for TODOs t1–tN"`.
8. Tell the author to annotate each item and commit with `scripts/author-commit`.

## Format per item
```
## t3 — manuscript/ch04-the-crossing.md:57 [next]
Directive: <verbatim>
Interpretation: <what you think the author wants, one or two sentences>
Effect / verification: <desired reader effect, what to preserve, and how to check it; link the active cycle if applicable>
Approach: <concrete plan: what changes, what stays, target length, beats>
Risks / ripple: <continuity, voice, pacing effects>
Questions: <only if needed>
Author:
```
For scope `auto`, the Interpretation must say which text you will change or where you will insert.
Offer alternatives (A/B) only when the directive is genuinely open. Mark the one you recommend.
