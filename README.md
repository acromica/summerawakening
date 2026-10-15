# Hydra: a fiction workbench

A git repository for writing fiction with AI agents (Claude Code, Codex, or both) in iterative cycles with a human author.
The author owns the work and makes every decision.
Agents draft, critique, and revise on request, and every change is a commit that records which pass, model, and prompt produced it.

The aim is fiction that holds up for critics and general readers alike, so the workbench does more than generate text. It tests drafts the way readers meet them: cold reads with no access to the plan, a scored reader panel, and blind comparison of alternative drafts. It also learns your taste from your edits.

**Contents:** [Quick start](#quick-start) · [Recommended workflow](#recommended-workflow) · [One sentence per line](#write-one-sentence-per-line) · [TODO markers](#todo-markers) · [Workflow reference](#workflow-reference) · [What the critics look for](#what-the-critics-look-for) · [Repository map](#repository-map) · [Scripts](#scripts) · [Skills](#skills) · [Several models](#working-with-both-harnesses-and-several-models) · [Prompt retention](#prompt-retention) · [Tips](#tips-for-getting-high-quality-work) · [Troubleshooting](#troubleshooting)

---

## Quick start

Use one repository per book. Create a new **private, empty GitHub repository** for the book (no README, license, or .gitignore), then run these commands in a terminal. Replace `YOUR-USERNAME` and `my-novel` with your GitHub account and repository name:

```bash
git clone https://github.com/acromica/hydra.git my-novel
cd my-novel
scripts/setup.sh --new-book --remote https://github.com/YOUR-USERNAME/my-novel.git
git push -u origin main
```

Use `--new-book` only when starting a new book: it deletes the clone's Git history and remote configuration while keeping the workbench files. It requires a clean, standalone clone. Setup initializes a new `main` branch, installs hooks, aliases, and skill links, creates the book's first commit, and adds your repository as `origin`. It does not create the GitHub repository or push automatically.

Check `git rev-list --count HEAD`: it should print `1`. `git log` should show only `Scaffold fiction workbench`, with no Hydra commits.

If Git asks for your identity, set `git config user.name "Your Name"` and `git config user.email "you@example.com"`, then rerun setup **without `--new-book`**. You can also omit `--remote` and connect later with `git remote add origin URL`. Normal setup refuses to replace an existing, different `origin`.

After the first push, push regularly (`git push`): the repository is your backup, and its history is the book's memory.

Requirements: git, bash, and python3. `pandoc` is optional and used for compiling to docx, epub, or pdf.

Your first author task is to choose **2–3 strong passages of your own prose** and place them in `bible/style.md`: ideally dialogue, physical action, and interiority. Agents must not invent or choose substitute exemplars for you. Leave the fields blank until you can supply them; exploratory planning can still proceed. Add brief voice notes and prune the starter banned-phrase list to taste.

Then establish a compact creative brief:

1. `plan/premise.md`:

   1. **title** - This is not the title that the book will be published under, it is functional: the AI reads it as a signal of the book's genre, tone, and central theme, and it will shape both feedback and generated text around it. Mark whether the title is a working title or final, and briefly explain what it means, especially if it's a metaphor, double meaning, or reference that pays off late in the story, so the AI doesn't take it too literally or flag it as unfulfilled. Avoid titles that match or closely echo well-known books or films, since the AI may blend in elements of those works; if you keep one, note that your story is unrelated. Make sure the title fits the audience description, and if you're undecided, leave it blank or use a neutral placeholder like "Untitled Thriller" rather than a misleading title. Once a draft exists, revisit the title with the AI, since the finished book may be about something slightly different than you first planned.

   2. **logline** - A one- or two-sentence summary of a story that captures its core premise and hook. A good logline usually covers the protagonist (often described by a defining trait rather than a name), the inciting incident or situation that sets the story in motion, the goal the protagonist pursues, and the central conflict or stakes that stand in the way. Aim is to convey what makes the story distinctive and compelling, not to summarize the whole plot or reveal the ending.

   3. **audience** - An audience description tells an AI collaborator whose judgment to simulate, so its feedback reflects your actual readers instead of a generic one. It should cover the age category, the specific genre and its conventions (including any you're deliberately breaking), two or three comparable titles, the emotional payoff readers come for, the expectations they'd punish you for violating, content and prose-style boundaries, and who the book is *not* for. For example: "Adult readers of *Gone Girl* and *The Secret History* who want psychological complexity and building dread over action, expect a twist that recontextualizes earlier scenes, and aren't looking for a fast airport thriller." Tie feedback requests to it directly, such as "Where would this reader skim or put the book down?" You can also ask the AI to separate notes about your audience from its own general craft opinions.

   4. **Length target:** number of words

   5. **what the book must never become** - This section protects your book's identity. AI collaborators tend to pull stories toward safe, familiar versions of themselves, so describe the bad version of your book that a well-meaning editor might steer you toward. Consider covering genre or tone drift (a grief novel sliding into a procedural), betrayals of core character traits, thematic misreadings (a book about addiction becoming a cautionary tale), specific tropes you're avoiding, and content lines that must never appear on the page. Also name common AI tendencies, since they're the likeliest drift: moralizing, tidy resolutions, softened villains, over-explained subtext, therapy-speak in dialogue, characters who all sound alike, and ornate prose where the style should be spare.

      Keep the list to about five to ten items so each carries weight. Be concrete: "the relationship between Mara and Eli must never become romantic; its power is that it stays unresolved" works better than "never a romance." Give a brief reason for each item so the AI can apply the principle to situations you didn't anticipate, and mark which items are hard limits and which are strong preferences the AI may question. Agents flag any suggestion that moves toward one of these items and name which one, so you can decide whether the drift is a mistake or a deliberate change.

      > **Example**

      > What this book must never become:
      > - A redemption story. Daniel doesn't earn forgiveness, and the book shouldn't imply he deserves it.
      > - A courtroom drama. The trial happens off-page; the story is about the family, not the verdict.
      > - Sentimental. Grief is shown through behavior and silence, never through characters explaining their feelings.
      > - Neatly resolved. The ending leaves the sisters' relationship damaged but open.
      > - Preachy about addiction. No character delivers the moral, and no one is simply a victim or a villain.
      > - Hard limit: no on-page violence against children.

2. Check that the premise and your chosen voice exemplars describe the same book. Leave unresolved creative questions open rather than filling every template field.

3. `plan/readers.md`: the reader panel (a critic, your core reader, a skeptical general reader) that scores chapters. Ask an agent to draft it from your premise ("Draft plan/readers.md from the premise"), then correct it.

4. `bible/characters/`: copy `_template.md` once per character. Its "Role in the story" section asks for want, need, the lie the character believes, and the wound behind it.

5. `bible/world.md` and `plan/outline.md`. Scene cards (`plan/scenes/`) are optional up front; the drafting skill writes them if you don't.

Commit with `scripts/author-commit "Set up story bible"`, then open Claude Code (`claude`) or Codex (`codex`) in the repo and start working.

**Cloning an existing book onto a new machine?** Do not use `--new-book`; keep `.git` so you retain the book's history and remote. Run `scripts/setup.sh` once to restore local hook settings and skill links; it preserves existing commits. `scripts/agent-preflight` checks hook readiness and asks you to run setup if needed.

**A series?** Start book two from a fresh copy of the workbench and write `bible/prior-books.md`: the facts, threads, and end states from earlier books that the new one depends on. Agents load that instead of the old manuscript.

---

## Recommended workflow

### The one rule

**Commit your edits before any agent runs:** `scripts/author-commit "what I changed"`.
Agents run `scripts/agent-preflight` first, and it refuses to start on a dirty working tree.
This keeps your words and the agent's words in separate commits, so history always shows who wrote what, and the learning loop can tell your edits from theirs.

### Assign models by role

Draft with one model, and critique, cold-read, and judge with another. A model reviewing its own text misses its own habits. A typical split:

| Role | Model | Why |
|---|---|---|
| Drafting, TODO implementation, line edits | Model A | Consistency of voice across the book |
| Developmental critique, reader panel | Model B | Different habits, so it sees A's tics |
| Cold read, blind judging | Model B or C, **fresh session** | Must not carry the plan or know who wrote what |

Revise the split from evidence in `models.md`: blind-judge results, your review minutes, and how many findings proved useful. Don't rank models by how much of their text survived your edits; that number depends on what you happened to review.

### The cycle: draft, diagnose, revise, verify

Use **exploration** while discovering the story and **revision** when improving an existing unit. A unit can be a scene, chapter, or connected sequence; choose enough narrative context to judge cause and effect without commissioning an unlimited pass.

1. **Set the brief.** Establish audience, intended experience, voice exemplars, and the few boundaries that protect this book. Choosing exemplars remains the author's first setup task.
2. **Draft a meaningful unit.** During exploration, fix blockers and maintain essential facts, knowledge changes, and end states. Keep moving through the sequence; defer optional critique and sentence polishing.
3. **Read it yourself first.** Before opening AI feedback, note what worked, where attention changed, and the most consequential uncertainty. The agent must not fabricate this author reaction.
4. **Choose one evaluation that answers that uncertainty.** Use the table below. A chapter does not automatically need every pass, or any pass beyond your own reading.
5. **Revise toward one explicit reader effect.** Identify what to preserve and what is out of scope. Use scoped TODOs for local work and a ripple plan for cross-chapter changes.
6. **Verify and stop.** Read the changed unit in context, test the intended effect, check continuity consequences, and refresh affected memory. Stop when the objective is satisfied, the agreed effort limit is reached, or the evidence exposes a decision for the author. An inconclusive check is not success and does not authorize another rewrite.
7. **Review at milestones.** At a complete sequence and a full draft, seek independent human target readers. Record their unprompted reactions before discussing intent. Address structure before polishing sentences.

For example: “Readers should suspect the brother while understanding why the protagonist trusts him” is a useful revision objective. A fresh reader's predictions and account of the relationship can test it. Do not tell the reader the expected answer before their reaction is recorded.

### Choose the smallest useful evaluation

| Uncertainty | Evaluation | Evidence to look for |
|---|---|---|
| What does the page communicate or make readers expect? | Fresh-session cold read | Unprompted understanding, predictions, confusion, attention changes |
| Does the sequence work structurally? | Focused developmental critique | Causal or emotional problem with quoted evidence; strengths to preserve |
| Are facts, timing, or character knowledge consistent? | Continuity check | Specific contradiction or knowledge leak |
| Which consequential approach works better? | Blind alternatives | Preference with reasons, confidence, or a valid tie |
| Are voices distinct, or do sentences obstruct the intended effect? | Voice check or line edit | Specific passages; use after structure is stable unless explicitly requested earlier |
| How might audience priorities differ? | Optional simulated reader panel | Diagnostic disagreements; scores are not independent reader votes or proof of quality |

### Keep a cycle on track

For substantial or multi-session work, use `plan/cycle.md` as a short working note. Fill it from the author's request and actual observations; do not require a separate approval ceremony when the request already authorizes the work. Small, explicit TODOs can carry their objective and verification in the directive and completion report instead.

Record the scope, baseline revision, intended effect, strengths to preserve, evaluation, effort limit, and stopping condition. Add evidence after revision, including unresolved consequences and which memory files were refreshed. Link existing reports and plans instead of duplicating them. Keep feedback dispositions in `feedback/INDEX.md` under the author's control.

```bash
scripts/workflow status          # current cycle and next useful action
scripts/workflow check           # missing fields or unclosed verification; no prose grading
```

`Status: idle` means no cycle is active. Use `active`, `awaiting-author`, `verified`, or `deferred` as work proceeds. Only mark `verified` when evidence addresses the objective and continuity/memory consequences are accounted for. If fresh reading or an author decision is still needed, record that limit. The script checks record completeness, not literary success. Previous cycles remain in Git history; replace the note when starting a new one.

### Cadence and stopping rules

| When | Do |
|---|---|
| Every agent-written passage | Inspect slop flags and preserve intentional effects; do not optimize toward zero heuristic hits |
| During exploration | Maintain facts and end states needed by the next unit (`scripts/memory-status` shows what's out of date); fix blockers and defer optional polish |
| After the author reads a unit | Select a focused evaluation only when it answers a consequential uncertainty |
| After revision | Check the chosen effect and collateral continuity; refresh only affected canon, summaries, threads, and synopsis |
| At a complete sequence | Gather independent human reactions when available; use a fresh AI cold read as explicitly provisional evidence if humans are unavailable |
| At a full draft | Review whole-book structure and payoffs with human readers; commission additional AI passes for identified questions |
| When structure is stable | Address scene execution, character voice, continuity, then line editing; an explicit author request may choose a different order |
| When the objective is met or the effort limit is reached | Record evidence and remaining decisions; do not automatically start another pass |

Use `scripts/reader-copy manuscript/ch01-*.md manuscript/ch02-*.md` to create a comment-free, line-preserving bundle for a fresh AI reader. It prints the output directory; it does not open the text in the preparing session. Use `scripts/compile.sh docx` for a human-readable whole-book copy. Neither command contacts readers.

For human feedback, ask where attention changed, what they understood or predicted, what moved them, and what they remembered later. Capture actual responses and the revision they read; do not substitute simulated answers. Triage notes through the existing feedback protocol. Track author review time and useful findings if helpful, without turning word count or model scores into quality targets.

### Revision order for a full draft

Revise from the outside in. Each level can invalidate the work below it:

1. **Structure:** does the book keep its promises, and does each chapter move it forward? (cold read, whole-book critique, structural revision)
2. **Scenes:** what does each scene contribute to the intended experience—pressure, discovery, relationship, atmosphere, or pleasure? Revise or remove scenes whose contribution does not justify their place. (critique, TODOs)
3. **Characters and voice:** wants, arcs, distinct dialogue. (critique, voice check)
4. **Continuity:** facts, timeline, who knows what. (continuity check)
5. **Lines:** rhythm, precision, tics. (line edit, slop check, stats)

---

## Write one sentence per line

**Put each sentence on its own line in every manuscript file.**
Separate paragraphs with a blank line, as usual.

```markdown
Mara stood at the ferry rail.
The water was the colour of old pewter.
She did not wave.

"I'm not coming back," she said.
```

This is the single most important convention in the repo, for five reasons:

- **Markdown renders it identically.** A single line break inside a paragraph displays as a space, so readers and compiled output never see the difference.
- **Diffs become readable.** Git compares lines, so if a paragraph is one long line, changing one word marks the whole paragraph as changed. With one sentence per line, you see exactly which sentences an agent touched.
- **Review and merging get easier.** Two passes that touched different sentences in the same paragraph merge cleanly instead of conflicting, and `git blame` tells you who last shaped each sentence (you or which model).
- **The learning loop gets precise.** `scripts/learn-diff` traces each sentence you rewrote back to the commit that last wrote it (approximately: a later punctuation fix moves the credit).
- **TODO scopes stay precise.** A marker sits cleanly between sentences and paragraphs.

You don't need to type this way. Write however you like, then run:

```bash
scripts/semantic-lines.py manuscript/ch03-*.md   # reflow in place
```

The pre-commit hook reminds you if a manuscript file isn't reflowed. It never blocks a commit.
Agents are instructed to always write this way.

---

## TODO markers

TODO markers are HTML comments, so they're invisible in any Markdown preview and in compiled output.
Put a TODO wherever you want a change:

```markdown
<!-- TODO [next]: Make her refusal colder. She shouldn't explain herself. -->
<!-- TODO [prev]: Cut this paragraph by half. Keep the ferry image. -->
<!-- TODO [insert]: New short scene: Eli finds the letter and doesn't open it. ~400 words. -->

<!-- TODO [start]: Rewrite this stretch as one continuous flashback, present tense. -->
...existing text...
<!-- TODO [end] -->

<!-- TODO: Something feels off in this exchange, fix the rhythm. -->
```

| Scope | Meaning |
|---|---|
| `[next]` | Revise the paragraph right after the marker |
| `[prev]` | Revise the paragraph right before the marker |
| `[insert]` | Write new text at the marker |
| `[start]` … `[end]` | Revise everything between the two markers. Use this whenever "adjacent" could be ambiguous. |
| none | `auto`: the agent infers the scope and states its interpretation in the plan or commit |

Directives can span several lines inside the comment.
Be as specific as you like about intent, tone, length, or what must be kept.

**IDs.** You don't need to write them.
`python3 scripts/todo.py ids` numbers every marker (`t1`, `t2`, …) so plans, commits, and questions can refer to each one. Ids are never reused: numbering continues past every id in the book's history. Agents run it automatically.

**Agent questions.** When a directive is ambiguous, the agent leaves a question beside the marker instead of guessing:

```markdown
<!-- AGENT-Q t3: Should Eli be alone here? In ch04 Jo is with him. -->
```

To answer, edit the TODO (or delete the question and add a new TODO), commit, and run again.

**What happens to the directive?** When an agent resolves a TODO, it removes the marker and quotes the original directive in the commit message. To see every directive ever given, run `git log --grep=Directive`.

**Locked text.** Wrap anything finished in `<!-- LOCKED -->` … `<!-- /LOCKED -->`. The commit hook rejects any agent commit that changes it; agents propose changes to locked text in `feedback/` instead.

---

## Workflow reference

The [recommended workflow](#recommended-workflow) strings these together. Each one also works on its own.

### 1. Revise with TODOs: plan mode

Use plan mode when the changes are substantial, interact with each other, or when you want to approve the approach before any prose is written.

1. Read the chapter, edit freely, and add TODO markers.
2. `scripts/author-commit "ch04: edits + TODOs"`
3. Tell the agent: **"Plan the TODOs."** It runs the `todo-plan` skill.
4. Open `plan/todo-plan.md`. Under each item, write one of:
   - `Author: approve`
   - `Author: modify: keep the ferry, lose the gulls, 200 words max`
   - `Author: skip`
5. `scripts/author-commit "annotated plan"`
6. Tell the agent: **"Implement the plan."**
7. `scripts/review` shows a word-level diff of everything since your last commit.

Claude Code also has a built-in plan mode (Shift+Tab) that's useful for thinking a task through. The `plan/todo-plan.md` file is what makes the plan reviewable, versioned, and usable from Codex too.

### 2. Revise with TODOs: direct mode

Use direct mode for small, clear directives.

1. Edit, add TODOs, and run `scripts/author-commit "…"`.
2. Tell the agent: **"Implement the TODOs."**
3. The agent makes one commit per TODO, runs a scope check, and reports.
4. `scripts/review`. If you don't like a change, run `git revert <hash>` for that one TODO and adjust the directive.

### 3. Draft a new chapter

1. Add beats to `plan/outline.md` (and, if you like, scene cards in `plan/scenes/ch05.md`), then run `scripts/new-chapter 05 "The Crossing"`.
2. Commit, then tell the agent: **"Draft ch05 from the outline."** It runs the `scene-draft` skill: it writes the scene card first if you didn't, drafts, runs the slop checks, and reports word count, liberties taken, and open questions.
3. Read it yourself first. Continue the sequence during exploration, or select one evaluation for the uncertainty you identified (workflows 4–7).
4. For revision, name the intended effect and what to preserve; edit or add TODOs and commit. Continue with workflow 1 or 2, then verify the effect in context and stop when the objective is met.

### 4. Cross-model critique

Critique passes write reports to `feedback/` and never touch the manuscript.

1. In Codex (if Claude drafted), or the reverse: **"Critique ch05: does the refusal feel earned?"** A routine report focuses on up to three priority findings and what to preserve. Ask for a comprehensive review when you need one. It checks the page against the scene cards, `bible/threads.md`, your audience, and the "must never become" list, using the [craft lenses](#what-the-critics-look-for).
2. Read the report. It ends with ready-to-paste TODO markers. Paste the ones you agree with into the chapter.
3. Triage (workflow 8) so every finding gets an answer, then commit.

Other report-only passes: **"continuity check on ch01–ch05"**, **"voice check on the dialogue in ch05"**, and **"slop check on ch05"**.

### 5. Cold read: what a reader actually gets

Most editing passes read your bible first. A cold reader should encounter only the page; the simulated panel also limits its inputs to the page and audience description.

1. In a fresh session, ideally with a model that didn't draft the chapters: **"Cold read ch01–ch05."**
2. The `cold-read` skill uses reader-mode preflight and a sanitized reader bundle, then commits a reaction log: what it felt, predicted, misunderstood, where the story's spell broke, and where it would put the book down.
3. Only then does it read your intent (premise, scene cards) and add an **intent gap** table: what you meant, what the reader got, and a suggested TODO.

### 6. Reader panel and scores

**"Reader report on ch05."** The `reader-report` skill reads as each persona in `plan/readers.md` (a critic, your core reader, a skeptical general reader), scores each chapter on a fixed rubric with quoted evidence, names where each would stop reading, and says where the personas disagree.
Scores go to `feedback/scores.tsv` with the model, rubric version, input revision, scope, and confidence, as diagnostic observations. Compare only the same model, rubric version, and reading conditions. Scores alone do not establish improvement, and three personas from one model are one reader in three costumes, not three readers. Calibrate them: record real readers in `feedback/human/` (template provided) on the same revision, add their scores with `source = human`, and note where the AI readers agreed and where they missed.

### 7. Alternatives, judged blind

For scenes that matter most, get several versions and choose without knowing who wrote which.

```bash
# "Draft two alternatives for ch07: one where Mara stays, one where she leaves."  -> alt/ch07-stays, alt/ch07-leaves
scripts/blind-compare prepare manuscript/ch07-the-ferry.md alt/ch07-stays alt/ch07-leaves
# in another model: "Blind-judge 20261015-142233"
scripts/blind-compare reveal 20261015-142233
git merge alt/ch07-leaves          # or graft the best lines by hand; delete the other branch
```

The judge sees only `A.md` and `B.md`, ranks them against the scene card and your target reader, and quotes the losers' best lines worth grafting. Record each reveal in `models.md`: over time, routing rests on blind wins, not reputation.

### 8. Triage feedback

Reports pile up, and critics re-flag choices you made on purpose. **"Triage the feedback."** The `feedback-triage` skill walks you through open findings in `feedback/INDEX.md` a few at a time, first marking duplicates and notes whose passage has since changed. For each, it separates what the reader experienced from the critic's diagnosis and suggested fix, so you can accept one and reject the other. Accepted items become TODO markers for you to paste. Rejected items stay recorded so critics don't re-raise them; only the ones you call a lasting artistic choice go into **Deliberate choices** in `decisions.md`. You can also defer an item to a milestone. An implemented item is `done`; it becomes `verified` only once its effect was checked (a reread in context, a cold read, a reader).

### 9. Structural revision

TODOs fix paragraphs. For a change across chapters (cut a subplot, move a reveal, merge two characters): **"Plan a structural revision: move the letter reveal from ch12 to ch08."**
The `structural-revision` skill writes a ripple map into `plan/revision-plan.md` (every chapter affected, what changes, canon and thread effects, order of work). You annotate it like a TODO plan. Then it places scoped TODO markers in each chapter, and the normal TODO workflow carries them out, followed by canon-update and a continuity check across the range.

### 10. Keep the bible current

After merging a chapter: **"Update canon."**
The `canon-update` skill records new facts, timeline entries, arc checkpoints, setups and payoffs in `bible/threads.md`, and rewrites the chapter's `plan/summaries/chNN.md`, including its **end state** (who knows what, where everything is). Neighbouring passes load these short summaries instead of whole chapters. Each summary records the chapter revision it was written from, so `scripts/memory-status` (also shown by preflight) lists summaries that are older than their chapter, and the canon entries citing those chapters. Canon distinguishes established facts from characters' beliefs, author-only truths, open possibilities, and superseded facts after a rewrite. If a new fact contradicts existing canon without a rewrite explaining it, it goes to `open-questions.md` rather than overwriting anything.

### 11. Teach the agents your taste

Every few cycles: **"Learn from my edits."**
`scripts/learn-diff` traces every prose sentence you changed back to the agent pass and model that last wrote it. The skill turns patterns that recur across scenes into hypotheses ("you cut characters explaining their feelings: a rule, or just these scenes?") with before/after evidence. Confirmed ones become proposed additions to `bible/style.md` and character voice notes. Its counts describe what you edited in that window; they are not a model ranking.
Nothing is applied automatically. You copy in what you agree with.
Over time, your own edits become the strongest guidance in the repo.

### 12. Share a readable copy

`scripts/compile.sh docx` (or `epub`, `pdf`, `md`) writes to `build/`. All TODO and AGENT-Q comments are stripped.

---

## What the critics look for

`reference/craft-lenses.md` distils established craft teaching into diagnostic questions the critique, cold-read, reader-report, blind-judge, structural-revision, line-edit, and slop skills use:

| Lens | From | Asks |
|---|---|---|
| 0. Contribution (always first) | — | What does this passage give the reader (pressure, discovery, relationship, atmosphere, comedy, pleasure)? Is it vivid and worth its length? A scene that delivers its contribution works on its own terms, with or without a conventional turn |
| Scene function | Shawn Coyne (*Story Grid*), Dwight Swain, try/fail cycles | Does each scene shift a value? Is there a real choice (best bad choice, or irreconcilable goods)? Does it end *yes, but* or *no, and*? |
| Promise, progress, payoff | Brandon Sanderson; Mary Robinette Kowal (MICE) | Does the opening's promise get kept? Does every chapter show progress? Are payoffs earned, surprising, and inevitable? Do threads close in the right order? |
| Character arc | K. M. Weiland; Kurt Vonnegut | Want vs. need, the lie, the wound; does change come through costly choices? |
| Escalation | George Saunders | Does each beat raise the stakes? "What has this page done to us?" |
| The fictive dream | John Gardner | Psychic-distance jumps, needless explanation, sentimentality, frigidity, mannerism |
| Line-level order and tics | Swain; Elmore Leonard | Stimulus before reaction; said-bookisms, "suddenly", exclamation marks (counted by `scripts/stats`) |

They are lenses, not laws. Choose which suit your book in the **Craft lenses** field of `plan/premise.md`: a contemplative, comic, or episodic novel may not want scene turns or arc models, and "not applicable" is never a defect. Your `style.md`, `decisions.md`, and premise override them, agent-written scene cards are hypotheses rather than standards, and a report must quote the text rather than lecture about a framework. Edit the file to add the teachers you trust.

---

## Repository map

| Path | What it holds | Who edits it |
|---|---|---|
| `AGENTS.md` | Instructions for all agents: the single source of truth | Author |
| `CLAUDE.md` | One line, `@AGENTS.md`, so Claude Code reads the same rules | Nobody |
| `plan/premise.md` | Logline, audience, comps, non-goals, and which craft lenses suit the book | Author |
| `plan/readers.md` | Reader-panel personas and the scoring rubric | Author; agents draft |
| `plan/outline.md` | Parts → chapters → planned beats | Author |
| `plan/scenes/chNN.md` | Scene cards: goal, value shift, crisis, outcome, final image, what the reader should feel | Author or the scene-draft skill |
| `plan/summaries/chNN.md` | What each written chapter contains, plus its end state (who knows what, where things are) | The canon-update skill |
| `plan/synopsis.md` | Book and part summaries: the whole shape in one page | The canon-update skill |
| `plan/cycle.md` | Current unit, reader-effect objective, evaluation, stopping condition, and verification evidence | Author and agents, from authorized work |
| `plan/revision-plan.md` | Goals for the current revision pass; ripple maps for structural changes | Author; structural-revision skill |
| `plan/todo-plan.md` | The agent's plan for open TODOs, which the author annotates | Agent, then author |
| `bible/characters/*.md` | One file per character: role (want, need, lie, wound), background, personality, desires, physical, voice, arc | Author; agents propose |
| `bible/style.md` | Voice, POV, exemplar passages, do and don't lists, banned phrases | Author |
| `bible/world.md`, `themes.md` | Setting and rules; what the book is about underneath | Author |
| `bible/timeline.md`, `canon.md` | Chronology, and facts established in the prose (with beliefs, author-only truths, and superseded facts marked) | The canon-update skill |
| `bible/threads.md` | Setups and payoffs, typed (milieu, inquiry, character, event): every promise the book makes and whether it's kept | The canon-update skill |
| `manuscript/chNN-title.md` | The book, one chapter per file; `chNN` is the id, the rest follows the chapter heading | Both |
| `feedback/` | Critique, cold-read, reader-panel, continuity, and other reports, dated and named by model | Agents |
| `feedback/INDEX.md` | Every finding from every report, with your disposition (open, deferred, accepted, rejected, duplicate, superseded, done, verified) | Agents add; author decides |
| `feedback/scores.tsv` | AI and human scores per chapter, with rubric version, input revision, and confidence | The reader-report skill; you, for human readers |
| `feedback/human/` | Real readers' responses, recorded verbatim from the template | You |
| `decisions.md` | Your rulings, plus **Deliberate choices** critics must not re-flag; binding on every agent | Author |
| `open-questions.md` | Unresolved story problems | Both |
| `models.md` | What each model has actually been good at in this book | Author |
| `reference/craft-lenses.md` | What critics look for (see above) | Author |
| `prompts/` | Logs of every prompt, plus a library of prompts worth reusing | Automatic |
| `.skills/` | Skill definitions, linked into `.claude/skills`, `.agents/skills`, and `.codex/skills` | Author |
| `scripts/` | Helper commands | — |
| `build/` | Compiled copies and blind comparisons (git-ignored) | Scripts |

Why split characters into separate files? Agents load only the characters in the current scene, which keeps their context focused and stops one character's traits from bleeding into another's. The same logic applies to per-chapter summaries: agents load the neighbouring chapters' summaries, never the whole book.

---

## Scripts

| Command | What it does |
|---|---|
| `scripts/setup.sh [--new-book] [--quiet] [--remote URL]` | Initializes Git if absent, installs hooks, `git wdiff` / `git passes` aliases and skill links, and creates the first commit. Optionally adds `origin`. Preserves history unless `--new-book` explicitly resets it. `--quiet` suppresses the summary. |
| `scripts/author-commit "msg"` | Commits all your changes as `Pass: author-edit` and lists open TODOs. **Run this before every agent pass.** |
| `scripts/agent-preflight [--reader]` | Used by agents: stops if hooks aren't ready or the tree is dirty, records the starting revision (so `agent-commit` can tell if you committed meanwhile), then shows the last pass, open TODOs, marker problems, untriaged feedback, stale memory, and the cycle status. Reader mode hides TODOs, cycle notes, and commit subjects |
| `scripts/workflow status` / `check` | Shows the current cycle or checks its completeness; never grades prose or changes state |
| `scripts/reader-copy FILE…` | Creates a comment-free, line-preserving reader bundle with source revision and hashes |
| `scripts/agent-commit …` | Used by agents: commits only the named `--files` (required), refuses if other work is already staged or you committed during the pass, and records `Pass`, `Model`, `Harness`, `Todo`, `Directive`, `Prompt-Log`, and `Prompt-Session` trailers |
| `scripts/review [path]` | Word-level diff of everything agents did since your last commit |
| `scripts/passes` | Timeline of commits showing pass type and model (`git passes` works too) |
| `scripts/learn-diff [--last N \| --since REV] [--stats]` | Agent-written prose you changed, each line traced to the pass and model that last wrote it; summary counts are not a model ranking |
| `scripts/memory-status [--brief \| --check]` | Chapter summaries older than their chapter (by `Source revision:`), and canon entries citing those chapters |
| `scripts/reader-copy FILES…` | Comment-free, line-preserving chapter bundle with a manifest, for cold reads and reader panels |
| `scripts/workflow [status \| check]` | Current cycle note and its next step; `check` validates completeness only |
| `scripts/stats [FILES…]` | Per-chapter words, sentence-length spread, dialogue share, tic rates, and phrases repeated across the book; `--slop` lists banned-phrase and tic hits by line |
| `scripts/blind-compare prepare PATH REV…` / `reveal ID` | Anonymises alternative versions into `build/blind/ID/A.md, B.md…` for a blind judge, then reveals who wrote which |
| `scripts/check-locked` | Fails if a `LOCKED` span differs between HEAD and the staged text (run by the commit-msg hook) |
| `python3 scripts/todo.py list` | Lists open TODOs and AGENT-Qs with file:line |
| `python3 scripts/todo.py ids` | Assigns ids (never reused) and normalizes markers |
| `python3 scripts/todo.py check-scope <commit>` | Fails if any manuscript line changed since `<commit>` lies outside a TODO's scope (`--staged --ids t3` checks one commit) |
| `python3 scripts/todo.py lint` | Rejects malformed, duplicate, or unmatched TODO markers |
| `python3 scripts/todo.py check-resolved` | Fails if any TODO is still open without an AGENT-Q |
| `scripts/semantic-lines.py FILE…` | Reflows prose to one sentence per line (`--check` only reports) |
| `scripts/new-chapter NN "Title"` | Creates `manuscript/chNN-title.md` with a heading and a draft TODO |
| `scripts/chapter-names [--check]` | Renames chapter files to match their headings after a title change (`--check` only lists mismatches) |
| `scripts/compile.sh [docx\|epub\|pdf\|md]` | Builds a reader copy in `build/` |
| `scripts/import-codex-sessions.sh` | Copies Codex prompts for this repo into `prompts/codex/` |
| `git wdiff A B -- file` | Word-level diff between any two commits or branches |

### Git hooks

- **commit-msg** adds `Pass: author-edit` to any commit without a Pass trailer, so a plain `git commit` from you is always recorded as yours. From an agent shell (Claude Code or Codex) it rejects such a commit instead, so agent text is never mislabelled as yours. For agent commits it checks the **staged** text, never the working copy:
  - the pass name is known, and no `LOCKED` span changed;
  - report passes (critique, cold-read, reader-report, blind-judge, continuity, voice-check, slop-check, learn-from-edits) wrote only to `feedback/` and `prompts/`; planning and memory passes changed only comment markers in `manuscript/`;
  - TODO markers are well formed;
  - for `todo-implement`: each named TODO existed and is resolved (an AGENT-Q counts as awaiting you, not done), and every changed line lies inside that TODO's scope, unless the commit body explains it under `Out-of-scope:`.
- **pre-commit** gives a gentle reminder when manuscript files aren't one sentence per line.

---

Run the regression tests with `python3 -m unittest discover -s tests -v`. They build temporary repositories and check every safeguard above (scope, staged-text TODO checks, commit isolation, pass boundaries, locked text), plus blind-compare bundles, memory freshness, learn-diff attribution, reflow, cycle notes, and reader-copy isolation. Run them after changing any script or hook.

## Skills

Skills live in `.skills/<name>/SKILL.md`. Setup links that folder into `.claude/skills` (Claude Code) and `.agents/skills` and `.codex/skills` (Codex), so both harnesses use the same definitions.
Codex's skill folder has changed between versions. If Codex doesn't see the skills, check its current docs and add the right path to the loop in `scripts/setup.sh`.

| Skill | Edits the manuscript? | Say something like |
|---|---|---|
| `scene-draft` | Yes | "Draft ch05 from the outline" / "Draft two alternatives for ch07" |
| `todo-plan` | No; writes `plan/todo-plan.md` | "Plan the TODOs" |
| `todo-implement` | Yes, only within TODO scopes | "Implement the TODOs" / "Implement the plan" |
| `line-edit` | Yes | "Line edit the second half of ch03" |
| `developmental-critique` | No; writes to `feedback/` | "Critique Act I" |
| `cold-read` | No; writes to `feedback/` | "Cold read ch01–ch05" |
| `reader-report` | No; writes to `feedback/` and `scores.tsv` | "Reader report on ch05" / "How would critics take this?" |
| `blind-judge` | No; writes to `feedback/` | "Blind-judge 20261015-142233" |
| `feedback-triage` | No; updates `feedback/INDEX.md` and `decisions.md` | "Triage the feedback" |
| `structural-revision` | Only to insert TODO markers, after you approve the plan | "Plan a structural revision: …" |
| `continuity-check` | No; writes to `feedback/` | "Check continuity in ch01–ch06" |
| `voice-check` | No; writes to `feedback/` | "Do Mara and Jo sound too alike?" |
| `slop-detector` | Its own text only; reports on yours | "Slop check ch04" (agents also run it on everything they write) |
| `canon-update` | No; updates the bible, threads, summaries, and synopsis | "Update canon" |
| `learn-from-edits` | No; proposes style changes | "Learn from my edits" |
| `compile` | No | "Compile a docx for my readers" |

To add a skill, create `.skills/<name>/SKILL.md` with `name` and `description` frontmatter. The description decides when an agent reaches for it, so say plainly when it applies.
Candidate skills you might add later: `beat-sheet` (outline from premise), `epigraph-and-titles`, and `query-letter`.

---

## Working with both harnesses and several models

- **One set of instructions.** Codex reads `AGENTS.md` directly, and Claude Code reads it through the import in `CLAUDE.md`. Never put rules in only one of them.
- **Provenance.** Agents must pass `--model` and `--harness` to `agent-commit`, so `scripts/passes` shows who did what.
- **Route by evidence.** After a pass worth remembering, add a row to `models.md`: your review minutes, useful findings out of total, continuity defects introduced, and blind results. Update the "Current routing" section as patterns emerge. Word counts, numbers of passes, slop-hit counts, and rising AI scores are not evidence of quality.
- **Cross-model review.** A model critiquing its own draft tends to miss its own habits, so draft with one model and critique, cold-read, and judge with another.
- **Fresh sessions for fresh eyes.** Run cold reads and blind judging in a new session, so the model carries no memory of the plan or of who drafted what.
- **Parallel drafts.** Use `alt/*` branches and blind judging (workflow 7) to compare models on the same scene or TODO.

---

## Prompt retention

- **Claude Code:** `.claude/settings.json` registers a `UserPromptSubmit` hook (`scripts/log-prompt.sh`). Every prompt is appended to `prompts/claude/YYYY-MM.jsonl` with its timestamp, session, branch, and HEAD commit.
- **Codex:** Codex keeps session transcripts under `~/.codex/sessions`. Run `scripts/import-codex-sessions.sh` before committing to copy this repo's prompts into `prompts/codex/`.
- **Linking prompts to commits.** Agent commits carry a `Prompt-Log:` trailer naming the harness's newest log file and, when the session is known (Claude Code's session id, or `--session` from the agent), a `Prompt-Session:` trailer. Search the log for that session to find the prompts that produced the commit. Nothing is recorded when the session is unknown, rather than guessing.
- **Privacy.** Logs are committed with the book and contain everything you typed. Before sharing a book repository, review `prompts/`; to keep logs local only, add `prompts/claude/` and `prompts/codex/` to `.gitignore`.
- **`prompts/library/`** is for prompts that worked especially well. Save them by hand with a note on why.
- Commit the logs along with your work (`author-commit` picks them up). When you later reevaluate the framework, the logs, `models.md`, the `feedback/` reports, and `git passes` give you the complete record.

---

## Tips for getting high-quality work

- **Your exemplar passages set the ceiling.** Agents imitate examples far better than they follow adjectives like "lyrical" or "spare".
- **Choose a useful unit.** Draft enough connected scenes to assess their effect; revise one consequential uncertainty at a time. Use `plan/cycle.md` for substantial work.
- **Structure before sentences.** Don't line-edit a chapter whose scenes may still be cut.
- **Be concrete in TODOs.** "Colder: she refuses in four words and leaves" beats "make this better". When you don't know what you want, ask for options in plan mode or for alternatives judged blind.
- **Record rulings in `decisions.md`.** If you correct the same thing twice, it belongs there or in `style.md`, or you'll correct it a third time.
- **Protect what's finished.** Wrap sentences you never want touched in `<!-- LOCKED -->` … `<!-- /LOCKED -->`. The commit hook rejects any agent commit that changes them.
- **Test on readers.** Cold reads and simulated panels supply hypotheses. Independent human responses at sequence and full-draft milestones test whether the intended experience reaches readers.
- **Answer every note.** Triage feedback so rejected notes become Deliberate choices; otherwise each new critic spends its attention re-arguing them.
- **Read the diff, not just the result.** `scripts/review` shows exactly what the agent changed. Scan it for stray edits, then read the chapter clean.
- **Keep critiques separate from rewrites.** Ask for the report first, decide, then direct changes through TODOs. This keeps you in charge of the book's direction.
- **Revert freely.** Every TODO is its own commit, so `git revert <hash>` undoes one change without touching the rest.
- **Keep the bible lean.** Put in facts the story needs. Every extra paragraph competes for the agent's attention.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| The agent says the tree is dirty | Run `scripts/author-commit "…"`, then ask again |
| `check-scope` or the commit hook reports out-of-scope edits | Revert them (`git checkout <base> -- file` for that hunk, or edit by hand). A genuine continuity fix or typo is allowed when the commit body explains it under `Out-of-scope:` |
| `agent-commit` says other files are already staged, or that you committed during the pass | It is protecting your work. Commit or unstage your own changes (`scripts/author-commit` or `git restore --staged`), then ask the agent to re-run its preflight and check its edits against yours |
| `scripts/memory-status` reports stale summaries | Ask for "Update canon for chNN" before drafting chapters that depend on them |
| A `todo-implement` commit is rejected | A TODO named in the commit is still in the text. Resolve it or add an AGENT-Q. |
| The agent edited too much | Tighten the scope with `[start]`/`[end]`, lock the surrounding text, and add a line to `decisions.md` |
| Claude Code doesn't see the skills, or hooks don't run after a clone | Run `scripts/setup.sh` (it relinks `.claude/skills` and sets `core.hooksPath`) |
| Codex doesn't see the skills | Check its docs for the current skills folder and add that path in `scripts/setup.sh` |
| An agent's commit is rejected for "no Pass: trailer" | It ran a bare `git commit`; it must use `scripts/agent-commit`. Committing your own work from inside an agent session? Use `scripts/author-commit`, or prefix with `WORKBENCH_AUTHOR=1` |
| A commit is rejected for a LOCKED span | An agent changed locked text. Revert that hunk; if the change is wanted, make it yourself |
| `git push` asks for a password or is denied over SSH | Use HTTPS with the GitHub CLI: `gh auth login`, then `gh auth setup-git` (or per repo: `git config credential.https://github.com.helper '!gh auth git-credential'`) |
| Prompts aren't being logged | Make sure `scripts/log-prompt.sh` is executable and that Claude Code was started in the repo root |
