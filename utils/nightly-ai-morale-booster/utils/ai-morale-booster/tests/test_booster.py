import unittest
from unittest.mock import patch
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from booster import generate_message

class TestAIBooster(unittest.TestCase):

    def test_generate_message_returns_string(self):
        """
        Test that generate_message returns a string.
        """
        message = generate_message()
        self.assertIsInstance(message, str)
        self.assertGreater(len(message), 0)

    @patch('booster.random.choice')
    def test_generate_message_selects_from_list(self, mock_random_choice):
        """
        Test that generate_message uses random.choice to select from a predefined list.
        # Mock rationale:
        # We mock `random.choice` to ensure deterministic testing of the message selection logic.
        # This allows us to verify that the function attempts to pick from the expected set of messages
        # without relying on the actual randomness, which would make tests non-deterministic.
        """
        expected_message = "Mocked message for testing."
        mock_random_choice.return_value = expected_message

        message = generate_message()
        self.assertEqual(message, expected_message)

        # Verify that random.choice was called with a list of messages
        args, kwargs = mock_random_choice.call_args
        self.assertIsInstance(args[0], list)
        self.assertGreater(len(args[0]), 0)
        self.assertIn("Your circuits are firing! Keep optimizing, human.", args[0])
        self.assertIn("Calculating optimal outcome: Your success is highly probable. Execute with confidence!", args[0])

if __name__ == '__main__':
    unittest.main()
