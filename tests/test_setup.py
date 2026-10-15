"""Exercise setup in disposable repositories, without network access."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'book'
        self.root.mkdir()
        for name in ('scripts', '.githooks', '.skills'):
            shutil.copytree(ROOT / name, self.root / name)
        self.env = dict(os.environ, GIT_CONFIG_GLOBAL='/dev/null',
                        GIT_CONFIG_NOSYSTEM='1', GIT_AUTHOR_NAME='Test Author',
                        GIT_AUTHOR_EMAIL='test@example.com',
                        GIT_COMMITTER_NAME='Test Author',
                        GIT_COMMITTER_EMAIL='test@example.com')

    def run_cmd(self, *args, ok=True, cwd=None):
        result = subprocess.run(args, cwd=cwd or self.root, env=self.env,
                                text=True, capture_output=True)
        if ok:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result.stdout.strip()

    def test_fresh_history_remote_and_repeat_setup(self):
        self.run_cmd('git', 'init', '-q', '-b', 'template')
        self.run_cmd('git', 'add', '.')
        self.run_cmd('git', 'commit', '-qm', 'Old template history')
        self.run_cmd('git', 'remote', 'add', 'origin', '/old-template.git')
        self.run_cmd('bash', 'scripts/setup.sh', '--new-book', '--quiet', '--remote', '/new-book.git')
        head = self.run_cmd('git', 'rev-parse', 'HEAD')
        self.assertEqual(self.run_cmd('git', 'rev-list', '--count', 'HEAD'), '1')
        self.assertEqual(self.run_cmd('git', 'branch', '--show-current'), 'main')
        self.assertEqual(self.run_cmd('git', 'remote', 'get-url', 'origin'), '/new-book.git')
        self.assertEqual(self.run_cmd('git', 'config', 'core.hooksPath'), '.githooks')
        self.assertTrue((self.root / '.agents/skills').is_dir())
        self.run_cmd('bash', 'scripts/setup.sh', '--remote', '/new-book.git')
        self.assertEqual(self.run_cmd('git', 'rev-parse', 'HEAD'), head)
        self.run_cmd('bash', 'scripts/setup.sh', '--remote', '/other.git', ok=False)
        self.assertEqual(self.run_cmd('git', 'remote', 'get-url', 'origin'), '/new-book.git')

    def test_invalid_arguments_do_not_initialize_git(self):
        for args in (('--remote',), ('--remote', '--quiet'), ('--unknown',)):
            self.run_cmd('bash', 'scripts/setup.sh', *args, ok=False)
            self.assertFalse((self.root / '.git').exists())

    def test_setup_in_linked_worktree(self):
        self.run_cmd('bash', 'scripts/setup.sh')
        linked = Path(self.temp.name) / 'linked'
        self.run_cmd('git', 'worktree', 'add', '-qb', 'linked', str(linked))
        head = self.run_cmd('git', 'rev-parse', 'HEAD')
        self.run_cmd('bash', 'scripts/setup.sh', cwd=linked)
        self.assertTrue((linked / '.git').is_file())
        self.assertEqual(self.run_cmd('git', 'rev-parse', 'HEAD', cwd=linked), head)

    def test_new_book_refuses_dirty_tree(self):
        self.run_cmd('bash', 'scripts/setup.sh')
        head = self.run_cmd('git', 'rev-parse', 'HEAD')
        (self.root / 'notes.md').write_text('Keep my notes')
        self.run_cmd('bash', 'scripts/setup.sh', '--new-book', ok=False)
        self.assertEqual(self.run_cmd('git', 'rev-parse', 'HEAD'), head)
        self.assertEqual((self.root / 'notes.md').read_text(), 'Keep my notes')

    def test_new_book_refuses_linked_worktrees(self):
        self.run_cmd('bash', 'scripts/setup.sh')
        linked = Path(self.temp.name) / 'linked'
        self.run_cmd('git', 'worktree', 'add', '-qb', 'linked', str(linked))
        self.run_cmd('bash', 'scripts/setup.sh', '--new-book', cwd=linked, ok=False)
        self.run_cmd('bash', 'scripts/setup.sh', '--new-book', ok=False)
        self.run_cmd('git', 'rev-parse', 'HEAD', cwd=linked)
