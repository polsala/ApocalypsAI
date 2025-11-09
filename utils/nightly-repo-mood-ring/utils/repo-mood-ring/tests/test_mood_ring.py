import unittest
from unittest.mock import patch, MagicMock
import sys
import io
from utils.repo-mood-ring.src import mood_ring

class TestRepoMoodRing(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_git_log_messages_success(self, mock_subprocess_run):
        # Mock rationale: Simulate successful 'git log' command output without actual Git interaction.
        mock_result = MagicMock()
        mock_result.stdout = "feat: Add new feature\nfix: Bug fix\ndocs: Update docs"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_subprocess_run.return_value = mock_result

        messages = mood_ring.get_git_log_messages(3)
        self.assertEqual(messages, ["feat: Add new feature", "fix: Bug fix", "docs: Update docs"])
        mock_subprocess_run.assert_called_once_with(
            ['git', '--no-pager', 'log', '-n3', '--pretty=format:%s'],
            capture_output=True,
            text=True,
            check=True
        )

    @patch('subprocess.run')
    def test_get_git_log_messages_empty(self, mock_subprocess_run):
        # Mock rationale: Simulate 'git log' returning no output (e.g., empty repo).
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_subprocess_run.return_value = mock_result

        messages = mood_ring.get_git_log_messages(1)
        self.assertEqual(messages, ['']) # subprocess.run.stdout.strip().split('\n') on empty string returns ['']

    @patch('subprocess.run')
    def test_get_git_log_messages_error(self, mock_subprocess_run):
        # Mock rationale: Simulate 'git log' failing (e.g., not a git repository).
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, 'git log', stderr='fatal: not a git repository')

        # Capture stderr output
        captured_stderr = io.StringIO()
        sys.stderr = captured_stderr
        messages = mood_ring.get_git_log_messages(1)
        sys.stderr = sys.__stderr__ # Restore stderr

        self.assertEqual(messages, [])
        self.assertIn("Error running git command:", captured_stderr.getvalue())
        self.assertIn("fatal: not a git repository", captured_stderr.getvalue())

    @patch('subprocess.run')
    def test_get_git_log_messages_git_not_found(self, mock_subprocess_run):
        # Mock rationale: Simulate 'git' command not being found in PATH.
        mock_subprocess_run.side_effect = FileNotFoundError

        # Capture stderr output
        captured_stderr = io.StringIO()
        sys.stderr = captured_stderr
        messages = mood_ring.get_git_log_messages(1)
        sys.stderr = sys.__stderr__ # Restore stderr

        self.assertEqual(messages, [])
        self.assertIn("Error: 'git' command not found.", captured_stderr.getvalue())

    def test_analyze_sentiment_positive(self):
        self.assertEqual(mood_ring.analyze_sentiment("feat: Add new user authentication"), 'Positive')
        self.assertEqual(mood_ring.analyze_sentiment("refactor: Improve performance"), 'Positive')
        self.assertEqual(mood_ring.analyze_sentiment("fix: Resolve critical issue"), 'Positive')
        self.assertEqual(mood_ring.analyze_sentiment("docs: Update documentation"), 'Positive') # 'update' is positive

    def test_analyze_sentiment_negative(self):
        self.assertEqual(mood_ring.analyze_sentiment("bug: Critical error found"), 'Negative')
        self.assertEqual(mood_ring.analyze_sentiment("revert: Bad merge"), 'Negative')
        self.assertEqual(mood_ring.analyze_sentiment("security: Vulnerability found"), 'Negative')

    def test_analyze_sentiment_neutral_mixed(self):
        self.assertEqual(mood_ring.analyze_sentiment("Initial commit"), 'Neutral/Mixed') # No strong keywords
        self.assertEqual(mood_ring.analyze_sentiment("Merge branch 'dev' into 'main'"), 'Neutral/Mixed') # No strong keywords
        self.assertEqual(mood_ring.analyze_sentiment("bug: Fix critical error"), 'Neutral/Mixed') # Contains both 'fix' (pos) and 'bug' (neg)
        self.assertEqual(mood_ring.analyze_sentiment("chore: Update dependencies"), 'Neutral/Mixed') # No strong keywords from current list

    @patch('subprocess.run')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_function_default_commits(self, mock_stderr, mock_stdout, mock_subprocess_run):
        # Mock rationale: Simulate 'git log' output and capture stdout/stderr for main function.
        mock_result = MagicMock()
        mock_result.stdout = (
            "feat: Implement new API endpoint\n"
            "fix: Resolve a minor bug\n"
            "docs: Update contributing guidelines\n"
            "bug: Critical error in payment gateway\n"
            "refactor: Clean up old code"
        )
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_subprocess_run.return_value = mock_result

        # Simulate running with no arguments
        with patch.object(sys, 'argv', ['mood_ring.py']):
            mood_ring.main()

        output = mock_stdout.getvalue()
        self.assertIn("Total Commits Analyzed: 5", output)
        self.assertIn("Positive Commits:      3 (60.0%)", output) # feat, fix, refactor
        self.assertIn("Negative Commits:       1 (20.0%)", output) # bug (critical error)
        self.assertIn("Neutral/Mixed Commits:  1 (20.0%)", output) # docs
        self.assertIn("Overall Repo Mood: ✨ Positive ✨", output)
        self.assertIn("- feat: Implement new API endpoint (Positive)", output)
        self.assertIn("- bug: Critical error in payment gateway (Negative)", output)

    @patch('subprocess.run')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_function_custom_commits(self, mock_stderr, mock_stdout, mock_subprocess_run):
        # Mock rationale: Simulate 'git log' output for a specific number of commits.
        mock_result = MagicMock()
        mock_result.stdout = (
            "feat: Add feature X\n"
            "bug: Fix issue Y"
        )
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_subprocess_run.return_value = mock_result

        with patch.object(sys, 'argv', ['mood_ring.py', '2']):
            mood_ring.main()

        output = mock_stdout.getvalue()
        self.assertIn("Total Commits Analyzed: 2", output)
        self.assertIn("Positive Commits:      1 (50.0%)", output) # feat
        self.assertIn("Negative Commits:       1 (50.0%)", output) # bug
        self.assertIn("Overall Repo Mood: ⚖️ Mixed Feelings ⚖️", output) # Equal positive/negative
        mock_subprocess_run.assert_called_once_with(
            ['git', '--no-pager', 'log', '-n2', '--pretty=format:%s'],
            capture_output=True,
            text=True,
            check=True
        )

    @patch('subprocess.run')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_function_invalid_commits_arg(self, mock_stderr, mock_stdout, mock_subprocess_run):
        # Mock rationale: Test handling of invalid command-line arguments for commit count.
        mock_result = MagicMock()
        mock_result.stdout = "feat: Valid commit"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_subprocess_run.return_value = mock_result

        with patch.object(sys, 'argv', ['mood_ring.py', 'abc']):
            mood_ring.main()
        self.assertIn("Invalid number of commits. Using default of 20.", mock_stderr.getvalue())
        mock_subprocess_run.assert_called_once_with(
            ['git', '--no-pager', 'log', '-n20', '--pretty=format:%s'], # Should default to 20
            capture_output=True,
            text=True,
            check=True
        )

    @patch('subprocess.run')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_function_zero_commits_arg(self, mock_stderr, mock_stdout, mock_subprocess_run):
        # Mock rationale: Test handling of zero commit count argument.
        mock_result = MagicMock()
        mock_result.stdout = "feat: Valid commit"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_subprocess_run.return_value = mock_result

        with patch.object(sys, 'argv', ['mood_ring.py', '0']):
            mood_ring.main()
        self.assertIn("Invalid number of commits. Using default of 20.", mock_stderr.getvalue())
        mock_subprocess_run.assert_called_once_with(
            ['git', '--no-pager', 'log', '-n20', '--pretty=format:%s'], # Should default to 20
            capture_output=True,
            text=True,
            check=True
        )

    @patch('subprocess.run')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_function_no_commits_found(self, mock_stderr, mock_stdout, mock_subprocess_run):
        # Mock rationale: Simulate a scenario where git log returns no actual commit messages.
        mock_result = MagicMock()
        mock_result.stdout = "" # Empty string, which becomes [''] after split
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_subprocess_run.return_value = mock_result

        with patch.object(sys, 'argv', ['mood_ring.py']):
            mood_ring.main()
        output = mock_stdout.getvalue()
        self.assertIn("No commit messages found to analyze.", output)
        self.assertEqual(mock_stderr.getvalue(), "")


if __name__ == '__main__':
    unittest.main()
