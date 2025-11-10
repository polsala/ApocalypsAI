import unittest
from unittest.mock import patch
import sys
import io

# Mock rationale:
# The booster.py script uses random.choice to select an affirmation.
# To make tests deterministic, we need to mock random.choice to always return
# a predictable value. This ensures that the test output is consistent
# regardless of when or how many times it's run.
# We also mock sys.stdout to capture the printed output for verification.

class TestAIMoraleBooster(unittest.TestCase):

    @patch('random.choice')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_get_affirmation_deterministic(self, mock_stdout, mock_random_choice):
        """
        Test that get_affirmation returns a specific message when random.choice is mocked.
        """
        # Mock rationale: Ensure random.choice returns a fixed value for deterministic testing.
        mock_random_choice.return_value = "Test affirmation for deterministic check."

        from src.booster import get_affirmation, main

        # Test get_affirmation directly
        affirmation = get_affirmation()
        self.assertEqual(affirmation, "Test affirmation for deterministic check.")
        mock_random_choice.assert_called_once() # Ensure it was called

        # Test main function output with the mocked random.choice
        main()
        expected_output = "[AI Morale Booster]\n\"Test affirmation for deterministic check.\"\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('random.choice')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_another_affirmation(self, mock_stdout, mock_random_choice):
        """
        Test with a different mocked affirmation to ensure flexibility.
        """
        # Mock rationale: Verify the system works with different mocked random outputs.
        mock_random_choice.return_value = "Another test message for the AI."

        from src.booster import main

        main()
        expected_output = "[AI Morale Booster]\n\"Another test message for the AI.\"\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        mock_random_choice.assert_called_once()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_prints_message(self, mock_stdout):
        """
        Test that the main function prints a message to stdout.
        This test doesn't mock random.choice, so it will pick a random one.
        It primarily checks that *something* is printed in the correct format.
        """
        from src.booster import main, get_affirmation

        main()
        output = mock_stdout.getvalue()
        self.assertTrue(output.startswith("[AI Morale Booster]\n\""))
        self.assertTrue(output.endswith("\"\n"))
        # Ensure the printed message is one of the actual affirmations
        # (This implicitly tests get_affirmation without mocking its random choice)
        # We can't assert a specific message, but we can check its format and origin.
        # To be more robust, we could re-import and check against the internal list,
        # but for this test, checking format and presence is sufficient.
        # The deterministic tests cover specific content.

if __name__ == '__main__':
    unittest.main()
