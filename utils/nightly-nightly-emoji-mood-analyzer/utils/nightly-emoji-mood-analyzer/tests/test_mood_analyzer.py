import unittest
from unittest.mock import mock_open, patch
import os
import sys

# Ensure the src directory is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from mood_analyzer import analyze_mood, main

class TestMoodAnalyzer(unittest.TestCase):
    def test_analyze_mood_basic(self):
        text = "I am happy but also a bit sad. Nothing angry here."
        expected = {
            "😊": 1,  # happy
            "😢": 1,  # sad
            "😠": 1,  # angry
            "😐": 0,  # neutral
        }
        self.assertEqual(analyze_mood(text), expected)

    @patch("builtins.open", new_callable=mock_open, read_data="Okay, fine, meh.")
    def test_cli_neutral(self, m):
        # Mock rationale: simulate a file containing only neutral words.
        test_argv = ["mood_analyzer.py", "dummy.txt"]
        with patch.object(sys, "argv", test_argv):
            with patch("sys.stdout") as mock_stdout:
                exit_code = main()
                self.assertEqual(exit_code, 0)
                # Gather printed output
                printed = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
                self.assertIn("😐: 3", printed)  # okay, fine, meh
                self.assertIn("😊: 0", printed)
                self.assertIn("😢: 0", printed)
                self.assertIn("😠: 0", printed)

if __name__ == "__main__":
    unittest.main()
