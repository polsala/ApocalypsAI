import unittest
from utils.cron_expression_describer.src.describe import describe_cron

class TestCronDescriber(unittest.TestCase):
    def test_all_asterisks(self):
        expr = "* * * * *"
        expected = (
            "At every minute, every hour, every day, of every month, on every weekday."
        )
        self.assertEqual(describe_cron(expr), expected)

    def test_specific_minute_hour(self):
        expr = "15 3 * * *"
        expected = (
            "At minute 15, hour 3, every day, of every month, on every weekday."
        )
        self.assertEqual(describe_cron(expr), expected)

    def test_full_specification(self):
        expr = "30 14 10 6 1,3,5"
        expected = (
            "At minute 30, hour 14, on day 10, of June, on weekdays Monday, Wednesday, Friday."
        )
        self.assertEqual(describe_cron(expr), expected)

    def test_invalid_field_count(self):
        expr = "* * * *"  # only 4 fields
        with self.assertRaises(ValueError):
            describe_cron(expr)

    def test_weekday_zero_and_seven(self):
        expr = "0 0 * * 0,7"
        expected = (
            "At minute 0, hour 0, every day, of every month, on weekdays Sunday, Sunday."
        )
        self.assertEqual(describe_cron(expr), expected)

# Mock rationale: All tests use deterministic inputs and never perform network I/O.

if __name__ == "__main__":
    unittest.main()
