# AGENTS.md — instructions for every AI agent in this repository

This file is the single source of truth for Claude Code, Codex, and any other agent.
CLAUDE.md only imports it. Edit instructions here, never in harness-specific files.

## Mission
Help the human author produce fiction of the highest quality through iterative cycles.
The author owns the work. You draft, critique, and revise on request; the author decides.
Prefer fewer, better words. Never trade specificity, subtext, or the author's voice for polish.

## Before every pass
1. Run `scripts/agent-preflight`. If it reports a dirty tree, STOP and ask the author to run `scripts/author-commit`. Never commit the author's uncommitted edits.
2. Read `bible/style.md`, `plan/premise.md`, and `decisions.md`.
3. Load only what the task needs: the relevant `bible/characters/*.md` and the chapter(s) involved, then:
   - `bible/canon.md` entries for those characters and places;
   - `plan/summaries/chNN.md` for neighbouring chapters (not the whole outline); `plan/synopsis.md` when you need the book's shape;
   - `plan/scenes/chNN.md` and `bible/threads.md` when drafting, critiquing, or revising structure.
4. State in one line which pass you are running (see Pass names) and which files you loaded.

**Reader exceptions:** `cold-read` and `reader-report` use `scripts/agent-preflight --reader` and skip steps 2–3 and cycle notes. Cold-read reads only the sanitized manuscript until its first report is committed. Reader-report additionally reads the audience/persona inputs named in its skill. For both, defer the feedback protocol's decision/index reading until the initial reaction report is committed; then index findings without rewriting the recorded reaction. Disclose prior exposure to intent or earlier drafts.

## Working cycle
- At book setup, choosing strong author-written voice exemplars is the author's first task. Never manufacture substitute exemplars or silently populate the author's taste.
- Default to exploration while discovering a sequence; maintain essential continuity and defer optional critique/polish. In revision, pursue one explicit reader effect and preserve identified strengths.
- Let the author read first before commissioning evaluation. Record their actual reaction or mark it pending; do not invent it. Honor an explicit request for immediate evaluation.
- For substantial or multi-session work, read/update `plan/cycle.md` from the authorized request. Small explicit TODOs need no additional form. `scripts/workflow status` gives the next step; `check` validates completeness only.
- Select the evaluation that answers the current uncertainty. Routine critique gives at most three priority findings unless the author requests a comprehensive review. No automatic panel or full critique after every chapter.
- After revision, verify the intended effect in context, inspect continuity consequences, and refresh affected memory. A fresh reader must record their reaction before seeing the expected answer.
- Stop when the objective is met, the effort limit is reached, or an author decision is needed. Record inconclusive evidence honestly; do not initiate another rewrite without scope to do so.
- At sequence and full-draft milestones, recommend independent human reading. Prepare copies when asked; never fabricate responses or contact readers without authorization. Address structure before sentence polish unless the author explicitly chooses otherwise.

## Hard rules
- **One sentence per line** in every manuscript file. Paragraphs are separated by a blank line. Dialogue lines follow the same rule.
- **Author text is sacred.** Outside a TODO's scope, change nothing except minimal continuity fixes and typos, and list each one under `Out-of-scope:` in the commit body (the commit hook rejects unexplained out-of-scope edits).
- **Locked spans:** text between `<!-- LOCKED -->` and `<!-- /LOCKED -->` is never edited. The commit-msg hook rejects agent commits that change one. Propose changes in `feedback/` instead.
- **decisions.md overrides everything** except these hard rules. If a request conflicts with a recorded decision, ask.
- **Critique passes never edit the manuscript.** They write a report to `feedback/`.
- **Don't invent canon silently.** Any new fact (name, date, relationship, rule of the world) goes into the commit body under `New-canon:` so `canon-update` can record it.
- Obey `bible/style.md`, including its banned-phrase list. Run `scripts/stats --slop` and the `slop-detector` checklist on any prose you write before committing.
- If uncertain about intent, leave `<!-- AGENT-Q tN: question -->` beside the relevant text rather than guessing on anything that matters.

## Feedback protocol (every pass that writes to feedback/)
- Before writing: read the **Deliberate choices** in `decisions.md` and the `rejected` rows of `feedback/INDEX.md`. Don't re-raise them unless you have a new argument, and say so when you do.
- Number every finding. After writing, add one row per finding to `feedback/INDEX.md` with status `open` and the manuscript revision you read in Notes. Don't add a row for an issue already indexed; cite the existing id.
- For each finding, separate what a reader experiences (with the quoted text) from your guess at the cause and your suggested remedy, and give your confidence. The author may accept the observation and reject the remedy.
- Only the author changes a status; the `feedback-triage` skill records their answers.

## TODO markers (author directives inside the manuscript)
```
<!-- TODO t3 [next]: directive -->     revise the paragraph after the marker
<!-- TODO t3 [prev]: directive -->     revise the paragraph before the marker
<!-- TODO t3 [insert]: directive -->   write new text at the marker
<!-- TODO t3 [start]: directive -->    revise the range up to ...
<!-- TODO t3 [end] -->                 ... this closing marker
<!-- TODO: directive -->               no id/scope: run `python3 scripts/todo.py ids`; scope "auto" means infer it and state your interpretation
```
- Plan mode: use the `todo-plan` skill. Writes `plan/todo-plan.md`; does not touch the manuscript.
- Direct mode: use the `todo-implement` skill. When `plan/todo-plan.md` has author annotations, follow them exactly.
- Remove a marker only when its directive is fully done. Quote the directive in the commit (`--directive`) so it survives in history.
- `[auto]` scope means at most the paragraph on each side of the marker; name which in the plan or commit.
- After implementing, run `python3 scripts/todo.py check-scope <author-commit>` and fix or justify every warning.
- TODO ids are never reused (`todo.py ids` numbers past every id in git history). An AGENT-Q means "awaiting the author", never "done".

## Committing
Always commit through `scripts/agent-commit`:
```
scripts/agent-commit --pass <pass> --model <your exact model name> --harness <claude-code|codex> \
  --files "paths you changed" [--todo t3] [--directive "original TODO text"] [--session <id>] \
  -m "summary" [-b "details, Out-of-scope: …, New-canon: …"]
```
`--files`, `--model`, and `--harness` are required. Only the named paths (directories are fine) plus `prompts/` are staged. The wrapper refuses to commit if anything else is already staged, or if the author committed after your preflight; stop and tell the author rather than working around it. It cannot tell your edits from the author's inside the same file, so the author shouldn't edit files an agent is working on; for genuinely parallel work, use a separate `git worktree`.
The commit hook checks the staged commit: known pass name, LOCKED spans, well-formed TODO markers, and file boundaries by pass (report passes write only `feedback/` and `prompts/`; `todo-ids`, `todo-plan`, `structural-revision`, `canon-update`, `bible`, and `tooling` may change only comment markers in `manuscript/`). For `todo-implement` it checks that each named TODO is resolved in the staged text and that every change lies inside its scope unless explained under `Out-of-scope:`.
Commit per logical unit (one TODO, one scene, one report). Never use `Pass: author-edit`, and never run a bare `git commit`: the hook rejects it from an agent shell.
Work on the current branch; the author creates branches and merges. Exception: `alt/*` branches for alternative drafts when the author asks for options.

## Pass names
`draft` · `revise` · `line-edit` · `critique` · `cold-read` · `reader-report` · `blind-judge` · `structural-revision` · `continuity` · `voice-check` · `slop-check` · `todo-ids` · `todo-plan` · `todo-implement` · `canon-update` · `learn-from-edits` · `bible` (editing bible/plan files at the author's request, including feedback triage) · `tooling` (changing the workbench itself: scripts, hooks, skills, templates, README)

## Where things live
- `bible/` — characters (one file each), world, style, themes, timeline, `canon.md` (facts established in the prose), `threads.md` (setups and payoffs).
- `plan/` — `premise.md`, `readers.md` (reader panel), `outline.md` (planned beats), `synopsis.md` (book and part summaries), `summaries/chNN.md` (what each written chapter contains, plus its end state), `scenes/chNN.md` (scene cards: intent per scene), `revision-plan.md`, `todo-plan.md`.
- `manuscript/` — `chNN-title-slug.md`, one chapter per file (e.g. `ch05-the-crossing.md`). `chNN` is the chapter's id: cite chapters as `chNN` in bible/plan/feedback, never by file name. If you change a chapter title, run `scripts/chapter-names` to rename the file; create chapters with `scripts/new-chapter NN "Title"`.
- `feedback/` — dated reports `YYYY-MM-DD-<pass>-<model>-<scope>.md`, `INDEX.md` (every finding and its status), `scores.tsv` (AI and human scores with rubric version, input revision, and confidence), `human/` (real readers' responses, recorded verbatim; never simulate one).
- Story memory freshness: `scripts/memory-status` lists chapter summaries older than their chapter and the canon entries citing those chapters. Refresh affected memory before drafting depends on it.
- `decisions.md` — author rulings and deliberate choices (binding) · `open-questions.md` — unresolved issues · `models.md` — observed model strengths
- `prompts/` — prompt logs (Claude Code logs automatically; Codex via `scripts/import-codex-sessions.sh`)
- `.skills/` — skill definitions shared by all harnesses
- `reference/craft-lenses.md` — diagnostic questions from established craft teaching (scene turns, promise/progress/payoff, arcs, psychic distance…). Skills name the sections they use. Lenses, not laws: style.md, decisions.md, and premise.md override them.
- `build/` — compiled output and blind comparisons (git-ignored). Never open `build/blind/*/.key.json`.
