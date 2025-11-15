import unittest
import sys
import os
from datetime import datetime

# Mock rationale: adjust sys.path to import the utility module without external dependencies.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from emoji_clock import get_emoji_time

class TestEmojiClock(unittest.TestCase):
    def test_known_time(self):
        fixed_dt = datetime(2023, 1, 1, 9, 5)  # 09:05
        expected = "0️⃣9️⃣⏰0️⃣5️⃣"
        self.assertEqual(get_emoji_time(fixed_dt), expected)

    def test_midnight(self):
        fixed_dt = datetime(2023, 1, 1, 0, 0)  # 00:00
        expected = "0️⃣0️⃣⏰0️⃣0️⃣"
        self.assertEqual(get_emoji_time(fixed_dt), expected)

if __name__ == "__main__":
    unittest.main()
