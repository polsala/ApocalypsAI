import unittest
import sys
from unittest.mock import patch
from io import StringIO
from src.analyzer import analyze_commit, generate_summary, main

class TestCelestialCommitAnalyzer(unittest.TestCase):

    def test_analyze_commit_conventional_feat_with_scope(self):
        message = "feat(auth): add user login functionality"
        result = analyze_commit(message)
        self.assertTrue(result["is_conventional"])
        self.assertEqual(result["type"], "feat")
        self.assertEqual(result["scope"], "auth")
        self.assertEqual(result["subject"], "add user login functionality")
        self.assertGreater(result["sentiment_score"], 0)
        self.assertGreaterEqual(result["celestial_alignment_score"], 80) # feat + scope + positive sentiment
        self.assertIn("Conventional Commit structure detected", result["insights"][0])
        self.assertIn("Positive cosmic energy detected", result["insights"][1])

    def test_analyze_commit_conventional_fix_no_scope(self):
        message = "fix: resolve critical bug in payment processing"
        result = analyze_commit(message)
        self.assertTrue(result["is_conventional"])
        self.assertEqual(result["type"], "fix")
        self.assertIsNone(result["scope"])
        self.assertEqual(result["subject"], "resolve critical bug in payment processing")
        self.assertGreater(result["sentiment_score"], 0) # fix, resolve
        self.assertGreaterEqual(result["celestial_alignment_score"], 70) # fix + positive sentiment
        self.assertIn("Conventional Commit structure detected", result["insights"][0])
        self.assertIn("Positive cosmic energy detected", result["insights"][1])

    def test_analyze_commit_non_conventional(self):
        message = "initial commit"
        result = analyze_commit(message)
        self.assertFalse(result["is_conventional"])
        self.assertIsNone(result["type"])
        self.assertIsNone(result["scope"])
        self.assertEqual(result["subject"], "initial commit")
        self.assertEqual(result["sentiment_score"], 0)
        self.assertLess(result["celestial_alignment_score"], 50) # No conventional structure
        self.assertIn("This commit drifts from conventional patterns", result["insights"][0])
        self.assertIn("Neutral cosmic vibrations", result["insights"][1])

    def test_analyze_commit_negative_sentiment(self):
        message = "fix: introduced a critical bug, failed to resolve"
        result = analyze_commit(message)
        self.assertTrue(result["is_conventional"])
        self.assertEqual(result["type"], "fix")
        self.assertLess(result["sentiment_score"], 0) # bug, failed
        self.assertLess(result["celestial_alignment_score"], 50) # fix + negative sentiment
        self.assertIn("A shadow of negativity looms", result["insights"][1])

    def test_analyze_commit_neutral_sentiment(self):
        message = "chore: update dependencies"
        result = analyze_commit(message)
        self.assertTrue(result["is_conventional"])
        self.assertEqual(result["type"], "chore")
        self.assertEqual(result["sentiment_score"], 0)
        self.assertGreaterEqual(result["celestial_alignment_score"], 50) # chore + neutral
        self.assertIn("Neutral cosmic vibrations", result["insights"][1])

    def test_generate_summary_empty(self):
        summary = generate_summary([])
        self.assertIn("No commit messages provided", summary)

    def test_generate_summary_multiple_commits(self):
        results = [
            analyze_commit("feat(api): add new endpoint"),
            analyze_commit("fix: resolve minor UI glitch"),
            analyze_commit("WIP: working on something big") # Non-conventional
        ]
        summary = generate_summary(results)
        self.assertIn("Total of **3** commit messages", summary)
        self.assertIn("Conventional Commits: 2 / 3 (66.7%)", summary)
        self.assertIn("Average Celestial Alignment Score", summary)
        self.assertIn("add new endpoint", summary)
        self.assertIn("resolve minor UI glitch", summary)
        self.assertIn("WIP: working on something big", summary)
        self.assertIn("Conventional Commit structure detected", summary)
        self.assertIn("This commit drifts from conventional patterns", summary)

    @patch('sys.stdin', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_from_stdin(self, mock_stderr, mock_stdout, mock_stdin):
        # Mock rationale: Simulate user input from stdin and capture stdout/stderr.
        mock_stdin.write("feat: implement new feature\nfix(bug): critical issue resolved\n")
        mock_stdin.seek(0) # Rewind the mock stdin to the beginning

        # Mock rationale: Simulate command-line arguments.
        with patch('sys.argv', ['analyzer.py']):
            main()

        output = mock_stdout.getvalue()
        self.assertIn("Celestial Commit Analysis Report", output)
        self.assertIn("Total of **2** commit messages", output)
        self.assertIn("Conventional Commits: 2 / 2 (100.0%)", output)
        self.assertIn("implement new feature", output)
        self.assertIn("critical issue resolved", output)
        self.assertEqual(mock_stderr.getvalue().strip(), "Enter commit messages (one per line). Press Ctrl+D (Unix) or Ctrl+Z then Enter (Windows) to finish:")

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_from_file(self, mock_stderr, mock_stdout, mock_open):
        # Mock rationale: Simulate reading from a file without actually creating one.
        file_content = "chore: update docs\nrefactor: clean up code\n"
        mock_open.return_value.__enter__.return_value.readlines.return_value = file_content.splitlines(keepends=True)

        # Mock rationale: Simulate command-line arguments.
        with patch('sys.argv', ['analyzer.py', 'test_commits.txt']):
            main()

        output = mock_stdout.getvalue()
        self.assertIn("Celestial Commit Analysis Report", output)
        self.assertIn("Total of **2** commit messages", output)
        self.assertIn("Conventional Commits: 2 / 2 (100.0%)", output)
        self.assertIn("update docs", output)
        self.assertIn("clean up code", output)
        mock_open.assert_called_once_with('test_commits.txt', 'r', encoding='utf-8')
        self.assertEqual(mock_stderr.getvalue(), "") # No stderr output for successful file read

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_file_not_found(self, mock_stderr, mock_stdout):
        # Mock rationale: Simulate command-line arguments for a non-existent file.
        with patch('sys.argv', ['analyzer.py', 'non_existent_file.txt']):
            # Mock rationale: sys.exit is called, so we catch SystemExit.
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1) # Expect exit code 1 for error

        self.assertIn("Error: File not found at 'non_existent_file.txt'", mock_stderr.getvalue())
        self.assertEqual(mock_stdout.getvalue(), "")

    @patch('sys.stdin', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_no_messages_provided(self, mock_stderr, mock_stdout, mock_stdin):
        # Mock rationale: Simulate empty stdin input.
        mock_stdin.write("\n\n") # Empty lines
        mock_stdin.seek(0)

        # Mock rationale: Simulate command-line arguments.
        with patch('sys.argv', ['analyzer.py']):
            # Mock rationale: sys.exit is called, so we catch SystemExit.
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 2) # Expect exit code 2 for no-op

        self.assertIn("No commit messages provided.", mock_stderr.getvalue())
        self.assertEqual(mock_stdout.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_help_message(self, mock_stdout):
        # Mock rationale: Simulate --help argument.
        with patch('sys.argv', ['analyzer.py', '--help']):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0) # Expect exit code 0 for help

        output = mock_stdout.getvalue()
        self.assertIn("Usage: python analyzer.py [file_path]", output)
        self.assertIn("Reads commit messages line by line", output)
