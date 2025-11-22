import unittest
from unittest.mock import patch
import sys
import io

# Mock rationale: We need to ensure that `random.choice` always returns a predictable
# value for testing purposes, rather than a truly random one. This makes the test
# deterministic and repeatable.
@patch('random.choice')
class TestBooster(unittest.TestCase):

    def setUp(self):
        # Import booster here to ensure mocks are active when it's loaded
        # if it were to be reloaded, but for simple scripts, direct import is fine.
        # We'll just ensure the patch is active for the duration of the test.
        from src import booster
        self.booster = booster
        self.original_stdout = sys.stdout
        sys.stdout = self.mock_stdout = io.StringIO()

    def tearDown(self):
        sys.stdout = self.original_stdout
        del self.booster

    def test_get_random_morale_message(self, mock_random_choice):
        # Mock rationale: Ensure a specific message is chosen to verify the function's output.
        expected_message = "Test Message 1"
        self.booster.MORALE_MESSAGES = [expected_message, "Test Message 2"] # Temporarily override for test
        mock_random_choice.return_value = expected_message

        result = self.booster.get_random_morale_message()
        self.assertEqual(result, expected_message)
        mock_random_choice.assert_called_once_with(self.booster.MORALE_MESSAGES)

    def test_main_prints_message(self, mock_random_choice):
        # Mock rationale: Control the message returned by `get_random_morale_message`
        # to verify that `main` prints the correct formatted output.
        expected_message_content = "A very specific morale boost."
        mock_random_choice.return_value = expected_message_content

        # Temporarily override MORALE_MESSAGES for this test to ensure mock works as expected
        self.booster.MORALE_MESSAGES = [expected_message_content]

        self.booster.main()
        printed_output = self.mock_stdout.getvalue().strip()
        expected_output = f"[MUTANT MORALE BOOSTER] {expected_message_content}"
        self.assertEqual(printed_output, expected_output)
        mock_random_choice.assert_called_once_with(self.booster.MORALE_MESSAGES)

    def test_main_prints_any_message_from_list(self, mock_random_choice):
        # Mock rationale: Verify that `main` can print any message from the original list
        # by iterating through a few and ensuring they are correctly formatted.
        # This also implicitly tests that the `MORALE_MESSAGES` list is accessible.
        test_messages = ["First test message", "Second test message"]
        self.booster.MORALE_MESSAGES = test_messages # Temporarily override for test

        for i, msg in enumerate(test_messages):
            mock_random_choice.return_value = msg
            self.mock_stdout = io.StringIO() # Reset stdout for each iteration
            sys.stdout = self.mock_stdout

            self.booster.main()
            printed_output = self.mock_stdout.getvalue().strip()
            expected_output = f"[MUTANT MORALE BOOSTER] {msg}"
            self.assertEqual(printed_output, expected_output)
            # Ensure random.choice was called with the correct list
            mock_random_choice.assert_called_with(self.booster.MORALE_MESSAGES)
            mock_random_choice.reset_mock() # Reset mock for next iteration

        sys.stdout = self.original_stdout # Restore stdout after loop

if __name__ == '__main__':
    unittest.main()
