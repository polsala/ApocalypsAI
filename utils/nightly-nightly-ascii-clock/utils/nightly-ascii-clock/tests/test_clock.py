import unittest
from unittest.mock import patch
import datetime

# Mock rationale: we patch datetime.datetime.now to return a deterministic
# timestamp so the test is fully offline and repeatable.

from utils.nightly_ascii_clock.src.clock import get_ascii_time


class TestAsciiClock(unittest.TestCase):
    def test_ascii_time_fixed(self):
        fixed_dt = datetime.datetime(2023, 1, 1, 9, 5)  # 09:05
        expected_output = (
            " _   _   :   _   _ \n"
            "| | | |   .   _| |_ \n"
            "|_| |_|   .   |_   _|"
        )
        # Patch datetime.datetime.now to return our fixed datetime.
        with patch('datetime.datetime') as mock_dt:
            mock_dt.now.return_value = fixed_dt
            mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
            result = get_ascii_time(datetime.datetime.now())
        self.assertEqual(result, expected_output)

    def test_ascii_time_datetime_input(self):
        # Directly pass a datetime.time instance.
        t = datetime.time(23, 59)
        expected_output = (
            " _   _   :   _   _ \n"
            "|_| |_   .   _| |_ \n"
            " _|  _|   .   |_   _|"
        )
        result = get_ascii_time(t)
        self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()
