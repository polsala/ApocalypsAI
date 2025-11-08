import unittest
import sys
import io
from unittest.mock import patch

# Mock rationale: We need to ensure the test can import the module
# even if it's not in the standard Python path. This is a common pattern
# for self-contained utilities where the test is run from within its own directory.
# We also mock sys.argv, sys.stdout, and sys.stderr for CLI tests to capture output
# and prevent actual program exit.
sys.path.insert(0, 'src')
import emoji_suggester
sys.path.pop(0)

class TestEmojiSuggester(unittest.TestCase):

    def test_feature_commit(self):
        message = "feat: Add new user authentication module"
        expected = ["✨"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_bug_fix_commit(self):
        message = "fix(auth): Resolve critical bug in login flow"
        expected = ["🐛"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_docs_update_commit(self):
        message = "docs: Update README with installation instructions"
        expected = ["📚"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_style_format_commit(self):
        message = "style: Format code with black"
        expected = ["🎨"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_refactor_commit(self):
        message = "refactor: Clean up old utility functions"
        expected = ["♻️"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_test_commit(self):
        message = "test: Add unit tests for new feature"
        expected = ["🧪"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_chore_ci_commit(self):
        message = "chore: Update dependencies and CI config"
        expected = ["⚙️"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_performance_commit(self):
        message = "perf: Optimize database queries"
        expected = ["⚡"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_security_commit(self):
        message = "security: Patch XSS vulnerability"
        expected = ["🔒"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_dependencies_commit(self):
        message = "dep: Upgrade requests library"
        expected = ["📦"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_release_commit(self):
        message = "release: Version 1.0.0"
        expected = ["🚀"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_merge_commit(self):
        message = "Merge branch 'dev' into 'main'"
        expected = ["🔀"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_revert_commit(self):
        message = "revert: Revert previous breaking change"
        expected = ["⏪"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_build_commit(self):
        message = "build: Update Dockerfile for new image"
        expected = ["🏗️"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_remove_commit(self):
        message = "remove: Old unused files"
        expected = ["🗑️"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_update_commit(self):
        message = "update: All packages to latest versions"
        expected = ["⬆️"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_downgrade_commit(self):
        message = "downgrade: Library X due to compatibility issues"
        expected = ["⬇️"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_hotfix_commit(self):
        message = "hotfix: Critical production bug"
        expected = ["🚑"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_wip_commit(self):
        message = "wip: Feature X in progress"
        expected = ["🚧"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_initial_commit(self):
        message = "initial commit"
        expected = ["🎉"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_breaking_change_commit(self):
        message = "breaking: API changes require client updates"
        expected = ["💥"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_multiple_emojis(self):
        message = "chore: Update dependencies and refactor old code"
        # Expected order is sorted based on the emoji character itself
        expected = ["⚙️", "♻️"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_no_match(self):
        message = "A very generic commit message with no keywords"
        expected = []
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_empty_message(self):
        message = ""
        expected = []
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_case_insensitivity(self):
        message = "FIX: Typo in variable name"
        expected = ["🐛"]
        self.assertEqual(emoji_suggester.suggest_emojis(message), expected)

    def test_cli_output_single(self):
        # Mock rationale: sys.argv is mocked to simulate command-line arguments.
        # sys.stdout is mocked to capture the printed output.
        with patch('sys.argv', ['emoji_suggester.py', 'feat: Implement user profiles']),
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            emoji_suggester.main()
            self.assertEqual(mock_stdout.getvalue().strip(), '✨')

    def test_cli_output_multiple(self):
        # Mock rationale: sys.argv is mocked to simulate command-line arguments.
        # sys.stdout is mocked to capture the printed output.
        with patch('sys.argv', ['emoji_suggester.py', 'chore: Update deps and refactor']),
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            emoji_suggester.main()
            # Emojis are sorted, so ⚙️ comes before ♻️
            self.assertEqual(mock_stdout.getvalue().strip(), '⚙️ ♻️')

    def test_cli_no_args(self):
        # Mock rationale: sys.argv is mocked to simulate no command-line arguments.
        # sys.stderr is mocked to capture the error output.
        # sys.exit is mocked to prevent the program from actually exiting.
        with patch('sys.argv', ['emoji_suggester.py']),
             patch('sys.stderr', new_callable=io.StringIO) as mock_stderr,
             self.assertRaises(SystemExit) as cm:
            emoji_suggester.main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn('Usage:', mock_stderr.getvalue())
