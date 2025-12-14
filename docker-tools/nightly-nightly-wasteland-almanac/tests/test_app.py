import unittest
import os
import sys
from datetime import datetime
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Mock rationale: We need to mock the 'datetime' module to ensure that
# datetime.now() returns a predictable value, making the "daily wisdom"
# selection deterministic for testing purposes.
# We also mock file I/O to prevent actual disk access during tests,
# ensuring tests are fast, isolated, and offline.

class TestWastelandAlmanac(unittest.TestCase):

    def setUp(self):
        # Mock rationale: Ensure Flask app is created in a test context
        # without running the actual server.
        from app import app
        self.app = app.test_client()
        self.app.testing = True

        # Create a temporary data directory and files for testing
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
        os.makedirs(self.test_data_dir, exist_ok=True)

        self.wisdom_content = [
            "Test Wisdom 1",
            "Test Wisdom 2",
            "Test Wisdom 3"
        ]
        self.foraging_content = [
            "Test Foraging Tip 1",
            "Test Foraging Tip 2"
        ]
        self.lore_content = [
            "Test Lore 1"
        ]

        with open(os.path.join(self.test_data_dir, 'wisdom.txt'), 'w') as f:
            f.write('\n'.join(self.wisdom_content))
        with open(os.path.join(self.test_data_dir, 'foraging_tips.txt'), 'w') as f:
            f.write('\n'.join(self.foraging_content))
        with open(os.path.join(self.test_data_dir, 'lore.txt'), 'w') as f:
            f.write('\n'.join(self.lore_content))

        # Mock rationale: Patch DATA_DIR to point to our test data directory
        # so load_data reads from our controlled test files.
        self.patcher_data_dir = patch('app.DATA_DIR', self.test_data_dir)
        self.patcher_data_dir.start()

    def tearDown(self):
        self.patcher_data_dir.stop()
        # Clean up temporary test data directory
        for f in os.listdir(self.test_data_dir):
            os.remove(os.path.join(self.test_data_dir, f))
        os.rmdir(self.test_data_dir)

    @patch('app.datetime')
    def test_index_page_content(self, mock_datetime):
        # Mock rationale: Set a specific date to ensure deterministic daily wisdom selection.
        # This makes the random.seed(day_of_year) in app.py predictable.
        mock_datetime.now.return_value = datetime(2023, 1, 15) # Day of year 15
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow other datetime calls

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The Nightly Wasteland Almanac", response.data)
        self.assertIn(b"Today's Wisdom", response.data)
        self.assertIn(b"Foraging Tips", response.data)
        self.assertIn(b"Wasteland Lore", response.data)

        # Check for specific content from our mocked data files
        # Based on day_of_year 15 and random.seed, 'Test Wisdom 2' (index 1) should be selected.
        self.assertIn(self.wisdom_content[1].encode('utf-8'), response.data)
        self.assertNotIn(self.wisdom_content[0].encode('utf-8'), response.data)
        self.assertNotIn(self.wisdom_content[2].encode('utf-8'), response.data)
        
        for tip in self.foraging_content:
            self.assertIn(tip.encode('utf-8'), response.data)
        
        for lore in self.lore_content:
            self.assertIn(lore.encode('utf-8'), response.data)

    @patch('app.datetime')
    def test_daily_wisdom_determinism(self, mock_datetime):
        # Mock rationale: Test that the daily wisdom is consistent for the same day.
        mock_datetime.now.return_value = datetime(2023, 3, 10) # Day of year 69
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        response1 = self.app.get('/')
        # For day 69, with seed 69, random.choice picks index 0 ('Test Wisdom 1')
        wisdom_day_69 = self.wisdom_content[0]
        self.assertIn(wisdom_day_69.encode('utf-8'), response1.data)

        # Request again for the same day, should be the same wisdom
        response2 = self.app.get('/')
        self.assertIn(wisdom_day_69.encode('utf-8'), response2.data)

        # Mock rationale: Change the date, wisdom should change
        mock_datetime.now.return_value = datetime(2023, 3, 11) # Day of year 70
        response3 = self.app.get('/')
        # For day 70, with seed 70, random.choice picks index 1 ('Test Wisdom 2')
        wisdom_day_70 = self.wisdom_content[1]
        self.assertIn(wisdom_day_70.encode('utf-8'), response3.data)
        self.assertNotIn(wisdom_day_69.encode('utf-8'), response3.data)

    @patch('app.os.path.exists', return_value=False) # Mock rationale: Simulate missing data directory
    @patch('builtins.open', side_effect=FileNotFoundError) # Mock rationale: Simulate FileNotFoundError
    def test_missing_data_files(self, mock_open, mock_exists):
        # Mock rationale: Ensure the app handles missing data files gracefully
        # by returning default messages.
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No wisdom today. Just the wind.", response.data)
        self.assertIn(b"No foraging_tips found. The wastes are silent.", response.data)
        self.assertIn(b"No lore found. The wastes are silent.", response.data)

    def test_load_data_empty_file(self):
        # Mock rationale: Test behavior with an empty data file.
        empty_file_path = os.path.join(self.test_data_dir, 'empty.txt')
        with open(empty_file_path, 'w') as f:
            f.write('')
        
        from app import load_data
        data = load_data('empty.txt')
        self.assertEqual(data, [])

    def test_load_data_with_empty_lines(self):
        # Mock rationale: Test behavior with data files containing empty lines.
        mixed_content_path = os.path.join(self.test_data_dir, 'mixed.txt')
        with open(mixed_content_path, 'w') as f:
            f.write('Item 1\n\nItem 2\n')
        
        from app import load_data
        data = load_data('mixed.txt')
        self.assertEqual(data, ['Item 1', 'Item 2'])

if __name__ == '__main__':
    unittest.main()
