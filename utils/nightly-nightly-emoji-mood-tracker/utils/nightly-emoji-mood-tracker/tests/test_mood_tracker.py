import unittest
from unittest import mock
from pathlib import Path

# Mock rationale: All file I/O is mocked so the tests run offline and deterministically.

from src.mood_tracker import load_entries, summarize, format_summary


class TestMoodTracker(unittest.TestCase):
    SAMPLE_LOG = """\
2025-11-20 happy
2025-11-21 sad
2025-11-22 happy
2025-11-23 neutral
"""

    @mock.patch("pathlib.Path.open")
    def test_load_entries(self, mock_open):
        # Mock the file handle to iterate over SAMPLE_LOG lines
        mock_file = mock.mock_open(read_data=self.SAMPLE_LOG).return_value
        mock_file.__iter__.return_value = self.SAMPLE_LOG.splitlines(True)
        mock_open.return_value = mock_file

        entries = load_entries("dummy/path.log")
        expected = [
            ("2025-11-20", "happy"),
            ("2025-11-21", "sad"),
            ("2025-11-22", "happy"),
            ("2025-11-23", "neutral"),
        ]
        self.assertEqual(entries, expected)

    def test_summarize(self):
        entries = [
            ("2025-11-20", "happy"),
            ("2025-11-21", "sad"),
            ("2025-11-22", "happy"),
            ("2025-11-23", "neutral"),
        ]
        summary = summarize(entries)
        self.assertEqual(summary["total"], 4)
        self.assertDictEqual(summary["counts"], {"happy": 2, "sad": 1, "neutral": 1})
        self.assertEqual(summary["most_common"], ("happy", "😄", 2))

    def test_format_summary(self):
        summary = {
            "total": 4,
            "counts": {"happy": 2, "sad": 1, "neutral": 1},
            "most_common": ("happy", "😄", 2),
        }
        output = format_summary(summary)
        expected_lines = [
            "Total entries: 4",
            "happy   😄 : 2",
            "sad     😢 : 1",
            "angry   😠 : 0",
            "neutral 😐 : 1",
            "Most common mood: 😄 (happy)",
        ]
        self.assertEqual(output.splitlines(), expected_lines)

    @mock.patch("src.mood_tracker.load_entries")
    @mock.patch("builtins.print")
    def test_cli_success(self, mock_print, mock_load):
        # Mock load_entries to return a known list
        mock_load.return_value = [
            ("2025-11-20", "happy"),
            ("2025-11-21", "sad"),
        ]
        from src.mood_tracker import main
        exit_code = main(["--file", "dummy.log"])
        self.assertEqual(exit_code, 0)
        # Ensure print was called at least once (the summary output)
        self.assertTrue(mock_print.called)

    @mock.patch("src.mood_tracker.load_entries", side_effect=Exception("boom"))
    @mock.patch("builtins.print")
    def test_cli_failure(self, mock_print, _):
        from src.mood_tracker import main
        exit_code = main(["--file", "dummy.log"])
        self.assertEqual(exit_code, 1)
        mock_print.assert_called_with("Error: boom", file=mock.ANY)


if __name__ == "__main__":
    unittest.main()
