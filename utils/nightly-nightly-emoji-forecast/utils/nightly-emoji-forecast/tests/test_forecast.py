import datetime
import unittest
from unittest.mock import patch, MagicMock

from utils.nightly_emoji_forecast.src.forecast import get_forecast, EMOJIS


class TestEmojiForecast(unittest.TestCase):
    def test_zero_hash_returns_first_emoji(self):
        """Mock SHA‑256 to return a digest of all zeros.
        Expected index is 0 → EMOJIS[0] (☀️).
        """
        mock_hash = MagicMock()
        mock_hash.hexdigest.return_value = "0" * 64
        with patch(
            "utils.nightly_emoji_forecast.src.forecast.hashlib.sha256",
            return_value=mock_hash,
        ):
            date = datetime.date(1999, 12, 31)
            self.assertEqual(get_forecast(date), EMOJIS[0])

    def test_f_hash_returns_sixth_emoji(self):
        """Mock SHA‑256 to return a digest of all 'f'.
        The integer value of "f"*64 modulo 10 is 5, so we expect EMOJIS[5] (🌧️).
        # Mock rationale: deterministic result without real hashing.
        """
        mock_hash = MagicMock()
        mock_hash.hexdigest.return_value = "f" * 64
        with patch(
            "utils.nightly_emoji_forecast.src.forecast.hashlib.sha256",
            return_value=mock_hash,
        ):
            date = datetime.date(2023, 1, 1)
            self.assertEqual(get_forecast(date), EMOJIS[5])


if __name__ == "__main__":
    unittest.main()
