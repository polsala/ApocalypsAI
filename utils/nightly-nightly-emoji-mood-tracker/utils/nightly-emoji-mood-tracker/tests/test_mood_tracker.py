import unittest
import sys
import os
from io import StringIO
from unittest import mock

# Mock rationale: we avoid filesystem/network by feeding StringIO directly.
# Adjust sys.path so the src module can be imported without installing a package.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from mood_tracker import get_mood, process_lines, main


class TestMoodTracker(unittest.TestCase):
    def test_get_mood_positive(self):
        self.assertEqual(get_mood("I am feeling great today!"), "😊")

    def test_get_mood_negative(self):
        self.assertEqual(get_mood("This is the worst day."), "😞")

    def test_get_mood_neutral(self):
        self.assertEqual(get_mood("Just an ordinary sentence."), "😐")

    def test_process_lines(self):
        lines = ["I love pizza\n", "It is bad\n", "Nothing special\n"]
        expected = ["😊 I love pizza", "😞 It is bad", "😐 Nothing special"]
        self.assertEqual(process_lines(lines), expected)

    @mock.patch('sys.argv', ['mood_tracker.py', '--file', '-'])
    @mock.patch('sys.stdin', new=StringIO("I am happy\nI am sad\nNeutral line\n"))
    def test_cli_stdout(self):
        # Mock print to capture CLI output without writing to stdout.
        with mock.patch('builtins.print') as mock_print:
            main()
            mock_print.assert_any_call("😊 I am happy")
            mock_print.assert_any_call("😞 I am sad")
            mock_print.assert_any_call("😐 Neutral line")


if __name__ == "__main__":
    unittest.main()
