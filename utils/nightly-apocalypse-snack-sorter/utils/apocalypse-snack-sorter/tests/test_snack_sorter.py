import unittest
import os
import json
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta
import io
import sys

# Adjust path to import snack_sorter from src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from snack_sorter import SnackStash, DATA_FILE, DATE_FORMAT

class TestSnackStash(unittest.TestCase):

    def setUp(self):
        # Ensure a clean state for each test
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def tearDown(self):
        # Clean up after tests
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_snacks_empty_file(self, mock_file, mock_exists):
        # Mock rationale: Simulate an empty or non-existent data file to test initial state.
        mock_exists.return_value = False
        stash = SnackStash()
        self.assertEqual(stash.snacks, [])
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = "[]"
        stash = SnackStash()
        self.assertEqual(stash.snacks, [])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_snacks_existing_data(self, mock_file, mock_exists):
        # Mock rationale: Simulate an existing data file with pre-defined snacks.
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = json.dumps([
            {"name": "Test Bar", "quantity": 1, "expiry": "2025-01-01"}
        ])
        stash = SnackStash()
        self.assertEqual(len(stash.snacks), 1)
        self.assertEqual(stash.snacks[0]["name"], "Test Bar")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print') # Mock print to capture output
    def test_load_snacks_corrupt_data(self, mock_print, mock_file, mock_exists):
        # Mock rationale: Simulate a corrupt JSON file to ensure graceful handling.
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = "{invalid json"
        stash = SnackStash()
        self.assertEqual(stash.snacks, [])
        mock_print.assert_called_with(f"Warning: Could not decode {DATA_FILE}. Starting with empty stash.")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False) # Mock rationale: Ensure no existing file for clean add.
    def test_add_snack(self, mock_exists, mock_file):
        # Mock rationale: Prevent actual file I/O and capture what would be written.
        stash = SnackStash()
        stash.add_snack("Survival Crackers", 3, "2025-06-30")
        self.assertEqual(len(stash.snacks), 1)
        self.assertEqual(stash.snacks[0]["name"], "Survival Crackers")
        mock_file.assert_called_with(DATA_FILE, 'w')
        handle = mock_file()
        handle.write.assert_called_once()
        written_data = json.loads(handle.write.call_args[0][0])
        self.assertEqual(written_data[0]["name"], "Survival Crackers")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    @patch('builtins.print')
    def test_add_snack_invalid_date(self, mock_print, mock_exists, mock_file):
        # Mock rationale: Test error handling for invalid date format without actual file I/O.
        stash = SnackStash()
        stash.add_snack("Bad Date Bar", 1, "2025/06/30")
        self.assertEqual(len(stash.snacks), 0) # Should not add
        mock_print.assert_called_with(f"Error: Invalid expiry date format. Please use YYYY-MM-DD (e.g., {datetime.now().strftime(DATE_FORMAT)}).")
        mock_file.assert_not_called() # Should not attempt to save

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('datetime.datetime') # Mock rationale: Control the current date for deterministic expiry calculations.
    def test_list_snacks(self, mock_dt, mock_stdout, mock_exists, mock_file):
        # Mock rationale: Simulate existing snacks and control current date for consistent output.
        mock_dt.now.return_value = datetime(2024, 1, 1) # Set a fixed "today"
        mock_dt.strptime = datetime.strptime # Allow actual strptime to work
        mock_dt.timedelta = timedelta # Allow actual timedelta to work

        mock_file.return_value.read.return_value = json.dumps([
            {"name": "Fresh Fruit Roll", "quantity": 2, "expiry": "2024-03-01"}, # Expires in 2 months
            {"name": "Ancient Grain Bar", "quantity": 1, "expiry": "2025-01-01"}, # Expires in 1 year
            {"name": "Expired Ration", "quantity": 5, "expiry": "2023-12-01"} # Expired
        ])
        stash = SnackStash()
        stash.list_snacks()
        output = mock_stdout.getvalue()

        self.assertIn("--- Your Apocalypse Snack Stash ---", output)
        self.assertIn("Expired Ration (x5) - Expires: 2023-12-01 (EXPIRED!) 💀", output)
        self.assertIn("Fresh Fruit Roll (x2) - Expires: 2024-03-01 (Expires in 59 days!) ⚠️", output) # 2024-03-01 - 2024-01-01 = 59 days
        self.assertIn("Ancient Grain Bar (x1) - Expires: 2025-01-01", output)
        # Check order: Expired, Fresh, Ancient
        self.assertTrue(output.find("Expired Ration") < output.find("Fresh Fruit Roll"))
        self.assertTrue(output.find("Fresh Fruit Roll") < output.find("Ancient Grain Bar"))

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('datetime.datetime') # Mock rationale: Control the current date for deterministic expiry calculations.
    def test_get_urgent_snacks(self, mock_dt, mock_stdout, mock_exists, mock_file):
        # Mock rationale: Simulate existing snacks and control current date for consistent urgent snack detection.
        mock_dt.now.return_value = datetime(2024, 1, 1) # Set a fixed "today"
        mock_dt.strptime = datetime.strptime # Allow actual strptime to work
        mock_dt.timedelta = timedelta # Allow actual timedelta to work

        mock_file.return_value.read.return_value = json.dumps([
            {"name": "Soon-to-Expire Bar", "quantity": 2, "expiry": "2024-02-15"}, # 45 days
            {"name": "Long-Lasting MRE", "quantity": 1, "expiry": "2025-06-01"}, # Not urgent
            {"name": "Expired Goo", "quantity": 3, "expiry": "2023-11-01"}, # Expired, thus urgent
            {"name": "Week-Away Wafers", "quantity": 4, "expiry": "2024-01-08"} # 7 days
        ])
        stash = SnackStash()
        stash.get_urgent_snacks()
        output = mock_stdout.getvalue()

        self.assertIn("--- Urgent Munchies! (Eat These First!) ---", output)
        self.assertIn("Expired Goo (x3) - Expires: 2023-11-01 (EXPIRED!) 💀", output)
        self.assertIn("Week-Away Wafers (x4) - Expires: 2024-01-08 (Expires in 7 days! DANGER!) 🔥", output)
        self.assertIn("Soon-to-Expire Bar (x2) - Expires: 2024-02-15 (Expires in 45 days!) ⚠️", output)
        self.assertNotIn("Long-Lasting MRE", output) # Should not be urgent

        # Check order: Expired, Week-Away, Soon-to-Expire
        self.assertTrue(output.find("Expired Goo") < output.find("Week-Away Wafers"))
        self.assertTrue(output.find("Week-Away Wafers") < output.find("Soon-to-Expire Bar"))

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_list_empty_stash(self, mock_stdout, mock_exists, mock_file):
        # Mock rationale: Simulate an empty stash to test the "empty" message.
        stash = SnackStash()
        stash.list_snacks()
        output = mock_stdout.getvalue()
        self.assertIn("Your apocalypse snack stash is currently empty. Better stock up!", output)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_urgent_empty_stash(self, mock_stdout, mock_exists, mock_file):
        # Mock rationale: Simulate an empty stash to test the "no urgent" message.
        stash = SnackStash()
        stash.get_urgent_snacks()
        output = mock_stdout.getvalue()
        self.assertIn("Your apocalypse snack stash is currently empty. No urgent munchies needed!", output)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('datetime.datetime')
    def test_no_urgent_snacks_within_threshold(self, mock_dt, mock_stdout, mock_exists, mock_file):
        # Mock rationale: Simulate snacks that are all far from expiry to test the "no urgent" message.
        mock_dt.now.return_value = datetime(2024, 1, 1)
        mock_dt.strptime = datetime.strptime
        mock_dt.timedelta = timedelta

        mock_file.return_value.read.return_value = json.dumps([
            {"name": "Future Feast", "quantity": 1, "expiry": "2024-04-01"}, # 91 days
            {"name": "Eternal Edibles", "quantity": 1, "expiry": "2025-01-01"}
        ])
        stash = SnackStash()
        stash.get_urgent_snacks()
        output = mock_stdout.getvalue()
        self.assertIn("All your snacks are safe for now. Keep calm and carry on munching!", output)


if __name__ == '__main__':
    unittest.main()
