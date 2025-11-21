import datetime
import unittest
from src.forecast import get_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_known_date(self):
        """Validate deterministic output for a fixed date.

        The expected emoji is derived from the algorithm used in ``forecast.py``.
        # Mock rationale: we hard‑code the expected value to guarantee the test
        # remains deterministic and does not depend on the implementation details
        # of the hashing function beyond what is documented.
        """
        test_date = datetime.date(2023, 1, 1)  # 20230101 % 9 == 0
        expected = "☀️"
        self.assertEqual(get_forecast(test_date), expected)

    def test_cycle_length(self):
        """Ensure the forecast cycles through all emojis over nine consecutive days.

        # Mock rationale: we iterate over a range of dates and collect the emojis;
        # the set should contain exactly the nine defined emojis, confirming the
        # modulo operation covers the full list.
        """
        start = datetime.date(2023, 1, 1)
        emojis = {get_forecast(start + datetime.timedelta(days=i)) for i in range(9)}
        self.assertEqual(len(emojis), 9)

if __name__ == "__main__":
    unittest.main()
