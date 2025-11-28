import unittest
from unittest.mock import patch, mock_open
import sys
import json

# Mock rationale: We need to simulate file system interactions (reading log and config files)
# without actually touching the disk. `mock_open` allows us to provide predefined content
# for file reads, making tests deterministic and offline.
# Mock rationale: We also need to capture `print` output and `sys.exit` calls to verify
# the script's behavior without affecting the test runner's console or exiting prematurely.

from src.scrubber import load_config, scrub_log, main

class TestGloomGlimmerLogScrubber(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self._string_io = sys.StringIO()

        # Capture stderr for testing error messages
        self.held_stderr = sys.stderr
        sys.stderr = self._string_io_err = sys.StringIO()

    def tearDown(self):
        # Restore stdout and stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    def get_stdout(self):
        return self._string_io.getvalue()

    def get_stderr(self):
        return self._string_io_err.getvalue()

    # --- Test load_config function ---

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        'keywords_to_highlight': ['ERROR', 'CRITICAL'],
        'keywords_to_ignore': ['DEBUG', 'INFO']
    }))
    def test_load_config_success(self, mock_file):
        config = load_config('dummy_config.json')
        self.assertEqual(config['keywords_to_highlight'], ['error', 'critical'])
        self.assertEqual(config['keywords_to_ignore'], ['debug', 'info'])
        mock_file.assert_called_once_with('dummy_config.json', 'r')

    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('sys.exit')
    def test_load_config_invalid_json(self, mock_exit, mock_file):
        load_config('dummy_config.json')
        self.assertIn('Error: Invalid JSON', self.get_stderr())
        mock_exit.assert_called_once_with(1)

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.exit')
    def test_load_config_file_not_found(self, mock_exit, mock_file):
        load_config('non_existent_config.json')
        self.assertIn('Error: Config file not found', self.get_stderr())
        mock_exit.assert_called_once_with(1)

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({}))
    def test_load_config_empty_config(self, mock_file):
        config = load_config('empty_config.json')
        self.assertEqual(config['keywords_to_highlight'], [])
        self.assertEqual(config['keywords_to_ignore'], [])

    # --- Test scrub_log function ---

    @patch('builtins.open', new_callable=mock_open, read_data='INFO: Normal line\nERROR: Critical issue\nDEBUG: Debug message\nALERT: System warning\n')
    def test_scrub_log_basic_filtering(self, mock_file):
        config = {
            'keywords_to_highlight': ['error', 'alert'],
            'keywords_to_ignore': ['debug', 'info']
        }
        scrub_log('dummy.log', config)
        expected_output = 'ERROR: Critical issue\nALERT: System warning\n'
        self.assertEqual(self.get_stdout(), expected_output)

    @patch('builtins.open', new_callable=mock_open, read_data='No relevant lines here.\nAnother irrelevant line.\n')
    def test_scrub_log_no_matches(self, mock_file):
        config = {
            'keywords_to_highlight': ['error'],
            'keywords_to_ignore': ['irrelevant']
        }
        scrub_log('dummy.log', config)
        self.assertEqual(self.get_stdout(), '')

    @patch('builtins.open', new_callable=mock_open, read_data='DEBUG: This should be ignored.\nERROR: But this should not.\n')
    def test_scrub_log_ignore_takes_precedence(self, mock_file):
        # If a line contains both an ignore and a highlight keyword, ignore should win.
        config = {
            'keywords_to_highlight': ['error'],
            'keywords_to_ignore': ['debug', 'error'] # 'error' is in both lists
        }
        scrub_log('dummy.log', config)
        self.assertEqual(self.get_stdout(), '') # Nothing should be printed because 'error' is ignored

    @patch('builtins.open', new_callable=mock_open, read_data='info: lowercase info\nerror: lowercase error\n')
    def test_scrub_log_case_insensitivity(self, mock_file):
        config = {
            'keywords_to_highlight': ['ERROR'],
            'keywords_to_ignore': ['INFO']
        }
        scrub_log('dummy.log', config)
        expected_output = 'error: lowercase error\n'
        self.assertEqual(self.get_stdout(), expected_output)

    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_scrub_log_empty_log_file(self, mock_file):
        config = {
            'keywords_to_highlight': ['error'],
            'keywords_to_ignore': []
        }
        scrub_log('empty.log', config)
        self.assertEqual(self.get_stdout(), '')

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.exit')
    def test_scrub_log_file_not_found(self, mock_exit, mock_file):
        config = {
            'keywords_to_highlight': ['error'],
            'keywords_to_ignore': []
        }
        scrub_log('non_existent.log', config)
        self.assertIn('Error: Log file not found', self.get_stderr())
        mock_exit.assert_called_once_with(1)

    # --- Test main function ---

    @patch('sys.argv', ['scrubber.py', '--log-file', 'test.log', '--config-file', 'test_config.json'])
    @patch('src.scrubber.load_config')
    @patch('src.scrubber.scrub_log')
    @patch('sys.exit')
    def test_main_success(self, mock_exit, mock_scrub_log, mock_load_config):
        mock_config = {'keywords_to_highlight': ['error'], 'keywords_to_ignore': []}
        mock_load_config.return_value = mock_config
        
        main()
        
        mock_load_config.assert_called_once_with('test_config.json')
        mock_scrub_log.assert_called_once_with('test.log', mock_config)
        mock_exit.assert_not_called() # Ensure sys.exit was not called on success

    @patch('sys.argv', ['scrubber.py', '--log-file', 'test.log', '--config-file', 'non_existent_config.json'])
    @patch('src.scrubber.load_config')
    @patch('src.scrubber.scrub_log')
    @patch('sys.exit')
    def test_main_config_load_failure(self, mock_exit, mock_scrub_log, mock_load_config):
        # Simulate load_config calling sys.exit(1) internally
        mock_load_config.side_effect = lambda x: mock_exit(1) 
        
        with self.assertRaises(SystemExit) as cm:
            main()
        
        self.assertEqual(cm.exception.code, 1)
        mock_load_config.assert_called_once_with('non_existent_config.json')
        mock_scrub_log.assert_not_called() # scrub_log should not be called if config loading fails
        mock_exit.assert_called_once_with(1) # Ensure sys.exit was called

    @patch('sys.argv', ['scrubber.py', '--log-file', 'non_existent.log', '--config-file', 'test_config.json'])
    @patch('src.scrubber.load_config')
    @patch('src.scrubber.scrub_log')
    @patch('sys.exit')
    def test_main_scrub_log_failure(self, mock_exit, mock_scrub_log, mock_load_config):
        mock_config = {'keywords_to_highlight': ['error'], 'keywords_to_ignore': []}
        mock_load_config.return_value = mock_config
        # Simulate scrub_log calling sys.exit(1) internally
        mock_scrub_log.side_effect = lambda x, y: mock_exit(1)
        
        with self.assertRaises(SystemExit) as cm:
            main()
        
        self.assertEqual(cm.exception.code, 1)
        mock_load_config.assert_called_once_with('test_config.json')
        mock_scrub_log.assert_called_once_with('non_existent.log', mock_config)
        mock_exit.assert_called_once_with(1)
