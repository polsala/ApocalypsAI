import unittest
import sys
import io
import random
from unittest.mock import patch
from datetime import datetime

# Assuming nudger.py is in the parent directory for testing purposes
# In a real setup, you might adjust sys.path or use a test runner that handles modules.
# For self-contained utility, we'll assume it's run from its own directory or path is set.
from src.nudger import get_nudge_message, main

class TestNudger(unittest.TestCase):

    def test_get_nudge_message_hydrate(self):
        # Mock rationale: Ensure deterministic output for random.choice.
        # We want to test that a message from the 'hydrate' category is returned.
        with patch('random.choice', return_value="Hydration Protocol Initiated: Remember to refuel your internal reservoirs!"):
            message = get_nudge_message("hydrate")
            self.assertIn("Hydration Protocol Initiated", message)
            self.assertIn("reservoirs", message)

    def test_get_nudge_message_snack(self):
        # Mock rationale: Ensure deterministic output for random.choice.
        with patch('random.choice', return_value="Energy Reserves Low: Seek out a delicious, non-radioactive snack!"):
            message = get_nudge_message("snack")
            self.assertIn("Energy Reserves Low", message)
            self.assertIn("snack", message)

    def test_get_nudge_message_break(self):
        # Mock rationale: Ensure deterministic output for random.choice.
        with patch('random.choice', return_value="System Overload Imminent: Initiate short break protocol!"):
            message = get_nudge_message("break")
            self.assertIn("System Overload Imminent", message)
            self.assertIn("break protocol", message)

    def test_get_nudge_message_random(self):
        # Mock rationale: Ensure deterministic output for random.choice when 'random' category is chosen.
        # We pick a specific message that exists in the combined list.
        with patch('random.choice', return_value="Your organic systems require liquid sustenance. Drink water!"):
            message = get_nudge_message("random")
            self.assertIn("organic systems require liquid sustenance", message)
            self.assertIn("Drink water!", message)

    def test_get_nudge_message_unknown_category(self):
        message = get_nudge_message("unknown_category")
        self.assertIn("Unknown nourishment category", message)
        self.assertIn("'unknown_category'", message)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.nudger.get_nudge_message', return_value="Test Nudge Message")
    @patch('src.nudger.datetime') # Mock rationale: Freeze datetime for deterministic output string.
    def test_main_output(self, mock_datetime, mock_get_nudge, mock_stdout):
        # Mock rationale: Ensure deterministic timestamp for the output.
        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 30, 0)
        mock_datetime.strftime = datetime.strftime # Keep original strftime behavior

        # Mock rationale: Simulate command-line arguments.
        with patch('sys.argv', ['nudger.py', '--category', 'snack']):
            main()
            output = mock_stdout.getvalue().strip()
            self.assertIn("[2023-10-27 10:30:00] Nudge: Test Nudge Message", output)
            mock_get_nudge.assert_called_once_with("snack")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.nudger.get_nudge_message', return_value="Another Test Nudge Message")
    @patch('src.nudger.datetime') # Mock rationale: Freeze datetime for deterministic output string.
    def test_main_output_default_random(self, mock_datetime, mock_get_nudge, mock_stdout):
        # Mock rationale: Ensure deterministic timestamp for the output.
        mock_datetime.now.return_value = datetime(2023, 10, 27, 11, 0, 0)
        mock_datetime.strftime = datetime.strftime # Keep original strftime behavior

        # Mock rationale: Simulate command-line arguments (no category specified, so it defaults to random).
        with patch('sys.argv', ['nudger.py']):
            main()
            output = mock_stdout.getvalue().strip()
            self.assertIn("[2023-10-27 11:00:00] Nudge: Another Test Nudge Message", output)
            mock_get_nudge.assert_called_once_with("random")
