import unittest
import os
import tempfile
import shutil
from datetime import datetime
from unittest.mock import patch

# Import the functions to be tested
from src.compiler import compile_chronicle, extract_date_from_filename

class TestChronicleCompiler(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test files
        # Mock rationale: Using tempfile ensures tests are isolated, deterministic, and don't affect the actual filesystem.
        self.test_dir = tempfile.mkdtemp()
        self.output_file = os.path.join(self.test_dir, 'compiled_chronicle.txt')

    def tearDown(self):
        # Clean up the temporary directory after tests
        # Mock rationale: Ensures no test artifacts are left behind, maintaining a clean state for subsequent runs.
        shutil.rmtree(self.test_dir)

    def _create_test_file(self, filename, content):
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath

    def test_extract_date_from_filename(self):
        self.assertEqual(extract_date_from_filename('2023-01-01_log.txt'), datetime(2023, 1, 1))
        self.assertEqual(extract_date_from_filename('2024-12-31_report.txt'), datetime(2024, 12, 31))
        self.assertIsNone(extract_date_from_filename('log_2023-01-01.txt')) # Incorrect format
        self.assertIsNone(extract_date_from_filename('just_a_file.txt'))
        self.assertIsNone(extract_date_from_filename('2023-13-01_invalid_month.txt'))

    def test_compile_chronicle_basic_ordering(self):
        self._create_test_file('2023-01-03_event_C.txt', 'Content C: Third event.')
        self._create_test_file('2023-01-01_event_A.txt', 'Content A: First event.')
        self._create_test_file('2023-01-02_event_B.txt', 'Content B: Second event.')

        compile_chronicle(self.test_dir, self.output_file)

        expected_content = (
            "--- 2023-01-01 ---\nContent A: First event.\n\n"
            "--- 2023-01-02 ---\nContent B: Second event.\n\n"
            "--- 2023-01-03 ---\nContent C: Third event.\n\n"
        )
        with open(self.output_file, 'r', encoding='utf-8') as f:
            actual_content = f.read()
        self.assertEqual(actual_content, expected_content)

    def test_compile_chronicle_ignores_non_txt_files(self):
        self._create_test_file('2023-01-01_event.txt', 'Text content.')
        self._create_test_file('image.jpg', 'Binary content.')
        self._create_test_file('document.pdf', 'PDF content.')

        compile_chronicle(self.test_dir, self.output_file)

        expected_content = "--- 2023-01-01 ---\nText content.\n\n"
        with open(self.output_file, 'r', encoding='utf-8') as f:
            actual_content = f.read()
        self.assertEqual(actual_content, expected_content)

    def test_compile_chronicle_handles_no_date_files(self):
        self._create_test_file('2023-01-01_event.txt', 'Valid content.')
        self._create_test_file('no_date_file.txt', 'This file has no date in its name.')

        # Mock rationale: Suppress stderr output for this test to avoid cluttering test logs with expected warnings.
        with patch('sys.stderr') as mock_stderr, patch('sys.stdout'):
            compile_chronicle(self.test_dir, self.output_file)
            mock_stderr.write.assert_called_with("Warning: Could not extract date from 'no_date_file.txt'. Skipping.\n")

        expected_content = "--- 2023-01-01 ---\nValid content.\n\n"
        with open(self.output_file, 'r', encoding='utf-8') as f:
            actual_content = f.read()
        self.assertEqual(actual_content, expected_content)

    def test_compile_chronicle_empty_directory(self):
        # Mock rationale: Suppress stdout/stderr for this test to avoid cluttering test logs.
        with patch('sys.stdout'), patch('sys.stderr'):
            compile_chronicle(self.test_dir, self.output_file)
            self.assertTrue(os.path.exists(self.output_file))
            with open(self.output_file, 'r', encoding='utf-8') as f:
                self.assertEqual(f.read(), '') # Should create an empty file

    def test_compile_chronicle_output_file_creation(self):
        self._create_test_file('2023-01-01_event.txt', 'Content.')
        compile_chronicle(self.test_dir, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))

    def test_compile_chronicle_non_existent_input_dir(self):
        non_existent_dir = os.path.join(self.test_dir, 'non_existent')
        # Mock rationale: Capture sys.stderr and sys.exit to test error handling without terminating the test runner.
        with self.assertRaises(SystemExit) as cm, patch('sys.stderr') as mock_stderr:
            compile_chronicle(non_existent_dir, self.output_file)
        self.assertEqual(cm.exception.code, 1)
        mock_stderr.write.assert_called_with(f"Error: Input directory '{non_existent_dir}' not found.\n")

    def test_main_function_argument_parsing(self):
        # Mock rationale: Patch sys.argv to simulate command-line arguments and sys.exit to prevent actual exit.
        with patch('sys.argv', ['compiler.py', self.test_dir, self.output_file]), \
             patch('src.compiler.compile_chronicle') as mock_compile_chronicle,
             patch('sys.exit') as mock_exit,
             patch('sys.stdout'): # Suppress stdout from main's success message
            from src.compiler import main
            main()
            mock_compile_chronicle.assert_called_once_with(self.test_dir, self.output_file)
            mock_exit.assert_not_called()

    def test_main_function_invalid_arguments(self):
        # Mock rationale: Patch sys.argv to simulate incorrect command-line arguments and sys.exit to prevent actual exit.
        with patch('sys.argv', ['compiler.py', self.test_dir]), \
             patch('sys.exit') as mock_exit,
             patch('sys.stderr') as mock_stderr:
            from src.compiler import main
            main()
            mock_exit.assert_called_once_with(1)
            mock_stderr.write.assert_called_with("Usage: python src/compiler.py <input_directory> <output_file>\n")
