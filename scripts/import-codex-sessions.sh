#!/usr/bin/env bash
# Copy Codex session prompts for THIS repo into prompts/codex/.
# Codex stores sessions as JSONL under ~/.codex/sessions (override with CODEX_HOME).
set -euo pipefail
root=$(git rev-parse --show-toplevel)
src="${CODEX_HOME:-$HOME/.codex}/sessions"
[ -d "$src" ] || { echo "No Codex sessions at $src"; exit 0; }
mkdir -p "$root/prompts/codex"
python3 - "$src" "$root" <<'PY'
import json, os, sys, pathlib
src, root = sys.argv[1], sys.argv[2]
out_dir = pathlib.Path(root, "prompts/codex")
n = 0
for p in pathlib.Path(src).rglob("*.jsonl"):
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    if not any(root in l for l in lines[:5]):
        continue  # session was not run in this repo
    prompts, model = [], None
    for l in lines:
        try:
            ev = json.loads(l)
        except Exception:
            continue
        s = json.dumps(ev)
        pl = ev.get("payload", ev)
        model = model or pl.get("model")
        # user messages appear as role=user message items; format varies by Codex version
        if pl.get("role") == "user" or pl.get("type") == "user_message":
            text = pl.get("message") or " ".join(
                c.get("text", "") for c in pl.get("content", []) if isinstance(c, dict))
            if text and not text.startswith("<environment_context>"):
                prompts.append({"ts": ev.get("timestamp"), "prompt": text})
    if prompts:
        target = out_dir / (p.stem + ".jsonl")
        with open(target, "w", encoding="utf-8") as fh:
            for r in prompts:
                r.update({"harness": "codex", "model": model, "source": str(p)})
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        n += 1
print(f"Imported prompts from {n} Codex session(s) into prompts/codex/")
PY
