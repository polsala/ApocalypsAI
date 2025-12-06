import unittest
import os
from unittest.mock import patch, mock_open
from src.analyzer import LogAnalyzer

class TestLogAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = LogAnalyzer()

    def test_analyze_empty_content(self):
        log_content = ""
        events = self.analyzer.analyze_log_content(log_content)
        self.assertEqual(len(events), 0)

    def test_analyze_no_cataclysmic_events(self):
        log_content = (
            "INFO: Application started successfully\n"
            "DEBUG: Processing user request 123\n"
            "INFO: User logged in: testuser"
        )
        events = self.analyzer.analyze_log_content(log_content)
        self.assertEqual(len(events), 0)

    def test_analyze_single_error_event(self):
        log_content = (
            "INFO: Application started\n"
            "ERROR: Failed to connect to database\n"
            "INFO: User activity"
        )
        events = self.analyzer.analyze_log_content(log_content, 'app.log')
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['filename'], 'app.log')
        self.assertEqual(events[0]['line_num'], 2)
        self.assertEqual(events[0]['level'], 'ERROR')
        self.assertIn('Failed to connect to database', events[0]['message'])

    def test_analyze_multiple_event_types(self):
        log_content = (
            "INFO: System heartbeat\n"
            "WARNING: Disk space low\n"
            "CRITICAL: Core meltdown imminent!\n"
            "DEBUG: Temp file cleanup\n"
            "ERROR: Service unavailable\n"
            "APOCALYPSE: The end is nigh!"
        )
        events = self.analyzer.analyze_log_content(log_content, 'system.log')
        self.assertEqual(len(events), 5)

        # Check specific events
        self.assertEqual(events[0]['level'], 'WARNING')
        self.assertEqual(events[0]['line_num'], 2)
        self.assertIn('Disk space low', events[0]['message'])

        self.assertEqual(events[1]['level'], 'CRITICAL')
        self.assertEqual(events[1]['line_num'], 3)
        self.assertIn('Core meltdown imminent!', events[1]['message'])

        self.assertEqual(events[2]['level'], 'ERROR')
        self.assertEqual(events[2]['line_num'], 5)
        self.assertIn('Service unavailable', events[2]['message'])

        self.assertEqual(events[3]['level'], 'CRITICAL') # APOCALYPSE maps to CRITICAL
        self.assertEqual(events[3]['line_num'], 6)
        self.assertIn('The end is nigh!', events[3]['message'])

    def test_analyze_case_insensitivity(self):
        log_content = (
            "warning: low memory\n"
            "Error: file not found\n"
            "critical: system halt"
        )
        events = self.analyzer.analyze_log_content(log_content)
        self.assertEqual(len(events), 3)
        self.assertEqual(events[0]['level'], 'WARNING')
        self.assertEqual(events[1]['level'], 'ERROR')
        self.assertEqual(events[2]['level'], 'CRITICAL')

    def test_parse_log_file_success(self):
        mock_file_content = (
            "INFO: Normal operation\n"
            "ERROR: Something went wrong\n"
            "WARNING: Minor issue"
        )
        # Mock rationale: We need to simulate reading a file without actually touching the filesystem.
        # `mock_open` allows us to provide a string as the file content.
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as m_open:
            # Mock rationale: os.path.exists is called by parse_log_file. We need to ensure it returns True
            # so that the file reading logic is executed.
            with patch('os.path.exists', return_value=True):
                events = self.analyzer.parse_log_file('dummy.log')
                self.assertEqual(len(events), 2)
                self.assertEqual(events[0]['level'], 'ERROR')
                self.assertEqual(events[1]['level'], 'WARNING')
                m_open.assert_called_once_with('dummy.log', 'r', encoding='utf-8')

    def test_parse_log_file_not_found(self):
        # Mock rationale: Simulate a file not existing on the filesystem.
        with patch('os.path.exists', return_value=False):
            # Mock rationale: Suppress print statements to avoid polluting test output.
            with patch('builtins.print') as mock_print:
                events = self.analyzer.parse_log_file('non_existent.log')
                self.assertEqual(len(events), 0)
                mock_print.assert_called_once_with("Error: Log file not found at 'non_existent.log'")

    def test_parse_log_file_read_error(self):
        # Mock rationale: Simulate an IOError during file reading.
        with patch('builtins.open', mock_open()) as m_open:
            m_open.side_effect = IOError("Permission denied")
            # Mock rationale: os.path.exists is called by parse_log_file. We need to ensure it returns True
            # so that the file reading logic is executed.
            with patch('os.path.exists', return_value=True):
                # Mock rationale: Suppress print statements to avoid polluting test output.
                with patch('builtins.print') as mock_print:
                    events = self.analyzer.parse_log_file('unreadable.log')
                    self.assertEqual(len(events), 0)
                    mock_print.assert_called_once_with("Error reading file 'unreadable.log': Permission denied")

    def test_keyword_priority_single_line(self):
        # Test that only the highest priority matching keyword is reported per line
        # Based on the order in self.keywords dict (Python 3.7+ preserves insertion order)
        log_content = "This line contains a FATAL error and a WARNING."
        events = self.analyzer.analyze_log_content(log_content)
        self.assertEqual(len(events), 1)
        # FATAL maps to CRITICAL and is listed before WARNING in the keywords dict
        self.assertEqual(events[0]['level'], 'CRITICAL') 
        self.assertIn('FATAL error and a WARNING', events[0]['message'])

        log_content_2 = "An ERROR occurred, but also a CRITICAL system failure."
        events_2 = self.analyzer.analyze_log_content(log_content_2)
        self.assertEqual(len(events_2), 1)
        # CRITICAL is listed before ERROR in the keywords dict
        self.assertEqual(events_2[0]['level'], 'CRITICAL')
        self.assertIn('CRITICAL system failure', events_2[0]['message'])
