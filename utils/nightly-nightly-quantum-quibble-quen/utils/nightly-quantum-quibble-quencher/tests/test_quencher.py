import unittest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO
from src.quencher import quench_quibble, main

class TestQuencher(unittest.TestCase):

    @patch('random.choice')
    def test_quench_quibble_single_option(self, mock_choice):
        # Mock rationale: random.choice is non-deterministic. We need to control its output
        # to ensure our test always gets the expected result.
        options = ["Eat the last cookie"]
        mock_choice.return_value = "Eat the last cookie"
        result = quench_quibble(options)
        self.assertEqual(result, "Eat the last cookie")
        mock_choice.assert_called_once_with(options)

    @patch('random.choice')
    def test_quench_quibble_multiple_options(self, mock_choice):
        # Mock rationale: Same as above, ensure deterministic output from random.choice.
        options = ["Go left", "Go right", "Stay put"]
        mock_choice.return_value = "Go right"
        result = quench_quibble(options)
        self.assertEqual(result, "Go right")
        mock_choice.assert_called_once_with(options)

    def test_quench_quibble_empty_options(self):
        # This scenario is primarily for direct function calls, as argparse prevents empty lists from CLI.
        with self.assertRaises(ValueError) as cm:
            quench_quibble([])
        self.assertEqual(str(cm.exception), "Options list cannot be empty.")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.quencher.quench_quibble')
    def test_main_success(self, mock_quench, mock_parse_args, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale:
        # - sys.stdout/stderr: Capture print output for assertion.
        # - sys.exit: Prevent actual program exit during test.
        # - argparse.ArgumentParser.parse_args: Control CLI arguments passed to main.
        # - src.quencher.quench_quibble: Isolate main's logic from quench_quibble's implementation.
        mock_args = MagicMock()
        mock_args.options = ["Option A", "Option B"]
        mock_parse_args.return_value = mock_args
        mock_quench.return_value = "Option A"

        main()

        self.assertIn("The chosen path is: 'Option A'", mock_stdout.getvalue())
        mock_quench.assert_called_once_with(["Option A", "Option B"])
        mock_exit.assert_called_once_with(0)
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.quencher.quench_quibble')
    def test_main_error_from_quench_quibble(self, mock_quench, mock_parse_args, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: Same as test_main_success, but for error handling when quench_quibble raises ValueError.
        mock_args = MagicMock()
        # Simulate a scenario where quench_quibble might receive an empty list programmatically,
        # even though argparse's `nargs='+'` prevents this from the CLI directly.
        mock_args.options = [] 
        mock_parse_args.return_value = mock_args
        mock_quench.side_effect = ValueError("Options list cannot be empty.")

        main()

        self.assertIn("Error: Options list cannot be empty.", mock_stderr.getvalue())
        mock_quench.assert_called_once_with([])
        mock_exit.assert_called_once_with(1)
        self.assertEqual(mock_stdout.getvalue(), "")
