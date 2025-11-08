import unittest
import json
import os
from unittest.mock import patch, mock_open
from datetime import date, timedelta

# Adjust sys.path to allow importing snack_scheduler from the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import snack_scheduler

class TestSnackScheduler(unittest.TestCase):

    def setUp(self):
        # Define a base set of snacks for testing
        self.mock_snacks_data = [
            {
                "name": "Canned Beans",
                "last_checked": "2023-01-15",
                "check_frequency_days": 180
            },
            {
                "name": "MREs",
                "last_checked": "2023-06-01",
                "check_frequency_days": 365
            },
            {
                "name": "Water Purification Tablets",
                "last_checked": "2200-03-10", # Far future, should never be due
                "check_frequency_days": 90
            },
            {
                "name": "Survival Biscuits",
                "last_checked": "2024-07-01",
                "check_frequency_days": 14 # Short frequency
            }
        ]
        self.mock_snacks_json = json.dumps(self.mock_snacks_data)

    @patch('snack_scheduler.date')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_no_items_due(self, mock_stdout, mock_exists, mock_file, mock_date):
        # Mock rationale: Simulate the current date being before any snack is due.
        mock_date.today.return_value = date(2024, 7, 10)
        # Ensure date.fromisoformat works as expected, as it's a static method on the date class
        mock_date.fromisoformat = date.fromisoformat

        mock_file.return_value.read.return_value = self.mock_snacks_json

        snack_scheduler.main()
        output = mock_stdout.getvalue()

        self.assertIn("No items are due for checking. All clear for now!", output)
        self.assertNotIn("Canned Beans", output)
        self.assertNotIn("MREs", output)
        self.assertNotIn("Survival Biscuits", output)

    @patch('snack_scheduler.date')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_some_items_due_today_and_overdue(self, mock_stdout, mock_exists, mock_file, mock_date):
        # Mock rationale: Simulate a current date where some snacks are due today and others are overdue.
        mock_date.today.return_value = date(2024, 7, 15)
        mock_date.fromisoformat = date.fromisoformat

        mock_file.return_value.read.return_value = self.mock_snacks_json

        snack_scheduler.main()
        output = mock_stdout.getvalue()

        self.assertIn("Apocalypse Snack Scheduler Report (Today: 2024-07-15)", output)
        self.assertIn("Items due for checking:", output)
        self.assertIn("- Canned Beans - Overdue since 2023-07-14 (Last checked: 2023-01-15)", output)
        self.assertIn("- Survival Biscuits - Due today since 2024-07-15 (Last checked: 2024-07-01)", output)
        self.assertNotIn("MREs", output) # MREs next check would be 2024-06-01 + 365 days = 2025-06-01
        self.assertNotIn("Water Purification Tablets", output)

    @patch('snack_scheduler.date')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_config_file_not_found(self, mock_stdout, mock_exists, mock_file, mock_date):
        # Mock rationale: Simulate the configuration file not existing.
        mock_date.today.return_value = date(2024, 7, 15)
        snack_scheduler.main()
        output = mock_stdout.getvalue()
        self.assertIn(f"Error: Configuration file '{snack_scheduler.CONFIG_FILE}' not found.", output)

    @patch('snack_scheduler.date')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_invalid_json_config(self, mock_stdout, mock_exists, mock_file, mock_date):
        # Mock rationale: Simulate a malformed JSON configuration file.
        mock_date.today.return_value = date(2024, 7, 15)
        mock_file.return_value.read.return_value = "{invalid json"
        snack_scheduler.main()
        output = mock_stdout.getvalue()
        self.assertIn(f"Error: Invalid JSON in '{snack_scheduler.CONFIG_FILE}'.", output)

    @patch('snack_scheduler.date')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_invalid_item_data(self, mock_stdout, mock_exists, mock_file, mock_date):
        # Mock rationale: Simulate a configuration with missing or invalid fields for an item.
        invalid_data = [
            {
                "name": "Missing Last Checked",
                "check_frequency_days": 30
            },
            {
                "name": "Invalid Frequency",
                "last_checked": "2024-01-01",
                "check_frequency_days": "not_an_int"
            },
            {
                "name": "Invalid Date Format",
                "last_checked": "2024/01/01",
                "check_frequency_days": 30
            }
        ]
        mock_date.today.return_value = date(2024, 7, 15)
        mock_date.fromisoformat = date.fromisoformat

        mock_file.return_value.read.return_value = json.dumps(invalid_data)

        snack_scheduler.main()
        output = mock_stdout.getvalue()

        self.assertIn("Warning: Skipping item 'Missing Last Checked' due to missing or invalid 'last_checked' or 'check_frequency_days'.", output)
        self.assertIn("Warning: Skipping item 'Invalid Frequency' due to missing or invalid 'last_checked' or 'check_frequency_days'.", output)
        self.assertIn("Warning: Skipping item 'Invalid Date Format' due to invalid 'last_checked' date format: '2024/01/01'.", output)
        self.assertIn("No items are due for checking. All clear for now!", output) # Since all were skipped/invalid

    @patch('snack_scheduler.date')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_empty_config(self, mock_stdout, mock_exists, mock_file, mock_date):
        # Mock rationale: Simulate an empty list in the configuration file.
        mock_date.today.return_value = date(2024, 7, 15)
        mock_file.return_value.read.return_value = json.dumps([])
        snack_scheduler.main()
        output = mock_stdout.getvalue()
        self.assertIn("No items are due for checking. All clear for now!", output)
