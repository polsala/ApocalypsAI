import unittest
from unittest.mock import patch
import datetime
from src.affirmations import generate_affirmation, get_affirmation_components

class TestAffirmations(unittest.TestCase):

    @patch('random.choice')
    def test_generate_affirmation_deterministic_mock(self, mock_choice):
        # Mock rationale: random.choice is used to select components of the affirmation.
        # Mocking it ensures deterministic test results by controlling which components are chosen,
        # allowing verification of the string concatenation logic without actual randomness.
        mock_choice.side_effect = [
            "Even as the cosmic dust settles,",  # Starter
            "your resolve remains an unyielding beacon.", # Middle
            "Forge ahead." # Ending
        ]

        expected_affirmation = "Even as the cosmic dust settles, your resolve remains an unyielding beacon. Forge ahead."
        self.assertEqual(generate_affirmation(seed=123), expected_affirmation)
        self.assertEqual(mock_choice.call_count, 3)

    @patch('random.choice')
    def test_generate_affirmation_another_deterministic_mock(self, mock_choice):
        # Mock rationale: Similar to the above, this mock ensures a different, but still controlled,
        # sequence of choices for another deterministic test case.
        mock_choice.side_effect = [
            "Amidst the encroaching shadows,",  # Starter
            "your purpose shines brighter.", # Middle
            "Adapt and thrive." # Ending
        ]

        expected_affirmation = "Amidst the encroaching shadows, your purpose shines brighter. Adapt and thrive."
        self.assertEqual(generate_affirmation(seed=456), expected_affirmation)
        self.assertEqual(mock_choice.call_count, 3)

    @patch('datetime.date')
    @patch('random.seed')
    @patch('random.choice')
    def test_generate_affirmation_daily_consistency(self, mock_choice, mock_seed, mock_date):
        # Mock rationale: datetime.date.today() is used to generate a daily seed for consistency.
        # Mocking it allows us to fix the 'current date' for testing the seeding logic.
        # random.seed() is mocked to verify it's called with the correct date-based seed.
        # random.choice() is mocked to ensure the final affirmation is predictable after seeding.

        # Simulate a specific date
        mock_date.today.return_value = datetime.date(2023, 10, 27)
        
        # Define the choices that random.choice should return for this specific date's seed
        # These choices are arbitrary for the mock, as we are primarily testing the seed call.
        mock_choice.side_effect = [
            "When the fabric of reality frays,",
            "the potential for rebirth stirs.",
            "Discover new meaning."
        ]

        # Call generate_affirmation without a specific seed, so it uses the mocked date
        affirmation = generate_affirmation(seed=None)

        # Verify that random.seed was called with the correct date-based seed
        # 2023 * 10000 + 10 * 100 + 27 = 20231027
        mock_seed.assert_called_once_with(20231027)

        # Verify the affirmation generated with the mocked choices
        expected_affirmation = "When the fabric of reality frays, the potential for rebirth stirs. Discover new meaning."
        self.assertEqual(affirmation, expected_affirmation)
        self.assertEqual(mock_choice.call_count, 3)

    def test_get_affirmation_components(self):
        # Test rationale: Verifies that the component lists are correctly defined and non-empty.
        # This ensures the affirmation generator has content to work with.
        starters, middles, endings = get_affirmation_components()
        self.assertIsInstance(starters, list)
        self.assertIsInstance(middles, list)
        self.assertIsInstance(endings, list)
        self.assertGreater(len(starters), 0)
        self.assertGreater(len(middles), 0)
        self.assertGreater(len(endings), 0)
