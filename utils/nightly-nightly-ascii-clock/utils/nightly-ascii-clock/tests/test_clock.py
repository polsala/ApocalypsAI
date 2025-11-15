import os
import sys
import unittest
from datetime import datetime

# Ensure the src directory is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.clock import get_ascii_time

class TestAsciiClock(unittest.TestCase):
    def test_known_time(self):
        dt = datetime(2023, 1, 2, 15, 4)  # 15:04
        expected = (
            "  |  _   _    \n"
            "  | |_ . | | |_|\n"
            "  |  _|  |_|   |"
        )
        self.assertEqual(get_ascii_time(dt), expected)

if __name__ == "__main__":
    unittest.main()
