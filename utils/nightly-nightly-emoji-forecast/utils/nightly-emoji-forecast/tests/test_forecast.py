import unittest
from unittest import mock
from datetime import datetime

# Import the function under test.
from nightly_emoji_forecast import get_emoji_for_date

class TestEmojiForecast(unittest.TestCase):
    def test_known_dates(self):
        """Deterministic mapping checks for a few sample dates.

        The expected emojis are derived from the current implementation.
        If the implementation changes, update the expected values accordingly.
        """
        cases = {
            "2025-01-01": "🪐",
            "2025-12-25": "🎄",
            "2024-02-29": "🦄",  # Leap year date
            "2023-07-04": "🌈",
        }
        for date_str, expected in cases.items():
            with self.subTest(date=date_str):
                self.assertEqual(get_emoji_for_date(date_str), expected)

    def test_invalid_format_raises(self):
        """# Mock rationale: Ensure function validates input format without external calls.
        """
        invalid_dates = ["2025/01/01", "01-01-2025", "2025-13-01", "2025-00-10", ""]
        for bad in invalid_dates:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    get_emoji_for_date(bad)

    @mock.patch("nightly_emoji_forecast.datetime")
    def test_hash_consistency_with_mocked_datetime(self, mock_datetime):
        """# Mock rationale: Demonstrate that the function does not depend on the current time.
        The mock ensures that even if the implementation accidentally used `datetime.now()`,
        the test would still pass only if the function remains pure.
        """
        mock_datetime.strptime.side_effect = datetime.strptime
        # Re‑use a known date; the result must match the deterministic mapping.
        self.assertEqual(get_emoji_for_date("2025-12-25"), "🎄")

if __name__ == "__main__":
    unittest.main()
