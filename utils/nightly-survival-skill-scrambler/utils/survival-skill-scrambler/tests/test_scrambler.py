import unittest
from unittest.mock import patch
import sys
import io

# Add the src directory to the path to allow importing scrambler
# Mock rationale: This ensures the test can find the module 'scrambler' when run from the utility's root directory.
sys.path.insert(0, 'src')
from scrambler import get_random_skill, SURVIVAL_SKILLS, main
sys.path.pop(0)

class TestSurvivalSkillScrambler(unittest.TestCase):

    @patch('random.choice')
    def test_get_random_skill_deterministic(self, mock_choice):
        # Mock rationale: We mock random.choice to ensure deterministic test results.
        # This allows us to predict the output of get_random_skill without actual randomness.
        mock_choice.return_value = SURVIVAL_SKILLS[0]
        self.assertEqual(get_random_skill(), SURVIVAL_SKILLS[0])

        mock_choice.return_value = SURVIVAL_SKILLS[2]
        self.assertEqual(get_random_skill(), SURVIVAL_SKILLS[2])

    def test_get_random_skill_returns_string(self):
        # Test that the function always returns a string
        skill = get_random_skill()
        self.assertIsInstance(skill, str)

    def test_get_random_skill_is_from_list(self):
        # Test that the returned skill is one of the defined skills
        skill = get_random_skill()
        self.assertIn(skill, SURVIVAL_SKILLS)

    @patch('random.choice')
    def test_main_output(self, mock_choice):
        # Mock rationale: We mock random.choice to control the output of main()
        # and capture it for assertion. This makes the test deterministic.
        mock_choice.return_value = "Test Skill Challenge"

        # Mock rationale: We capture stdout to verify the printed output.
        # This allows us to test the main function's side effect (printing) deterministically.
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__ # Reset redirect

        self.assertEqual(captured_output.getvalue().strip(), "Your survival challenge for today: Test Skill Challenge")

if __name__ == '__main__':
    unittest.main()
