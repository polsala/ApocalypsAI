import unittest
from src.converter import convert_time


class TestTimezoneConverter(unittest.TestCase):
    def test_basic_conversion(self):
        # 2023-01-01 12:00:00 in New York (UTC-5) should be 2023-01-02 02:00:00 in Tokyo (UTC+9)
        src_time = "2023-01-01 12:00:00"
        expected = "2023-01-02 02:00:00"
        result = convert_time(src_time, "America/New_York", "Asia/Tokyo")
        self.assertEqual(result, expected)

    def test_custom_format(self):
        src_time = "01/02/2023 15:30"
        fmt = "%m/%d/%Y %H:%M"
        # Convert from London (UTC) to Los Angeles (UTC-8) on 2023-01-02 15:30 UTC => 2023-01-02 07:30 PST
        expected = "01/02/2023 07:30"
        result = convert_time(src_time, "Europe/London", "America/Los_Angeles", fmt)
        self.assertEqual(result, expected)

    def test_invalid_timezone(self):
        # Mock rationale: we expect a ValueError when an unknown timezone is supplied.
        with self.assertRaises(Exception):
            convert_time("2023-01-01 00:00:00", "Invalid/Zone", "Asia/Tokyo")

    def test_invalid_timestamp(self):
        # Mock rationale: malformed timestamp should raise a ValueError from datetime.strptime.
        with self.assertRaises(Exception):
            convert_time("not-a-date", "America/New_York", "Asia/Tokyo")


if __name__ == "__main__":
    unittest.main()
