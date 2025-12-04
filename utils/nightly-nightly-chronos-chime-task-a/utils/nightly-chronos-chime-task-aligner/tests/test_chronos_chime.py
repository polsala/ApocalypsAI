import unittest
from unittest.mock import patch, call
import sys
import io
import os
import argparse

# Add the src directory to the path for importing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import chronos_chime

class TestChronosChime(unittest.TestCase):

    @patch('time.sleep')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_single_cycle_no_break(self, mock_stdout, mock_sleep):
        # Mock rationale: time.sleep is mocked to prevent actual delays during testing.
        # sys.stdout is mocked to capture printed output for assertion.
        chronos_chime.run_timer(work_duration_min=1, break_duration_min=0, cycles=1)

        # Check sleep calls
        mock_sleep.assert_called_once_with(1 * 60) # 1 minute work

        # Check output
        output = mock_stdout.getvalue()
        self.assertIn("Starting Chronos-Chime Task Aligner for 1 cycles.", output)
        self.assertIn("🔔 Chronos-Chime: Cycle 1/1: Time to FOCUS! (1.0 min) 🔔", output)
        self.assertIn("🔔 Chronos-Chime: Cycle 1/1: Work session complete! 🔔", output)
        self.assertIn("🔔 Chronos-Chime: All cycles complete! Excellent alignment! 🔔", output)
        self.assertNotIn("Time for a RECHARGE", output) # No break for 0 min break

    @patch('time.sleep')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_multiple_cycles_with_breaks(self, mock_stdout, mock_sleep):
        # Mock rationale: time.sleep is mocked to prevent actual delays during testing.
        # sys.stdout is mocked to capture printed output for assertion.
        chronos_chime.run_timer(work_duration_min=1, break_duration_min=0.5, cycles=2)

        # Check sleep calls
        expected_sleep_calls = [
            call(1 * 60),   # Work 1
            call(0.5 * 60), # Break 1
            call(1 * 60),   # Work 2
        ]
        mock_sleep.assert_has_calls(expected_sleep_calls, any_order=False)
        self.assertEqual(mock_sleep.call_count, 3)

        # Check output
        output = mock_stdout.getvalue()
        self.assertIn("Starting Chronos-Chime Task Aligner for 2 cycles.", output)
        self.assertIn("🔔 Chronos-Chime: Cycle 1/2: Time to FOCUS! (1.0 min) 🔔", output)
        self.assertIn("🔔 Chronos-Chime: Cycle 1/2: Time for a RECHARGE! (0.5 min) 🔔", output)
        self.assertIn("🔔 Chronos-Chime: Cycle 2/2: Time to FOCUS! (1.0 min) 🔔", output)
        self.assertIn("🔔 Chronos-Chime: Cycle 2/2: Work session complete! 🔔", output)
        self.assertIn("🔔 Chronos-Chime: All cycles complete! Excellent alignment! 🔔", output)

    @patch('time.sleep', side_effect=KeyboardInterrupt)
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_keyboard_interrupt_during_work(self, mock_exit, mock_stdout, mock_sleep):
        # Mock rationale: time.sleep is mocked to raise KeyboardInterrupt, simulating user interruption.
        # sys.stdout is mocked to capture printed output for assertion.
        # sys.exit is mocked to prevent the test runner from exiting prematurely.
        chronos_chime.run_timer(work_duration_min=1, break_duration_min=1, cycles=1)

        output = mock_stdout.getvalue()
        self.assertIn("🔔 Chronos-Chime: Alignment interrupted. Until next time, stay aligned! 🔔", output)
        mock_exit.assert_called_once_with(0)

    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(work=0, break=5, cycles=1))
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_invalid_args_work(self, mock_exit, mock_stdout, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to provide specific command-line arguments.
        # sys.stdout is mocked to capture printed output for assertion.
        # sys.exit is mocked to prevent the test runner from exiting prematurely.
        chronos_chime.main()
        output = mock_stdout.getvalue()
        self.assertIn("Error: Work duration and cycles must be positive integers. Break duration must be non-negative.", output)
        mock_exit.assert_called_once_with(1)

    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(work=25, break=-1, cycles=1))
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_invalid_args_break(self, mock_exit, mock_stdout, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to provide specific command-line arguments.
        # sys.stdout is mocked to capture printed output for assertion.
        # sys.exit is mocked to prevent the test runner from exiting prematurely.
        chronos_chime.main()
        output = mock_stdout.getvalue()
        self.assertIn("Error: Work duration and cycles must be positive integers. Break duration must be non-negative.", output)
        mock_exit.assert_called_once_with(1)

    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(work=25, break=5, cycles=0))
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_invalid_args_cycles(self, mock_exit, mock_stdout, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to provide specific command-line arguments.
        # sys.stdout is mocked to capture printed output for assertion.
        # sys.exit is mocked to prevent the test runner from exiting prematurely.
        chronos_chime.main()
        output = mock_stdout.getvalue()
        self.assertIn("Error: Work duration and cycles must be positive integers. Break duration must be non-negative.", output)
        mock_exit.assert_called_once_with(1)

    @patch('time.sleep')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(work=1, break=1, cycles=1))
    def test_main_valid_args(self, mock_parse_args, mock_stdout, mock_sleep):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to provide specific command-line arguments.
        # sys.stdout is mocked to capture printed output for assertion.
        # time.sleep is mocked to prevent actual delays during testing.
        chronos_chime.main()
        output = mock_stdout.getvalue()
        self.assertIn("Starting Chronos-Chime Task Aligner for 1 cycles.", output)
        mock_sleep.assert_called_once_with(1 * 60)
