import unittest
from unittest.mock import patch
import sys
import os

# Add the src directory to the Python path for importing the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from morale_booster import generate_morale_boost

class TestMoraleBooster(unittest.TestCase):

    @patch('random.choice')
    def test_generate_morale_boost_deterministic(self, mock_choice):
        # Mock rationale: We need to ensure the output is predictable for testing.
        # By mocking random.choice, we can control which elements are selected
        # from the 'starters', 'middles', and 'enders' lists, making the test deterministic.
        mock_choice.side_effect = [
            "Remember, your efforts are", # starter
            "the backbone of progress",   # middle
            "! Keep shining!"             # ender
        ]
        expected_message = "[AI Morale Booster]: \"Remember, your efforts are the backbone of progress ! Keep shining!\""
        self.assertEqual(generate_morale_boost(), expected_message)

    def test_generate_morale_boost_returns_string(self):
        message = generate_morale_boost()
        self.assertIsInstance(message, str)

    def test_generate_morale_boost_starts_with_prefix(self):
        message = generate_morale_boost()
        self.assertTrue(message.startswith("[AI Morale Booster]: \"))

    def test_generate_morale_boost_ends_with_suffix(self):
        message = generate_morale_boost()
        self.assertTrue(message.endswith("\""))

    def test_generate_morale_boost_contains_positive_keywords(self):
        # This test is less deterministic but checks for general positivity.
        # It's a sanity check that the generated messages are indeed positive.
        message = generate_morale_boost().lower()
        positive_keywords = ['progress', 'beacon', 'awesome', 'future', 'essential', 'shining', 'counting', 'spirit', 'brilliance']
        self.assertTrue(any(keyword in message for keyword in positive_keywords))

if __name__ == '__main__':
    unittest.main()
