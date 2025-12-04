import unittest
from unittest.mock import mock_open, patch
import json
from datetime import datetime

from src.auditor import load_cache, audit_cache, generate_report, suggest_restock

class TestAuditor(unittest.TestCase):

    def setUp(self):
        self.mock_cache_data = {
            "cache_name": "Test Stash",
            "location": "Sector Alpha",
            "items": [
                {
                    "name": "Water Bottle",
                    "quantity": 5,
                    "unit": "bottles",
                    "expiry_date": "2025-01-01",
                    "min_quantity": 3
                },
                {
                    "name": "MRE",
                    "quantity": 2,
                    "unit": "packs",
                    "expiry_date": "2024-06-15",
                    "min_quantity": 5
                },
                {
                    "name": "First Aid Kit",
                    "quantity": 1,
                    "unit": "kit",
                    "expiry_date": None,
                    "min_quantity": 1
                },
                {
                    "name": "Canned Beans",
                    "quantity": 10,
                    "unit": "cans",
                    "expiry_date": "2023-03-01",
                    "min_quantity": 5
                },
                {
                    "name": "Batteries",
                    "quantity": 0,
                    "unit": "units",
                    "expiry_date": "2026-01-01",
                    "min_quantity": 2
                }
            ]
        }
        self.current_date_str = "2024-07-20"

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_cache_success(self, mock_json_load, mock_file_open):
        # Mock rationale: We don't want to hit the filesystem. `mock_open` simulates file opening,
        # and `json.load` is mocked to return our predefined data, ensuring deterministic input.
        mock_json_load.return_value = self.mock_cache_data
        
        result = load_cache('dummy_path.json')
        mock_file_open.assert_called_once_with('dummy_path.json', 'r')
        self.assertEqual(result, self.mock_cache_data)

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_cache_file_not_found(self, mock_file_open):
        # Mock rationale: Simulates a non-existent file without actual filesystem interaction.
        # `print` output is captured to ensure the error message is correct.
        with patch('builtins.print') as mock_print:
            result = load_cache('non_existent.json')
            self.assertIsNone(result)
            mock_print.assert_called_once_with("Error: Cache file not found at non_existent.json")

    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('json.load', side_effect=json.JSONDecodeError('Expecting value', 'invalid json', 0))
    def test_load_cache_invalid_json(self, mock_json_load, mock_file_open):
        # Mock rationale: Simulates a file with malformed JSON content.
        # `json.load` is mocked to raise the specific error, and `print` is captured.
        with patch('builtins.print') as mock_print:
            result = load_cache('invalid.json')
            self.assertIsNone(result)
            mock_print.assert_called_once_with("Error: Invalid JSON format in invalid.json")

    def test_audit_cache(self):
        audited = audit_cache(self.mock_cache_data, self.current_date_str)
        self.assertIsNotNone(audited)
        self.assertEqual(audited['cache_name'], "Test Stash")
        self.assertEqual(len(audited['items']), 5)

        # Water Bottle: OK
        self.assertFalse(audited['items'][0]['is_expired'])
        self.assertFalse(audited['items'][0]['is_low_stock'])

        # MRE: Low Stock
        self.assertFalse(audited['items'][1]['is_expired'])
        self.assertTrue(audited['items'][1]['is_low_stock'])

        # First Aid Kit: OK (no expiry)
        self.assertFalse(audited['items'][2]['is_expired'])
        self.assertFalse(audited['items'][2]['is_low_stock'])

        # Canned Beans: Expired
        self.assertTrue(audited['items'][3]['is_expired'])
        self.assertFalse(audited['items'][3]['is_low_stock'])

        # Batteries: Low Stock and not expired
        self.assertFalse(audited['items'][4]['is_expired'])
        self.assertTrue(audited['items'][4]['is_low_stock'])

    def test_audit_cache_empty_data(self):
        self.assertIsNone(audit_cache({}, self.current_date_str))
        self.assertIsNone(audit_cache(None, self.current_date_str))

    def test_generate_report(self):
        audited = audit_cache(self.mock_cache_data, self.current_date_str)
        report = generate_report(audited)
        
        self.assertIn("Auditing cache: Test Stash (Sector Alpha)", report)
        self.assertIn("Item: Water Bottle", report)
        self.assertIn("Quantity: 5 bottles (OK)", report)
        self.assertIn("Expiry: 2025-01-01 (OK)", report)
        self.assertIn("Item: MRE", report)
        self.assertIn("Quantity: 2 packs (LOW STOCK - Min: 5)", report)
        self.assertIn("Item: Canned Beans", report)
        self.assertIn("Expiry: 2023-03-01 (EXPIRED!)", report)
        self.assertIn("Item: First Aid Kit", report)
        self.assertIn("Expiry: No expiry date", report)
        self.assertIn("Item: Batteries", report)
        self.assertIn("Quantity: 0 units (LOW STOCK - Min: 2)", report)

    def test_generate_report_no_data(self):
        self.assertEqual(generate_report(None), "No cache data to report.")

    def test_suggest_restock(self):
        audited = audit_cache(self.mock_cache_data, self.current_date_str)
        suggestions = suggest_restock(audited)
        
        self.assertIn("--- Restock Suggestions ---", suggestions)
        self.assertIn("- MRE (Current: 2, Needed: 3)", suggestions)
        self.assertIn("- Canned Beans (Expired, consider replacement)", suggestions)
        self.assertIn("- Batteries (Current: 0, Needed: 2)", suggestions)
        self.assertEqual(len(suggestions), 4) # Header + 3 items

    def test_suggest_restock_all_clear(self):
        all_clear_data = {
            "cache_name": "All Clear",
            "location": "Safe Zone",
            "items": [
                {
                    "name": "Water",
                    "quantity": 10,
                    "unit": "liters",
                    "expiry_date": "2030-01-01",
                    "min_quantity": 5
                }
            ]
        }
        audited = audit_cache(all_clear_data, self.current_date_str)
        suggestions = suggest_restock(audited)
        self.assertIn("--- Restock Suggestions ---", suggestions)
        self.assertIn("- All clear! No immediate restock needed.", suggestions)
        self.assertEqual(len(suggestions), 2)

    def test_main_functionality(self):
        # Mock rationale: `argparse` is mocked to control CLI arguments.
        # `load_cache`, `audit_cache`, `generate_report`, `suggest_restock` are mocked
        # to isolate `main`'s orchestration logic and prevent actual file I/O or complex processing.
        # `print` is mocked to capture output.
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args,
             patch('src.auditor.load_cache') as mock_load_cache,
             patch('src.auditor.audit_cache') as mock_audit_cache,
             patch('src.auditor.generate_report') as mock_generate_report,
             patch('src.auditor.suggest_restock') as mock_suggest_restock,
             patch('builtins.print') as mock_print:

            mock_parse_args.return_value.cache_file = 'test_cache.json'
            mock_parse_args.return_value.current_date = self.current_date_str

            mock_load_cache.return_value = self.mock_cache_data
            mock_audit_cache.return_value = audit_cache(self.mock_cache_data, self.current_date_str)
            mock_generate_report.return_value = "Mock Report"
            mock_suggest_restock.return_value = ["Mock Suggestion 1", "Mock Suggestion 2"]

            from src.auditor import main
            main()

            mock_load_cache.assert_called_once_with('test_cache.json')
            mock_audit_cache.assert_called_once_with(self.mock_cache_data, self.current_date_str)
            mock_generate_report.assert_called_once_with(mock_audit_cache.return_value)
            mock_suggest_restock.assert_called_once_with(mock_audit_cache.return_value)
            mock_print.assert_any_call("Mock Report")
            mock_print.assert_any_call("Mock Suggestion 1\nMock Suggestion 2")

    def test_main_functionality_no_cache_data(self):
        # Mock rationale: Similar to above, but `load_cache` returns None to simulate file errors.
        # This tests the graceful exit path of `main`.
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args,
             patch('src.auditor.load_cache') as mock_load_cache,
             patch('src.auditor.audit_cache') as mock_audit_cache,
             patch('builtins.print') as mock_print:

            mock_parse_args.return_value.cache_file = 'non_existent.json'
            mock_parse_args.return_value.current_date = self.current_date_str

            mock_load_cache.return_value = None # Simulate file not found or invalid JSON

            from src.auditor import main
            main()

            mock_load_cache.assert_called_once_with('non_existent.json')
            mock_audit_cache.assert_not_called() # Should not proceed to audit if load fails
            mock_print.assert_not_called() # No report or suggestions if no cache data
