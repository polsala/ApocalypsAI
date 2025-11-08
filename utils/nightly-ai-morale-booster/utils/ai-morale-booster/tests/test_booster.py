import unittest
from unittest.mock import patch
import sys
import os

# Add the src directory to the Python path to allow importing booster.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))))

from booster import get_morale_message, MESSAGES

class TestAIMoraleBooster(unittest.TestCase):

    @patch('random.choice')
    def test_get_morale_message_returns_expected_message(self, mock_choice):
        # Mock rationale: random.choice is non-deterministic. Mocking it ensures
        # that our test always receives a predictable message, making the test deterministic.
        expected_message = "Test message for deterministic output."
        mock_choice.return_value = expected_message

        message = get_morale_message()
        self.assertEqual(message, expected_message)
        mock_choice.assert_called_once_with(MESSAGES)

    def test_get_morale_message_returns_string(self):
        message = get_morale_message()
        self.assertIsInstance(message, str)

    def test_messages_list_is_not_empty(self):
        self.assertGreater(len(MESSAGES), 0)

    def test_all_messages_are_strings(self):
        for message in MESSAGES:
            self.assertIsInstance(message, str)
