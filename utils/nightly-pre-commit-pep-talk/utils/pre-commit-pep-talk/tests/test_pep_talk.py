import unittest
from unittest.mock import patch, MagicMock
import sys
import io
import subprocess

# Add the src directory to the path to allow importing pep_talk
sys.path.insert(0, 'utils/pre-commit-pep-talk/src')
import pep_talk
sys.path.pop(0)

class TestPepTalkGenerator(unittest.TestCase):

    @patch('subprocess.run')
    def test_no_staged_changes(self, mock_subprocess_run):
        # Mock rationale: Simulate 'git diff --cached --numstat' returning no output,
        # indicating an empty staging area.
        mock_subprocess_run.return_value = MagicMock(
            stdout='', stderr='', returncode=0
        )
        num_files, additions, deletions = pep_talk.get_staged_changes_stats()
        self.assertEqual(num_files, 0)
        self.assertEqual(additions, 0)
        self.assertEqual(deletions, 0)
        self.assertIn("quiet tonight", pep_talk.generate_pep_talk(num_files, additions, deletions))

    @patch('subprocess.run')
    def test_small_staged_changes(self, mock_subprocess_run):
        # Mock rationale: Simulate 'git diff --cached --numstat' returning output
        # for a single file with a few lines changed.
        mock_subprocess_run.return_value = MagicMock(
            stdout='2\t1\tfile1.py\n',
            stderr='', returncode=0
        )
        num_files, additions, deletions = pep_talk.get_staged_changes_stats()
        self.assertEqual(num_files, 1)
        self.assertEqual(additions, 2)
        self.assertEqual(deletions, 1)
        self.assertIn("focused effort", pep_talk.generate_pep_talk(num_files, additions, deletions))

    @patch('subprocess.run')
    def test_medium_staged_changes(self, mock_subprocess_run):
        # Mock rationale: Simulate 'git diff --cached --numstat' returning output
        # for multiple files with a moderate number of lines changed.
        mock_subprocess_run.return_value = MagicMock(
            stdout='10\t5\tfileA.js\n5\t3\tfileB.css\n',
            stderr='', returncode=0
        )
        num_files, additions, deletions = pep_talk.get_staged_changes_stats()
        self.assertEqual(num_files, 2)
        self.assertEqual(additions, 15)
        self.assertEqual(deletions, 8)
        self.assertIn("weaving a tapestry", pep_talk.generate_pep_talk(num_files, additions, deletions))

    @patch('subprocess.run')
    def test_large_staged_changes(self, mock_subprocess_run):
        # Mock rationale: Simulate 'git diff --cached --numstat' returning output
        # for many files or a large number of lines changed.
        mock_subprocess_run.return_value = MagicMock(
            stdout='100\t50\tbig_feature.py\n20\t10\trefactor.js\n5\t5\tconfig.yaml\n',
            stderr='', returncode=0
        )
        num_files, additions, deletions = pep_talk.get_staged_changes_stats()
        self.assertEqual(num_files, 3)
        self.assertEqual(additions, 125)
        self.assertEqual(deletions, 65)
        self.assertIn("architect of digital empires", pep_talk.generate_pep_talk(num_files, additions, deletions))

    @patch('subprocess.run')
    def test_git_command_error(self, mock_subprocess_run):
        # Mock rationale: Simulate 'git diff' command failing (e.g., bad repo, permissions).
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, ['git', 'diff'], stderr='fatal: not a git repository')
        num_files, additions, deletions = pep_talk.get_staged_changes_stats()
        self.assertEqual(num_files, -1)
        self.assertEqual(additions, -1)
        self.assertEqual(deletions, -1)
        self.assertIn("cosmic energies of Git seem... unavailable", pep_talk.generate_pep_talk(num_files, additions, deletions))

    @patch('subprocess.run')
    def test_git_not_found(self, mock_subprocess_run):
        # Mock rationale: Simulate 'git' command not being found in PATH.
        mock_subprocess_run.side_effect = FileNotFoundError()
        num_files, additions, deletions = pep_talk.get_staged_changes_stats()
        self.assertEqual(num_files, -1)
        self.assertEqual(additions, -1)
        self.assertEqual(deletions, -1)
        self.assertIn("cosmic energies of Git seem... unavailable", pep_talk.generate_pep_talk(num_files, additions, deletions))

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('pep_talk.get_staged_changes_stats')
    def test_main_output(self, mock_get_stats, mock_stdout):
        # Mock rationale: Test the main function's output without actually running git.
        # We mock get_staged_changes_stats to control the scenario.
        mock_get_stats.return_value = (1, 5, 2) # Simulate small changes
        pep_talk.main()
        output = mock_stdout.getvalue()
        self.assertIn("✨ ApocalypsAI Pre-Commit Pep Talk ✨", output)
        self.assertIn("focused effort", output)

    @patch('subprocess.run')
    def test_binary_file_changes(self, mock_subprocess_run):
        # Mock rationale: Simulate 'git diff --cached --numstat' returning output
        # that includes binary files, which show '-' for additions/deletions.
        mock_subprocess_run.return_value = MagicMock(
            stdout='10\t5\ttext_file.txt\n-\t-\tbinary_image.png\n',
            stderr='', returncode=0
        )
        num_files, additions, deletions = pep_talk.get_staged_changes_stats()
        # Binary files should still count towards num_files, but not additions/deletions
        self.assertEqual(num_files, 2)
        self.assertEqual(additions, 10)
        self.assertEqual(deletions, 5)
        self.assertIn("weaving a tapestry", pep_talk.generate_pep_talk(num_files, additions, deletions))

    @patch('subprocess.run')
    def test_empty_line_in_numstat(self, mock_subprocess_run):
        # Mock rationale: Simulate 'git diff --cached --numstat' returning output
        # with an empty line, which should be gracefully handled.
        mock_subprocess_run.return_value = MagicMock(
            stdout='1\t1\tfile.txt\n\n2\t2\tfile2.txt\n',
            stderr='', returncode=0
        )
        num_files, additions, deletions = pep_talk.get_staged_changes_stats()
        self.assertEqual(num_files, 2)
        self.assertEqual(additions, 3)
        self.assertEqual(deletions, 3)
        self.assertIn("weaving a tapestry", pep_talk.generate_pep_talk(num_files, additions, deletions))
