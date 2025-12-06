import unittest
from unittest.mock import patch
import sys
import io

# Add the src directory to the path for importing the module
sys.path.insert(0, 'src')
from affirmations import get_random_affirmation, AFFIRMATIONS, main
sys.path.pop(0)

class TestAffirmations(unittest.TestCase):

    def test_get_random_affirmation_returns_string(self):
        """Test that get_random_affirmation returns a string."""
        affirmation = get_random_affirmation()
        self.assertIsInstance(affirmation, str)

    @patch('random.choice')
    def test_get_random_affirmation_is_from_list(self, mock_choice):
        """Test that get_random_affirmation returns an item from the predefined list."""
        # Mock rationale: We need to ensure determinism for the test. By mocking random.choice,
        # we can control which affirmation is 'chosen' and verify that the function behaves as expected.
        # This prevents tests from failing due to random selection.
        expected_affirmation = AFFIRMATIONS[0] # Pick the first one for predictable testing
        mock_choice.return_value = expected_affirmation

        affirmation = get_random_affirmation()
        self.assertEqual(affirmation, expected_affirmation)
        mock_choice.assert_called_once_with(AFFIRMATIONS)

    @patch('random.choice')
    def test_main_prints_affirmation(self, mock_choice):
        """Test that the main function prints an affirmation to stdout."""
        # Mock rationale: Similar to the above, we mock random.choice to ensure a predictable output.
        # Additionally, we capture stdout to verify that the main function prints the expected message.
        expected_affirmation = AFFIRMATIONS[1] # Pick another one for variety in testing
        mock_choice.return_value = expected_affirmation

        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            main()
            self.assertIn(f"Today's affirmation: {expected_affirmation}", captured_output.getvalue())
        finally:
            sys.stdout = sys.__stdout__ # Restore stdout

        mock_choice.assert_called_once_with(AFFIRMATIONS)

if __name__ == '__main__':
    unittest.main()
