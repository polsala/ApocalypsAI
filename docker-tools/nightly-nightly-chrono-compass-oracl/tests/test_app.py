import unittest
import json
from unittest.mock import patch
import datetime
# Assuming app.py is in src/ and tests are run from the root of the utility
from src.app import app, get_daily_alignment

class TestChronoCompassOracle(unittest.TestCase):

    def setUp(self):
        # Set up a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True

    def test_get_daily_alignment_determinism(self):
        """Tests that get_daily_alignment produces the same output for the same date."""
        # Test determinism for a specific date
        test_date = datetime.date(2023, 10, 27)
        alignment1 = get_daily_alignment(test_date)
        alignment2 = get_daily_alignment(test_date)
        self.assertEqual(alignment1, alignment2, "Alignment should be deterministic for the same date.")

        # Test that different dates produce different alignments (highly probable, but not guaranteed due to random.seed)
        # For practical purposes, with enough choices, this is a reasonable test.
        test_date_plus_one = datetime.date(2023, 10, 28)
        alignment3 = get_daily_alignment(test_date_plus_one)
        self.assertNotEqual(alignment1, alignment3, "Alignments for different dates should typically differ.")

    @patch('src.app.datetime') # Mock rationale: Ensures deterministic date for testing the API endpoint, making tests repeatable and independent of the current system date.
    def test_align_endpoint(self, mock_datetime):
        """Tests the /align endpoint for correct structure and content for a specific mocked date."""
        # Mock datetime.date.today() to return a fixed date
        fixed_date = datetime.date(2023, 1, 1)
        mock_datetime.date.today.return_value = fixed_date
        # Ensure the original date and datetime classes are available for methods like isoformat()
        mock_datetime.date = datetime.date
        mock_datetime.datetime = datetime.datetime

        response = self.app.get('/align')
        self.assertEqual(response.status_code, 200, "Expected a 200 OK status code.")
        data = json.loads(response.data.decode('utf-8'))

        self.assertIn("date", data, "Response should contain 'date' field.")
        self.assertIn("alignment", data, "Response should contain 'alignment' field.")
        self.assertIn("oracle_name", data, "Response should contain 'oracle_name' field.")
        self.assertEqual(data["date"], fixed_date.isoformat(), "Date in response should match mocked date.")
        self.assertEqual(data["oracle_name"], "Chrono-Compass Oracle", "Oracle name should be correct.")

        # Verify the alignment message is as expected for this specific mocked date
        expected_alignment = get_daily_alignment(fixed_date)
        self.assertEqual(data["alignment"], expected_alignment, "Alignment message should match deterministic generation.")

    @patch('src.app.datetime') # Mock rationale: Ensures deterministic date for testing the API endpoint with a different fixed date, verifying consistency across dates.
    def test_align_endpoint_different_date(self, mock_datetime):
        """Tests the /align endpoint with a different mocked date to ensure determinism holds."""
        # Mock datetime.date.today() to return a different fixed date
        fixed_date = datetime.date(2024, 2, 15)
        mock_datetime.date.today.return_value = fixed_date
        mock_datetime.date = datetime.date
        mock_datetime.datetime = datetime.datetime

        response = self.app.get('/align')
        self.assertEqual(response.status_code, 200, "Expected a 200 OK status code for the second date.")
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(data["date"], fixed_date.isoformat(), "Date in response for second date should match mocked date.")
        expected_alignment = get_daily_alignment(fixed_date)
        self.assertEqual(data["alignment"], expected_alignment, "Alignment message for second date should match deterministic generation.")

if __name__ == '__main__':
    unittest.main()
