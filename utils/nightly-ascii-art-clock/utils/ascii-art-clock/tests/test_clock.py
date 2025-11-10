import unittest
import sys
import os
import datetime
from unittest.mock import patch

# Add src directory to path so we can import the module under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from clock import render_time, main


class TestAsciiArtClock(unittest.TestCase):
    def test_render_time_known(self):
        dt = datetime.time(12, 34)
        result = render_time(dt)
        # Ensure the result has three lines and contains expected characters
        self.assertEqual(result.count("\n"), 2)
        self.assertIn("_", result)
        self.assertIn("|", result)

    @patch('clock.datetime')
    def test_main_output(self, mock_datetime):
        # Mock datetime.datetime.now() to return a fixed time 09:05
        mock_now = datetime.datetime(2023, 1, 1, 9, 5, 0)
        mock_datetime.datetime.now.return_value = mock_now

        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_called_once()
            output = mock_print.call_args[0][0]
            # Verify that hour and minute appear in the rendered output
            self.assertIn("09", output)
            self.assertIn("05", output)


if __name__ == "__main__":
    unittest.main()
