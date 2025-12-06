import unittest
from unittest.mock import patch
import sys
from io import StringIO

# Import the functions and data to be tested
from src.booster import get_random_boost, main, MESSAGES

class TestMoraleBooster(unittest.TestCase):

    @patch('random.choice')
    def test_get_random_boost_returns_message_from_list(self, mock_choice):
        # Mock rationale: We want to ensure that `get_random_boost` always selects
        # a message from the predefined `MESSAGES` list. By mocking `random.choice`,
        # we can control its return value to be a known message from the list,
        # making the test deterministic and independent of actual random selection.
        expected_message = MESSAGES[0] # Pick a specific message from the list for deterministic testing
        mock_choice.return_value = expected_message

        result = get_random_boost()
        self.assertEqual(result, expected_message)
        mock_choice.assert_called_once_with(MESSAGES)

    @patch('random.choice')
    def test_main_prints_boost_message(self, mock_choice):
        # Mock rationale: Similar to the above, we mock `random.choice` to ensure
        # a deterministic output for `main`. Additionally, we capture `sys.stdout`
        # to verify that the `main` function correctly prints the chosen message
        # to the console, without relying on actual console output during testing.
        expected_message = MESSAGES[1] # Pick another specific message for deterministic testing
        mock_choice.return_value = expected_message

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        main()

        # Restore stdout
        sys.stdout = sys.__stdout__

        self.assertIn(f"[Morale Booster Bot]: {expected_message}", captured_output.getvalue())
        mock_choice.assert_called_once_with(MESSAGES)

    def test_messages_list_is_not_empty(self):
        # Ensure there are messages to choose from, otherwise random.choice would fail.
        self.assertGreater(len(MESSAGES), 0)

    def test_messages_are_strings(self):
        # Ensure all messages in the list are strings.
        for message in MESSAGES:
            self.assertIsInstance(message, str)

if __name__ == '__main__':
    unittest.main()
