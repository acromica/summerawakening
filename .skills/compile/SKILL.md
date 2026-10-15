---
name: compile
description: Build the manuscript into docx, epub, pdf, or a single md file for readers, stripping TODO and AGENT-Q comments. Use when the author asks to compile, export, build, or share a readable copy.
---
# compile
Run `scripts/compile.sh <docx|epub|pdf|md>`. Output lands in `build/` (git-ignored).
Requires pandoc; pdf also needs a LaTeX engine. If pandoc is missing, use `md` and say so.
Before compiling, run `python3 scripts/todo.py list` and warn the author about any open TODOs or AGENT-Qs (they're stripped from the output, so readers won't see them).
