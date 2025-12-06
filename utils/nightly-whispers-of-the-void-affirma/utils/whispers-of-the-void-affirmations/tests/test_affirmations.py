import unittest
from unittest.mock import patch
import sys
import os

# Add the src directory to the Python path to allow importing affirmations.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from affirmations import generate_affirmation

class TestAffirmations(unittest.TestCase):

    @patch('random.choice')
    def test_generate_affirmation_deterministic(self, mock_choice):
        # Mock rationale: We need to ensure the output of generate_affirmation is predictable
        # for testing. By mocking random.choice, we control which elements are selected
        # from the various lists (templates, small_joys, etc.), making the test deterministic.

        # Test Case 1: Specific template and specific choices
        mock_choice.side_effect = [
            "Today, I will find joy in the small things, like {small_joy}.", # template
            "not being eaten by a rogue AI" # small_joy
        ]
        expected_affirmation = "Today, I will find joy in the small things, like not being eaten by a rogue AI."
        self.assertEqual(generate_affirmation(), expected_affirmation)
        self.assertEqual(mock_choice.call_count, 2)

        mock_choice.reset_mock() # Reset call count and side_effect

        # Test Case 2: Another specific template and specific choices
        mock_choice.side_effect = [
            "My resilience is stronger than any {apocalypse_threat}. Probably.", # template
            "mutant fungus" # apocalypse_threat
        ]
        expected_affirmation = "My resilience is stronger than any mutant fungus. Probably."
        self.assertEqual(generate_affirmation(), expected_affirmation)
        self.assertEqual(mock_choice.call_count, 2)

        mock_choice.reset_mock()

        # Test Case 3: A template requiring multiple choices
        mock_choice.side_effect = [
            "Every day is a new opportunity to {opportunity}, despite the {apocalypse_threat}.", # template
            "rebuild society (or my shelter)", # opportunity
            "zombie horde" # apocalypse_threat
        ]
        expected_affirmation = "Every day is a new opportunity to rebuild society (or my shelter), despite the zombie horde."
        self.assertEqual(generate_affirmation(), expected_affirmation)
        self.assertEqual(mock_choice.call_count, 3)

        mock_choice.reset_mock()

        # Test Case 4: Another template requiring multiple choices
        mock_choice.side_effect = [
            "I am a beacon of hope, even if that hope is just {small_hope}.", # template
            "finding an intact Wi-Fi signal" # small_hope
        ]
        expected_affirmation = "I am a beacon of hope, even if that hope is just finding an intact Wi-Fi signal."
        self.assertEqual(generate_affirmation(), expected_affirmation)
        self.assertEqual(mock_choice.call_count, 2)

        mock_choice.reset_mock()

        # Test Case 5: Template with 'shining_spirit'
        mock_choice.side_effect = [
            "Even in the void, my spirit shines, much like a {shining_spirit}.", # template
            "a flickering emergency light" # shining_spirit
        ]
        expected_affirmation = "Even in the void, my spirit shines, much like a a flickering emergency light."
        self.assertEqual(generate_affirmation(), expected_affirmation)
        self.assertEqual(mock_choice.call_count, 2)

        mock_choice.reset_mock()

        # Test Case 6: Template with 'vast_strength'
        mock_choice.side_effect = [
            "My inner strength is vast, like the {vast_strength}.", # template
            "desolate wasteland" # vast_strength
        ]
        expected_affirmation = "My inner strength is vast, like the desolate wasteland."
        self.assertEqual(generate_affirmation(), expected_affirmation)
        self.assertEqual(mock_choice.call_count, 2)


if __name__ == '__main__':
    unittest.main()
