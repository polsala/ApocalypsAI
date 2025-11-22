import unittest
from unittest.mock import patch
import sys
import io
from src import quibble_quencher

class TestQuibbleQuencher(unittest.TestCase):

    @patch('random.choice')
    def test_resolve_coin_flip(self, mock_choice):
        # Mock rationale: Ensure deterministic output for random.choice.
        # We want to test specific outcomes without actual randomness.
        mock_choice.return_value = "Heads"
        self.assertEqual(quibble_quencher.resolve_coin_flip(), "Heads")
        mock_choice.assert_called_once_with(["Heads", "Tails"])

        mock_choice.reset_mock() # Reset for next assertion
        mock_choice.return_value = "Tails"
        self.assertEqual(quibble_quencher.resolve_coin_flip(), "Tails")
        mock_choice.assert_called_once_with(["Heads", "Tails"])

    @patch('random.choice')
    def test_resolve_rps(self, mock_choice):
        # Mock rationale: Ensure deterministic output for random.choice.
        # We want to test specific outcomes without actual randomness.
        mock_choice.return_value = "Rock"
        self.assertEqual(quibble_quencher.resolve_rps(), "Rock")
        mock_choice.assert_called_once_with(["Rock", "Paper", "Scissors"])

        mock_choice.reset_mock() # Reset for next assertion
        mock_choice.return_value = "Paper"
        self.assertEqual(quibble_quencher.resolve_rps(), "Paper")
        mock_choice.assert_called_once_with(["Rock", "Paper", "Scissors"])

    @patch('random.choice')
    def test_resolve_choice(self, mock_choice):
        # Mock rationale: Ensure deterministic output for random.choice.
        # We want to test specific outcomes without actual randomness.
        options = ["Option A", "Option B", "Option C"]
        mock_choice.return_value = "Option B"
        self.assertEqual(quibble_quencher.resolve_choice(options), "Option B")
        mock_choice.assert_called_once_with(options)

        mock_choice.reset_mock() # Reset for next test case
        options_single = ["Only Option"]
        mock_choice.return_value = "Only Option"
        self.assertEqual(quibble_quencher.resolve_choice(options_single), "Only Option")
        mock_choice.assert_called_once_with(options_single)

    def test_resolve_choice_no_options(self):
        # Test error handling for empty options list
        with self.assertRaisesRegex(ValueError, "At least one option must be provided"): 
            quibble_quencher.resolve_choice([])

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['quibble_quencher.py', 'coin'])
    @patch('random.choice', return_value="Heads")
    def test_main_coin_flip(self, mock_random_choice, mock_stdout):
        # Mock rationale:
        # - sys.stdout: Capture print output to assert against it.
        # - sys.argv: Simulate command-line arguments for the script.
        # - random.choice: Control the outcome of the coin flip for determinism.
        quibble_quencher.main()
        self.assertIn("Quibble Quenched! Result: Heads", mock_stdout.getvalue())
        mock_random_choice.assert_called_once_with(["Heads", "Tails"])

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['quibble_quencher.py', 'rps'])
    @patch('random.choice', return_value="Scissors")
    def test_main_rps(self, mock_random_choice, mock_stdout):
        # Mock rationale:
        # - sys.stdout: Capture print output to assert against it.
        # - sys.argv: Simulate command-line arguments for the script.
        # - random.choice: Control the outcome of RPS for determinism.
        quibble_quencher.main()
        self.assertIn("Quibble Quenched! Result: Scissors", mock_stdout.getvalue())
        mock_random_choice.assert_called_once_with(["Rock", "Paper", "Scissors"])

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['quibble_quencher.py', 'choose', 'Alpha', 'Beta', 'Gamma'])
    @patch('random.choice', return_value="Beta")
    def test_main_choose(self, mock_random_choice, mock_stdout):
        # Mock rationale:
        # - sys.stdout: Capture print output to assert against it.
        # - sys.argv: Simulate command-line arguments for the script.
        # - random.choice: Control the chosen option for determinism.
        quibble_quencher.main()
        self.assertIn("Quibble Quenched! Result: Beta", mock_stdout.getvalue())
        mock_random_choice.assert_called_once_with(['Alpha', 'Beta', 'Gamma'])

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO) # Capture stderr for error messages
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during test
    @patch('sys.argv', ['quibble_quencher.py', 'choose'])
    def test_main_choose_no_options_error(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale:
        # - sys.stdout/stderr: Capture output.
        # - sys.exit: Prevent the test runner from exiting prematurely.
        # - sys.argv: Simulate command-line arguments.
        quibble_quencher.main()
        self.assertIn("Error: At least one option must be provided for 'choose' mode.", mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['quibble_quencher.py', 'unknown_mode'])
    def test_main_unknown_mode_error(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale:
        # - sys.stdout/stderr: Capture output.
        # - sys.exit: Prevent the test runner from exiting prematurely.
        # - sys.argv: Simulate command-line arguments.
        quibble_quencher.main()
        self.assertIn("Error: Unknown mode 'unknown_mode'", mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['quibble_quencher.py'])
    def test_main_no_args_error(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale:
        # - sys.stdout/stderr: Capture output.
        # - sys.exit: Prevent the test runner from exiting prematurely.
        # - sys.argv: Simulate command-line arguments.
        quibble_quencher.main()
        self.assertIn("Usage: python quibble_quencher.py <mode> [options...]", mock_stdout.getvalue())
        self.assertIn("Modes:", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
