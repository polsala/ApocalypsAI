import unittest
import sys
from unittest.mock import patch
from io import StringIO
import os

# Mock rationale: We need to test the `analyze_mood` function directly for unit tests.
# For `main`, we need to mock `sys.argv` and `sys.stdin` to simulate command-line
# arguments and piped input without actual user interaction or file I/O.
# We also mock `sys.stdout` to capture printed output for verification.

# Add the src directory to the Python path to allow importing mood_analyzer
# This assumes the test is run from the repository root or the utility's root directory.
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '../src')
sys.path.insert(0, src_path)

from mood_analyzer import analyze_mood, main
sys.path.pop(0)

class TestMoodAnalyzer(unittest.TestCase):

    def test_doom_and_gloom_mood(self):
        self.assertEqual(analyze_mood("All hope is lost, we are doomed!"), "Doom & Gloom")
        self.assertEqual(analyze_mood("The bleak future awaits."), "Doom & Gloom")
        self.assertEqual(analyze_mood("Utter futility in our efforts."), "Doom & Gloom")
        self.assertEqual(analyze_mood("I feel a sense of dread."), "Doom & Gloom")

    def test_prepper_panic_mood(self):
        self.assertEqual(analyze_mood("Time to stockpile supplies."), "Prepper Panic")
        self.assertEqual(analyze_mood("Building a bunker for survival."), "Prepper Panic")
        self.assertEqual(analyze_mood("Rationing is key during collapse."), "Prepper Panic")
        self.assertEqual(analyze_mood("We must prepare for the worst."), "Prepper Panic")

    def test_optimistic_oblivion_mood(self):
        self.assertEqual(analyze_mood("Looking for the bright side of the end."), "Optimistic Oblivion")
        self.assertEqual(analyze_mood("A new beginning is just around the corner."), "Optimistic Oblivion")
        self.assertEqual(analyze_mood("Embrace the adventure!"), "Optimistic Oblivion")
        self.assertEqual(analyze_mood("The dawn of a new era."), "Optimistic Oblivion")

    def test_chill_chaos_mood(self):
        self.assertEqual(analyze_mood("Whatever happens, happens."), "Chill Chaos")
        self.assertEqual(analyze_mood("Just chill and watch the world burn."), "Chill Chaos")
        self.assertEqual(analyze_mood("Accepting the inevitable."), "Chill Chaos")
        self.assertEqual(analyze_mood("Go with the flow."), "Chill Chaos")

    def test_neutral_numbness_mood(self):
        self.assertEqual(analyze_mood("The weather is quite mild today."), "Neutral Numbness")
        self.assertEqual(analyze_mood("Just another routine day."), "Neutral Numbness")
        self.assertEqual(analyze_mood("No specific feelings about anything."), "Neutral Numbness")
        self.assertEqual(analyze_mood(""), "Neutral Numbness") # Empty string
        self.assertEqual(analyze_mood("A cat sat on the mat."), "Neutral Numbness")

    def test_case_insensitivity(self):
        self.assertEqual(analyze_mood("DOOM is upon us!"), "Doom & Gloom")
        self.assertEqual(analyze_mood("Prepare for anything."), "Prepper Panic")
        self.assertEqual(analyze_mood("Hope for the best."), "Optimistic Oblivion")
        self.assertEqual(analyze_mood("Just CHILL."), "Chill Chaos")

    def test_multiple_keywords_priority(self):
        # The current implementation returns the first mood whose keyword is found
        # based on the order of `mood_keywords` dictionary iteration.
        # 'stockpile' (Prepper Panic) is checked before 'adventure' (Optimistic Oblivion).
        self.assertEqual(analyze_mood("I'm stocking up on canned goods, but also feeling a strange sense of adventure."), "Prepper Panic")
        # 'doom' (Doom & Gloom) is checked before 'whatever' (Chill Chaos).
        self.assertEqual(analyze_mood("This is doom, whatever shall we do?"), "Doom & Gloom")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['mood_analyzer.py', 'We are doomed!'])
    def test_main_with_argv(self, mock_stdout):
        # Mock rationale: Simulate command-line argument input.
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Current Apocalypse Mood: Doom & Gloom")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stdin', StringIO('Just another routine day.'))
    @patch('sys.argv', ['mood_analyzer.py'])
    def test_main_with_stdin(self, mock_stdout):
        # Mock rationale: Simulate piped input via stdin.
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Current Apocalypse Mood: Neutral Numbness")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.argv', ['mood_analyzer.py'])
    @patch('sys.stdin', StringIO('')) # Empty stdin
    @patch('sys.exit')
    def test_main_no_input(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: Simulate no input provided, expecting an error message and exit.
        main()
        self.assertIn("Please provide text to analyze.", mock_stdout.getvalue())
        mock_exit.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
