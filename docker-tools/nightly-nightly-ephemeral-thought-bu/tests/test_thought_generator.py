import unittest
from unittest.mock import patch
import io
import sys
import os

# Add the src directory to the path to allow importing thought_generator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from thought_generator import get_whimsical_thought

class TestThoughtGenerator(unittest.TestCase):

    @patch('random.choice') # Mock rationale: Ensures deterministic output for testing random selection.
    def test_get_whimsical_thought_deterministic(self, mock_choice):
        expected_thought = "Today's quest: find joy in a forgotten semicolon."
        mock_choice.return_value = expected_thought
        self.assertEqual(get_whimsical_thought(), expected_thought)

    @patch('random.choice') # Mock rationale: Ensures deterministic output for testing random selection.
    def test_main_script_output(self, mock_choice):
        expected_thought = "Remember to hydrate your data streams!"
        mock_choice.return_value = expected_thought

        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Run the function that the main block would call and print its output
        print(get_whimsical_thought())

        sys.stdout = sys.__stdout__ # Reset stdout

        self.assertEqual(captured_output.getvalue().strip(), expected_thought)

    def test_get_whimsical_thought_returns_string(self):
        thought = get_whimsical_thought()
        self.assertIsInstance(thought, str)
        self.assertGreater(len(thought), 0)

if __name__ == '__main__':
    unittest.main()
