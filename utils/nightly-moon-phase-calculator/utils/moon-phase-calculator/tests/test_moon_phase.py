import unittest
from unittest.mock import patch
import datetime

# Import the function under test
from utils.moon_phase_calculator.src.moon_phase import calculate_moon_phase

class TestMoonPhaseCalculator(unittest.TestCase):
    # Mock rationale: ensure deterministic behavior without relying on the actual current date.
    @patch('datetime.date')
    def test_known_new_moon(self, mock_date):
        mock_date.today.return_value = datetime.date(2000, 1, 6)
        name, emoji = calculate_moon_phase(mock_date.today())
        self.assertEqual(name, "New Moon")
        self.assertEqual(emoji, "🌑")

    @patch('datetime.date')
    def test_first_quarter(self, mock_date):
        mock_date.today.return_value = datetime.date(2000, 1, 14)
        name, emoji = calculate_moon_phase(mock_date.today())
        self.assertEqual(name, "First Quarter")
        self.assertEqual(emoji, "🌓")

    @patch('datetime.date')
    def test_full_moon(self, mock_date):
        mock_date.today.return_value = datetime.date(2000, 1, 21)
        name, emoji = calculate_moon_phase(mock_date.today())
        self.assertEqual(name, "Full Moon")
        self.assertEqual(emoji, "🌕")

    @patch('datetime.date')
    def test_last_quarter(self, mock_date):
        mock_date.today.return_value = datetime.date(2000, 1, 28)
        name, emoji = calculate_moon_phase(mock_date.today())
        self.assertEqual(name, "Last Quarter")
        self.assertEqual(emoji, "🌗")

if __name__ == "__main__":
    unittest.main()
