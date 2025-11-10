import unittest
from unittest.mock import patch, mock_open
import json
import os
from datetime import datetime

# Import the class and main function from the utility
from src.tracker import TemporalAnomalyTracker, main

class TestTemporalAnomalyTracker(unittest.TestCase):

    def setUp(self):
        # Define a consistent mock timestamp for all tests
        self.mock_iso_timestamp = '2023-10-27T10:00:00.000000'
        self.mock_datetime_obj = datetime.fromisoformat(self.mock_iso_timestamp)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_anomalies_existing_file(self, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate an existing data file with content.
        mock_os_exists.return_value = True
        mock_json_load.return_value = [{'timestamp': '2023-01-01T12:00:00', 'description': 'Test', 'severity': 1}]

        tracker = TemporalAnomalyTracker()
        self.assertEqual(len(tracker.anomalies), 1)
        self.assertEqual(tracker.anomalies[0]['description'], 'Test')
        mock_file_open.assert_called_once_with('anomalies.json', 'r')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_anomalies_no_file(self, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate no existing data file.
        mock_os_exists.return_value = False

        tracker = TemporalAnomalyTracker()
        self.assertEqual(tracker.anomalies, [])
        mock_file_open.assert_not_called()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_anomalies_malformed_json(self, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate a malformed JSON file.
        mock_os_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)

        tracker = TemporalAnomalyTracker()
        self.assertEqual(tracker.anomalies, [])
        mock_file_open.assert_called_once_with('anomalies.json', 'r')

    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('datetime.datetime')
    def test_add_anomaly(self, mock_datetime, mock_json_dump, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate adding an anomaly without actual file I/O and with a fixed timestamp.
        mock_datetime.now.return_value = self.mock_datetime_obj
        mock_datetime.now().isoformat.return_value = self.mock_iso_timestamp # Ensure isoformat returns consistent string

        tracker = TemporalAnomalyTracker()
        tracker.add_anomaly("Time skipped a beat", 4)

        expected_anomaly = {
            'timestamp': self.mock_iso_timestamp,
            'description': "Time skipped a beat",
            'severity': 4
        }
        self.assertEqual(len(tracker.anomalies), 1)
        self.assertEqual(tracker.anomalies[0], expected_anomaly)
        mock_file_open.assert_called_with('anomalies.json', 'w')
        mock_json_dump.assert_called_once_with([expected_anomaly], mock_file_open(), indent=4)

    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('datetime.datetime')
    def test_add_anomaly_invalid_severity(self, mock_datetime, mock_json_dump, mock_file_open, mock_os_exists):
        # Mock rationale: Test input validation without actual file I/O.
        tracker = TemporalAnomalyTracker()
        with self.assertRaises(ValueError):
            tracker.add_anomaly("Too severe", 6)
        with self.assertRaises(ValueError):
            tracker.add_anomaly("Not severe enough", 0)
        mock_json_dump.assert_not_called()

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_list_anomalies(self, mock_stdout, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate loading existing anomalies and capturing print output.
        mock_json_load.return_value = [
            {'timestamp': '2023-01-01T12:00:00', 'description': 'Deja vu loop', 'severity': 3},
            {'timestamp': '2023-01-02T13:00:00', 'description': 'Lost an hour', 'severity': 5}
        ]

        tracker = TemporalAnomalyTracker()
        tracker.list_anomalies()

        output = mock_stdout.getvalue()
        self.assertIn("Deja vu loop", output)
        self.assertIn("Lost an hour", output)
        self.assertIn("Severity: 3/5", output)
        self.assertIn("Severity: 5/5", output)

    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', return_value=[])
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_list_anomalies_empty(self, mock_stdout, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate no anomalies recorded and capture print output.
        tracker = TemporalAnomalyTracker()
        tracker.list_anomalies()

        output = mock_stdout.getvalue()
        self.assertIn("No temporal anomalies recorded yet.", output)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_export_anomalies(self, mock_json_dump, mock_json_load, mock_file_open, mock_os_exists):
        # Mock rationale: Simulate exporting anomalies to a file without actual file I/O.
        mock_anomalies = [
            {'timestamp': '2023-01-01T12:00:00', 'description': 'Export Test', 'severity': 2}
        ]
        mock_json_load.return_value = mock_anomalies

        tracker = TemporalAnomalyTracker()
        tracker.export_anomalies('export_data.json')

        mock_file_open.assert_called_with('export_data.json', 'w')
        mock_json_dump.assert_called_once_with(mock_anomalies, mock_file_open(), indent=4)

    @patch('sys.argv', ['tracker.py', 'add', 'A ripple in the spacetime continuum', '--severity', '3'])
    @patch('src.tracker.TemporalAnomalyTracker')
    def test_main_add_command(self, MockTemporalAnomalyTracker):
        # Mock rationale: Simulate CLI arguments and ensure the correct method is called on the tracker instance.
        mock_tracker_instance = MockTemporalAnomalyTracker.return_value
        main()
        mock_tracker_instance.add_anomaly.assert_called_once_with('A ripple in the spacetime continuum', 3)

    @patch('sys.argv', ['tracker.py', 'list'])
    @patch('src.tracker.TemporalAnomalyTracker')
    def test_main_list_command(self, MockTemporalAnomalyTracker):
        # Mock rationale: Simulate CLI arguments and ensure the correct method is called on the tracker instance.
        mock_tracker_instance = MockTemporalAnomalyTracker.return_value
        main()
        mock_tracker_instance.list_anomalies.assert_called_once()

    @patch('sys.argv', ['tracker.py', 'export', 'my_anomalies.json'])
    @patch('src.tracker.TemporalAnomalyTracker')
    def test_main_export_command(self, MockTemporalAnomalyTracker):
        # Mock rationale: Simulate CLI arguments and ensure the correct method is called on the tracker instance.
        mock_tracker_instance = MockTemporalAnomalyTracker.return_value
        main()
        mock_tracker_instance.export_anomalies.assert_called_once_with('my_anomalies.json')

    @patch('sys.argv', ['tracker.py', 'add', 'Invalid severity'])
    @patch('src.tracker.TemporalAnomalyTracker')
    @patch('builtins.print')
    def test_main_add_command_invalid_severity_error_handling(self, mock_print, MockTemporalAnomalyTracker):
        # Mock rationale: Simulate CLI arguments and an invalid severity, checking error handling.
        mock_tracker_instance = MockTemporalAnomalyTracker.return_value
        mock_tracker_instance.add_anomaly.side_effect = ValueError("Severity must be an integer between 1 and 5.")
        main()
        mock_print.assert_called_with("Error: Severity must be an integer between 1 and 5.")
