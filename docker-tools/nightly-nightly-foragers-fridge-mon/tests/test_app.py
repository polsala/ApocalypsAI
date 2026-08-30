import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import json

# Import the Flask app and database module
from src.app import app, get_spoil_warning
import src.database as database

class TestFridgeMonitor(unittest.TestCase):

    def setUp(self):
        # Set up a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True

        # Mock the database initialization to prevent actual file I/O
        # Mock rationale: We want to test the Flask application logic and spoilage calculation
        # without relying on a real SQLite database file, ensuring tests are fast,
        # deterministic, and don't create side effects on the filesystem.
        with patch('src.database.init_db') as mock_init_db:
            mock_init_db.return_value = None
            database.init_db() # Call it to ensure the mock is active

    @patch('src.database.add_item')
    @patch('src.database.get_all_items')
    def test_index_page_no_items(self, mock_get_all_items, mock_add_item):
        # Mock rationale: Simulate an empty database to test the rendering of the index page
        # when no items are present.
        mock_get_all_items.return_value = []
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No items in your fridge. Time to scavenge!", response.data)

    @patch('src.database.add_item')
    @patch('src.database.get_all_items')
    def test_index_page_with_items(self, mock_get_all_items, mock_add_item):
        # Mock rationale: Simulate a database with specific items to test how the index page
        # displays them, including freshness calculations and warnings.
        today_str = datetime.now().strftime('%Y-%m-%d')
        mock_get_all_items.return_value = [
            {'id': 1, 'name': 'Fresh Berry', 'added_date': today_str, 'spoil_days': 5, 'status': 'fresh'},
            {'id': 2, 'name': 'Mystery Meat', 'added_date': (datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d'), 'spoil_days': 5, 'status': 'fresh'}, # 1 day left
            {'id': 3, 'name': 'Old Ration', 'added_date': (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d'), 'spoil_days': 5, 'status': 'fresh'} # 1 day past spoilage
        ]
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Fresh Berry", response.data)
        self.assertIn(b"Freshness remaining: 5 days", response.data)
        self.assertIn(b"CRITICAL: Only 1 day left!", response.data)
        self.assertIn(b"is 1 days past its prime", response.data)

    @patch('src.database.add_item')
    def test_add_item(self, mock_add_item):
        # Mock rationale: Verify that the Flask route correctly calls the database function
        # with the provided form data. We don't need to test the database's internal logic here.
        mock_add_item.return_value = 1 # Simulate a successful add
        response = self.app.post('/add', data={'name': 'New Scavenge', 'spoil_days': '7'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        mock_add_item.assert_called_once_with('New Scavenge', 7)
        self.assertIn(b"Current Inventory", response.data)

    @patch('src.database.update_item_status')
    def test_update_status_consumed(self, mock_update_item_status):
        # Mock rationale: Verify that the Flask route correctly calls the database function
        # to update an item's status.
        response = self.app.post('/update_status/1/consumed', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        mock_update_item_status.assert_called_once_with(1, 'consumed')
        self.assertIn(b"Current Inventory", response.data)

    @patch('src.database.update_item_status')
    def test_update_status_spoiled(self, mock_update_item_status):
        # Mock rationale: Verify that the Flask route correctly calls the database function
        # to update an item's status.
        response = self.app.post('/update_status/2/spoiled', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        mock_update_item_status.assert_called_once_with(2, 'spoiled')
        self.assertIn(b"Current Inventory", response.data)

    def test_get_spoil_warning_fresh(self):
        # Test the spoilage warning logic directly
        today_str = datetime.now().strftime('%Y-%m-%d')
        warning, days_left = get_spoil_warning(today_str, 5)
        self.assertIsNone(warning)
        self.assertEqual(days_left, 5)

    def test_get_spoil_warning_one_day_left(self):
        today_str = (datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d')
        warning, days_left = get_spoil_warning(today_str, 5)
        self.assertIn("CRITICAL: Only 1 day left!", warning)
        self.assertIsNone(days_left)

    def test_get_spoil_warning_spoils_today(self):
        today_str = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        warning, days_left = get_spoil_warning(today_str, 5)
        self.assertIn("WARNING: This item spoils TODAY!", warning)
        self.assertIsNone(days_left)

    def test_get_spoil_warning_past_spoilage(self):
        today_str = (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d')
        warning, days_left = get_spoil_warning(today_str, 5)
        self.assertIn("is 1 days past its prime", warning)
        self.assertIsNone(days_left)

    def test_get_spoil_warning_multiple_days_past_spoilage(self):
        today_str = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
        warning, days_left = get_spoil_warning(today_str, 5)
        self.assertIn("is 5 days past its prime", warning)
        self.assertIsNone(days_left)

    def test_get_spoil_warning_three_days_left(self):
        today_str = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
        warning, days_left = get_spoil_warning(today_str, 5)
        self.assertIn("ALERT: Only 3 days left!", warning)
        self.assertIsNone(days_left)

# Mock the database module for tests that don't explicitly patch it,
# ensuring no real database operations occur during any test run.
# Mock rationale: This global patch ensures that even if a test doesn't
# explicitly mock database calls, no actual file I/O happens, maintaining
# test isolation and determinism.
database.get_db_connection = MagicMock(return_value=MagicMock())
database.init_db = MagicMock()
database.add_item = MagicMock()
database.get_all_items = MagicMock(return_value=[])
database.update_item_status = MagicMock()

if __name__ == '__main__':
    unittest.main()
