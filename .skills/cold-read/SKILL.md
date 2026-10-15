---
name: cold-read
description: Read chapters the way a first-time reader would, with no access to the bible, plan, or author intent, and record the moment-by-moment reading experience; then, as a separate second step, compare it with intent. Use when the author asks for a cold read, a fresh-eyes read, a beta read, "what does a reader actually get", or where readers would get lost or stop.
---
# cold-read
A real reader has only the page. Most editing passes load the bible first and therefore read the book with knowledge of intent. This pass exists to measure the gap.

## Isolation (this pass overrides AGENTS.md "Before every pass", steps 2–3)
- Run `scripts/agent-preflight --reader`, then use `scripts/reader-copy` for the requested chapters and read **only** its sanitized chapter files and manifest. Cite original chapter filenames and line numbers, which the bundle preserves. Don't open `bible/`, `plan/`, `decisions.md`, `open-questions.md`, `feedback/`, or `prompts/`, and don't read git log messages or commit bodies.
- Read in order from ch01 up to and including the scope. If the context budget won't allow it, start at the scope and say in the report that you began mid-book.
- Never open raw manuscript files to inspect comments. Do not load `plan/cycle.md` or the expected revision effect before committing the reaction. Record predictions before reading later chapters; disclose scope gaps and prior exposure.
- Best run by a model that neither drafted nor critiqued these chapters, in a fresh session.

## Step 1 — the reading (write it before anything else)
Write `feedback/YYYY-MM-DD-coldread-<model>-<scope>.md`, part 1, as you read:
1. **Reaction log** — every few pages, Saunders's question, "what has this page done to me?": `file:line` · what I feel · what I now know, expect, or worry about · am I pulled forward, coasting, or tempted to skim. (`reference/craft-lenses.md` §4 holds the method; it is general craft, not about this book, so reading it doesn't break isolation.)
2. **Confusions and dream breaks** — where I lost track of who, where, when, or why, and where something knocked me out of the story (a jarring sentence, a jump in distance, an explanation I didn't need) (file:line).
3. **Predictions** — what I think will happen, and how sure I am. A book is working when some are right and the wrong ones surprise.
4. **Put-down points** — the lines where a reader with other things to do would close the book, and why.
5. **What I think this book is about**, who I think the protagonist is and what they want, in my own words.
6. **Best and worst moments** — three each, quoted.

Commit part 1 (`--pass cold-read`) **before** reading anything else, so it is fixed before comparing against intent. Then read decisions and the feedback index to register numbered findings under the feedback protocol, without rewriting the initial reaction.

## Step 2 — intent gap (optional, after the commit)
Now read the active `plan/cycle.md` if any, `plan/premise.md`, `plan/scenes/` for the scope, and `plan/summaries/`. Append part 2: **Intent gap**, a table of intended effect · what the cold reader got · file:line · suggested TODO. Focus on misreadings that matter: subtext that didn't land, reveals that were guessed too early or not understood at all, characters read differently than intended (want, need, and arc as the premise means them), and promises the opening made to the cold reader that the plan doesn't intend to keep (`reference/craft-lenses.md` §2–3).
Add each gap to `feedback/INDEX.md` as `open`. Commit again with `--pass cold-read`.
