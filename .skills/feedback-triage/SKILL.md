---
name: feedback-triage
description: Walk the author through open items in feedback/INDEX.md and record each disposition (accepted, rejected, deferred, duplicate, superseded, not reproducible, done, verified), turn accepted items into TODO markers, and record lasting artistic rejections as Deliberate choices in decisions.md so later critics stop re-raising them. Use when the author asks to triage, go through, or act on feedback, or says which notes they agree with.
---
# feedback-triage
1. Preflight. List the `open` and expired `deferred` rows in `feedback/INDEX.md`, grouped by report, most severe first. Before presenting them, mark obvious duplicates of earlier rows (`duplicate (of …)`) and rows whose cited passage has since changed, so the author sees each issue once and knows which ones may no longer apply.
2. Present them in small batches (about five). For each, separate what the reader experienced (the observation) from the critic's guess at the cause and the proposed fix: the author may accept the observation and reject the fix. The author says accept, reject (with a reason), defer, or "no longer applies". Don't argue; one sentence of context per item if asked.
3. Record each answer in the Status column:
   - **accepted** — if the item is a local change, give the author a ready-to-paste TODO marker (don't insert it yourself unless asked; author TODOs are the author's). Note in the TODO what effect to check afterwards.
   - **rejected (reason)** — critics read rejected rows and won't re-raise them. Ask whether this is a lasting artistic choice for the book. Only if the author says yes, add a line to **Deliberate choices** in `decisions.md`: `- <the choice> — <author's reason> (feedback/<report>#<n>)`. A mistaken observation or an unwanted remedy is just rejected.
   - **deferred (until …)** — with the milestone or condition, e.g. "until the full draft".
   - **superseded / not-reproducible** — when the passage was rewritten or the problem no longer occurs at the current revision; name the revision.
4. When the author reports an accepted item implemented, set it to `done (commit)`. Set `verified (how)` only after the intended effect was checked (a reread in context, a cold read, a human reader); "done" means changed, not proven better.
5. Commit with `--pass bible -m "Triage feedback: N accepted, M rejected, K deferred"`.
