import unittest
from src.main import date_to_emoji

class TestEmojiCalendar(unittest.TestCase):
    def test_known_dates(self):
        # October 31 -> 🎃3️⃣1️⃣
        self.assertEqual(date_to_emoji("2023-10-31"), "🎃3️⃣1️⃣")
        # December 25 -> 🎄2️⃣5️⃣
        self.assertEqual(date_to_emoji("2022-12-25"), "🎄2️⃣5️⃣")
        # February 1 -> ❤️0️⃣1️⃣ (day padded to two digits)
        self.assertEqual(date_to_emoji("2021-02-01"), "❤️0️⃣1️⃣")

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            date_to_emoji("2021/02/01")  # wrong separator
        with self.assertRaises(ValueError):
            date_to_emoji("02-01-2021")  # wrong order
        with self.assertRaises(ValueError):
            date_to_emoji("2021-13-01")  # invalid month
        with self.assertRaises(ValueError):
            date_to_emoji("2021-00-10")  # invalid month
        with self.assertRaises(ValueError):
            date_to_emoji("2021-01-00")  # invalid day

    def test_edge_days(self):
        # First day of month
        self.assertEqual(date_to_emoji("2020-07-01"), "🏖️0️⃣1️⃣")
        # Last day of month (31)
        self.assertEqual(date_to_emoji("2020-08-31"), "🍉3️⃣1️⃣")

# Mock rationale: No external services are called; all logic is pure and deterministic.

if __name__ == "__main__":
    unittest.main()
