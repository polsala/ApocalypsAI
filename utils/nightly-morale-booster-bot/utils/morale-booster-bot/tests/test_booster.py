import unittest
from unittest.mock import patch
import datetime
from src.booster import get_morale_boost, MORALE_MESSAGES, get_daily_seed

class TestMoraleBooster(unittest.TestCase):

    @patch('random.choice')
    def test_get_morale_boost_returns_message(self, mock_choice):
        # Mock rationale: We want to ensure that `random.choice` is called and returns a string.
        # By mocking it, we can control its return value and verify the function's behavior
        # without relying on actual randomness.
        mock_choice.return_value = "Test message."
        boost = get_morale_boost(seed=123) # Provide a seed for good measure, though mock overrides
        self.assertIsInstance(boost, str)
        self.assertEqual(boost, "Test message.")
        mock_choice.assert_called_once_with(MORALE_MESSAGES)

    @patch('random.seed')
    @patch('random.choice')
    def test_get_morale_boost_uses_daily_seed_by_default(self, mock_choice, mock_seed):
        # Mock rationale: We need to verify that `random.seed` is called with the correct
        # daily seed when no explicit seed is provided to `get_morale_boost`.
        # `random.choice` is also mocked to prevent actual random selection and focus on seed logic.
        mock_choice.return_value = "Any message" # Value doesn't matter for this test
        
        # Calculate expected daily seed
        today = datetime.date.today()
        expected_seed = today.year * 10000 + today.month * 100 + today.day

        get_morale_boost()
        mock_seed.assert_called_once_with(expected_seed)
        mock_choice.assert_called_once_with(MORALE_MESSAGES)

    @patch('random.seed')
    @patch('random.choice')
    def test_get_morale_boost_uses_provided_seed(self, mock_choice, mock_seed):
        # Mock rationale: Verify that `random.seed` is called with the explicit seed
        # provided to `get_morale_boost`, overriding the default daily seed logic.
        mock_choice.return_value = "Another message"
        
        test_seed = 999
        get_morale_boost(seed=test_seed)
        mock_seed.assert_called_once_with(test_seed)
        mock_choice.assert_called_once_with(MORALE_MESSAGES)

    def test_get_daily_seed_determinism(self):
        # Test that the daily seed is consistent for the same day
        seed1 = get_daily_seed()
        seed2 = get_daily_seed()
        self.assertEqual(seed1, seed2)

        # Test that the seed changes for a different "day" (by mocking datetime)
        with patch('datetime.date') as mock_date:
            mock_date.today.return_value = datetime.date(2023, 1, 1)
            seed_jan1 = get_daily_seed()
            
            mock_date.today.return_value = datetime.date(2023, 1, 2)
            seed_jan2 = get_daily_seed()
            
            self.assertNotEqual(seed_jan1, seed_jan2)
            self.assertEqual(seed_jan1, 20230101)
            self.assertEqual(seed_jan2, 20230102)
