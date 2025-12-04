import unittest
import json
import os
import sys
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta

# Adjust sys.path to allow importing the module from src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import echo_recorder
sys.path.pop(0)

class TestEchoRecorder(unittest.TestCase):

    def setUp(self):
        # Ensure ECHOES_FILE points to a test-specific path to avoid conflicts
        # Mock rationale: Ensures tests don't interfere with actual files and are isolated.
        self.test_echoes_file = '/tmp/test_echoes.json'
        echo_recorder.ECHOES_FILE = self.test_echoes_file
        
        # Mock datetime.now() for deterministic timestamps
        # Mock rationale: Ensures that timestamps generated during tests are predictable and don't change with each test run, making comparisons reliable.
        self.mock_now = datetime(2023, 10, 27, 10, 0, 0)
        self.mock_now_str = self.mock_now.strftime(echo_recorder.DATE_FORMAT)
        self.patcher_datetime = patch('echo_recorder.datetime', wraps=datetime)
        self.mock_datetime = self.patcher_datetime.start()
        self.mock_datetime.now.return_value = self.mock_now
        self.mock_datetime.strptime = datetime.strptime # Keep original strptime for parsing existing echoes

        # Mock os.path.exists to control file presence
        # Mock rationale: Allows simulating file existence without actual disk I/O.
        self.patcher_exists = patch('os.path.exists')
        self.mock_exists = self.patcher_exists.start()
        self.mock_exists.return_value = False # Default: file does not exist

        # Mock open for file I/O
        # Mock rationale: Simulates file read/write operations without touching the filesystem, making tests fast and isolated.
        self.mock_file_content = ""
        self.mock_open_patch = patch('builtins.open', mock_open())
        self.mock_open_obj = self.mock_open_patch.start()

        # Capture print output
        # Mock rationale: Allows asserting on the console output of the utility.
        self.patcher_stdout = patch('sys.stdout', new_callable=unittest.mock.StringIO)
        self.mock_stdout = self.patcher_stdout.start()

    def tearDown(self):
        self.patcher_datetime.stop()
        self.patcher_exists.stop()
        self.mock_open_patch.stop()
        self.patcher_stdout.stop()

    def _set_mock_file_content(self, content, exists=True):
        """Helper to set the content that mock_open will 'read' and control os.path.exists."""
        self.mock_file_content = content
        self.mock_open_obj.return_value.__enter__.return_value.read.return_value = self.mock_file_content
        self.mock_exists.return_value = exists

    def test_add_echo_new_file(self):
        echo_recorder.add_echo("First whisper")
        
        # Check if file was opened in write mode
        self.mock_open_obj.assert_called_with(self.test_echoes_file, 'w', encoding='utf-8')
        
        # Check content written
        written_content = self.mock_open_obj.return_value.__enter__.return_value.write.call_args[0][0]
        expected_echoes = [{"timestamp": self.mock_now_str, "message": "First whisper"}]
        self.assertEqual(json.loads(written_content), expected_echoes)
        self.assertIn("Echo recorded: 'First whisper'", self.mock_stdout.getvalue())

    def test_add_echo_existing_file(self):
        initial_echoes = [{"timestamp": "2023-10-26T09:00:00", "message": "Old whisper"}]
        self._set_mock_file_content(json.dumps(initial_echoes))

        echo_recorder.add_echo("New whisper")

        written_content = self.mock_open_obj.return_value.__enter__.return_value.write.call_args[0][0]
        expected_echoes = initial_echoes + [{"timestamp": self.mock_now_str, "message": "New whisper"}]
        self.assertEqual(json.loads(written_content), expected_echoes)
        self.assertIn("Echo recorded: 'New whisper'", self.mock_stdout.getvalue())

    def test_list_echoes_no_file(self):
        self._set_mock_file_content("[]", exists=False) # Ensure file doesn't exist
        echo_recorder.list_echoes()
        self.assertIn("The temporal void is silent. No echoes found.", self.mock_stdout.getvalue())

    def test_list_echoes_empty_file(self):
        self._set_mock_file_content("[]")
        echo_recorder.list_echoes()
        self.assertIn("The temporal void is silent. No echoes found.", self.mock_stdout.getvalue())

    def test_list_echoes_with_content(self):
        echoes = [
            {"timestamp": "2023-10-26T09:00:00", "message": "Old whisper"},
            {"timestamp": self.mock_now_str, "message": "Current whisper"}
        ]
        self._set_mock_file_content(json.dumps(echoes))
        echo_recorder.list_echoes()
        output = self.mock_stdout.getvalue()
        self.assertIn("Whispers from the Temporal Void:", output)
        self.assertIn(f"  [1] {self.mock_now_str} - Current whisper", output) # Most recent first
        self.assertIn("  [2] 2023-10-26T09:00:00 - Old whisper", output)

    def test_search_echoes_no_file(self):
        self._set_mock_file_content("[]", exists=False)
        echo_recorder.search_echoes("test")
        self.assertIn("The temporal void is silent. No echoes to search.", self.mock_stdout.getvalue())

    def test_search_echoes_empty_file(self):
        self._set_mock_file_content("[]")
        echo_recorder.search_echoes("test")
        self.assertIn("The temporal void is silent. No echoes to search.", self.mock_stdout.getvalue())

    def test_search_echoes_found(self):
        echoes = [
            {"timestamp": "2023-10-26T09:00:00", "message": "This is a test message."},
            {"timestamp": self.mock_now_str, "message": "Another message with TEST keyword."}
        ]
        self._set_mock_file_content(json.dumps(echoes))
        echo_recorder.search_echoes("test")
        output = self.mock_stdout.getvalue()
        self.assertIn("Echoes containing 'test':", output)
        self.assertIn("This is a test message.", output)
        self.assertIn("Another message with TEST keyword.", output)

    def test_search_echoes_not_found(self):
        echoes = [
            {"timestamp": "2023-10-26T09:00:00", "message": "No match here."},
        ]
        self._set_mock_file_content(json.dumps(echoes))
        echo_recorder.search_echoes("nonexistent")
        self.assertIn("No echoes containing 'nonexistent' found", self.mock_stdout.getvalue())

    def test_purge_old_echoes_no_file(self):
        self._set_mock_file_content("[]", exists=False)
        echo_recorder.purge_old_echoes(7)
        self.assertIn("The temporal void is already clean. No echoes to purge.", self.mock_stdout.getvalue())

    def test_purge_old_echoes_empty_file(self):
        self._set_mock_file_content("[]")
        echo_recorder.purge_old_echoes(7)
        self.assertIn("The temporal void is already clean. No echoes to purge.", self.mock_stdout.getvalue())

    def test_purge_old_echoes_some_purged(self):
        # Mock now is 2023-10-27 10:00:00
        # Purge 7 days means anything before 2023-10-20 10:00:00
        echoes = [
            {"timestamp": "2023-10-19T09:00:00", "message": "Very old echo"}, # Should be purged
            {"timestamp": "2023-10-20T10:00:00", "message": "Exactly 7 days old"}, # Should be kept (>= cutoff)
            {"timestamp": "2023-10-21T11:00:00", "message": "Recent echo"}, # Should be kept
            {"timestamp": self.mock_now_str, "message": "Current echo"} # Should be kept
        ]
        self._set_mock_file_content(json.dumps(echoes))

        echo_recorder.purge_old_echoes(7)

        written_content = self.mock_open_obj.return_value.__enter__.return_value.write.call_args[0][0]
        expected_kept_echoes = [
            {"timestamp": "2023-10-20T10:00:00", "message": "Exactly 7 days old"},
            {"timestamp": "2023-10-21T11:00:00", "message": "Recent echo"},
            {"timestamp": self.mock_now_str, "message": "Current echo"}
        ]
        self.assertEqual(json.loads(written_content), expected_kept_echoes)
        self.assertIn("Purged 1 echoes older than 7 days", self.mock_stdout.getvalue())

    def test_purge_old_echoes_none_purged(self):
        echoes = [
            {"timestamp": "2023-10-26T09:00:00", "message": "Recent echo"},
            {"timestamp": self.mock_now_str, "message": "Current echo"}
        ]
        self._set_mock_file_content(json.dumps(echoes))
        echo_recorder.purge_old_echoes(7)
        self.assertIn("No echoes older than 7 days found to purge.", self.mock_stdout.getvalue())
        # Ensure no write operation if nothing changed
        self.mock_open_obj.return_value.__enter__.return_value.write.assert_not_called()

    def test_purge_old_echoes_malformed_timestamp(self):
        echoes = [
            {"timestamp": "2023-10-19T09:00:00", "message": "Old but valid"},
            {"timestamp": "INVALID_DATE", "message": "Malformed echo"}, # Should be kept as it cannot be parsed
            {"timestamp": self.mock_now_str, "message": "Current echo"}
        ]
        self._set_mock_file_content(json.dumps(echoes))
        echo_recorder.purge_old_echoes(7)
        
        written_content = self.mock_open_obj.return_value.__enter__.return_value.write.call_args[0][0]
        expected_kept_echoes = [
            {"timestamp": "INVALID_DATE", "message": "Malformed echo"},
            {"timestamp": self.mock_now_str, "message": "Current echo"}
        ]
        self.assertEqual(json.loads(written_content), expected_kept_echoes)
        self.assertIn("Purged 1 echoes older than 7 days", self.mock_stdout.getvalue())

    def test_load_echoes_corrupted_json(self):
        self._set_mock_file_content("this is not json")
        echoes = echo_recorder._load_echoes()
        self.assertEqual(echoes, [])

    # --- Test main function CLI parsing ---

    def test_main_add_command(self):
        with patch('sys.argv', ['echo_recorder.py', 'add', 'Test message for main']):
            echo_recorder.main()
            written_content = self.mock_open_obj.return_value.__enter__.return_value.write.call_args[0][0]
            expected_echoes = [{"timestamp": self.mock_now_str, "message": "Test message for main"}]
            self.assertEqual(json.loads(written_content), expected_echoes)
            self.assertIn("Echo recorded: 'Test message for main'", self.mock_stdout.getvalue())

    def test_main_list_command(self):
        echoes = [{"timestamp": self.mock_now_str, "message": "List test"}]
        self._set_mock_file_content(json.dumps(echoes))
        with patch('sys.argv', ['echo_recorder.py', 'list']):
            echo_recorder.main()
            self.assertIn("List test", self.mock_stdout.getvalue())

    def test_main_search_command(self):
        echoes = [{"timestamp": self.mock_now_str, "message": "Searchable content"}]
        self._set_mock_file_content(json.dumps(echoes))
        with patch('sys.argv', ['echo_recorder.py', 'search', 'content']):
            echo_recorder.main()
            self.assertIn("Searchable content", self.mock_stdout.getvalue())

    def test_main_purge_command(self):
        # Mock now is 2023-10-27 10:00:00
        echoes = [{"timestamp": "2023-10-19T09:00:00", "message": "Old echo to purge"}] # Older than 7 days
        self._set_mock_file_content(json.dumps(echoes))
        with patch('sys.argv', ['echo_recorder.py', 'purge', '7']):
            echo_recorder.main()
            written_content = self.mock_open_obj.return_value.__enter__.return_value.write.call_args[0][0]
            self.assertEqual(json.loads(written_content), [])
            self.assertIn("Purged 1 echoes older than 7 days", self.mock_stdout.getvalue())

    def test_main_invalid_command(self):
        with patch('sys.argv', ['echo_recorder.py', 'unknown_command']), \
             self.assertRaises(SystemExit) as cm:
            echo_recorder.main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Unknown command: unknown_command", self.mock_stdout.getvalue())

    def test_main_add_missing_message(self):
        with patch('sys.argv', ['echo_recorder.py', 'add']), \
             self.assertRaises(SystemExit) as cm:
            echo_recorder.main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Usage: python src/echo_recorder.py add <message>", self.mock_stdout.getvalue())

    def test_main_search_missing_keyword(self):
        with patch('sys.argv', ['echo_recorder.py', 'search']), \
             self.assertRaises(SystemExit) as cm:
            echo_recorder.main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Usage: python src/echo_recorder.py search <keyword>", self.mock_stdout.getvalue())

    def test_main_purge_missing_days(self):
        with patch('sys.argv', ['echo_recorder.py', 'purge']), \
             self.assertRaises(SystemExit) as cm:
            echo_recorder.main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Usage: python src/echo_recorder.py purge <days>", self.mock_stdout.getvalue())

    def test_main_purge_invalid_days(self):
        with patch('sys.argv', ['echo_recorder.py', 'purge', 'abc']), \
             self.assertRaises(SystemExit) as cm:
            echo_recorder.main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: 'days' must be a non-negative integer.", self.mock_stdout.getvalue())
        
        with patch('sys.argv', ['echo_recorder.py', 'purge', '-1']), \
             self.assertRaises(SystemExit) as cm:
            echo_recorder.main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: 'days' must be a non-negative integer.", self.mock_stdout.getvalue())
