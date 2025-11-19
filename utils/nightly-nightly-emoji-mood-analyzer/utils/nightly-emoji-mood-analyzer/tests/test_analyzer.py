import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

# Import the module under test
from utils.nightly-emoji-mood-analyzer.src.analyzer import replace_emoticons, format_report, main

class TestEmojiMoodAnalyzer(unittest.TestCase):
    def test_replace_emoticons_basic(self):
        input_text = "I am happy :) but also sad :( and surprised :o"
        expected_text = "I am happy 😄 but also sad 😞 and surprised 😲"
        transformed, counts = replace_emoticons(input_text)
        self.assertEqual(transformed, expected_text)
        self.assertEqual(counts, {"happy": 1, "sad": 1, "surprised": 1})

    def test_replace_emoticons_multiple_occurrences(self):
        input_text = ":) :) :-( :D"
        transformed, counts = replace_emoticons(input_text)
        self.assertEqual(transformed, "😄 😄 😞 😁")
        self.assertEqual(counts, {"happy": 3, "sad": 1, "surprised": 0})

    def test_format_report(self):
        counts = {"happy": 2, "sad": 0, "surprised": 1}
        report = format_report(counts)
        expected = "Mood Summary:\n  Happy    : 2\n  Sad      : 0\n  Surprised: 1"
        self.assertEqual(report, expected)

    @patch('builtins.open', new_callable=mock_open, read_data='Hello :)')
    @patch('pathlib.Path.is_file', return_value=True)
    @patch('pathlib.Path.read_text')
    def test_main_success(self, mock_read_text, mock_is_file, mock_file):
        # Mock rationale: we replace file I/O with in‑memory strings to keep the test offline.
        mock_read_text.return_value = 'Good morning :D and good night :('
        with patch('sys.stdout') as mock_stdout:
            exit_code = main(['dummy.txt'])
            self.assertEqual(exit_code, 0)
            # Ensure the transformed text and report were printed (simplified check)
            self.assertTrue(mock_stdout.write.called)

    @patch('pathlib.Path.is_file', return_value=False)
    def test_main_file_not_found(self, mock_is_file):
        with patch('sys.stdout') as mock_stdout:
            exit_code = main(['nonexistent.txt'])
            self.assertEqual(exit_code, 1)
            self.assertTrue(mock_stdout.write.called)

if __name__ == '__main__':
    unittest.main()
