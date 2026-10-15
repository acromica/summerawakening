"""Run with python3 -m unittest discover -s tests -v. No repository mutations."""
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    loader = importlib.machinery.SourceFileLoader(name, str(ROOT / 'scripts' / name))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


workflow = load('workflow')
reader = load('reader-copy')


class CycleTests(unittest.TestCase):
    def test_idle_template_and_comment_examples_are_not_active(self):
        fields, errors = workflow.inspect((ROOT / 'plan/cycle.md').read_text())
        self.assertEqual(fields['Status'], 'idle')
        self.assertEqual(errors, [])

    def test_active_cycle_exposes_missing_objective(self):
        _, errors = workflow.inspect('Status: active\nMode: revision\nScope: ch01\n')
        self.assertIn('Missing: Objective', errors)

    def test_verified_requires_evidence_and_memory_accounting(self):
        text = 'Status: verified\n' + '\n'.join(f'{k}: recorded' for k in workflow.FIELDS)
        text = text.replace('Mode: recorded', 'Mode: revision')
        _, errors = workflow.inspect(text)
        self.assertIn('Missing: Evidence', errors)
        self.assertIn('Missing: Continuity and memory', errors)
        _, errors = workflow.inspect(text + '\nEvidence: pending\nContinuity and memory: checked\n')
        self.assertIn('Evidence is still pending', errors)
        _, errors = workflow.inspect(text + '\nEvidence: report at revision abc\nContinuity and memory: no facts changed\n')
        self.assertEqual(errors, [])

    def test_duplicate_state_is_not_silently_overridden(self):
        _, errors = workflow.inspect('Status: active\nStatus: idle\n')
        self.assertIn('Duplicate field: Status', errors)


class ReaderTests(unittest.TestCase):
    def test_comments_removed_with_line_numbers_preserved(self):
        raw = '# Chapter\n\n<!-- TODO: secret\nanswer -->\nVisible.\n<!-- LOCKED -->Text.<!-- /LOCKED -->\n'
        result = reader.clean(raw)
        self.assertNotIn('secret', result)
        self.assertNotIn('TODO', result)
        self.assertEqual(result.splitlines()[4], 'Visible.')
        self.assertEqual(result.splitlines()[5], 'Text.')
        self.assertEqual(raw.count('\n'), result.count('\n'))

    def test_malformed_comments_fail_closed(self):
        for raw in ['Text.\n<!-- secret', '<!-- outer <!-- inner --> -->']:
            with self.assertRaises(ValueError):
                reader.clean(raw)

    def test_bundle_order_hashes_and_invalid_input(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'manuscript').mkdir()
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            tree = subprocess.check_output(['git', 'write-tree'], cwd=root, text=True).strip()
            revision = subprocess.check_output(['git', '-c', 'user.name=Test', '-c',
                'user.email=test@example.invalid', 'commit-tree', tree, '-m', 'Fixture'], cwd=root, text=True).strip()
            subprocess.run(['git', 'update-ref', 'HEAD', revision], cwd=root, check=True)
            ten = root / 'manuscript/ch10-ten.md'; ten.write_text('Ten.\n')
            two = root / 'manuscript/ch02-two.md'; two.write_text('<!-- hidden -->\nTwo.\n')
            output = reader.prepare(root, [ten, two])
            data = json.loads((output / 'manifest.json').read_text())
            self.assertEqual([x['file'] for x in data['files']], [two.name, ten.name])
            self.assertEqual(data['revision'], revision)
            self.assertTrue(data['manuscript_dirty'])
            self.assertNotEqual(data['files'][0]['source_sha256'], data['files'][0]['reader_sha256'])
            with self.assertRaises(ValueError):
                reader.prepare(root, [two, two])
            bad = root / 'manuscript/ch03-bad.md'; bad.write_text('<!-- unfinished')
            before = list((root / 'build').iterdir())
            with self.assertRaises(ValueError):
                reader.prepare(root, [two, bad])
            self.assertEqual(list((root / 'build').iterdir()), before)
            with self.assertRaises(ValueError):
                reader.prepare(root, [root / 'decisions.md'])

    def test_reader_preflight_hides_directives_and_reports_hook_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'scripts').mkdir(); (root / '.githooks').mkdir()
            shutil.copy(ROOT / 'scripts/agent-preflight', root / 'scripts/agent-preflight')
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            subprocess.run(['git', 'config', 'core.hooksPath', '.githooks'], cwd=root, check=True)
            for name in ['pre-commit', 'commit-msg']:
                path = root / '.githooks' / name
                path.write_text('#!/bin/sh\nexit 0\n'); path.chmod(0o755)
            # Ignore fixture files so a clean unborn repository can exercise reader mode.
            (root / '.git/info/exclude').write_text('*\n')
            result = subprocess.run(['scripts/agent-preflight', '--reader'], cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn('open TODOs', result.stdout)
            (root / '.githooks/commit-msg').chmod(0o644)
            result = subprocess.run(['scripts/agent-preflight', '--reader'], cwd=root, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('hooks are not ready', result.stdout)


if __name__ == '__main__':
    unittest.main()
