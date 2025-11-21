import unittest
import os
from unittest.mock import patch, MagicMock
from collections import defaultdict
from io import StringIO
import sys

# Import functions from the auditor script
from src.auditor import (
    get_survival_score,
    get_extension_description,
    audit_directory,
    format_size,
    print_report
)

class TestAuditor(unittest.TestCase):

    def test_get_survival_score(self):
        self.assertEqual(get_survival_score('.md'), (5, 'Critical'))
        self.assertEqual(get_survival_score('.json'), (5, 'Critical'))
        self.assertEqual(get_survival_score('.py'), (3, 'Essential'))
        self.assertEqual(get_survival_score('.sh'), (3, 'Essential'))
        self.assertEqual(get_survival_score('.log'), (1, 'Useful'))
        self.assertEqual(get_survival_score('.html'), (1, 'Useful'))
        self.assertEqual(get_survival_score('.tmp'), (0, 'Junk'))
        self.assertEqual(get_survival_score('.zip'), (0, 'Junk'))
        self.assertEqual(get_survival_score('.xyz'), (0, 'Unknown')) # Unknown extension

    def test_get_extension_description(self):
        self.assertEqual(get_extension_description('.py'), 'Python Source')
        self.assertEqual(get_extension_description('.md'), 'Markdown Document')
        self.assertEqual(get_extension_description('.json'), 'JSON Data')
        self.assertEqual(get_extension_description('.tmp'), 'Temporary File')
        self.assertEqual(get_extension_description('.xyz'), "''.xyz' File") # Unknown description

    def test_format_size(self):
        self.assertEqual(format_size(0), "0 B")
        self.assertEqual(format_size(500), "500 B")
        self.assertEqual(format_size(1023), "1023 B")
        self.assertEqual(format_size(1024), "1.0 KB")
        self.assertEqual(format_size(1536), "1.5 KB")
        self.assertEqual(format_size(1024 * 1024), "1.0 MB")
        self.assertEqual(format_size(1.5 * 1024 * 1024), "1.5 MB")
        self.assertEqual(format_size(1024 * 1024 * 1024), "1.0 GB")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    def test_audit_directory_success(self, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir, os.walk, and os.path.getsize are filesystem operations
        # that need to be mocked to ensure deterministic and offline testing.
        # We simulate a directory structure and file sizes without touching the actual disk.

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', [], ['file1.py', 'doc.md', 'data.json']),
            ('/mock/path/sub', [], ['temp.tmp', 'another.py', 'log.log']),
        ]
        # Define sizes for each file in the order they'd be encountered by os.walk
        mock_getsize.side_effect = [
            1000, # file1.py
            500,  # doc.md
            200,  # data.json
            100,  # temp.tmp
            1500, # another.py
            300,  # log.log
        ]

        results = audit_directory('/mock/path')

        self.assertEqual(results['target_path'], '/mock/path')
        self.assertEqual(results['total_files'], 6) # 2 .py, 1 .md, 1 .json, 1 .tmp, 1 .log
        self.assertEqual(results['total_size'], 3600) # 1000+500+200+100+1500+300
        # Scores:
        # .py: (1000 + 1500) -> 2 files * 3 points = 6
        # .md: 500 -> 1 file * 5 points = 5
        # .json: 200 -> 1 file * 5 points = 5
        # .tmp: 100 -> 1 file * 0 points = 0
        # .log: 300 -> 1 file * 1 point = 1
        # Total: 6 + 5 + 5 + 0 + 1 = 17
        self.assertEqual(results['overall_survival_score'], 17)

        self.assertIn('.py', results['file_type_breakdown'])
        self.assertEqual(results['file_type_breakdown']['.py']['count'], 2)
        self.assertEqual(results['file_type_breakdown']['.py']['size'], 2500)
        self.assertEqual(results['file_type_breakdown']['.py']['score'], 6)
        self.assertEqual(results['file_type_breakdown']['.py']['score_type'], 'Essential')

        self.assertIn('.md', results['file_type_breakdown'])
        self.assertEqual(results['file_type_breakdown']['.md']['count'], 1)
        self.assertEqual(results['file_type_breakdown']['.md']['size'], 500)
        self.assertEqual(results['file_type_breakdown']['.md']['score'], 5)
        self.assertEqual(results['file_type_breakdown']['.md']['score_type'], 'Critical')

        self.assertIn('.json', results['file_type_breakdown'])
        self.assertEqual(results['file_type_breakdown']['.json']['count'], 1)
        self.assertEqual(results['file_type_breakdown']['.json']['size'], 200)
        self.assertEqual(results['file_type_breakdown']['.json']['score'], 5)
        self.assertEqual(results['file_type_breakdown']['.json']['score_type'], 'Critical')

        self.assertIn('.tmp', results['file_type_breakdown'])
        self.assertEqual(results['file_type_breakdown']['.tmp']['count'], 1)
        self.assertEqual(results['file_type_breakdown']['.tmp']['size'], 100)
        self.assertEqual(results['file_type_breakdown']['.tmp']['score'], 0)
        self.assertEqual(results['file_type_breakdown']['.tmp']['score_type'], 'Junk')

        self.assertIn('.log', results['file_type_breakdown'])
        self.assertEqual(results['file_type_breakdown']['.log']['count'], 1)
        self.assertEqual(results['file_type_breakdown']['.log']['size'], 300)
        self.assertEqual(results['file_type_breakdown']['.log']['score'], 1)
        self.assertEqual(results['file_type_breakdown']['.log']['score_type'], 'Useful')

    @patch('os.path.isdir')
    def test_audit_directory_not_found(self, mock_isdir):
        # Mock rationale: os.path.isdir is a filesystem operation.
        # We simulate a non-existent directory.
        mock_isdir.return_value = False
        with self.assertRaises(FileNotFoundError):
            audit_directory('/nonexistent/path')

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getsize')
    def test_audit_directory_os_error_on_getsize(self, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate an OSError during os.path.getsize for a specific file.
        # This tests error handling and ensures the audit continues for other files.
        mock_walk.return_value = [
            ('/mock/path', [], ['file1.py', 'unreadable.txt', 'file2.md']),
        ]
        mock_getsize.side_effect = [
            1000, # file1.py
            OSError("Permission denied"), # unreadable.txt
            500,  # file2.md
        ]

        # Capture stderr to check for warning messages
        captured_stderr = StringIO()
        sys.stderr = captured_stderr

        results = audit_directory('/mock/path')

        sys.stderr = sys.__stderr__ # Restore stderr

        self.assertIn("Warning: Could not access file /mock/path/unreadable.txt", captured_stderr.getvalue())
        self.assertEqual(results['total_files'], 2) # unreadable.txt should be skipped
        self.assertEqual(results['total_size'], 1500) # 1000 + 500
        self.assertEqual(results['overall_survival_score'], 8) # .py (3) + .md (5)

    def test_print_report(self):
        audit_results = {
            'target_path': '/test/project',
            'total_files': 5,
            'total_size': 1234567, # ~1.2 MB
            'overall_survival_score': 14,
            'file_type_breakdown': {
                '.py': {'count': 2, 'size': 500000, 'score': 6, 'score_type': 'Essential'},
                '.md': {'count': 1, 'size': 100000, 'score': 5, 'score_type': 'Critical'},
                '.log': {'count': 1, 'size': 600000, 'score': 1, 'score_type': 'Useful'},
                '.tmp': {'count': 1, 'size': 34567, 'score': 0, 'score_type': 'Junk'},
            }
        }

        expected_output_parts = [
            "ApocalypsAI Asset Audit Report for: /test/project",
            "--- Overall Summary ---",
            "Total Files Scanned: 5",
            "Total Size: 1.2 MB",
            "Overall Survival Score: 14 points",
            "--- File Type Breakdown ---",
            ".md (Markdown Document)",
            "  Files: 1",
            "  Size: 100.0 KB",
            "  Survival Score: 5 (Critical)",
            ".py (Python Source)",
            "  Files: 2",
            "  Size: 488.3 KB",
            "  Survival Score: 6 (Essential)",
            ".log (Log File)",
            "  Files: 1",
            "  Size: 585.9 KB",
            "  Survival Score: 1 (Useful)",
            ".tmp (Temporary File)",
            "  Files: 1",
            "  Size: 33.8 KB",
            "  Survival Score: 0 (Junk)",
            "--- Survival Score Legend ---",
            "*   **Critical (5 points/file)**: Documentation, Configuration, Core Data",
            "*   **Essential (3 points/file)**: Source Code, Key Scripts",
            "*   **Useful (1 point/file)**: Logs, Auxiliary Data, Web Assets",
            "*   **Junk (0 points/file)**: Temporary, Backups, Archives, System Files",
            "*   **Unknown (0 points/file)**: Uncategorized files"
        ]

        # Capture stdout
        captured_stdout = StringIO()
        sys.stdout = captured_stdout

        print_report(audit_results)

        sys.stdout = sys.__stdout__ # Restore stdout

        output = captured_stdout.getvalue()
        for part in expected_output_parts:
            self.assertIn(part, output)

        # Check order of breakdown (Critical, Essential, Useful, Junk)
        # This is a bit fragile, but we can check the relative order of the first lines of each section
        md_index = output.find(".md (Markdown Document)")
        py_index = output.find(".py (Python Source)")
        log_index = output.find(".log (Log File)")
        tmp_index = output.find(".tmp (Temporary File)")

        self.assertTrue(md_index < py_index < log_index < tmp_index)


    @patch('sys.argv', ['auditor.py', '/mock/path'])
    @patch('src.auditor.audit_directory')
    @patch('src.auditor.print_report')
    @patch('sys.exit')
    def test_main_success(self, mock_exit, mock_print_report, mock_audit_directory):
        # Mock rationale: sys.argv is modified to simulate command-line arguments.
        # audit_directory, print_report, and sys.exit are mocked to control execution flow
        # and prevent actual filesystem access or program termination during test.
        mock_audit_directory.return_value = {} # Dummy results
        
        # Call the main block directly
        # This is a common pattern for testing `if __name__ == "__main__":`
        # We need to ensure the code under test is executed.
        # The `with` statement for `patch` ensures mocks are active only for the block.
        with patch('builtins.print'): # Suppress print calls from main for cleaner test output
            exec(open('src/auditor.py').read()) # Execute the main script content

        mock_audit_directory.assert_called_once_with('/mock/path')
        mock_print_report.assert_called_once_with({}) # Assert it was called with the dummy results
        mock_exit.assert_called_once_with(0)

    @patch('sys.argv', ['auditor.py'])
    @patch('sys.exit')
    def test_main_no_args(self, mock_exit):
        # Mock rationale: Simulate no arguments provided to the script.
        # sys.exit is mocked to prevent actual program termination.
        captured_stderr = StringIO()
        sys.stderr = captured_stderr

        with patch('builtins.print'): # Suppress print calls from main for cleaner test output
            exec(open('src/auditor.py').read()) # Execute the main script content

        sys.stderr = sys.__stderr__

        self.assertIn("Usage: python src/auditor.py <directory_path>", captured_stderr.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['auditor.py', '/nonexistent/path'])
    @patch('src.auditor.audit_directory')
    @patch('sys.exit')
    def test_main_file_not_found_error(self, mock_exit, mock_audit_directory):
        # Mock rationale: Simulate FileNotFoundError from audit_directory.
        mock_audit_directory.side_effect = FileNotFoundError("Directory not found")
        
        captured_stderr = StringIO()
        sys.stderr = captured_stderr

        with patch('builtins.print'): # Suppress print calls from main for cleaner test output
            exec(open('src/auditor.py').read()) # Execute the main script content

        sys.stderr = sys.__stderr__

        self.assertIn("Error: Directory not found", captured_stderr.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['auditor.py', '/path/to/error'])
    @patch('src.auditor.audit_directory')
    @patch('sys.exit')
    def test_main_unexpected_error(self, mock_exit, mock_audit_directory):
        # Mock rationale: Simulate a generic unexpected error from audit_directory.
        mock_audit_directory.side_effect = ValueError("Something went wrong")
        
        captured_stderr = StringIO()
        sys.stderr = captured_stderr

        with patch('builtins.print'): # Suppress print calls from main for cleaner test output
            exec(open('src/auditor.py').read()) # Execute the main script content

        sys.stderr = sys.__stderr__

        self.assertIn("An unexpected error occurred: Something went wrong", captured_stderr.getvalue())
        mock_exit.assert_called_once_with(1)
