import unittest
from unittest.mock import mock_open, patch
from pathlib import Path
from src.mood_summary import summarize, MOOD_EMOJI

class TestMoodSummary(unittest.TestCase):
    def setUp(self):
        # Mock CSV content
        self.csv_content = "date,mood\n2025-01-01,5\n2025-01-02,3\n2025-01-03,1\n"
        self.expected = MOOD_EMOJI[5] + MOOD_EMOJI[3] + MOOD_EMOJI[1]

    @patch("builtins.open", new_callable=mock_open, read_data="date,mood\n2025-01-01,5\n2025-01-02,3\n2025-01-03,1\n")
    def test_summarize(self, mock_file):
        # Mock Path.open to use our mock file
        with patch.object(Path, "open", mock_file):
            result = summarize("dummy/path.csv")
            self.assertEqual(result, self.expected)

    def test_invalid_mood(self):
        bad_csv = "date,mood\n2025-01-01,6\n"
        with patch("builtins.open", mock_open(read_data=bad_csv)):
            with patch.object(Path, "open", mock_open(read_data=bad_csv)):
                with self.assertRaises(ValueError):
                    summarize("dummy.csv")

    def test_missing_column(self):
        bad_csv = "date,score\n2025-01-01,5\n"
        with patch("builtins.open", mock_open(read_data=bad_csv)):
            with patch.object(Path, "open", mock_open(read_data=bad_csv)):
                with self.assertRaises(KeyError):
                    summarize("dummy.csv")

if __name__ == "__main__":
    unittest.main()
