import unittest
from unittest.mock import patch, mock_open
import sys
import io
import os

# Mock rationale: We need to simulate file system reads for .env files
# without actually creating files on disk. `unittest.mock.patch` and `mock_open`
# allow us to control the content returned when `open()` is called.

# Add the src directory to the path for importing the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from drift_detector import parse_env_file, detect_drift, main
sys.path.pop(0)

class TestDriftDetector(unittest.TestCase):

    def test_parse_env_file_basic(self):
        mock_file_content = """
KEY1=value1
KEY2=value2
"""
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as mock_file:
            keys = parse_env_file('dummy.env')
            self.assertEqual(keys, {'KEY1', 'KEY2'})
            mock_file.assert_called_once_with('dummy.env', 'r')

    def test_parse_env_file_with_comments_and_empty_lines(self):
        mock_file_content = """
# This is a comment

KEY_A=value_a
  # Another comment
KEY_B = value_b # Inline comment

# End of file
"""
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as mock_file:
            keys = parse_env_file('dummy.env')
            self.assertEqual(keys, {'KEY_A', 'KEY_B'})

    def test_parse_env_file_empty_file(self):
        with patch('builtins.open', mock_open(read_data="")) as mock_file:
            keys = parse_env_file('empty.env')
            self.assertEqual(keys, set())

    def test_parse_env_file_non_existent_file(self):
        # Mock rationale: os.path.exists needs to be mocked to simulate a file not existing.
        with patch('os.path.exists', return_value=False):
            keys = parse_env_file('non_existent.env')
            self.assertEqual(keys, set())

    def test_detect_drift_no_drift(self):
        template = {'A', 'B', 'C'}
        target = {'A', 'B', 'C'}
        missing, extra = detect_drift(template, target)
        self.assertEqual(missing, set())
        self.assertEqual(extra, set())

    def test_detect_drift_missing_keys(self):
        template = {'A', 'B', 'C'}
        target = {'A', 'B'}
        missing, extra = detect_drift(template, target)
        self.assertEqual(missing, {'C'})
        self.assertEqual(extra, set())

    def test_detect_drift_extra_keys(self):
        template = {'A', 'B'}
        target = {'A', 'B', 'C'}
        missing, extra = detect_drift(template, target)
        self.assertEqual(missing, set())
        self.assertEqual(extra, {'C'})

    def test_detect_drift_both_missing_and_extra(self):
        template = {'A', 'B', 'C'}
        target = {'A', 'D'}
        missing, extra = detect_drift(template, target)
        self.assertEqual(missing, {'B', 'C'})
        self.assertEqual(extra, {'D'})

    def test_main_no_drift(self):
        # Mock rationale: Simulate file content and command-line arguments.
        # `sys.argv` is mocked to pass arguments to `main()`.
        # `builtins.open` is mocked to provide file content.
        # `os.path.exists` is mocked to confirm files exist.
        mock_template_content = """KEY1=val1\nKEY2=val2"""
        mock_target_content = """KEY1=valA\nKEY2=valB"""

        with patch('sys.argv', ['drift_detector.py', '--template', 'template.env', '--target', 'target.env']),
             patch('builtins.open', side_effect=lambda f, mode: mock_open(read_data=mock_template_content if f == 'template.env' else mock_target_content).return_value),
             patch('os.path.exists', side_effect=lambda f: f in ['template.env', 'target.env']),
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("is perfectly aligned with the template.", output)
            self.assertNotIn("Missing Keys", output)
            self.assertNotIn("Extra Keys", output)

    def test_main_missing_keys(self):
        mock_template_content = """KEY1=val1\nKEY2=val2\nKEY3=val3"""
        mock_target_content = """KEY1=valA\nKEY2=valB"""

        with patch('sys.argv', ['drift_detector.py', '--template', 'template.env', '--target', 'target.env']),
             patch('builtins.open', side_effect=lambda f, mode: mock_open(read_data=mock_template_content if f == 'template.env' else mock_target_content).return_value),
             patch('os.path.exists', side_effect=lambda f: f in ['template.env', 'target.env']),
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Missing Keys in 'target.env': KEY3", output)
            self.assertNotIn("Extra Keys", output)

    def test_main_extra_keys(self):
        mock_template_content = """KEY1=val1\nKEY2=val2"""
        mock_target_content = """KEY1=valA\nKEY2=valB\nKEY_EXTRA=valC"""

        with patch('sys.argv', ['drift_detector.py', '--template', 'template.env', '--target', 'target.env']),
             patch('builtins.open', side_effect=lambda f, mode: mock_open(read_data=mock_template_content if f == 'template.env' else mock_target_content).return_value),
             patch('os.path.exists', side_effect=lambda f: f in ['template.env', 'target.env']),
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Extra Keys in 'target.env': KEY_EXTRA", output)
            self.assertNotIn("Missing Keys", output)

    def test_main_template_not_found(self):
        with patch('sys.argv', ['drift_detector.py', '--template', 'non_existent_template.env', '--target', 'target.env']),
             patch('os.path.exists', side_effect=lambda f: f == 'target.env'), # Only target exists
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout,
             patch('sys.exit') as mock_exit:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Error: Template file 'non_existent_template.env' not found.", output)
            mock_exit.assert_called_once_with(1)

    def test_main_multiple_targets(self):
        mock_template_content = """KEY1=val1\nKEY2=val2"""
        mock_target1_content = """KEY1=valA\nKEY2=valB\nKEY_EXTRA=valC"""
        mock_target2_content = """KEY1=valX\nKEY_MISSING=valY"""

        def mock_open_side_effect(f, mode):
            if f == 'template.env': return mock_open(read_data=mock_template_content).return_value
            if f == 'target1.env': return mock_open(read_data=mock_target1_content).return_value
            if f == 'target2.env': return mock_open(read_data=mock_target2_content).return_value
            raise FileNotFoundError(f)

        def mock_exists_side_effect(f):
            return f in ['template.env', 'target1.env', 'target2.env']

        with patch('sys.argv', ['drift_detector.py', '--template', 'template.env', '--target', 'target1.env', 'target2.env']),
             patch('builtins.open', side_effect=mock_open_side_effect),
             patch('os.path.exists', side_effect=mock_exists_side_effect),
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Extra Keys in 'target1.env': KEY_EXTRA", output)
            self.assertIn("Missing Keys in 'target2.env': KEY2", output)
            self.assertIn("Extra Keys in 'target2.env': KEY_MISSING", output)
