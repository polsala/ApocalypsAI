import unittest
from unittest.mock import patch
import io
import sys

# Import the booster module from the parent directory's src folder
# This assumes the test is run from the 'tests' directory.
sys.path.insert(0, '../src')
import booster
sys.path.pop(0) # Clean up path after import

class TestAIMoraleBooster(unittest.TestCase):

    @patch('random.choice')
    def test_get_morale_boost_deterministic(self, mock_choice):
        # Mock rationale: Ensure the random choice is deterministic for testing.
        # We want to verify that `get_morale_boost` correctly calls `random.choice`
        # and returns its result, regardless of the actual random outcome.
        expected_message = "Test message for deterministic choice."
        mock_choice.return_value = expected_message

        result = booster.get_morale_boost()
        self.assertEqual(result, expected_message)
        mock_choice.assert_called_once_with(booster.MESSAGES)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('booster.get_morale_boost')
    def test_main_output(self, mock_get_morale_boost, mock_stdout):
        # Mock rationale: Capture stdout to verify the printed output
        # and mock `get_morale_boost` to control the message being printed,
        # ensuring the test is deterministic and isolated from random choices.
        expected_message = "Another test message for main output."
        mock_get_morale_boost.return_value = expected_message

        booster.main()

        self.assertEqual(mock_stdout.getvalue(), expected_message + "\n")
        mock_get_morale_boost.assert_called_once()

if __name__ == '__main__':
    unittest.main()
