import unittest
from unittest.mock import patch
import datetime
import io
import sys

# Import the function to be tested
from src.booster import get_morale_boost, main, MORALE_BOOSTS

class TestMutantMoraleBooster(unittest.TestCase):

    @patch('random.choice')
    def test_get_morale_boost_deterministic(self, mock_choice):
        # Mock rationale: Ensure deterministic testing of random.choice.
        # We want to verify that get_morale_boost correctly calls random.choice
        # and returns its result, without relying on actual randomness.
        mock_choice.return_value = MORALE_BOOSTS[0]
        self.assertEqual(get_morale_boost(), MORALE_BOOSTS[0])
        mock_choice.assert_called_once_with(MORALE_BOOSTS)

        # Reset mock for a new call if needed, or use separate test methods
        mock_choice.reset_mock()
        mock_choice.return_value = MORALE_BOOSTS[1]
        self.assertEqual(get_morale_boost(), MORALE_BOOSTS[1])
        mock_choice.assert_called_once_with(MORALE_BOOSTS)

    def test_get_morale_boost_returns_string_from_list(self):
        # Ensure that the returned boost is always one of the predefined messages.
        boost = get_morale_boost()
        self.assertIsInstance(boost, str)
        self.assertIn(boost, MORALE_BOOSTS)

    @patch('src.booster.get_morale_boost')
    @patch('datetime.datetime')
    def test_main_output_format(self, mock_datetime, mock_get_morale_boost):
        # Mock rationale:
        # 1. Mock datetime.datetime.now() to ensure a deterministic timestamp in the output.
        # 2. Mock get_morale_boost() to ensure a deterministic message in the output.
        # This allows us to precisely predict and test the console output format.

        # Set up mock return values
        test_time = datetime.datetime(2023, 10, 27, 10, 30, 0)
        mock_datetime.now.return_value = test_time
        mock_get_morale_boost.return_value = "Test Morale Message!"

        expected_timestamp = test_time.strftime("%Y-%m-%d %H:%M:%S")
        expected_output = f"[{expected_timestamp}] Test Morale Message!\n"

        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Run main
        main()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Assert output
        self.assertEqual(captured_output.getvalue(), expected_output)
        mock_datetime.now.assert_called_once()
        mock_get_morale_boost.assert_called_once()

if __name__ == '__main__':
    unittest.main()
