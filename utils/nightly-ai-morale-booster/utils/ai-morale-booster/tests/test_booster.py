import unittest
import random
import sys
import os
from unittest.mock import patch, MagicMock

# Mock rationale: This is necessary to make the module importable when running tests
# from the 'tests' directory, ensuring the test environment can locate the source code.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from booster import generate_message, MESSAGES, CONTEXT_MESSAGES, main

class TestAIMoraleBooster(unittest.TestCase):

    @patch('random.choice')
    def test_generate_message_no_context(self, mock_choice):
        # Mock rationale: We need to ensure that the `random.choice` function
        # returns predictable results for testing purposes, rather than actual random choices.
        # This makes tests deterministic and repeatable.
        mock_choice.return_value = MESSAGES[0]
        message = generate_message()
        self.assertEqual(message, MESSAGES[0])
        mock_choice.assert_called_once_with(MESSAGES)

    @patch('random.choice')
    def test_generate_message_with_known_context(self, mock_choice):
        context = "pr_merged"
        # Mock rationale: Ensure random.choice returns a specific message from CONTEXT_MESSAGES[context].
        mock_choice.return_value = CONTEXT_MESSAGES[context][0]
        message = generate_message(context)
        self.assertEqual(message, CONTEXT_MESSAGES[context][0])
        mock_choice.assert_called_once_with(CONTEXT_MESSAGES[context])

    @patch('random.choice')
    def test_generate_message_with_unknown_context_falls_back_to_general(self, mock_choice):
        context = "unknown_event"
        # Mock rationale: Ensure random.choice falls back to MESSAGES when context is unknown.
        mock_choice.return_value = MESSAGES[1]
        message = generate_message(context)
        self.assertEqual(message, MESSAGES[1])
        mock_choice.assert_called_once_with(MESSAGES)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('random.choice')
    def test_main_script_output_no_context(self, mock_choice, mock_parse_args, mock_stdout):
        # Mock rationale: Ensure random.choice returns a specific message for CLI test.
        mock_choice.return_value = MESSAGES[2]
        # Mock rationale: Simulate command-line arguments without actually parsing sys.argv.
        mock_parse_args.return_value = MagicMock(context=None)

        main() # Call the main function directly

        # Mock rationale: We need to capture the output printed to stdout by the main script
        # to verify that the correct message is being displayed without actual console interaction.
        mock_stdout.write.assert_called_once_with(MESSAGES[2] + '\n')

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('random.choice')
    def test_main_script_output_with_context(self, mock_choice, mock_parse_args, mock_stdout):
        context = "new_utility"
        # Mock rationale: Ensure random.choice returns a specific message for CLI test with context.
        mock_choice.return_value = CONTEXT_MESSAGES[context][0]
        # Mock rationale: Simulate command-line arguments for a specific context.
        mock_parse_args.return_value = MagicMock(context=context)

        main() # Call the main function directly

        mock_stdout.write.assert_called_once_with(CONTEXT_MESSAGES[context][0] + '\n')

if __name__ == '__main__':
    unittest.main()
