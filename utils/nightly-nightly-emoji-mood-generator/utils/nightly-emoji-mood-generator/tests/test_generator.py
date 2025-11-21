import unittest
from pathlib import Path
from unittest.mock import patch

# Mock rationale: we avoid filesystem/network access; all inputs are supplied directly.

from src.generator import generate_mood_emoji, score_message, aggregate_score, map_score_to_emoji

class TestEmojiMoodGenerator(unittest.TestCase):
    def test_score_message_positive(self):
        msg = "Add new feature and improve performance"
        self.assertGreater(score_message(msg), 0)

    def test_score_message_negative(self):
        msg = "Fix bug that caused error and break build"
        self.assertLess(score_message(msg), 0)

    def test_aggregate_score_mixed(self):
        msgs = [
            "Add support for X",
            "Fix bug in Y",
            "Refactor module Z",
            "Remove deprecated API",
        ]
        total = aggregate_score(msgs)
        # Expected: +1 (Add) +1 (Refactor) -1 (Fix) -1 (Remove) = 0
        self.assertEqual(total, 0)

    def test_map_score_to_emoji_boundaries(self):
        self.assertEqual(map_score_to_emoji(-6), "😞")
        self.assertEqual(map_score_to_emoji(-5), "🙁")
        self.assertEqual(map_score_to_emoji(-1), "😐")
        self.assertEqual(map_score_to_emoji(0), "😐")
        self.assertEqual(map_score_to_emoji(1), "🙂")
        self.assertEqual(map_score_to_emoji(5), "😄")
        self.assertEqual(map_score_to_emoji(10), "😄")

    @patch('builtins.print')
    def test_cli_integration(self, mock_print):
        # Mock file reading via Path.read_text
        test_content = "Add feature\nFix bug\nRefactor code"
        with patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'read_text', return_value=test_content):
            # Import the module as if executed via CLI
            from src import generator as gen
            # Simulate sys.argv
            with patch('sys.argv', ['generator.py', 'dummy_path']):
                gen.main()
                # The messages yield: +1 (Add) -1 (Fix) +1 (Refactor) = 1 => 🙂
                mock_print.assert_called_once_with('🙂')

if __name__ == '__main__':
    unittest.main()
