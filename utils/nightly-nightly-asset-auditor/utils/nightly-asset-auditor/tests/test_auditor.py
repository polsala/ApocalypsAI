import unittest
import json
import os
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta
from io import StringIO

# Assuming auditor.py is in the parent directory of tests/
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from auditor import AssetAuditor, ASSETS_FILE, DATE_FORMAT

class TestAssetAuditor(unittest.TestCase):

    def setUp(self):
        # Ensure a clean state for each test
        self.test_assets_file = "test_assets.json"
        if os.path.exists(self.test_assets_file):
            os.remove(self.test_assets_file)

        # Mock datetime.now() for deterministic tests
        self.mock_now = datetime(2023, 10, 27, 10, 0, 0)
        self.mock_now_str = self.mock_now.strftime(DATE_FORMAT)

    def tearDown(self):
        if os.path.exists(self.test_assets_file):
            os.remove(self.test_assets_file)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_init_store_new_file(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate the file not existing to test initialization.
        mock_exists.return_value = False
        auditor = AssetAuditor(self.test_assets_file)
        auditor.init_store()

        mock_exists.assert_called_with(self.test_assets_file)
        mock_file_open.assert_called_with(self.test_assets_file, 'w')
        mock_file_open().write.assert_called_once_with('[]')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_init_store_existing_file(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate the file existing to test no-op behavior.
        mock_exists.return_value = True
        auditor = AssetAuditor(self.test_assets_file)
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            auditor.init_store()
            self.assertIn("already exists", mock_stdout.getvalue())
        mock_file_open.assert_not_called() # Should not open for writing if exists

    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    @patch('auditor.datetime') # Mock rationale: Control the timestamp for deterministic tests.
    def test_add_asset(self, mock_datetime, mock_file_open, mock_exists):
        mock_datetime.now.return_value = self.mock_now
        mock_datetime.strptime = datetime.strptime # Keep original strptime

        auditor = AssetAuditor(self.test_assets_file)
        auditor.add_asset("Secret Plans", "Document", "/docs/plans.txt", "Top secret plans", "Encrypted USB")

        expected_assets = [{
            "name": "Secret Plans",
            "type": "Document",
            "path_or_url": "/docs/plans.txt",
            "description": "Top secret plans",
            "backup_location": "Encrypted USB",
            "last_audited": self.mock_now_str,
        }]
        mock_file_open.assert_called_with(self.test_assets_file, 'w')
        mock_file_open().write.assert_called_once_with(json.dumps(expected_assets, indent=4))
        self.assertEqual(auditor.assets, expected_assets)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('auditor.datetime') # Mock rationale: Control the timestamp for deterministic tests.
    def test_add_asset_duplicate(self, mock_datetime, mock_file_open, mock_exists):
        mock_datetime.now.return_value = self.mock_now
        mock_datetime.strptime = datetime.strptime # Keep original strptime

        initial_assets = [{
            "name": "Secret Plans",
            "type": "Document",
            "path_or_url": "/docs/plans.txt",
            "description": "Top secret plans",
            "backup_location": "Encrypted USB",
            "last_audited": self.mock_now_str,
        }]
        mock_file_open.return_value.read.return_value = json.dumps(initial_assets)

        auditor = AssetAuditor(self.test_assets_file)
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            auditor.add_asset("Secret Plans", "Document", "/docs/plans.txt", "Top secret plans", "Encrypted USB")
            self.assertIn("Error: Asset with name 'Secret Plans' already exists.", mock_stdout.getvalue())
        
        # Should not have called write again
        mock_file_open.assert_called_with(self.test_assets_file, 'r') # Only read
        self.assertEqual(auditor.assets, initial_assets) # Assets should remain unchanged

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('auditor.datetime') # Mock rationale: Control the timestamp for deterministic tests.
    def test_update_asset(self, mock_datetime, mock_file_open, mock_exists):
        initial_now = datetime(2023, 10, 26, 9, 0, 0)
        updated_now = datetime(2023, 10, 27, 10, 0, 0)
        mock_datetime.now.side_effect = [initial_now, updated_now]
        mock_datetime.strptime = datetime.strptime # Keep original strptime

        initial_assets = [{
            "name": "Secret Plans",
            "type": "Document",
            "path_or_url": "/docs/plans.txt",
            "description": "Top secret plans",
            "backup_location": "Encrypted USB",
            "last_audited": initial_now.strftime(DATE_FORMAT),
        }]
        mock_file_open.return_value.read.return_value = json.dumps(initial_assets)

        auditor = AssetAuditor(self.test_assets_file)
        auditor.update_asset("Secret Plans", new_path_or_url="/docs/plans_v2.txt", new_backup_location="Cloud Vault")

        expected_assets = [{
            "name": "Secret Plans",
            "type": "Document",
            "path_or_url": "/docs/plans_v2.txt",
            "description": "Top secret plans",
            "backup_location": "Cloud Vault",
            "last_audited": updated_now.strftime(DATE_FORMAT),
        }]
        # First call to open is for reading, second for writing
        mock_file_open.assert_any_call(self.test_assets_file, 'r')
        mock_file_open.assert_any_call(self.test_assets_file, 'w')
        mock_file_open().write.assert_called_once_with(json.dumps(expected_assets, indent=4))
        self.assertEqual(auditor.assets, expected_assets)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('auditor.datetime') # Mock rationale: Control the timestamp for deterministic tests.
    def test_audit_asset(self, mock_datetime, mock_file_open, mock_exists):
        initial_now = datetime(2023, 10, 26, 9, 0, 0)
        audited_now = datetime(2023, 10, 27, 10, 0, 0)
        mock_datetime.now.side_effect = [initial_now, audited_now]
        mock_datetime.strptime = datetime.strptime # Keep original strptime

        initial_assets = [{
            "name": "Emergency Kit List",
            "type": "Document",
            "path_or_url": "/docs/kit.md",
            "description": "List of emergency supplies",
            "backup_location": "Printed Copy",
            "last_audited": initial_now.strftime(DATE_FORMAT),
        }]
        mock_file_open.return_value.read.return_value = json.dumps(initial_assets)

        auditor = AssetAuditor(self.test_assets_file)
        auditor.audit_asset("Emergency Kit List")

        expected_assets = [{
            "name": "Emergency Kit List",
            "type": "Document",
            "path_or_url": "/docs/kit.md",
            "description": "List of emergency supplies",
            "backup_location": "Printed Copy",
            "last_audited": audited_now.strftime(DATE_FORMAT),
        }]
        mock_file_open.assert_any_call(self.test_assets_file, 'r')
        mock_file_open.assert_any_call(self.test_assets_file, 'w')
        mock_file_open().write.assert_called_once_with(json.dumps(expected_assets, indent=4))
        self.assertEqual(auditor.assets, expected_assets)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('auditor.datetime') # Mock rationale: Control the timestamp for deterministic tests.
    def test_find_stale_assets(self, mock_datetime, mock_file_open, mock_exists):
        current_time = datetime(2023, 10, 27, 10, 0, 0)
        mock_datetime.now.return_value = current_time
        mock_datetime.strptime = datetime.strptime # Keep original strptime

        stale_asset_time = current_time - timedelta(days=31)
        fresh_asset_time = current_time - timedelta(days=15)

        initial_assets = [
            {
                "name": "Very Stale Doc",
                "type": "Document",
                "path_or_url": "/docs/stale.txt",
                "description": "Old document",
                "backup_location": "Archive",
                "last_audited": stale_asset_time.strftime(DATE_FORMAT),
            },
            {
                "name": "Fresh Report",
                "type": "Report",
                "path_or_url": "/reports/fresh.pdf",
                "description": "Recent report",
                "backup_location": "Cloud",
                "last_audited": fresh_asset_time.strftime(DATE_FORMAT),
            },
        ]
        mock_file_open.return_value.read.return_value = json.dumps(initial_assets)

        auditor = AssetAuditor(self.test_assets_file)
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            stale_assets = auditor.find_stale_assets(days=30)
            self.assertIn("Very Stale Doc", mock_stdout.getvalue())
            self.assertNotIn("Fresh Report", mock_stdout.getvalue())

        self.assertEqual(len(stale_assets), 1)
        self.assertEqual(stale_assets[0]['name'], "Very Stale Doc")

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_list_assets(self, mock_file_open, mock_exists):
        initial_assets = [{
            "name": "Test Asset",
            "type": "Test Type",
            "path_or_url": "/test/path",
            "description": "A test asset",
            "backup_location": "Test Backup",
            "last_audited": "2023-01-01T12:00:00",
        }]
        mock_file_open.return_value.read.return_value = json.dumps(initial_assets)

        auditor = AssetAuditor(self.test_assets_file)
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            auditor.list_assets()
            output = mock_stdout.getvalue()
            self.assertIn("Test Asset", output)
            self.assertIn("Test Type", output)
            self.assertIn("/test/path", output)
            self.assertIn("A test asset", output)
            self.assertIn("Test Backup", output)
            self.assertIn("2023-01-01T12:00:00", output)

    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    def test_list_assets_empty(self, mock_file_open, mock_exists):
        auditor = AssetAuditor(self.test_assets_file) # Loads empty assets
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            auditor.list_assets()
            self.assertIn("No assets found.", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
