import unittest
from unittest.mock import patch
from src.main import suggest_emoji, main


class TestEmojiCommitHelper(unittest.TestCase):
    def test_keyword_mapping(self):
        self.assertEqual(suggest_emoji("Fix bug in parser"), "🐛")
        self.assertEqual(suggest_emoji("Add new feature for API"), "✨")
        self.assertEqual(suggest_emoji("Update docs for README"), "📚")
        self.assertEqual(suggest_emoji("Refactor authentication module"), "🔧")
        self.assertEqual(suggest_emoji("Write tests for edge cases"), "✅")
        self.assertEqual(suggest_emoji("Improve performance of query"), "🚀")
        self.assertEqual(suggest_emoji("Chore: clean up lint warnings"), "🧹")
        self.assertEqual(suggest_emoji("Random commit without keyword"), "🤖")

    @patch('sys.argv', ['main.py', 'Add', 'new', 'feature'])
    def test_cli_output(self):
        # Mock rationale: simulate command line arguments without actual CLI call
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_called_once_with('✨ Add new feature')


if __name__ == '__main__':
    unittest.main()
