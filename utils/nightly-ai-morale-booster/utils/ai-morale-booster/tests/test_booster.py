import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Add the src directory to the Python path to allow importing booster.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from booster import get_morale_message, MESSAGES, main

class TestAIMoraleBooster(unittest.TestCase):

    @patch('random.choice')
    def test_get_morale_message_general(self, mock_choice):
        # Mock rationale: random.choice is non-deterministic.
        # We need to control its output to ensure our test is predictable.
        expected_message = MESSAGES["general"][0]
        mock_choice.return_value = expected_message

        message = get_morale_message("general")
        self.assertEqual(message, expected_message)
        mock_choice.assert_called_once_with(MESSAGES["general"])

    @patch('random.choice')
    def test_get_morale_message_humor(self, mock_choice):
        # Mock rationale: random.choice is non-deterministic.
        # We need to control its output to ensure our test is predictable.
        expected_message = MESSAGES["humor"][1]
        mock_choice.return_value = expected_message

        message = get_morale_message("humor")
        self.assertEqual(message, expected_message)
        mock_choice.assert_called_once_with(MESSAGES["humor"])

    @patch('random.choice')
    def test_get_morale_message_invalid_category_defaults_to_general(self, mock_choice):
        # Mock rationale: random.choice is non-deterministic.
        # We need to control its output to ensure our test is predictable.
        expected_message = MESSAGES["general"][2]
        mock_choice.return_value = expected_message

        message = get_morale_message("non_existent_category")
        self.assertEqual(message, expected_message)
        mock_choice.assert_called_once_with(MESSAGES["general"]) # Should default to general

    def test_all_messages_are_strings(self):
        for category in MESSAGES:
            for message in MESSAGES[category]:
                self.assertIsInstance(message, str)
                self.assertGreater(len(message), 0) # Ensure messages are not empty

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('booster.get_morale_message')
    def test_main_function_default_category(self, mock_get_message, mock_parse_args, mock_stdout):
        # Mock rationale:
        # 1. sys.stdout: We want to capture what main() prints to stdout without affecting the console.
        # 2. argparse.ArgumentParser.parse_args: We want to control the arguments passed to main()
        #    without actually parsing command-line arguments.
        # 3. booster.get_morale_message: We want to isolate the main() function's behavior
        #    and ensure it calls get_morale_message with the correct arguments and prints its return value.
        mock_parse_args.return_value = MagicMock(category="general")
        mock_get_message.return_value = "Test General Message"

        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Test General Message")
        mock_get_message.assert_called_once_with("general")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('booster.get_morale_message')
    def test_main_function_specific_category(self, mock_get_message, mock_parse_args, mock_stdout):
        # Mock rationale: Same as above, but for a specific category.
        mock_parse_args.return_value = MagicMock(category="affirmation")
        mock_get_message.return_value = "Test Affirmation Message"

        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Test Affirmation Message")
        mock_get_message.assert_called_once_with("affirmation")

if __name__ == '__main__':
    unittest.main()
