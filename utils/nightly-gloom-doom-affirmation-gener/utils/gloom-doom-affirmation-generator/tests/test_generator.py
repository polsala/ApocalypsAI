import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the Python path to allow importing generator.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from generator import get_affirmation, AFFIRMATIONS

class TestGloomDoomAffirmationGenerator(unittest.TestCase):

    def test_get_affirmation_returns_string(self):
        """
        Test that get_affirmation returns a string.
        """
        affirmation = get_affirmation()
        self.assertIsInstance(affirmation, str)
        self.assertGreater(len(affirmation), 0)

    @patch('random.choice')
    def test_get_affirmation_returns_specific_affirmation_when_mocked(self, mock_choice):
        """
        Test that get_affirmation returns a specific affirmation when random.choice is mocked.
        # Mock rationale: random.choice is non-deterministic. Mocking it ensures the test
        # always returns a predictable value, making the test deterministic.
        """
        mock_choice.return_value = "This is a mocked affirmation."
        affirmation = get_affirmation()
        self.assertEqual(affirmation, "This is a mocked affirmation.")
        mock_choice.assert_called_once_with(AFFIRMATIONS)

    def test_get_affirmation_returns_from_list(self):
        """
        Test that the returned affirmation is one of the predefined ones.
        """
        affirmation = get_affirmation()
        self.assertIn(affirmation, AFFIRMATIONS)

    @patch('generator.AFFIRMATIONS', []) # Mock rationale: Test edge case of empty affirmations list.
    def test_get_affirmation_with_empty_list(self):
        """
        Test that get_affirmation handles an empty list of affirmations gracefully.
        # Mock rationale: Temporarily modifying the AFFIRMATIONS list allows testing
        # an edge case without altering the original data or requiring file I/O.
        """
        affirmation = get_affirmation()
        self.assertEqual(affirmation, "No affirmations found. Perhaps the apocalypse got them all.")

    @patch('builtins.print')
    @patch('generator.get_affirmation')
    def test_main_prints_affirmation(self, mock_get_affirmation, mock_print):
        """
        Test that the main function calls get_affirmation and prints its output.
        # Mock rationale: We want to verify that main orchestrates the calls correctly
        # without actually printing to stdout or relying on random choices.
        """
        mock_get_affirmation.return_value = "Mocked affirmation for main."
        from generator import main # Re-import main after patching
        main()
        mock_get_affirmation.assert_called_once()
        mock_print.assert_any_call("✨ Your daily dose of existential dread, served with a side of hope:")
        mock_print.assert_any_call("\"Mocked affirmation for main.\"")

if __name__ == '__main__':
    unittest.main()
