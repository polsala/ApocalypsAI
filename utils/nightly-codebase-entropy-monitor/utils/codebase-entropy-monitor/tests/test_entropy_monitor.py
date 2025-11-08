import unittest
import os
import datetime
from unittest.mock import patch, mock_open
from io import StringIO

# Mock rationale: We need to control the filesystem state (files, directories, modification times)
# and file contents to ensure deterministic and isolated tests without actual disk I/O.
# datetime.datetime.now() is mocked to fix the 'current' time for consistent age calculations.

# Import the functions to be tested
from utils.codebase_entropy_monitor.src.entropy_monitor import (
    get_file_age_days,
    count_lines_of_code,
    check_python_docstrings,
    scan_codebase,
    format_report,
    main
)

class TestEntropyMonitor(unittest.TestCase):

    # Fix the 'current' time for all tests to ensure deterministic age calculations
    MOCK_NOW = datetime.datetime(2023, 10, 26, 10, 0, 0)

    @patch('datetime.datetime')
    def test_get_file_age_days(self, mock_dt):
        mock_dt.now.return_value = self.MOCK_NOW
        mock_dt.fromtimestamp.side_effect = lambda ts: datetime.datetime.fromtimestamp(ts)
        mock_dt.side_effect = lambda *args, **kwargs: datetime.datetime(*args, **kwargs) # Allow real datetime creation

        # Mock os.path.exists and os.path.getmtime
        with patch('os.path.exists', return_value=True),
             patch('os.path.getmtime', return_value=datetime.datetime(2023, 7, 26, 10, 0, 0).timestamp()):
            self.assertEqual(get_file_age_days('/path/to/file.txt'), 92) # 26 Oct - 26 Jul = 3 months = ~92 days

        with patch('os.path.exists', return_value=False):
            self.assertIsNone(get_file_age_days('/nonexistent/file.txt'))

    def test_count_lines_of_code(self):
        # Mock rationale: Simulate file content without actual file system access.
        mock_file_content = """
# This is a comment
line1

  line2  # inline comment
line3
"""
        with patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('os.path.exists', return_value=True):
            self.assertEqual(count_lines_of_code('/path/to/code.py'), 3)

        mock_empty_file = """
# Only comments

"""
        with patch('builtins.open', mock_open(read_data=mock_empty_file)), \
             patch('os.path.exists', return_value=True):
            self.assertEqual(count_lines_of_code('/path/to/empty.py'), 0)

        with patch('os.path.exists', return_value=False):
            self.assertEqual(count_lines_of_code('/nonexistent/file.txt'), 0)

    def test_check_python_docstrings(self):
        # Mock rationale: Simulate Python file content for AST parsing.
        python_code_with_docs = """
def func_with_doc():
    """A docstring."""
    pass

class ClassWithDoc:
    """Class docstring."""
    def method_with_doc(self):
        """Method docstring."""
        pass
"""
        with patch('builtins.open', mock_open(read_data=python_code_with_docs)), \
             patch('os.path.exists', return_value=True):
            self.assertEqual(check_python_docstrings('/path/to/good.py'), [])

        python_code_missing_docs = """
def func_no_doc():
    pass

class ClassNoDoc:
    def method_no_doc(self):
        pass
"""
        with patch('builtins.open', mock_open(read_data=python_code_missing_docs)), \
             patch('os.path.exists', return_value=True):
            expected = [
                '  - func_no_doc (line 1)',
                '  - ClassNoDoc (line 5)',
                '  - method_no_doc (line 6)'
            ]
            self.assertEqual(check_python_docstrings('/path/to/bad.py'), expected)

        # Test non-python file
        self.assertEqual(check_python_docstrings('/path/to/text.txt'), [])

        # Test non-existent file
        with patch('os.path.exists', return_value=False):
            self.assertEqual(check_python_docstrings('/nonexistent/file.py'), [])

    @patch('datetime.datetime')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_codebase(self, mock_file_open, mock_os_walk, mock_os_isdir, mock_os_exists, mock_dt):
        # Mock rationale: Simulate a directory structure and file contents/metadata
        # for a full scan without touching the actual filesystem.
        mock_dt.now.return_value = self.MOCK_NOW
        mock_dt.fromtimestamp.side_effect = lambda ts: datetime.datetime.fromtimestamp(ts)
        mock_dt.side_effect = lambda *args, **kwargs: datetime.datetime(*args, **kwargs)

        # Simulate a directory structure
        mock_os_walk.return_value = [
            ('/project', [], ['stale_file.txt', 'large_file.py', 'good_file.py', 'no_doc.py']),
            ('/project/subdir', [], ['another_stale.txt'])
        ]

        # Mock file modification times
        def mock_getmtime(path):
            if 'stale_file.txt' in path: return datetime.datetime(2023, 1, 1).timestamp() # Very old
            if 'another_stale.txt' in path: return datetime.datetime(2023, 5, 1).timestamp() # Old enough for 90 days
            return datetime.datetime(2023, 10, 20).timestamp() # Recent

        # Mock file contents
        def mock_read_data(filepath):
            if 'large_file.py' in filepath:
                return "\n" * 600 # 600 lines
            elif 'good_file.py' in filepath:
                return """def func_with_doc():\n    """Doc"""\n    pass"""
            elif 'no_doc.py' in filepath:
                return """def func_no_doc():\n    pass"""
            return "some content"

        mock_file_open.side_effect = lambda f, *args, **kwargs: mock_open(read_data=mock_read_data(f)).return_value

        with patch('os.path.getmtime', side_effect=mock_getmtime):
            report = scan_codebase('/project', min_stale_days=90, max_file_loc=500)

            self.assertIn('/project/stale_file.txt (age: 298 days)', report['stale_files'])
            self.assertIn('/project/subdir/another_stale.txt (age: 178 days)', report['stale_files'])
            self.assertIn('/project/large_file.py (LOC: 600)', report['large_files'])
            self.assertIn('/project/no_doc.py', report['undocumented_python_files'])
            self.assertIn('  - func_no_doc (line 1)', report['undocumented_python_files']['/project/no_doc.py'])
            self.assertNotIn('/project/good_file.py', report['undocumented_python_files'])

        # Test non-directory path
        with patch('os.path.isdir', return_value=False):
            report = scan_codebase('/nonexistent_dir')
            self.assertIn('error', report)

    @patch('datetime.datetime')
    def test_format_report(self, mock_dt):
        mock_dt.now.return_value = self.MOCK_NOW
        mock_dt.strftime.return_value = self.MOCK_NOW.strftime('%Y-%m-%d %H:%M:%S')

        # Test with all issues
        report_with_issues = {
            'stale_files': ['/path/to/stale.txt (age: 100 days)'],
            'large_files': ['/path/to/large.py (LOC: 600)'],
            'undocumented_python_files': {
                '/path/to/undoc.py': ['  - func_no_doc (line 1)']
            }
        }
        formatted = format_report(report_with_issues, 90, 500)
        self.assertIn('[!] Stale Files', formatted)
        self.assertIn('[!] Large Files', formatted)
        self.assertIn('[!] Undocumented Python Code', formatted)

        # Test with no issues
        report_no_issues = {
            'stale_files': [],
            'large_files': [],
            'undocumented_python_files': {}
        }
        formatted = format_report(report_no_issues, 90, 500)
        self.assertIn('[*] No stale files detected. Good job!', formatted)
        self.assertIn('[*] No overly large files detected. Keep it concise!', formatted)
        self.assertIn('[*] All Python functions/classes appear to have docstrings. Excellent documentation!', formatted)

        # Test with error
        report_with_error = {'error': 'Path not found.'}
        formatted = format_report(report_with_error, 90, 500)
        self.assertIn('ERROR: Path not found.', formatted)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('utils.codebase_entropy_monitor.src.entropy_monitor.scan_codebase')
    @patch('utils.codebase_entropy_monitor.src.entropy_monitor.format_report')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_print_to_console(self, mock_parse_args, mock_format_report, mock_scan_codebase, mock_stdout):
        # Mock rationale: Simulate command-line arguments and capture stdout
        # to verify the main function's behavior without actual execution of scan/file I/O.
        mock_parse_args.return_value = type('Args', (object,), {
            'path': '/mock/project',
            'stale_days': 90,
            'max_file_loc': 500,
            'output': None
        })()
        mock_scan_codebase.return_value = {'stale_files': []}
        mock_format_report.return_value = "Mocked Report Output"

        main()
        self.assertIn("Mocked Report Output", mock_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('utils.codebase_entropy_monitor.src.entropy_monitor.scan_codebase')
    @patch('utils.codebase_entropy_monitor.src.entropy_monitor.format_report')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_save_to_file(self, mock_parse_args, mock_format_report, mock_scan_codebase, mock_stdout, mock_file_open):
        # Mock rationale: Simulate command-line arguments and file writing
        # to verify the main function's behavior when saving to a file.
        mock_parse_args.return_value = type('Args', (object,), {
            'path': '/mock/project',
            'stale_days': 90,
            'max_file_loc': 500,
            'output': 'report.txt'
        })()
        mock_scan_codebase.return_value = {'stale_files': []}
        mock_format_report.return_value = "Mocked Report Output"

        main()
        mock_file_open.assert_called_once_with('report.txt', 'w', encoding='utf-8')
        mock_file_open().write.assert_called_once_with("Mocked Report Output")
        self.assertIn("Entropy report saved to report.txt", mock_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('utils.codebase_entropy_monitor.src.entropy_monitor.scan_codebase')
    @patch('utils.codebase_entropy_monitor.src.entropy_monitor.format_report')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_save_to_file_error(self, mock_parse_args, mock_format_report, mock_scan_codebase, mock_stdout, mock_file_open):
        # Mock rationale: Simulate an IOError during file writing to ensure error handling.
        mock_parse_args.return_value = type('Args', (object,), {
            'path': '/mock/project',
            'stale_days': 90,
            'max_file_loc': 500,
            'output': '/invalid/path/report.txt'
        })()
        mock_scan_codebase.return_value = {'stale_files': []}
        mock_format_report.return_value = "Mocked Report Output"
        mock_file_open.side_effect = IOError("Permission denied")

        main()
        self.assertIn("Error saving report to /invalid/path/report.txt: Permission denied", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
