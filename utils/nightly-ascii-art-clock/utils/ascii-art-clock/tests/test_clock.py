import unittest
from datetime import datetime
from src.clock import render_time

class TestAsciiArtClock(unittest.TestCase):
    def test_fixed_time_rendering(self):
        # Fixed datetime: 12:34:56
        dt = datetime(2023, 1, 1, 12, 34, 56)
        output = render_time(dt)
        lines = output.splitlines()
        # Should always be three rows
        self.assertEqual(len(lines), 3)
        # The colon pattern uses a centered dot (·) – should appear twice
        self.assertEqual(output.count('·'), 2)
        # Verify that the hour "12" appears correctly in the first row
        # Digit 1 row0 is three spaces, digit 2 row0 is " _ "
        self.assertTrue(lines[0].startswith('    _'))
        # Verify that the minute "34" row1 contains the pattern for digit 3 (" _|")
        self.assertIn(' _|', lines[1])
        # Verify that the second "56" row2 contains the pattern for digit 6 ("|_|")
        self.assertIn('|_|', lines[2])

    def test_invalid_character_raises(self):
        # Mock a datetime that would produce an unsupported character (e.g., negative hour)
        class BadDateTime(datetime):
            @property
            def hour(self):
                return -1
        with self.assertRaises(ValueError):
            render_time(BadDateTime.now())

if __name__ == '__main__':
    unittest.main()
