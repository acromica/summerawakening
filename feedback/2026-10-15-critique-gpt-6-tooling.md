# Repository evaluation: collaborative novel writing

Date: 2026-10-15. Reviewed baseline: e2f1d9c. Pass: critique. Model: gpt-6.

This is a tooling and workflow audit, not a manuscript critique.
The repository contains an empty manuscript and mostly unfilled book templates; it provides no completed writing cycles with which to establish literary effectiveness.
Findings below distinguish reproduced failures, implementation observations, and proposed workflow improvements.
No manuscript, script, skill, or binding decision was changed during this review.

The workbench has a strong foundation for accountable collaboration: explicit author ownership, small reversible changes, separation of critique from revision, and a durable record of decisions.
Its main weaknesses are incomplete enforcement of editing boundaries, evaluation methods without demonstrated calibration, and a process that could consume too much author attention.
The next investment should make the existing loop trustworthy and economical, then test whether it improves reader experience.

## Strengths worth preserving

The author reads before receiving criticism and decides which notes become instructions.
The combination of scoped TODOs, locked spans, recorded decisions, and critique-only passes gives practical form to author ownership (`AGENTS.md`, README recommended workflow).
The explicit “must never become” list and author-written exemplars help protect the particular book from generic improvement advice.

Plain Markdown and Git make the work portable, inspectable, and recoverable.
Sentence-per-line formatting improves review granularity; pass, model, and directive trailers preserve useful context for changes.
Small commits can support selective acceptance and reversal, provided the commit boundaries are reliable.

The evaluation methods ask different questions: developmental critique checks intention, cold reading checks what the page communicates, blind comparison examines alternatives, and continuity checking checks facts.
Cold-read's requirement to commit the initial reaction before inspecting intent is particularly valuable.
Blind judging allows a toss-up, and the slop-detector explicitly treats many flags as candidates rather than automatic faults.

The repository also addresses long-form work rather than just isolated generation: chapter end states, character knowledge, setup/payoff tracking, structural ripple maps, and structure-before-polish revision order.
Learning from actual author edits is a promising way to improve collaboration without continually re-explaining taste.
These are strengths of the design, not yet demonstrated outcomes from a novel written here.

## Findings and improvements

### 1. High — commits can absorb unrelated author work

**Reproduced.** `scripts/agent-commit:27–35` stages selected paths but does not restrict the existing index; line 61 commits everything staged.
In a disposable repository, staging `unrelated.txt`, then invoking `agent-commit --files report.md`, committed both files.
The default `git add -A` is broader still.
Preflight's clean-tree check protects only the start of a pass; an author can save or stage work afterward.
Even a selected file can contain concurrent author changes that a path allowlist cannot distinguish.

Require explicit paths, reject unrelated staged content, and capture the starting HEAD and selected-file content hashes.
Detect concurrent changes before applying edits and before committing; stop on conflicts without silently absorbing them.
For true simultaneous work, offer isolated worktrees as an explicit future workflow change, since current instructions require the current branch.
Test both unrelated-file staging and same-file concurrent edits.

### 2. High — TODO scope checks accept edits beyond the authorized range

**Reproduced.** `scripts/todo.py:244` tests whether a diff hunk overlaps any allowed range, rather than whether all changed material is authorized.
A fixture with a `[next]` paragraph followed by a protected paragraph passed after both were rewritten as one contiguous change.
The script printed “All manuscript edits fall inside TODO scopes.”
The `auto` implementation also allows twelve lines on either side, despite its comment describing adjacent paragraphs (`scripts/todo.py:222–223`).

Validate all changed old lines and insertion boundaries against the union of explicitly authorized ranges.
Validate the named TODO for each commit, not merely all TODOs present at the baseline.
Represent inferred `auto` scope explicitly before implementation, and reject malformed, duplicate, or unmatched markers.
Run this check against the staged patch before committing, with recorded exceptions for authorized continuity fixes.
Add fixtures for adjacent edits, deletions, insertions, range markers, renames, and new files.

### 3. High — TODO completion checks examine the wrong version

**Reproduced.** `.githooks/commit-msg` calls `todo.py check-ids`, which reads working-tree files (`scripts/todo.py:166–179`).
A staged file containing an unresolved `t2` passed when the working copy had removed `t2`.
The reverse can also create a false rejection.
An ID that never existed is not distinguished from a successfully resolved ID.

Check the parent and index snapshots: the claimed ID must exist in the parent and be removed or explicitly deferred in the staged result.
Distinguish “resolved” from “awaiting answer”; an AGENT-Q is not successful completion.
Make the final checker understand author-approved skips: the implementation skill permits them, but `check-resolved` currently does not.

### 4. High — infrastructure failures are not reliably surfaced, and there is no tracked test suite

**Observed.** Preflight printed `could not lock config file .git/config: Read-only file system` in this environment, then reported a clean tree and exited zero.
`scripts/agent-preflight:7` invokes setup without propagating its failure; setup writes Git configuration even during an ordinary check.
This run establishes a reporting failure, not that hooks are necessarily absent in this checkout.
No tracked automated test suite or CI configuration was found.

Separate read-only diagnostics from explicit setup/repair and propagate errors with clear distinctions between tree cleanliness and hook readiness.
Build a standard-library test suite using temporary repositories before adding more workflow features.
Cover commit isolation, staged-versus-working content, scope boundaries, locked spans, TODO grammar, sentence reflow, and export ordering/comment removal.
Keep literary heuristics advisory; make factual workflow invariants testable and blocking.

### 5. High — reader isolation is an instruction, not an enforced input boundary

**Implementation observation.** Cold-read forbids plan and TODO knowledge, but its mandatory preflight prints open TODO directives and the latest author commit subject.
Telling the reader to ignore comments still exposes the comments when raw manuscript files are read.
The general feedback protocol also requires reading decisions before writing a report, conflicting with cold-read's explicit prohibition unless the exception is broadened.
Reader-report says not to read the bible, while `AGENTS.md` requires it for every pass except cold-read.

Create a reader-only export and a read-only preflight that reveal no directives, commit subjects, author intent, or prior judgments.
Use fresh sessions with an explicit allowlist of inputs; disclose prior exposure if isolation cannot be achieved.
Clarify exceptions for both cold-read and reader-report, including when feedback indexing and decision-based deduplication occur.
For long manuscripts, record predictions before later chapters are supplied, then compare them with subsequent reactions.
Report reading coverage and omissions rather than implying that a mid-book sample was a whole-book read.

### 6. High — numerical reader scores lack empirical calibration

**Methodological limitation.** The 1–5 rubric and line-specific evidence are useful prompts for judgment.
However, “a professional editor would leave the chapter alone” is an undefined anchor, not a calibration procedure (`.skills/reader-report/SKILL.md:17`).
Three personas produced by one model are three prompted perspectives, not three independent readers.
Keeping the same model controls one variable; it does not control run variation, prompt changes, or rubric interpretation.
The instruction to record a commit is valuable, but the score table lacks rubric version, input coverage, run identity, and uncertainty.

Treat scores as diagnostic observations, never a release gate or proof of professional quality.
Develop author-approved anchor examples and compare revisions blind under the same conditions.
Repeat a sample of judgments, reverse candidate order, allow ties, and record confidence and disagreement.
Record the exact model identifier, rubric/prompt version, full manuscript revision, and input scope.
Calibrate against independent target-reader responses to complete narrative units, including remembered details, confusion, emotional effect, and willingness to continue.
Introduce human reading at an early meaningful milestone rather than relying on it only after extensive AI-led revision.

### 7. Medium — blind comparisons need stronger reproducibility and input validation

**Partly reproduced.** Randomized labels and stripped comments are good foundations.
`scripts/blind-compare:48` supports eight letters without validating the candidate count; nine candidates produce `KeyError: 'letter'` after partial output is written.
Second-resolution directory names can collide, and source paths/revisions are processed after the output directory is created.
These latter cases were identified by inspection, not executed.

Validate all candidates first, support arbitrary labels or reject excessive counts, use unique run IDs, and publish the bundle atomically.
Store full commit IDs and content hashes, and retain the actual judged bundle with its eventual result.
Include an unchanged baseline when useful, and separate judgment of scene effect from sentence preference.
Use fresh judges and repeated order-balanced comparisons for consequential decisions.
If promising lines are grafted into the winner, judge the resulting scene again: attractive fragments do not guarantee a coherent whole.

### 8. Medium — sentence survival is not a fair model-quality metric

**Implementation observation.** `scripts/learn-diff:117–142` compares edits from a selected author-commit window with all agent-attributed lines standing at HEAD.
Those are different populations; the output also counts blank lines, headings, and comments.
Git blame records the most recent line-level change, not the full history of creative contribution.
A punctuation edit can transfer attribution, and surviving prose may simply not have been reviewed yet.
README's claim that sentence-per-line makes learning “exact” overstates what is measured.

Keep before/after examples as evidence for tentative preferences.
Compare matched cohorts of reviewed passages, filter non-prose, and record revision purpose and task difficulty.
Separate acceptance, author revision time, factual defects, and blind reading preference.
Ask the author to confirm recurring stylistic hypotheses before turning them into rules; repeated cuts can have a local structural cause.
Do not rank models using a survival ratio derived from the current summary columns.

### 9. High — the default cycle can overinvest in chapter-level refinement

**Workflow judgment.** Every chapter receives critique, triage, review, and canon maintenance; additional periodic passes add further reports and author decisions (README cadence).
This is thorough, but it has no explicit effort budget, stopping criterion, or distinction between discovery drafting and revision.
The ten-part developmental report can generate work proportional to its template rather than to the chapter's actual needs.
The README wisely defers polishing, yet repeated full chapter critique can still optimize material later removed from the book.

Offer two modes: exploration and revision.
During exploration, draft a meaningful sequence, fix blockers, and maintain essential continuity; use a brief diagnosis of the largest risks.
During revision, choose one reader-effect objective, edit the necessary scope, then verify that effect and inspect collateral damage.
Limit routine criticism to the few highest-impact findings and explicitly identify what to preserve.
Set a review-time budget and stop when the objective is met or further work needs an author decision.
Reserve full panels, alternatives, and whole-book passes for consequential uncertainties and milestones.

### 10. High — craft frameworks can quietly become a house aesthetic

**Workflow judgment.** The repository says craft lenses are not laws, and scene-card fields may be left blank.
Nevertheless, the critique template asks every scene for a crisis, polarity shift, and outcome; character templates foreground want/need, lie, and wound; structural revision asks for MICE nesting.
These repeated defaults may pressure exploratory, comic, episodic, contemplative, or deliberately unresolved fiction toward a narrower shape.
An agent can also write a scene card and then have its own design evaluated for compliance rather than for worth.

Distinguish the author's desired experience from an agent's proposed means of achieving it.
Mark agent-generated cards as hypotheses and judge both the scene and the usefulness of the card.
Make craft frameworks selectable per book and permit “not applicable” without penalty.
Ask what a scene contributes—atmosphere, perception, pleasure, relationship, pressure, discovery—before requiring a conventional turn.
Use quality questions that include specificity, subtext, memorable perception, and intentional ambiguity, not only clarity and forward motion.

### 11. Medium — prose diagnostics sometimes present proxies as verdicts

**Implementation observation.** `scripts/stats:92` equates low sentence-length spread with monotonous rhythm, though the number cannot establish that conclusion.
Dialogue percentage counts lines containing quotation marks, and “fragment” percentage counts short final lines; neither is a direct linguistic classification.
The tokenizer is English/ASCII-oriented, and phrase detection can miss variants or flag benign substrings.
The slop-detector appropriately advises judgment, but scene-draft's “fix hits” instruction is less qualified.

Label outputs precisely as counts or heuristics and remove aesthetic conclusions from the script.
Use the author's exemplars and the current scene's purpose as context, not universal target distributions.
Align drafting instructions with the detector: inspect flags, fix unwanted habits, preserve intentional effects.
Add examples proving that repeated motifs, short complete sentences, and deliberate rhythmic uniformity survive the workflow.
Reducing flagged phrases is not itself a quality objective.

### 12. High — long-form memory has no freshness or fact-status mechanism

**Implementation observation.** Canon-update usefully derives summaries from the manuscript, but facts, timeline, threads, character files, synopsis, and scene cards overlap.
There is no machine-readable indication of which manuscript revision each derived record reflects.
Canon-update mainly describes adding facts and flagging contradictions; deletion, authorized retcon, and downstream invalidation are less explicit.
Short summaries can also omit the detail a later scene depends on.

Treat the manuscript as the authority for what is established and the plan as intended future work.
Record source revision and stable scene references for derived records, and flag them as stale when source scenes change.
Distinguish established fact, character belief, author-only intention, unresolved possibility, and superseded fact.
Make removal and retcon reconciliation explicit, with author decisions retained.
Add lightweight dependency lookup for reveals, objects, promises, and knowledge changes; retrieve original passages when the exact wording matters.
Avoid expanding every summary indefinitely: use compact summaries plus traceable evidence.

### 13. Medium — feedback tracking can turn into an accumulating obligation

**Workflow judgment.** The index makes decisions visible and prevents repeated criticism.
However, every finding becomes an open item, “later” remains open, and every rejection becomes a deliberate choice (`.skills/feedback-triage/SKILL.md`).
A mistaken observation, a rejected remedy, and a lasting artistic decision are not equivalent.
Line citations also drift after revision, and repeated reports can create duplicate issues.

Give findings stable IDs, source revisions, severity, confidence, and a short evidence quotation.
Separate observed reader effect from proposed cause and suggested remedy.
Support deferred, duplicate, superseded, and no-longer-reproducible dispositions, always recording the author's decision.
Promote a rejection to a binding artistic choice only when the author intends that scope.
Link a change to its follow-up check so “implemented” and “verified effective” remain distinguishable.

### 14. Medium — provenance is useful but not yet reliable enough for experiment tracking

**Implementation observation.** `scripts/agent-commit:40–43` chooses the most recently modified prompt file across both harnesses.
This may associate a commit with another session or harness; the Codex importer does not emit the `session` field that the fallback expects.
The wrapper warns about an absent model instead of requiring complete provenance, and the hooks do not enforce a pass vocabulary or critique-only file boundaries.

Pass an explicit run/session identifier through the workflow and associate a commit with an exact prompt record rather than file modification time.
Require valid pass, model, and harness metadata; make a tooling-audit pass available instead of overloading fiction critique.
Validate allowed file categories by pass, with explicit exceptions when authorized.
Track tool/skill versions and input revisions for experiments.
Document what prompt logs retain and give the author control over retention and redaction before sharing a book repository.

## Suggested operating technique

1. Establish a compact creative brief: audience, intended experience, exemplars, and the few boundaries that protect the book's identity. Leave exploratory questions open.
2. Draft a complete narrative unit with enough context to preserve cause and effect. Keep essential continuity current; defer optional criticism.
3. Have the author read first and record what worked, where attention changed, and the most important uncertainty.
4. Select the evaluation that answers that uncertainty: cold read for comprehension and effect, continuity check for facts, developmental critique for structure, or blind alternatives for a consequential choice.
5. Revise toward one explicit effect. Use narrow authorization where appropriate and a cross-chapter plan where necessary. Preserve identified strengths.
6. Verify the changed effect, check continuity consequences, refresh affected memory, and stop the cycle when the objective is satisfied.
7. At complete-sequence and full-draft milestones, use independent human readers and reconsider the book's structure before polishing sentences.

For example, “make this chapter better” invites unlimited rewriting.
“Readers should suspect the brother while still understanding why the protagonist trusts him” supplies a testable reading objective without prescribing the prose.
A fresh reader's unprompted prediction and account of the relationship can then reveal whether the revision helped.

## Implementation order and evidence of success

First repair findings 1–5 and add regression coverage: safe commits, accurate scope/completion checks, clear preflight failures, and isolated reader inputs.
Next introduce the shorter cycle and freshness tracking from findings 9 and 12.
Then improve evaluation records and run a small pilot comparing the current full cycle with the selective cycle on reasonably comparable narrative units.
Keep the brief and author constant where possible, balance assignment by task difficulty, and retain both versions for blind evaluation.
Such a pilot can expose practical problems; it will not establish a universal best writing method from a few chapters.

Measure author minutes spent reviewing, time to an accepted unit, corrections caused by continuity errors, useful versus duplicate findings, and independent reading preference with reasons.
Check whether gains survive in the surrounding sequence and final novel.
Do not optimize raw word production, number of passes, fewer flagged phrases, or average model score as substitutes for literary quality.

## Validation record

Preflight reported a clean tree at e2f1d9c, with the setup error noted in finding 4.
Inspected repository instructions, README, templates, workflow skills, hooks, and scripts; the manuscript contains no chapters.
Four executable cases ran in a disposable repository under `/tmp`, using the repository's commit wrapper for fixture commits:

| Case | Observed result |
|---|---|
| Rewrite authorized paragraph and adjacent unauthorized paragraph in one hunk | Scope checker exited 0 |
| Leave TODO in index, remove it only from working copy | Commit-message hook exited 0 |
| Pre-stage unrelated file, commit using `--files report.md` | Both files committed |
| Prepare nine blind candidates | Exit 1, `KeyError: 'letter'` |

No existing blind-comparison key was opened.
Other code observations are identified as inspection findings; no claims are made about measured reader outcomes, runtime performance at novel scale, or external product capabilities.
