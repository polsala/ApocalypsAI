import io
import json
import sys
import unittest
from unittest import mock

# Mock rationale: we avoid filesystem I/O by patching Path.read_text to return a controlled string.
# This keeps the test deterministic and offline.

from src.emoji_stats import count_emojis, main

class TestEmojiStats(unittest.TestCase):
    def test_count_emojis_basic(self):
        text = "Hello 😀😀 world 🚀! ❤️❤️❤️"
        expected = {"😀": 2, "❤️": 3, "🚀": 1}
        self.assertEqual(count_emojis(text), expected)

    def test_count_emojis_no_emoji(self):
        self.assertEqual(count_emojis("Just plain text."), {})

    @mock.patch('src.emoji_stats.Path')
    def test_cli_success(self, mock_path_cls):
        # Mock rationale: simulate a file containing known emojis.
        mock_path = mock.Mock()
        mock_path.read_text.return_value = "👍👍👍👍"
        mock_path_cls.return_value = mock_path

        with mock.patch('sys.argv', ['emoji_stats.py', 'dummy.txt']):
            with mock.patch('builtins.print') as mock_print:
                exit_code = main()
                self.assertEqual(exit_code, 0)
                mock_print.assert_called_once()
                printed = mock_print.call_args[0][0]
                self.assertEqual(json.loads(printed), {"👍": 4})

    @mock.patch('src.emoji_stats.Path')
    def test_cli_file_error(self, mock_path_cls):
        # Mock rationale: force an IOError when reading the file.
        mock_path = mock.Mock()
        mock_path.read_text.side_effect = IOError("cannot read")
        mock_path_cls.return_value = mock_path

        with mock.patch('sys.argv', ['emoji_stats.py', 'missing.txt']):
            with mock.patch('builtins.print') as mock_print:
                exit_code = main()
                self.assertEqual(exit_code, 1)
                # Ensure error message was printed to stderr
                mock_print.assert_called()
                args, kwargs = mock_print.call_args
                self.assertIn('Error reading file', args[0])
                self.assertEqual(kwargs.get('file'), sys.stderr)

if __name__ == '__main__':
    unittest.main()
