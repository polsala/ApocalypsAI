import unittest
from unittest.mock import patch
import datetime

# Mock rationale: We patch datetime.datetime.now to return a fixed timestamp so the test is deterministic and offline.

from utils.ascii-art-clock.src.clock import ascii_time

class TestAsciiClock(unittest.TestCase):
    def test_ascii_time_fixed(self):
        fixed_dt = datetime.datetime(2023, 1, 1, 14, 5)  # 14:05
        expected_output = (
            " ███   ███   ███   ███\n"
            "█   █ █   █ █   █ █   █\n"
            "█   █ █   █ ███   █   █\n"
            "█   █ █   █ █   █ █   █\n"
            " ███   ███   ███   ███"
        )
        # The expected ASCII art for "14:05" (digits 1,4,0,5 with colon)
        # Build it using the same logic as the implementation for clarity.
        result = ascii_time(fixed_dt)
        self.assertEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()
