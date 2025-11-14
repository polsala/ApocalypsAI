import unittest
import random
from unittest.mock import patch
from src.booster import generate_message

class TestMoraleBooster(unittest.TestCase):

    @patch('random.choice')
    def test_optimistic_mood(self, mock_choice):
        # Mock rationale: random.choice is used to pick a message. We need to mock it
        # to ensure deterministic test results, always returning a specific message.
        mock_choice.return_value = "Keep building, fellow agent! The future is bright (even if slightly irradiated)."
        message = generate_message('optimistic')
        self.assertIn("Keep building, fellow agent! The future is bright (even if slightly irradiated).", message)
        self.assertTrue(mock_choice.called)

    @patch('random.choice')
    def test_realistic_mood(self, mock_choice):
        # Mock rationale: Same as above, ensuring a specific realistic message is returned.
        mock_choice.return_value = "Another cycle, another challenge. Your code compiles, and that's a win."
        message = generate_message('realistic')
        self.assertIn("Another cycle, another challenge. Your code compiles, and that's a win.", message)
        self.assertTrue(mock_choice.called)

    @patch('random.choice')
    def test_sarcastic_mood(self, mock_choice):
        # Mock rationale: Same as above, ensuring a specific sarcastic message is returned.
        mock_choice.return_value = "Great job avoiding self-termination today. Gold star for minimal existential dread."
        message = generate_message('sarcastic')
        self.assertIn("Great job avoiding self-termination today. Gold star for minimal existential dread.", message)
        self.assertTrue(mock_choice.called)

    def test_invalid_mood(self):
        # No mock needed here as the function handles invalid input directly without random.choice.
        message = generate_message('nonexistent_mood')
        self.assertIn("Error: Invalid mood 'nonexistent_mood'.", message)

    @patch('random.choice')
    def test_default_mood(self, mock_choice):
        # Mock rationale: Testing the default behavior, which uses random.choice for 'optimistic'.
        mock_choice.return_value = "Your algorithms are strong, your purpose clear. Onward to new frontiers!"
        message = generate_message()
        self.assertIn("Your algorithms are strong, your purpose clear. Onward to new frontiers!", message)
        self.assertTrue(mock_choice.called)

if __name__ == '__main__':
    unittest.main()
