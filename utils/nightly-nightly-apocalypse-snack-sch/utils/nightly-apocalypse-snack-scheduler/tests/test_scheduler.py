import unittest
from unittest.mock import patch, mock_open
from datetime import date, timedelta
import sys
import io

# Import the functions from the scheduler module
# Assuming scheduler.py is in src/ and tests are in tests/
# We need to adjust sys.path or import directly if running from project root
# For self-contained utility, assume tests are run from the util_name directory
# or that the src/scheduler.py is directly importable.
# Let's assume a simple import for now, as the test runner will handle paths.
from src.scheduler import load_snacks, get_expiry_status, print_report, main

class TestScheduler(unittest.TestCase):

    # Mock rationale: We need to control the current date to test expiry logic deterministically.
    # Patching date.today() allows us to simulate different "today" dates without waiting for real time.
    @patch('src.scheduler.date')
    def test_get_expiry_status_expired(self, mock_date):
        mock_date.today.return_value = date(2024, 1, 15)
        mock_date.fromisoformat = date.fromisoformat # Ensure fromisoformat works normally

        snack = {'name': 'Expired Ration', 'quantity': 1, 'expiry_date': '2024-01-01'}
        status = get_expiry_status(snack, mock_date.today(), 30)
        self.assertEqual(status['status'], 'EXPIRED')
        self.assertEqual(status['days_left'], -14)
        self.assertEqual(status['color'], 'red')

    # Mock rationale: Same as above, controlling the current date for deterministic testing.
    @patch('src.scheduler.date')
    def test_get_expiry_status_expiring_soon(self, mock_date):
        mock_date.today.return_value = date(2024, 1, 15)
        mock_date.fromisoformat = date.fromisoformat

        snack = {'name': 'Soon-to-Expire Bar', 'quantity': 2, 'expiry_date': '2024-02-10'}
        status = get_expiry_status(snack, mock_date.today(), 30)
        self.assertEqual(status['status'], 'Expiring Soon')
        self.assertEqual(status['days_left'], 26)
        self.assertEqual(status['color'], 'yellow')

    # Mock rationale: Same as above, controlling the current date for deterministic testing.
    @patch('src.scheduler.date')
    def test_get_expiry_status_ok(self, mock_date):
        mock_date.today.return_value = date(2024, 1, 15)
        mock_date.fromisoformat = date.fromisoformat

        snack = {'name': 'Fresh MRE', 'quantity': 3, 'expiry_date': '2025-01-01'}
        status = get_expiry_status(snack, mock_date.today(), 30)
        self.assertEqual(status['status'], 'OK')
        self.assertEqual(status['days_left'], 352)
        self.assertEqual(status['color'], 'green')

    # Mock rationale: Same as above, controlling the current date for deterministic testing.
    @patch('src.scheduler.date')
    def test_get_expiry_status_expiring_today(self, mock_date):
        mock_date.today.return_value = date(2024, 1, 15)
        mock_date.fromisoformat = date.fromisoformat

        snack = {'name': 'Last Day Ration', 'quantity': 1, 'expiry_date': '2024-01-15'}
        status = get_expiry_status(snack, mock_date.today(), 30)
        self.assertEqual(status['status'], 'Expiring Soon') # Or 'OK' depending on threshold logic, but 0 days is <= 30
        self.assertEqual(status['days_left'], 0)
        self.assertEqual(status['color'], 'yellow')

    # Mock rationale: We need to simulate file system access without actually creating files.
    # mock_open allows us to provide arbitrary string content as if it were read from a file.
    @patch('builtins.open', new_callable=mock_open, read_data="""
- name: Test Snack 1
  quantity: 10
  expiry_date: 2025-01-01
- name: Test Snack 2
  quantity: 5
  expiry_date: 2024-06-30
""")
    def test_load_snacks_success(self, mock_file):
        snacks = load_snacks("dummy_path.yaml")
        self.assertEqual(len(snacks), 2)
        self.assertEqual(snacks[0]['name'], 'Test Snack 1')
        mock_file.assert_called_once_with("dummy_path.yaml", 'r')

    # Mock rationale: Simulate a FileNotFoundError without needing to delete actual files.
    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.exit', return_value=None) # Mock sys.exit to prevent actual exit during test
    @patch('sys.stderr', new_callable=io.StringIO) # Capture stderr output
    def test_load_snacks_file_not_found(self, mock_stderr, mock_exit, mock_file):
        snacks = load_snacks("non_existent.yaml")
        self.assertIsNone(snacks) # load_snacks exits, so it returns None
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Configuration file not found", mock_stderr.getvalue())

    # Mock rationale: Simulate a YAML parsing error without needing to create malformed files.
    @patch('builtins.open', new_callable=mock_open, read_data="""
- name: Malformed Snack
  quantity: 10
  expiry_date: 2025-01-01
  - this is not valid yaml
""")
    @patch('sys.exit', return_value=None)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_load_snacks_yaml_error(self, mock_stderr, mock_exit, mock_file):
        snacks = load_snacks("malformed.yaml")
        self.assertIsNone(snacks)
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error parsing YAML file", mock_stderr.getvalue())

    # Mock rationale: Test handling of invalid date format in snack data.
    @patch('src.scheduler.date')
    def test_get_expiry_status_invalid_date(self, mock_date):
        mock_date.today.return_value = date(2024, 1, 15)
        mock_date.fromisoformat = date.fromisoformat

        snack = {'name': 'Bad Date Snack', 'quantity': 1, 'expiry_date': 'not-a-date'}
        status = get_expiry_status(snack, mock_date.today(), 30)
        self.assertEqual(status['status'], 'Invalid Date')
        self.assertIsNone(status['days_left'])
        self.assertEqual(status['color'], 'red')

    # Mock rationale: Capture stdout to verify the printed report content.
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.scheduler.date') # Mock date.today() for deterministic report date
    def test_print_report(self, mock_date, mock_stdout):
        mock_date.today.return_value = date(2024, 1, 15)
        mock_date.fromisoformat = date.fromisoformat

        statuses = [
            {'name': 'Expired Item', 'quantity': 1, 'status': 'EXPIRED', 'days_left': -10, 'color': 'red'},
            {'name': 'Soon Item', 'quantity': 2, 'status': 'Expiring Soon', 'days_left': 20, 'color': 'yellow'},
            {'name': 'OK Item', 'quantity': 3, 'status': 'OK', 'days_left': 300, 'color': 'green'},
            {'name': 'Invalid Item', 'quantity': 'N/A', 'status': 'Invalid Date', 'days_left': None, 'color': 'red'}
        ]
        print_report(statuses)
        output = mock_stdout.getvalue()

        self.assertIn("--- Apocalypse Snack Inventory Report ---", output)
        self.assertIn("Report Date: 2024-01-15", output)
        self.assertIn("[EXPIRED] Expired Item (Qty: 1) - Expired 10 days ago!", output)
        self.assertIn("[Expiring Soon] Soon Item (Qty: 2) - 20 days left.", output)
        self.assertIn("[OK] OK Item (Qty: 3) - 300 days left.", output)
        self.assertIn("[Invalid Date] Invalid Item (Qty: N/A) - Invalid expiry date format.", output)
        # Check sorting: Expired first, then soonest
        self.assertTrue(output.find("Expired Item") < output.find("Soon Item"))
        self.assertTrue(output.find("Soon Item") < output.find("OK Item"))


    # Mock rationale: Test the main function's end-to-end behavior.
    # We need to mock command-line arguments, file reading, and date.today().
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.scheduler.date')
    @patch('builtins.open', new_callable=mock_open, read_data="""
- name: Main Test Snack 1
  quantity: 1
  expiry_date: 2024-01-10 # Expired by 2024-01-15
- name: Main Test Snack 2
  quantity: 2
  expiry_date: 2024-02-10 # Expiring soon by 2024-01-15 (within 90 days)
- name: Main Test Snack 3
  quantity: 3
  expiry_date: 2025-01-10 # OK
""")
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function(self, mock_parse_args, mock_file, mock_date, mock_stdout):
        # Set up mock arguments
        mock_parse_args.return_value.config = "test_snacks.yaml"
        mock_parse_args.return_value.warning_days = 90

        # Set up mock date
        mock_date.today.return_value = date(2024, 1, 15)
        mock_date.fromisoformat = date.fromisoformat

        main()
        output = mock_stdout.getvalue()

        self.assertIn("--- Apocalypse Snack Inventory Report ---", output)
        self.assertIn("Report Date: 2024-01-15", output)
        self.assertIn("[EXPIRED] Main Test Snack 1 (Qty: 1) - Expired 5 days ago!", output)
        self.assertIn("[Expiring Soon] Main Test Snack 2 (Qty: 2) - 26 days left.", output)
        self.assertIn("[OK] Main Test Snack 3 (Qty: 3) - 361 days left.", output)
        mock_file.assert_called_once_with("test_snacks.yaml", 'r')

    # Mock rationale: Test main function with no snacks in config.
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.scheduler.date')
    @patch('builtins.open', new_callable=mock_open, read_data="[]") # Empty YAML list
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_no_snacks(self, mock_parse_args, mock_file, mock_date, mock_stdout):
        mock_parse_args.return_value.config = "empty_snacks.yaml"
        mock_parse_args.return_value.warning_days = 90
        mock_date.today.return_value = date(2024, 1, 15)
        mock_date.fromisoformat = date.fromisoformat

        main()
        output = mock_stdout.getvalue()
        self.assertIn("No snacks found in inventory.", output)
        mock_file.assert_called_once_with("empty_snacks.yaml", 'r')

if __name__ == '__main__':
    unittest.main()
