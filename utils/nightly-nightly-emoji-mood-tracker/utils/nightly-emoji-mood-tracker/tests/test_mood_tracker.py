import unittest
from unittest.mock import mock_open, patch
from datetime import datetime

# Import the module under test
from src.mood_tracker import add_entry, summary, DATA_PATH


class TestMoodTracker(unittest.TestCase):
    @patch("src.mood_tracker.Path.home")
    @patch("src.mood_tracker.Path.exists")
    @patch("src.mood_tracker.open", new_callable=mock_open, read_data="{}")
    def test_add_entry_creates_file(self, mock_file, mock_exists, mock_home):
        # Mock rationale: simulate a fresh environment where the data file does not exist yet.
        mock_home.return_value = "/tmp"
        mock_exists.return_value = False
        add_entry("2023-10-01", "😊")
        # Verify that the file was opened for writing at the expected location.
        mock_file.assert_called_with("/tmp/.emoji_mood_tracker.json", "w", encoding="utf-8")
        handle = mock_file()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        self.assertIn('"2023-10-01": "😊"', written_content)

    @patch("src.mood_tracker.Path.home")
    @patch("src.mood_tracker.Path.exists")
    @patch("src.mood_tracker.open", new_callable=mock_open, read_data='{"2023-10-01":"😊","2023-10-02":"😢"}')
    @patch("src.mood_tracker.datetime")
    def test_summary_last_two_days(self, mock_datetime, mock_file, mock_exists, mock_home):
        # Mock rationale: fix today's date to 2023‑10‑02 so the summary window is deterministic.
        mock_home.return_value = "/tmp"
        mock_exists.return_value = True
        mock_datetime.today.return_value = datetime(2023, 10, 2)
        result = summary(2)
        expected = "2023-10-01: 😊\n2023-10-02: 😢"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
