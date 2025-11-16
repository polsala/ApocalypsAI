import unittest
from unittest.mock import patch
import sys
import os

# Add the src directory to the Python path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from booster import MoraleBooster, main

class TestMoraleBooster(unittest.TestCase):

    def setUp(self):
        self.booster = MoraleBooster()

    def test_get_random_morale_boost_returns_string(self):
        boost = self.booster.get_random_morale_boost()
        self.assertIsInstance(boost, str)
        self.assertGreater(len(boost), 0)

    def test_get_random_morale_boost_is_from_list(self):
        boost = self.booster.get_random_morale_boost()
        self.assertIn(boost, self.booster.quotes)

    @patch('random.choice')
    def test_get_random_morale_boost_deterministic(self, mock_choice):
        # Mock rationale: random.choice is non-deterministic, so we mock it to ensure
        # tests always receive a predictable output for consistent testing.
        expected_quote = "Your resilience is stronger than any mutated fungus. Keep growing!"
        mock_choice.return_value = expected_quote

        boost = self.booster.get_random_morale_boost()
        self.assertEqual(boost, expected_quote)
        mock_choice.assert_called_once_with(self.booster.quotes)

    @patch('builtins.print')
    @patch('booster.MoraleBooster.get_random_morale_boost')
    def test_main_prints_boost(self, mock_get_boost, mock_print):
        # Mock rationale: builtins.print is mocked to prevent actual console output
        # during tests and to assert that print was called with the expected arguments.
        # MoraleBooster.get_random_morale_boost is mocked to control the quote returned
        # and ensure deterministic testing of the main function's output formatting.
        expected_quote = "Test quote for main function."
        mock_get_boost.return_value = expected_quote

        main()

        mock_get_boost.assert_called_once()
        mock_print.assert_any_call("\n✨ Mutant Morale Boost ✨\n")
        mock_print.assert_any_call(f'"{expected_quote}"\n')
