# Prompt logs
- `claude/YYYY-MM.jsonl` — every Claude Code prompt, logged by `.claude/settings.json` → `scripts/log-prompt.sh`.
- `codex/<session>.jsonl` — Codex prompts, imported with `scripts/import-codex-sessions.sh`.
- `library/` — reusable prompts that worked well. Save them here by hand with a note on why they worked.
Commits carry a `Prompt-Log:` trailer pointing at the newest log file at commit time.
