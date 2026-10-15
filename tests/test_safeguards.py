"""Regression tests for the author-ownership safeguards, run against disposable repositories.

Run: python3 -m unittest discover -s tests -v
Each test copies the real scripts/ and .githooks/ into a temporary repository; nothing here touches
this repository. Several cases reproduce defects found in the 2026-10-15 tooling audit
(feedback/2026-10-15-critique-gpt-6-tooling.md): adjacent out-of-scope rewrites, TODO checks reading
the working copy, and --files absorbing already-staged author work.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

CHAPTER = """CHAPTER 1 — One
---------------

Para A one.
Para A two.

<!-- TODO t1 [next]: colder -->
Para B one.
Para B two.

Para C protected.

<!-- LOCKED -->
Locked line.
<!-- /LOCKED -->
"""
CH = "manuscript/ch01-one.md"
AGENT = ["--model", "test-model", "--harness", "claude-code"]


class Repo:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name)
        shutil.copytree(ROOT / "scripts", self.path / "scripts",
                        ignore=shutil.ignore_patterns("__pycache__", "build"))
        shutil.copytree(ROOT / ".githooks", self.path / ".githooks")
        for d in ("manuscript", "feedback", "plan/summaries"):
            (self.path / d).mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / "plan/cycle.md", self.path / "plan/cycle.md")
        self.write(CH, CHAPTER)
        self.run("git", "init", "-q", "-b", "main")
        self.run("git", "config", "user.email", "test@example.invalid")
        self.run("git", "config", "user.name", "Test")
        self.run("git", "config", "core.hooksPath", ".githooks")
        self.author_commit("base")

    def close(self):
        self.tmp.cleanup()

    def env(self, agent):
        env = {k: v for k, v in os.environ.items()
               if not k.startswith(("CLAUDE", "CODEX")) and k != "WORKBENCH_AUTHOR"}
        if agent:
            env["CLAUDECODE"] = "1"
        return env

    def run(self, *cmd, agent=False, check=True):
        r = subprocess.run(cmd, cwd=self.path, capture_output=True, text=True, env=self.env(agent))
        if check and r.returncode:
            raise AssertionError(f"{cmd} failed:\n{r.stdout}\n{r.stderr}")
        return r

    def write(self, rel, text):
        p = self.path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def read(self, rel):
        return (self.path / rel).read_text(encoding="utf-8")

    def author_commit(self, msg):
        self.run("git", "add", "-A")
        self.run("git", "commit", "-q", "-m", msg)

    def agent_commit(self, pass_, files, msg="agent change", extra=(), check=False):
        return self.run("scripts/agent-commit", "--pass", pass_, *AGENT, "--files", files,
                        "-m", msg, *extra, agent=True, check=check)

    def head(self):
        return self.run("git", "rev-parse", "HEAD").stdout.strip()


class SafeguardTests(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()

    def tearDown(self):
        self.repo.close()

    def edit(self, old, new):
        self.repo.write(CH, self.repo.read(CH).replace(old, new))

    # --- TODO scope ---------------------------------------------------------------

    def test_in_scope_todo_commit_passes(self):
        self.edit("<!-- TODO t1 [next]: colder -->\nPara B one.\nPara B two.", "Para B, colder.")
        r = self.repo.agent_commit("todo-implement", CH, extra=("--todo", "t1"))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_adjacent_unauthorized_rewrite_is_rejected(self):
        # One contiguous hunk covering the authorized paragraph AND the protected one after it.
        self.edit("<!-- TODO t1 [next]: colder -->\nPara B one.\nPara B two.\n\nPara C protected.",
                  "Para B, colder.\nPara C, rewritten.")
        before = self.repo.head()
        r = self.repo.agent_commit("todo-implement", CH, extra=("--todo", "t1"))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("outside the named TODO scope", r.stdout + r.stderr)
        self.assertEqual(self.repo.head(), before)

    def test_out_of_scope_edit_allowed_only_with_explanation(self):
        self.edit("<!-- TODO t1 [next]: colder -->\nPara B one.\nPara B two.", "Para B, colder.")
        self.edit("Para A one.", "Para A one, typo fixed.")
        r = self.repo.agent_commit("todo-implement", CH, extra=("--todo", "t1"))
        self.assertNotEqual(r.returncode, 0)
        r = self.repo.agent_commit("todo-implement", CH, extra=(
            "--todo", "t1", "-b", "Out-of-scope: fixed a typo in the paragraph before (ch01:4)."))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_scope_check_reports_adjacent_rewrite_across_a_pass(self):
        base = self.repo.head()
        self.edit("Para C protected.", "Para C changed.")
        self.repo.author_commit("simulate stray change")
        r = self.repo.run("python3", "scripts/todo.py", "check-scope", base, check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("outside any TODO scope", r.stdout)

    # --- TODO completion against the staged text -------------------------------------

    def test_todo_check_reads_the_index_not_the_working_copy(self):
        self.edit("Para B one.", "Para B, colder.")  # marker still present
        self.repo.run("git", "add", CH)
        self.edit("<!-- TODO t1 [next]: colder -->\n", "")  # removed only in the working copy
        r = self.repo.run("git", "commit", "-q", "-m", "t1", "-m", "Pass: todo-implement\nTodo: t1",
                          agent=True, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("still open in the staged text", r.stdout + r.stderr)

    def test_unknown_todo_id_is_rejected(self):
        self.edit("<!-- TODO t1 [next]: colder -->\nPara B one.\nPara B two.", "Para B, colder.")
        r = self.repo.agent_commit("todo-implement", CH, extra=("--todo", "t9"))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("no such open TODO", r.stdout + r.stderr)

    def test_agent_question_counts_as_awaiting_not_resolved(self):
        self.edit("<!-- TODO t1 [next]: colder -->", "<!-- TODO t1 [next]: colder -->\n<!-- AGENT-Q t1: how cold? -->")
        r = self.repo.agent_commit("todo-implement", CH, extra=("--todo", "t1"))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("awaiting", r.stdout + r.stderr)

    def test_check_resolved_honours_author_skip_in_plan(self):
        r = self.repo.run("python3", "scripts/todo.py", "check-resolved", check=False)
        self.assertEqual(r.returncode, 1)
        self.repo.write("plan/todo-plan.md", "# TODO plan\n\n## t1 — ch01 [next]\nDirective: colder\nAuthor: skip\n")
        r = self.repo.run("python3", "scripts/todo.py", "check-resolved", check=False)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_lint_rejects_duplicate_and_unmatched_markers(self):
        self.edit("Para A one.", "<!-- TODO t1 [prev]: again -->\n<!-- TODO t2 [start]: range -->\nPara A one.")
        r = self.repo.run("python3", "scripts/todo.py", "lint", check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("duplicate id t1", r.stdout)
        self.assertIn("never closed", r.stdout)

    def test_ids_are_never_reused(self):
        self.edit("<!-- TODO t1 [next]: colder -->\nPara B one.\nPara B two.", "Para B, colder.")
        self.repo.agent_commit("todo-implement", CH, extra=("--todo", "t1"), check=True)
        self.edit("Para C protected.", "Para C protected.\n<!-- TODO [prev]: warmer -->")
        self.repo.run("python3", "scripts/todo.py", "ids")
        self.assertIn("TODO t2 [prev]", self.repo.read(CH))

    # --- commit isolation ----------------------------------------------------------

    def test_prestaged_unrelated_work_is_never_absorbed(self):
        self.repo.write("notes.md", "author's private notes\n")
        self.repo.run("git", "add", "notes.md")
        self.repo.write("feedback/report.md", "report\n")
        before = self.repo.head()
        r = self.repo.agent_commit("critique", "feedback/report.md")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("already staged", r.stdout + r.stderr)
        self.assertEqual(self.repo.head(), before)

    def test_unnamed_files_are_left_unstaged(self):
        self.repo.write("feedback/report.md", "report\n")
        self.repo.write("notes.md", "author's notes\n")
        self.repo.agent_commit("critique", "feedback/report.md", check=True)
        files = self.repo.run("git", "show", "--name-only", "--format=").stdout.split()
        self.assertEqual(files, ["feedback/report.md"])

    def test_author_commit_during_pass_stops_agent_commit(self):
        self.repo.run("scripts/agent-preflight", agent=True)
        self.edit("Para A one.", "Para A one, author's change.")
        self.repo.author_commit("author edits mid-pass")
        self.repo.write("feedback/report.md", "report\n")
        r = self.repo.agent_commit("critique", "feedback/report.md")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("author committed during this pass", r.stdout + r.stderr)

    def test_files_model_and_harness_are_required(self):
        self.repo.write("feedback/report.md", "report\n")
        for args in (["--pass", "critique", "-m", "x", *AGENT],
                     ["--pass", "critique", "-m", "x", "--files", "feedback", "--harness", "codex"],
                     ["--pass", "critique", "-m", "x", "--files", "feedback", "--model", "m"]):
            r = self.repo.run("scripts/agent-commit", *args, agent=True, check=False)
            self.assertNotEqual(r.returncode, 0, args)

    def test_bare_commit_from_agent_shell_is_rejected(self):
        self.repo.write("feedback/report.md", "report\n")
        self.repo.run("git", "add", "-A")
        r = self.repo.run("git", "commit", "-q", "-m", "sneaky", agent=True, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("agent-commit", r.stdout + r.stderr)

    # --- pass boundaries and locked text --------------------------------------------

    def test_report_pass_may_not_touch_manuscript(self):
        self.edit("Para C protected.", "Para C improved by a critic.")
        r = self.repo.agent_commit("critique", "manuscript")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("writes only to feedback/", r.stdout + r.stderr)

    def test_marker_only_pass_may_add_markers_but_not_prose(self):
        self.edit("Para C protected.", "Para C protected.\n<!-- TODO t2 [prev]: staged by plan -->")
        r = self.repo.agent_commit("structural-revision", "manuscript")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.edit("Para A two.", "Para A two, quietly edited.")
        r = self.repo.agent_commit("canon-update", "manuscript")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("may not change manuscript prose", r.stdout + r.stderr)

    def test_locked_span_is_protected_from_agents(self):
        self.edit("Locked line.", "Unlocked line.")
        r = self.repo.agent_commit("revise", CH)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("LOCKED", r.stdout + r.stderr)

    def test_unknown_pass_is_rejected(self):
        self.repo.write("feedback/report.md", "report\n")
        r = self.repo.agent_commit("polish-everything", "feedback")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("unknown Pass", r.stdout + r.stderr)

    # --- blind comparison -----------------------------------------------------------

    def branch_with(self, name, text):
        self.repo.run("git", "switch", "-q", "-c", name, "main")
        self.edit("Para B one.", text)
        self.repo.author_commit(name)
        self.repo.run("git", "switch", "-q", "main")

    def test_blind_compare_validates_before_writing(self):
        self.branch_with("alt/a", "Version A.")
        r = self.repo.run("scripts/blind-compare", "prepare", CH, "alt/a", "no-such-branch", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse((self.repo.path / "build/blind").exists()
                         and any(p for p in (self.repo.path / "build/blind").iterdir()))
        r = self.repo.run("scripts/blind-compare", "prepare", CH, "alt/a", "alt/a", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("identical", r.stdout + r.stderr)

    def test_blind_compare_bundle_records_full_ids_and_hashes(self):
        self.branch_with("alt/a", "Version A.")
        self.branch_with("alt/b", "Version B.")
        self.repo.run("scripts/blind-compare", "prepare", CH, "alt/a", "alt/b")
        (bundle,) = [p for p in (self.repo.path / "build/blind").iterdir() if not p.name.startswith(".")]
        key = json.loads((bundle / ".key.json").read_text())
        self.assertEqual({c["letter"] for c in key["candidates"]}, {"A", "B"})
        for c in key["candidates"]:
            self.assertEqual(len(c["commit"]), 40)
            self.assertEqual(len(c["judged_sha256"]), 64)
            self.assertNotIn("TODO", (bundle / f"{c['letter']}.md").read_text())

    # --- memory freshness and learning ----------------------------------------------

    def test_memory_status_flags_summary_after_chapter_changes(self):
        rev = self.repo.head()
        self.repo.write("plan/summaries/ch01.md", f"# ch01\nSource revision: {rev}\n")
        self.repo.write("bible/canon.md", "- Mara owns the ferry (ch01)\n")
        self.repo.author_commit("summary")
        r = self.repo.run("scripts/memory-status", "--check", check=False)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.edit("Para A one.", "Para A one, changed.")
        self.repo.author_commit("change chapter")
        r = self.repo.run("scripts/memory-status", "--check", check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("stale", r.stdout)
        self.assertIn("1 canon entries", r.stdout)

    def test_learn_diff_traces_author_change_to_agent_prose_only(self):
        self.edit("<!-- TODO t1 [next]: colder -->\nPara B one.\nPara B two.", "Agent sentence.")
        self.repo.agent_commit("todo-implement", CH, extra=("--todo", "t1"), check=True)
        self.edit("Agent sentence.", "Author's sentence.")
        self.edit("CHAPTER 1 — One", "CHAPTER 1 — Uno")
        self.repo.author_commit("author revises")
        r = self.repo.run("scripts/learn-diff")
        self.assertIn("- Agent sentence.", r.stdout)
        self.assertIn("todo-implement/test-model", r.stdout)
        self.assertNotIn("CHAPTER", r.stdout)
        self.assertIn("not a model ranking", r.stdout)


class ReflowTests(unittest.TestCase):
    def test_initials_and_dialogue(self):
        import importlib.machinery
        import importlib.util
        loader = importlib.machinery.SourceFileLoader("semantic_lines", str(ROOT / "scripts/semantic-lines.py"))
        mod = importlib.util.module_from_spec(importlib.util.spec_from_loader("semantic_lines", loader))
        loader.exec_module(mod)
        self.assertEqual(mod.reflow('"Go," she said. "Now." He met J. R. Smith. It was 5 p.m. Then rain.'),
                         '"Go," she said.\n"Now."\nHe met J. R. Smith.\nIt was 5 p.m.\nThen rain.')


if __name__ == "__main__":
    unittest.main()
