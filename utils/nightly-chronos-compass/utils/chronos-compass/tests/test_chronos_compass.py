import unittest
import sys
import io
from unittest.mock import patch
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# Mock rationale:
# datetime.now() is non-deterministic and depends on the system's current time.
# To ensure tests are repeatable and independent of when they are run,
# we mock datetime.now() to return a fixed, known point in time.
# This allows us to predict the output for timezone conversions and displays.

# Add src directory to path for importing the module
sys.path.insert(0, 'src')
import chronos_compass
sys.path.pop(0)

class TestChronosCompass(unittest.TestCase):

    # Define a fixed "current" time for deterministic tests
    MOCKED_NOW_UTC = datetime(2023, 10, 27, 10, 30, 0, tzinfo=timezone.utc)

    @patch('chronos_compass.datetime')
    def test_display_current_time_valid_timezones(self, mock_datetime):
        # Mock rationale: See above. We want a fixed point in time.
        mock_datetime.now.return_value = self.MOCKED_NOW_UTC
        mock_datetime.strptime = datetime.strptime # Ensure strptime works normally
        mock_datetime.fromtimestamp = datetime.fromtimestamp # Ensure fromtimestamp works normally
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow datetime constructor

        captured_output = io.StringIO()
        sys.stdout = captured_output

        chronos_compass.display_current_time(['UTC', 'America/New_York', 'Asia/Tokyo'])

        sys.stdout = sys.__stdout__ # Restore stdout
        output = captured_output.getvalue()

        self.assertIn("Current Time Across Zones:", output)
        self.assertIn("UTC: 2023-10-27 10:30", output)
        self.assertIn("America/New_York: 2023-10-27 06:30", output) # UTC-4
        self.assertIn("Asia/Tokyo: 2023-10-27 19:30", output) # UTC+9

    @patch('chronos_compass.datetime')
    def test_display_current_time_invalid_timezone(self, mock_datetime):
        # Mock rationale: See above.
        mock_datetime.now.return_value = self.MOCKED_NOW_UTC
        mock_datetime.strptime = datetime.strptime
        mock_datetime.fromtimestamp = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        captured_output = io.StringIO()
        sys.stdout = captured_output

        chronos_compass.display_current_time(['Invalid/Timezone'])

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Error: Timezone 'Invalid/Timezone' not found.", output)

    @patch('chronos_compass.datetime')
    def test_convert_time_valid_conversion(self, mock_datetime):
        # Mock rationale: datetime.strptime is used internally, but we don't need to mock now() for conversion
        # as the input time is explicit. We mock datetime itself to ensure consistency with other tests
        # and to prevent any accidental calls to datetime.now() if the function were to change.
        mock_datetime.strptime = datetime.strptime
        mock_datetime.fromtimestamp = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        captured_output = io.StringIO()
        sys.stdout = captured_output

        chronos_compass.convert_time("2023-10-27 14:00", "Europe/London", "America/Los_Angeles")

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Conversion:", output)
        # London is UTC+1 (BST), Los Angeles is UTC-7 (PDT)
        # 14:00 BST (UTC+1) is 13:00 UTC
        # 13:00 UTC is 06:00 PDT (UTC-7)
        self.assertIn("2023-10-27 14:00 Europe/London  ->  2023-10-27 06:00 America/Los_Angeles", output)

    @patch('chronos_compass.datetime')
    def test_convert_time_invalid_from_timezone(self, mock_datetime):
        # Mock rationale: See above.
        mock_datetime.strptime = datetime.strptime
        mock_datetime.fromtimestamp = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        captured_output = io.StringIO()
        sys.stdout = captured_output

        chronos_compass.convert_time("2023-10-27 14:00", "Invalid/From", "America/Los_Angeles")

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Error: 'Invalid/From' not found. Please use valid IANA timezone names.", output)

    @patch('chronos_compass.datetime')
    def test_convert_time_invalid_to_timezone(self, mock_datetime):
        # Mock rationale: See above.
        mock_datetime.strptime = datetime.strptime
        mock_datetime.fromtimestamp = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        captured_output = io.StringIO()
        sys.stdout = captured_output

        chronos_compass.convert_time("2023-10-27 14:00", "Europe/London", "Invalid/To")

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Error: 'Invalid/To' not found. Please use valid IANA timezone names.", output)

    @patch('chronos_compass.datetime')
    def test_convert_time_invalid_time_format(self, mock_datetime):
        # Mock rationale: See above.
        mock_datetime.strptime = datetime.strptime
        mock_datetime.fromtimestamp = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        captured_output = io.StringIO()
        sys.stdout = captured_output

        chronos_compass.convert_time("2023/10/27 14:00", "Europe/London", "America/Los_Angeles")

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Error: Invalid time format '2023/10/27 14:00'. Expected 'YYYY-MM-DD HH:MM'.", output)

if __name__ == '__main__':
    unittest.main()
