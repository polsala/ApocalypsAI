import unittest
import json
import os
import sys
from unittest.mock import patch, mock_open, call

# Add the src directory to the path to allow importing focus_sentinel
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import focus_sentinel

class TestFocusSentinel(unittest.TestCase):

    def setUp(self):
        # Define a mock config for all tests
        self.mock_config_content = {
            "distraction_keywords": [
                "social", "game", "video"
            ],
            "reminder_message": "Hey, focus up!",
            "check_interval_seconds": 0.01 # Speed up tests
        }
        self.mock_config_json = json.dumps(self.mock_config_content)
        self.mock_config_path = 'mock_config.json'

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_load_config_existing(self, mock_file_open, mock_path_exists):
        # Mock rationale: Simulate an existing config file to test loading.
        mock_file_open.return_value.read.return_value = self.mock_config_json
        config = focus_sentinel.load_config(self.mock_config_path)
        self.assertEqual(config, self.mock_config_content)
        mock_path_exists.assert_called_with(self.mock_config_path)
        mock_file_open.assert_called_with(self.mock_config_path, 'r')

    @patch('os.makedirs') # Mock rationale: Prevent actual directory creation during test.
    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print') # Mock rationale: Capture print output for default config creation message.
    def test_load_config_default_creation(self, mock_print, mock_file_open, mock_path_exists, mock_makedirs):
        # Mock rationale: Simulate no existing config file to test default creation.
        # We need to ensure the default config is written and then loaded.
        config = focus_sentinel.load_config(self.mock_config_path)
        
        # Check if a default config was written
        mock_file_open.assert_called_with(self.mock_config_path, 'w')
        written_content = mock_file_open().write.call_args[0][0]
        self.assertIn('"distraction_keywords":', written_content)
        self.assertIn('"reminder_message":', written_content)
        self.assertIn('"check_interval_seconds":', written_content)
        
        # The returned config should be the default one (after being written)
        self.assertIsInstance(config, dict)
        self.assertIn('distraction_keywords', config)
        self.assertEqual(config['check_interval_seconds'], 5)
        
        # Check that makedirs was called for the config path's directory
        mock_makedirs.assert_called_once_with(os.path.dirname(self.mock_config_path), exist_ok=True)
        mock_print.assert_any_call(f"Created default config at {self.mock_config_path}")

    @patch('builtins.print')
    @patch('time.sleep')
    @patch('focus_sentinel.load_config')
    def test_run_sentinel_distraction_detected(self, mock_load_config, mock_sleep, mock_print):
        # Mock rationale: Simulate config loading, sleep, and print output for deterministic testing.
        mock_load_config.return_value = self.mock_config_content
        
        simulated_titles = [
            "Work Document - Microsoft Word",
            "My Awesome Game - Steam", # Contains 'game'
            "Email Inbox",
            "Watching a funny video on YouTube" # Contains 'video'
        ]

        # Run for a few iterations to hit both clear and distracting titles
        focus_sentinel.run_sentinel(simulated_titles=simulated_titles, max_iterations=len(simulated_titles))

        # Check if print was called with the reminder message for distracting titles
        # We need to filter print calls for the actual reminder messages
        reminder_calls = [call_arg[0] for call_arg in mock_print.call_args_list if "Hey, focus up!" in call_arg[0]]
        
        self.assertIn(f"Hey, focus up! (Detected: 'My Awesome Game - Steam')", reminder_calls[0])
        self.assertIn(f"Hey, focus up! (Detected: 'Watching a funny video on YouTube')", reminder_calls[1])
        
        # Ensure sleep was called for each iteration
        self.assertEqual(mock_sleep.call_count, len(simulated_titles))

    @patch('builtins.print')
    @patch('time.sleep')
    @patch('focus_sentinel.load_config')
    def test_run_sentinel_no_distraction(self, mock_load_config, mock_sleep, mock_print):
        # Mock rationale: Simulate config loading, sleep, and print output for deterministic testing.
        mock_load_config.return_value = self.mock_config_content
        
        simulated_titles = [
            "Work Document - Microsoft Word",
            "Email Inbox",
            "Code Editor - VS Code"
        ]

        focus_sentinel.run_sentinel(simulated_titles=simulated_titles, max_iterations=len(simulated_titles))

        # Check that the reminder message was NOT printed
        for call_arg in mock_print.call_args_list:
            self.assertNotIn("Hey, focus up!", call_arg[0])
        
        # Ensure sleep was called for each iteration
        self.assertEqual(mock_sleep.call_count, len(simulated_titles))

    def test_get_active_window_title_mock(self):
        # Test with a list of titles
        titles = ["Title A", "Title B", "Title C"]
        self.assertEqual(focus_sentinel.get_active_window_title_mock(titles, 0), "Title A")
        self.assertEqual(focus_sentinel.get_active_window_title_mock(titles, 1), "Title B")
        self.assertEqual(focus_sentinel.get_active_window_title_mock(titles, 2), "Title C")
        # Test wrapping around
        self.assertEqual(focus_sentinel.get_active_window_title_mock(titles, 3), "Title A")
        # Test with empty list
        self.assertEqual(focus_sentinel.get_active_window_title_mock([], 0), "")
        # Test with None
        self.assertEqual(focus_sentinel.get_active_window_title_mock(None, 0), "")

if __name__ == '__main__':
    unittest.main()
