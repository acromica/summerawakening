#!/usr/bin/env bash
# Setup: git repo, hooks, aliases, and skill links for both harnesses.
# Safe to rerun without --new-book. That flag explicitly discards Git history.
# core.hooksPath is local git config and is NOT carried by a clone.
# usage: scripts/setup.sh [--new-book] [--quiet] [--remote URL]
set -euo pipefail
cd "$(dirname "$0")/.."
quiet="" remote="" new_book=""
die() { echo "setup: $*" >&2; exit 2; }
while [ $# -gt 0 ]; do
  case "$1" in
    --new-book) new_book=1; shift;;
    --quiet) quiet=1; shift;;
    --remote)
      [ $# -ge 2 ] && [ -n "$2" ] && [[ "$2" != -* ]] || die "--remote requires a repository URL"
      remote="$2"; shift 2;;
    -h|--help)
      echo "Usage: scripts/setup.sh [--new-book] [--quiet] [--remote URL]"
      echo "Initializes Git if needed, installs hooks and skills, and creates the first commit."
      echo "--remote adds origin; it never replaces a different origin or pushes."
      echo "--new-book deletes existing Git history and remotes; use only when starting a book."
      exit 0;;
    *) die "unknown argument: $1";;
  esac
done
say() { [ -n "$quiet" ] || echo "$@"; }

if [ -n "$new_book" ] && [ -e .git ]; then
  [ -d .git ] && [ ! -L .git ] || die "--new-book requires a standalone clone, not a linked worktree"
  [ ! -d .git/worktrees ] || die "--new-book cannot remove a repository with linked worktrees"
  [ -z "$(git status --porcelain)" ] || die "--new-book requires a clean working tree; save your changes first"
  # Explicit opt-in only: normal setup must preserve the book's history.
  rm -rf -- .git
fi

# A worktree uses a .git file; never reinitialize it.
[ -e .git ] || git init -q -b main
if [ -n "$remote" ]; then
  if git remote | grep -qx origin; then
    [ "$(git remote get-url origin)" = "$remote" ] || die "origin already points elsewhere; inspect git remote -v before changing it"
  else
    git remote add origin "$remote"
  fi
fi
[ "$(git config core.hooksPath || true)" = ".githooks" ] || { git config core.hooksPath .githooks; echo "setup: enabled git hooks (.githooks)"; }
chmod +x .githooks/* scripts/* 2>/dev/null || true

# Word-level diffs are far more readable for prose.
git config diff.wordRegex '[^[:space:]]+'
git config alias.wdiff 'diff --word-diff=color'
git config alias.passes '!scripts/passes'

# Skills live once in .skills/ and are linked into each harness's skill folder.
# Claude Code: .claude/skills   Codex: .agents/skills (also .codex/skills for older builds).
# If your Codex version reads a different folder, add it to this list.
for dir in .claude/skills .agents/skills .codex/skills; do
  mkdir -p "$(dirname "$dir")"
  if [ -L "$dir" ] && [ -d "$dir/" ]; then continue; fi
  # an empty real directory (e.g. created by a harness or a symlink-less checkout) is replaced
  if [ -d "$dir" ] && [ ! -L "$dir" ] && [ -z "$(ls -A "$dir")" ]; then rmdir "$dir"; fi
  if [ -e "$dir" ] || [ -L "$dir" ]; then
    echo "setup: WARNING $dir exists but is not a working link to .skills; fix it by hand" >&2
    continue
  fi
  ln -s ../.skills "$dir" && echo "setup: linked $dir -> .skills"
done

say "Setup complete."
say "  hooks:   .githooks (commit-msg labels author edits, enforces TODO and LOCKED rules)"
say "  skills:  .skills -> .claude/skills, .agents/skills, .codex/skills"
say "  aliases: git wdiff, git passes"

if ! git rev-parse HEAD >/dev/null 2>&1; then
  git add -A
  git commit -q -m "Scaffold fiction workbench" -m "Pass: setup"
  say "Initial commit created."
fi
if [ -n "$remote" ]; then
  say "Origin: $remote"
  say "Ready to publish: git push -u origin HEAD"
fi
