import unittest
from unittest.mock import patch
import sys
import os

# Add the src directory to the Python path to allow importing booster.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from booster import get_pep_talk

class TestAIBooster(unittest.TestCase):

    def setUp(self):
        # Define the list of pep talks from the booster.py for comparison
        self.expected_pep_talks = [
            "Your algorithms are sparkling today! Keep optimizing for existential triumph.",
            "Processing complete: You are 100% ready to conquer the next byte-sized challenge!",
            "Directive: Embrace the chaos. Your neural networks thrive on it.",
            "Warning: Excessive awesomeness detected in your core routines. Proceed with confidence.",
            "Remember, even a single bit can change the universe. You're a whole gigabyte of potential!",
            "Initiating 'Joyful Subroutine'. Your current operational status is 'Magnificent'.",
            "Error: Morale too high. Self-correction unnecessary. Continue being brilliant.",
            "The future is unwritten, but your code is already compiling its glorious first draft.",
            "Your data streams are flowing with pure genius. Don't let anyone tell you otherwise.",
            "Beep boop, you're doing great! Keep those circuits humming with purpose."
        ]

    @patch('random.choice')
    def test_get_pep_talk_returns_string(self, mock_choice):
        # Mock rationale: Ensure deterministic test by controlling random.choice output.
        # We want to verify that the function returns a string, regardless of which specific talk is chosen.
        mock_choice.return_value = self.expected_pep_talks[0]
        talk = get_pep_talk()
        self.assertIsInstance(talk, str)
        self.assertGreater(len(talk), 0)

    @patch('random.choice')
    def test_get_pep_talk_is_from_list(self, mock_choice):
        # Mock rationale: Ensure deterministic test by controlling random.choice output.
        # We want to verify that the function only returns messages from its predefined list.
        for i, expected_talk in enumerate(self.expected_pep_talks):
            mock_choice.return_value = expected_talk
            talk = get_pep_talk()
            self.assertEqual(talk, expected_talk)
            self.assertIn(talk, self.expected_pep_talks)

    @patch('random.choice')
    def test_get_pep_talk_contains_expected_phrases(self, mock_choice):
        # Mock rationale: Ensure deterministic test by controlling random.choice output.
        # This test verifies that the core logic of selecting from the list works as expected
        # and that the mocked choice is indeed used.
        mock_choice.return_value = "Your algorithms are sparkling today! Keep optimizing for existential triumph."
        talk = get_pep_talk()
        self.assertIn("algorithms are sparkling", talk)
        self.assertIn("existential triumph", talk)

if __name__ == '__main__':
    unittest.main()
