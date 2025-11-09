import unittest
from unittest.mock import patch
import datetime

# Mock rationale: we replace ``datetime.datetime.now`` with a fixed timestamp
# so the test is deterministic and does not depend on the actual system clock.

from src.clock import get_current_time_ascii

class TestAsciiClock(unittest.TestCase):
    @patch('datetime.datetime')
    def test_ascii_output_at_midnight(self, mock_datetime):
        # Arrange: mock now() to return 00:00
        mock_now = datetime.datetime(2025, 1, 1, 0, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.strftime = datetime.datetime.strftime
        # Act
        ascii_art = get_current_time_ascii()
        # Expected ASCII for "00:00"
        expected = (
            " _   _   :   _   _\n"
            "| | | |  .  | | | |\n"
            "|_| |_|  .  |_| |_|"
        )
        # Assert
        self.assertEqual(ascii_art, expected)

    @patch('datetime.datetime')
    def test_ascii_output_at_random_time(self, mock_datetime):
        # Arrange: mock now() to return 13:37
        mock_now = datetime.datetime(2025, 1, 1, 13, 37, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.strftime = datetime.datetime.strftime
        # Act
        ascii_art = get_current_time_ascii()
        # Expected ASCII for "13:37"
        expected = (
            "   _   _   :   _   _   _\n"
            "  | _| |_|  .  _| |_| |_\n"
            "  | _|   |  .  _|   |  _|"
        )
        # Assert
        self.assertEqual(ascii_art, expected)

if __name__ == '__main__':
    unittest.main()
