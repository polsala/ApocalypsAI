import unittest
import os
import sys
from unittest.mock import patch, mock_open
from io import StringIO

# Add the src directory to the Python path to import dream_reader
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import dream_reader

class TestDreamReader(unittest.TestCase):

    def test_analyze_logs_nightmare(self):
        # Mock rationale: Simulating log file content to test pattern matching without actual file I/O.
        log_content = "INFO: Starting service.\nERROR: Database connection failed.\nWARN: Retrying..."
        dreams = dream_reader.analyze_logs(log_content)
        self.assertIn("nightmare", dreams)
        self.assertEqual(dream_reader.get_interpretation(dreams), "The Whispers of Doubt: Your container is grappling with inner turmoil, seeking resolution. Address its fears before they manifest into a full-blown nightmare.")

    def test_analyze_logs_metamorphosis(self):
        # Mock rationale: Simulating log file content to test pattern matching without actual file I/O.
        log_content = "INFO: Service running.\nContainer myapp Exited with code 137.\nINFO: Restarting container myapp."
        dreams = dream_reader.analyze_logs(log_content)
        self.assertIn("metamorphosis", dreams)
        self.assertEqual(dream_reader.get_interpretation(dreams), "The Metamorphosis Cycle: Your service is undergoing a profound transformation, shedding its old form to embrace a new beginning. Patience is key during this chrysalis stage.")

    def test_analyze_logs_awakening(self):
        # Mock rationale: Simulating log file content to test pattern matching without actual file I/O.
        log_content = "INFO: Application started successfully.\nINFO: Listening on port 8080."
        dreams = dream_reader.analyze_logs(log_content)
        self.assertIn("awakening", dreams)
        self.assertEqual(dream_reader.get_interpretation(dreams), "The Awakening: A new purpose has been found! Your container is ready to embark on its journey, radiating potential and eager to connect.")

    def test_analyze_logs_burden(self):
        # Mock rationale: Simulating a large log file content to trigger the 'burden' dream type.
        log_content = "\n".join([f"INFO: Log line {i}" for i in range(100)]) # 100 lines > 50 threshold
        dreams = dream_reader.analyze_logs(log_content)
        self.assertIn("burden", dreams)
        self.assertEqual(dream_reader.get_interpretation(dreams), "The Burden of Many Thoughts: Your container's mind is racing, processing a multitude of ideas. Ensure it has moments of calm to avoid burnout.")

    def test_analyze_logs_serene_slumber(self):
        # Mock rationale: Simulating log file content with no specific patterns to test default interpretation.
        log_content = "INFO: Routine check.\nDEBUG: Heartbeat received."
        dreams = dream_reader.analyze_logs(log_content)
        self.assertNotIn("nightmare", dreams)
        self.assertNotIn("metamorphosis", dreams)
        self.assertNotIn("awakening", dreams)
        self.assertNotIn("burden", dreams) # Less than 50 lines
        self.assertEqual(dream_reader.get_interpretation(dreams), "The Serene Slumber: All is calm, all is bright. Your container rests peacefully, a testament to its stable and harmonious existence.")

    def test_analyze_logs_mixed_dreams_priority(self):
        # Mock rationale: Simulating log content with multiple patterns to test interpretation priority.
        log_content = "INFO: Started successfully.\nERROR: Critical failure.\nINFO: Restarting container."
        dreams = dream_reader.analyze_logs(log_content)
        # Nightmare should take precedence
        self.assertIn("nightmare", dreams)
        self.assertIn("metamorphosis", dreams)
        self.assertIn("awakening", dreams)
        self.assertEqual(dream_reader.get_interpretation(dreams), "The Whispers of Doubt: Your container is grappling with inner turmoil, seeking resolution. Address its fears before they manifest into a full-blown nightmare.")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_function_success(self, mock_stdout, mock_exists, mock_file):
        # Mock rationale: Mocking file system operations and stdout to test the main function's flow
        # without actual file I/O or printing to console during test.
        mock_file.return_value.read.return_value = "INFO: Application started successfully.\nINFO: Listening on port 8080."
        
        # Mock sys.argv
        with patch('sys.argv', ['dream_reader.py', '/fake/path/app.log']):
            dream_reader.main()
            output = mock_stdout.getvalue()
            self.assertIn("The Awakening", output)
            self.assertIn("Detected Dreams: awakening", output)

    @patch('os.path.exists', return_value=False)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_function_file_not_found(self, mock_exit, mock_stdout, mock_exists):
        # Mock rationale: Mocking file system operations and stdout/exit to test error handling
        # without actual file I/O or exiting the test runner.
        with patch('sys.argv', ['dream_reader.py', '/nonexistent/path/app.log']):
            dream_reader.main()
            output = mock_stdout.getvalue()
            self.assertIn("Error: Log file not found", output)
            mock_exit.assert_called_with(1)

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_function_file_read_error(self, mock_exit, mock_stdout, mock_exists, mock_open_file):
        # Mock rationale: Mocking file system operations and stdout/exit to test error handling
        # without actual file I/O or exiting the test runner.
        with patch('sys.argv', ['dream_reader.py', '/fake/path/app.log']):
            dream_reader.main()
            output = mock_stdout.getvalue()
            self.assertIn("Error reading log file: Permission denied", output)
            mock_exit.assert_called_with(1)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_function_no_arguments(self, mock_exit, mock_stdout):
        # Mock rationale: Mocking stdout/exit to test argument validation
        # without printing to console or exiting the test runner.
        with patch('sys.argv', ['dream_reader.py']):
            dream_reader.main()
            output = mock_stdout.getvalue()
            self.assertIn("Usage: python dream_reader.py <path_to_log_file>", output)
            mock_exit.assert_called_with(1)
