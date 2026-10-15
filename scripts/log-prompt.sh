#!/usr/bin/env bash
# Claude Code UserPromptSubmit hook: append every prompt to prompts/claude/YYYY-MM.jsonl.
# Receives the hook JSON on stdin. Never blocks the prompt.
root="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
mkdir -p "$root/prompts/claude"
HOOK_INPUT="$(cat)" \
HOOK_OUT="$root/prompts/claude/$(date +%Y-%m).jsonl" \
HOOK_BRANCH="$(git -C "$root" branch --show-current 2>/dev/null)" \
HOOK_HEAD="$(git -C "$root" rev-parse --short HEAD 2>/dev/null)" \
python3 - <<'PY'
import json, os, datetime
try:
    data = json.loads(os.environ.get("HOOK_INPUT") or "{}")
except Exception:
    data = {"raw": os.environ.get("HOOK_INPUT")}
rec = {
    "ts": datetime.datetime.now().isoformat(timespec="seconds"),
    "harness": "claude-code",
    "model_env": os.environ.get("ANTHROPIC_MODEL"),
    "session": data.get("session_id"),
    "branch": os.environ.get("HOOK_BRANCH"),
    "head": os.environ.get("HOOK_HEAD"),
    "prompt": data.get("prompt", data.get("raw")),
}
with open(os.environ["HOOK_OUT"], "a", encoding="utf-8") as fh:
    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
PY
exit 0
