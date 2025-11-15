import unittest
from datetime import datetime
from unittest.mock import patch
import os
import sys

# Add the src directory to sys.path so we can import the module directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from emoji_clock import get_emoji_time

class TestEmojiClock(unittest.TestCase):
    @patch("emoji_clock.datetime")
    def test_fixed_time(self, mock_datetime):
        # Mock rationale: patch datetime.now to return a fixed datetime for deterministic offline testing.
        mock_datetime.now.return_value = datetime(2023, 1, 1, 9, 5)
        result = get_emoji_time()
        expected = "0️⃣9️⃣:0️⃣5️⃣"
        self.assertEqual(result, expected)

    def test_custom_datetime(self):
        dt = datetime(2022, 12, 31, 23, 59)
        result = get_emoji_time(dt)
        expected = "2️⃣3️⃣:5️⃣9️⃣"
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
