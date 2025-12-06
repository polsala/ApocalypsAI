import unittest
from unittest.mock import patch
import sys
import os

# Add the src directory to the Python path to allow importing greeter.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from greeter import get_gloom_glimmer_message, GREETINGS, SURVIVAL_TIPS

class TestGreeter(unittest.TestCase):

    @patch('random.choice')
    def test_get_gloom_glimmer_message_deterministic(self, mock_choice):
        # Mock rationale: We need to ensure that random.choice returns predictable values
        # for deterministic testing. This allows us to verify the output format and content
        # without relying on actual randomness.
        mock_choice.side_effect = [GREETINGS[0], SURVIVAL_TIPS[0]]

        expected_message = f"{GREETINGS[0]}\nSurvival Tip: {SURVIVAL_TIPS[0]}"
        self.assertEqual(get_gloom_glimmer_message(), expected_message)
        self.assertEqual(mock_choice.call_count, 2)

    @patch('random.choice')
    def test_get_gloom_glimmer_message_format(self, mock_choice):
        # Mock rationale: Similar to the above, we mock random.choice to control the output
        # and verify that the message always contains a greeting, a newline, and a tip prefix.
        mock_choice.side_effect = [GREETINGS[1], SURVIVAL_TIPS[1]]

        message = get_gloom_glimmer_message()
        self.assertIsInstance(message, str)
        self.assertIn('\nSurvival Tip:', message)
        self.assertTrue(message.startswith(GREETINGS[1]))
        self.assertTrue(message.endswith(SURVIVAL_TIPS[1]))

    def test_greetings_list_not_empty(self):
        self.assertGreater(len(GREETINGS), 0, "GREETINGS list should not be empty")

    def test_survival_tips_list_not_empty(self):
        self.assertGreater(len(SURVIVAL_TIPS), 0, "SURVIVAL_TIPS list should not be empty")

if __name__ == '__main__':
    unittest.main()
