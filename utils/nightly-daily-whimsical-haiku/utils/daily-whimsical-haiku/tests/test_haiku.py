import datetime
import unittest

# Mock rationale: Import the module from its relative location without needing any external packages.
from utils.daily-whimsical-haiku.src.haiku import generate_haiku

class TestHaikuGenerator(unittest.TestCase):
    def test_deterministic_output(self):
        """Ensure a known date yields the expected haiku.

        Mock rationale: By fixing the date we avoid any nondeterminism.
        """
        mock_date = datetime.date(2023, 4, 1)  # 20230401
        haiku = generate_haiku(mock_date)
        expected = (
            "Silent moon whispers\n"
            "across the sleepy town\n"
            "time folds into light."
        )
        self.assertEqual(haiku, expected)

    def test_repeatability_same_day(self):
        """Calling the function twice for the same day must return identical results.

        Mock rationale: No external state changes between calls.
        """
        today = datetime.date.today()
        self.assertEqual(generate_haiku(today), generate_haiku(today))

if __name__ == "__main__":
    unittest.main()
