#!/usr/bin/env bash
# Build the manuscript for readers. HTML comments (TODOs, AGENT-Qs) are stripped.
# usage: scripts/compile.sh [docx|epub|pdf|md]   (needs pandoc; pdf needs a LaTeX engine)
set -euo pipefail
fmt="${1:-docx}"
mkdir -p build
tmp=$(mktemp)
for f in manuscript/*.md; do
  python3 - "$f" <<'PY'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
print(re.sub(r"<!--.*?-->\n?", "", t, flags=re.S).strip() + "\n\n")
PY
done > "$tmp"
title=$(grep -m1 '^title:' plan/premise.md 2>/dev/null | cut -d: -f2- | xargs || echo "Manuscript")
out="build/manuscript.$fmt"
if [ "$fmt" = md ]; then cp "$tmp" "$out"; else
  pandoc "$tmp" -f markdown -o "$out" --metadata title="${title:-Manuscript}"
fi
rm -f "$tmp"
echo "Wrote $out"
