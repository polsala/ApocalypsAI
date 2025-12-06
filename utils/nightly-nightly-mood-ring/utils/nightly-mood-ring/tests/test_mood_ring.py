import unittest
import datetime
from unittest.mock import patch

# Import the function under test
from src.mood_ring import get_mood

class TestMoodRing(unittest.TestCase):
    def test_mood_by_hour_ranges(self):
        """Verify that each hour range maps to the correct emoji.

        # Mock rationale: we patch ``datetime.datetime.now`` to control the
        # current hour without relying on the real system clock, ensuring the
        # test is deterministic and offline.
        """
        test_cases = [
            (2, "🌑"),   # Midnight range
            (5, "🌅"),   # Dawn range
            (10, "☀️"),  # Morning range
            (13, "😎"),  # Noon range
            (17, "🌆"),  # Evening range
            (22, "🌙"),  # Night range
        ]
        for hour, expected in test_cases:
            with patch('src.mood_ring.datetime.datetime') as mock_dt:
                # Mock ``now()`` to return a datetime with the desired hour
                mock_dt.now.return_value = datetime.datetime(2023, 1, 1, hour, 0, 0)
                # Ensure that constructing a new datetime works as expected
                mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
                self.assertEqual(get_mood(), expected, f"Hour {hour} should map to {expected}")

    def test_explicit_datetime_argument(self):
        """Calling ``get_mood`` with an explicit datetime bypasses the mock.
        """
        dt = datetime.datetime(2023, 1, 1, 9, 30)
        self.assertEqual(get_mood(dt), "☀️")

if __name__ == "__main__":
    unittest.main()
