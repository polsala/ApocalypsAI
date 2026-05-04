import unittest
from unittest.mock import patch
import datetime
import io
import sys
from src.tip_of_the_day import get_tip, main, TIPS

class TestTipOfTheDay(unittest.TestCase):
    def test_get_tip_fixed_date(self):
        # March 1, 2023 is the 60th day of the year
        fixed_date = datetime.date(2023, 3, 1)
        self.assertEqual(get_tip(fixed_date), TIPS[9])  # 60-1 = 59; 59 % 10 = 9

    @patch('datetime.date')
    def test_main_output(self, mock_date):
        # Mock today() to return a known date
        mock_date.today.return_value = datetime.date(2023, 3, 1)
        captured = io.StringIO()
        sys_stdout_original = sys.stdout
        sys.stdout = captured
        try:
            main()
        finally:
            sys.stdout = sys_stdout_original
        expected = "Survival Tip for 2023-03-01: Never leave a fire unattended; the ash may become a new species."
        self.assertIn(expected, captured.getvalue().strip())

if __name__ == '__main__':
    unittest.main()
