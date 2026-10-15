---
name: slop-detector
description: Detect generic AI-flavoured prose, clichés, repetition, and the banned phrases in bible/style.md. Use on every agent-written passage before committing, and whenever the author asks to check for clichés, purple prose, or "AI-sounding" writing.
---
# slop-detector
Run on text you produced (or text the author points at). Fix hits in your own text; report hits in author text.

## Start with the numbers
1. `scripts/stats --slop <files>` lists banned-phrase and tic hits with file:line. Treat every hit as a candidate, not a verdict: a deliberate "not X but Y" can be right.
2. `scripts/stats <files>` (or no files, for the whole book) shows sentence-length spread, paragraphs ending in fragments, tic rates per 1,000 words, and phrases repeated across chapters. Repetition across chapters is the tic you are least able to see yourself; check every repeated phrase that isn't a deliberate motif (see `bible/threads.md`).

## Then check by reading
- Rule of three used reflexively (three adjectives, three clauses, three beats).
- Emotion named after it's been shown ("She was angry." after slamming a door).
- Tidy epiphanies, moral summaries, or a closing line that explains the scene.
- Abstract nouns doing the work of images: weight, silence, tension, something, everything, the air.
- "Not X, but Y" constructions and rhetorical antithesis used as a tic.
- Characters "nodding", "smiling softly", "letting out a breath" as filler beats.
- Uniform sentence length across a paragraph; every paragraph ending on a punchy fragment.
- Over-precise hedging ("almost", "somehow", "a kind of") and stacked similes.
- Dialogue in which people speak in complete, articulate paragraphs about their feelings.
- Leonard's surface tics (`reference/craft-lenses.md` §7): tags other than "said", adverbs on "said", "suddenly", exclamation marks, weather openings. `scripts/stats --slop` lists most of them. Treat them as flags; the style guide decides.
- Reaction before stimulus ("She flinched as the glass shattered").

## Output
When used as a pass: `feedback/YYYY-MM-DD-slop-<scope>.md` listing file:line, the hit, and a suggested alternative. Add findings to `feedback/INDEX.md`. Commit with `--pass slop-check`.
If a phrase keeps recurring, propose adding it to the banned list (the author decides).
