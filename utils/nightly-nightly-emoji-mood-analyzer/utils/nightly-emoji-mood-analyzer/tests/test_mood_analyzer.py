import unittest
import sys
import pathlib
from unittest.mock import mock_open, patch

# Adjust sys.path so that the src module can be imported when tests are run from the
# utils/nightly-emoji-mood-analyzer directory.
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

# Mock rationale: simulate file content without disk I/O
from mood_analyzer import analyze_mood, load_text_from_path


class TestMoodAnalyzer(unittest.TestCase):
    def test_positive_mood(self):
        text = "I am feeling happy and wonderful today!"
        self.assertEqual(analyze_mood(text), "😊")

    def test_negative_mood(self):
        text = "It was a terrible, awful day."
        self.assertEqual(analyze_mood(text), "😞")

    def test_neutral_mood(self):
        text = "The day was okay, nothing special."
        self.assertEqual(analyze_mood(text), "😐")

    def test_load_text_from_path(self):
        mock_content = "I love this good moment."
        m = mock_open(read_data=mock_content)
        with patch("builtins.open", m):
            result = load_text_from_path("dummy.txt")
        self.assertEqual(result, mock_content)

    def test_integration_file_based(self):
        # Mock file containing mixed sentiment
        mock_content = "I love the food but the service was terrible."
        m = mock_open(read_data=mock_content)
        with patch("builtins.open", m):
            text = load_text_from_path("journal.txt")
        self.assertEqual(analyze_mood(text), "😐")


if __name__ == "__main__":
    unittest.main()
