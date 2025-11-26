import unittest
from datetime import date
from src.zen_quote import get_quote

class TestZenQuote(unittest.TestCase):
    def test_repeatability(self):
        """# Mock rationale: the same date must always yield the same quote."""
        d = date(2024, 2, 29)
        first = get_quote(d)
        second = get_quote(d)
        self.assertEqual(first, second)

    def test_different_dates(self):
        """# Mock rationale: different dates should (most likely) give different quotes, ensuring the hash is used."""
        q1 = get_quote(date(2023, 1, 1))
        q2 = get_quote(date(2023, 1, 2))
        # It's possible they collide, but extremely unlikely with our small set.
        self.assertNotEqual(q1, q2)

if __name__ == "__main__":
    unittest.main()
