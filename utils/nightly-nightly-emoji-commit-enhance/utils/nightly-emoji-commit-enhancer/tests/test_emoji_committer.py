import unittest
from unittest import mock
from utils.nightly_emoji_commit_enhancer.src import emoji_committer

class TestEmojiCommitEnhancer(unittest.TestCase):
    def test_add_emoji_feat(self):
        msg = "Add new authentication flow"
        expected = "✨ Add new authentication flow"
        self.assertEqual(emoji_committer.add_emoji(msg), expected)

    def test_add_emoji_fix(self):
        msg = "Fix bug in parser"
        expected = "🐛 Fix bug in parser"
        self.assertEqual(emoji_committer.add_emoji(msg), expected)

    def test_add_emoji_docs(self):
        msg = "Update README documentation"
        expected = "📝 Update README documentation"
        self.assertEqual(emoji_committer.add_emoji(msg), expected)

    def test_default_emoji(self):
        msg = "Reorganize project structure"
        expected = "🔧 Reorganize project structure"
        self.assertEqual(emoji_committer.add_emoji(msg), expected)

    def test_already_emoji(self):
        msg = "✨ Add sparkle"
        # Should not double‑prefix
        self.assertEqual(emoji_committer.add_emoji(msg), msg)

    def test_cli_with_argument(self):
        test_msg = "Refactor module layout"
        expected = "🔨 Refactor module layout"
        with mock.patch('sys.argv', ['emoji_committer.py', test_msg]):
            with mock.patch('builtins.print') as mock_print:
                emoji_committer.main()
                mock_print.assert_called_once_with(expected)

    def test_cli_stdin(self):
        test_msg = "Improve performance of query engine"
        expected = "⚡ Improve performance of query engine"
        with mock.patch('sys.argv', ['emoji_committer.py']):
            with mock.patch('sys.stdin', mock.Mock(read=mock.Mock(return_value=test_msg))):
                with mock.patch('builtins.print') as mock_print:
                    emoji_committer.main()
                    mock_print.assert_called_once_with(expected)

# Mock rationale: All external interactions (stdin, argv, print) are mocked to keep tests deterministic and offline.

if __name__ == '__main__':
    unittest.main()
