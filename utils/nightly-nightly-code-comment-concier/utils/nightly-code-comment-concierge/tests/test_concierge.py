import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, mock_open
import json

# Import the functions from the concierge module
from utils.nightly-code-comment-concierge.src.concierge import (
    scan_file, scan_directory, generate_report, COMMENT_PATTERNS, SCAN_FILE_EXTENSIONS
)

class TestConcierge(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def _create_test_file(self, filename, content):
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath

    @patch('builtins.open', new_callable=mock_open)
    def test_scan_file_basic(self, mock_file_open):
        # Mock rationale: Avoid actual file system I/O for deterministic tests.
        # We control the content returned by 'open'.
        mock_file_open.return_value.readlines.return_value = [
            "# This is a regular comment\n",
            "# TODO: Implement feature X\n",
            "def func():\n",
            "    # FIXME: This logic is broken\n",
            "    pass # HACK: Temporary workaround\n"
        ]
        mock_file_open.return_value.__iter__.return_value = iter(mock_file_open.return_value.readlines.return_value)

        filepath = "dummy/path/to/file.py"
        findings = scan_file(filepath, COMMENT_PATTERNS)

        self.assertEqual(len(findings), 3)
        self.assertEqual(findings[0]['type'], 'TODO')
        self.assertEqual(findings[0]['line'], 2)
        self.assertEqual(findings[0]['message'], 'Implement feature X')
        self.assertEqual(findings[1]['type'], 'FIXME')
        self.assertEqual(findings[1]['line'], 4)
        self.assertEqual(findings[1]['message'], 'This logic is broken')
        self.assertEqual(findings[2]['type'], 'HACK')
        self.assertEqual(findings[2]['line'], 5)
        self.assertEqual(findings[2]['message'], 'Temporary workaround')

    @patch('builtins.open', new_callable=mock_open)
    def test_scan_file_no_comments(self, mock_file_open):
        # Mock rationale: Test scenario where no relevant comments are found.
        mock_file_open.return_value.readlines.return_value = [
            "import os\n",
            "def hello():\n",
            "    print('Hello')\n"
        ]
        mock_file_open.return_value.__iter__.return_value = iter(mock_file_open.return_value.readlines.return_value)

        filepath = "dummy/path/to/another_file.py"
        findings = scan_file(filepath, COMMENT_PATTERNS)
        self.assertEqual(len(findings), 0)

    @patch('builtins.open', new_callable=mock_open)
    def test_scan_file_different_patterns(self, mock_file_open):
        # Mock rationale: Verify all defined comment patterns are correctly identified.
        mock_file_open.return_value.readlines.return_value = [
            "# BUG: Critical error in calculation\n",
            "# NOTE: This function is deprecated\n",
            "# todo: lowercase todo\n",
            "# fixme: lowercase fixme\n"
        ]
        mock_file_open.return_value.__iter__.return_value = iter(mock_file_open.return_value.readlines.return_value)

        filepath = "dummy/path/to/mixed_file.md"
        findings = scan_file(filepath, COMMENT_PATTERNS)

        self.assertEqual(len(findings), 4)
        self.assertEqual(findings[0]['type'], 'BUG')
        self.assertEqual(findings[1]['type'], 'NOTE')
        self.assertEqual(findings[2]['type'], 'TODO') # Case-insensitive regex should match
        self.assertEqual(findings[3]['type'], 'FIXME') # Case-insensitive regex should match

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_directory_basic(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory structure and file contents without actual disk access.
        # This ensures deterministic behavior and isolation.
        mock_os_walk.return_value = [
            ('/root', ['src', 'docs'], ['README.md']),
            ('/root/src', [], ['main.py', 'utils.py']),
            ('/root/docs', [], ['guide.md'])
        ]

        # Define content for each mocked file
        file_contents = {
            os.path.join('/root', 'README.md'): "# Project\nNo comments here.\n",
            os.path.join('/root/src', 'main.py'): "# TODO: Main logic\nprint('hello')\n",
            os.path.join('/root/src', 'utils.py'): "# FIXME: Bad util\n# HACK: Temp fix\n",
            os.path.join('/root/docs', 'guide.md'): "# NOTE: Update this guide\n"
        }

        def mock_open_side_effect(filepath, *args, **kwargs):
            if filepath in file_contents:
                mock_file = mock_open(read_data=file_contents[filepath])
                mock_file.return_value.__iter__.return_value = iter(file_contents[filepath].splitlines(keepends=True))
                return mock_file.return_value
            raise FileNotFoundError(f"Mocked file not found: {filepath}")

        mock_file_open.side_effect = mock_open_side_effect

        directory = '/root'
        findings = scan_directory(directory, COMMENT_PATTERNS)

        self.assertEqual(len(findings), 3) # main.py, utils.py, guide.md
        self.assertIn(os.path.join('/root/src', 'main.py'), findings)
        self.assertIn(os.path.join('/root/src', 'utils.py'), findings)
        self.assertIn(os.path.join('/root/docs', 'guide.md'), findings)
        self.assertEqual(len(findings[os.path.join('/root/src', 'main.py')]), 1)
        self.assertEqual(len(findings[os.path.join('/root/src', 'utils.py')]), 2)
        self.assertEqual(len(findings[os.path.join('/root/docs', 'guide.md')]), 1)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_directory_exclude_dirs(self, mock_file_open, mock_os_walk):
        # Mock rationale: Ensure that specified directories are skipped during traversal.
        mock_os_walk.return_value = [
            ('/root', ['venv', 'node_modules', 'src'], ['main.py']),
            ('/root/venv', [], ['activate']),
            ('/root/node_modules', [], ['package.js']),
            ('/root/src', [], ['feature.py'])
        ]

        file_contents = {
            os.path.join('/root', 'main.py'): "# TODO: Root main\n",
            os.path.join('/root/src', 'feature.py'): "# FIXME: Feature bug\n"
        }

        def mock_open_side_effect(filepath, *args, **kwargs):
            if filepath in file_contents:
                mock_file = mock_open(read_data=file_contents[filepath])
                mock_file.return_value.__iter__.return_value = iter(file_contents[filepath].splitlines(keepends=True))
                return mock_file.return_value
            raise FileNotFoundError(f"Mocked file not found: {filepath}")

        mock_file_open.side_effect = mock_open_side_effect

        directory = '/root'
        exclude_dirs = ['venv', 'node_modules']
        findings = scan_directory(directory, COMMENT_PATTERNS, exclude_dirs=exclude_dirs)

        self.assertEqual(len(findings), 2) # main.py and feature.py should be found
        self.assertIn(os.path.join('/root', 'main.py'), findings)
        self.assertIn(os.path.join('/root/src', 'feature.py'), findings)
        self.assertNotIn(os.path.join('/root/venv', 'activate'), findings)
        self.assertNotIn(os.path.join('/root/node_modules', 'package.js'), findings)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_directory_exclude_files(self, mock_file_open, mock_os_walk):
        # Mock rationale: Ensure that specified files are skipped during scanning.
        mock_os_walk.return_value = [
            ('/root', [], ['main.py', 'temp.py', 'config.json'])
        ]

        file_contents = {
            os.path.join('/root', 'main.py'): "# TODO: Main logic\n",
            os.path.join('/root', 'temp.py'): "# FIXME: Temp file\n",
            os.path.join('/root', 'config.json'): "{}\n"
        }

        def mock_open_side_effect(filepath, *args, **kwargs):
            if filepath in file_contents:
                mock_file = mock_open(read_data=file_contents[filepath])
                mock_file.return_value.__iter__.return_value = iter(file_contents[filepath].splitlines(keepends=True))
                return mock_file.return_value
            raise FileNotFoundError(f"Mocked file not found: {filepath}")

        mock_file_open.side_effect = mock_open_side_effect

        directory = '/root'
        exclude_files = ['temp.py', 'config.json']
        findings = scan_directory(directory, COMMENT_PATTERNS, exclude_files=exclude_files)

        self.assertEqual(len(findings), 1) # Only main.py should be found
        self.assertIn(os.path.join('/root', 'main.py'), findings)
        self.assertNotIn(os.path.join('/root', 'temp.py'), findings)
        self.assertNotIn(os.path.join('/root', 'config.json'), findings)

    def test_generate_report_json(self):
        # Mock rationale: Test the JSON output format with predefined findings.
        mock_findings = {
            "/path/to/file1.py": [
                {"type": "TODO", "line": 10, "message": "Implement X"},
                {"type": "FIXME", "line": 20, "message": "Fix Y"}
            ],
            "/path/to/file2.md": [
                {"type": "NOTE", "line": 5, "message": "Review Z"}
            ]
        }

        report_json = generate_report(mock_findings, output_format='json')
        report_data = json.loads(report_json)

        self.assertEqual(report_data['total_findings'], 3)
        self.assertEqual(len(report_data['files']), 2)
        self.assertEqual(report_data['summary_by_type']['TODO'], 1)
        self.assertEqual(report_data['summary_by_type']['FIXME'], 1)
        self.assertEqual(report_data['summary_by_type']['NOTE'], 1)
        self.assertEqual(report_data['summary_by_type']['HACK'], 0)

    def test_generate_report_text(self):
        # Mock rationale: Test the human-readable text output format with predefined findings.
        mock_findings = {
            "/path/to/script.sh": [
                {"type": "BUG", "line": 3, "message": "Shell script error"}
            ]
        }

        report_text = generate_report(mock_findings, output_format='text')

        self.assertIn("--- Code Comment Concierge Report ---", report_text)
        self.assertIn("Total Findings: 1", report_text)
        self.assertIn("File: /path/to/script.sh", report_text)
        self.assertIn("  L3: BUG: Shell script error", report_text)
        self.assertIn("--- Summary by Type ---", report_text)
        self.assertIn("BUG: 1", report_text)
        self.assertIn("TODO: 0", report_text) # Ensure all types are listed, even if zero

    @patch('sys.argv', ['concierge.py', '--path', '/mock/repo', '--output-format', 'json'])
    @patch('os.path.isdir', return_value=True)
    @patch('utils.nightly-code-comment-concierge.src.concierge.scan_directory')
    @patch('utils.nightly-code-comment-concierge.src.concierge.generate_report')
    @patch('builtins.print')
    def test_main_cli_json_output(self, mock_print, mock_generate_report, mock_scan_directory, mock_isdir):
        # Mock rationale: Test the main CLI entry point without actual file system or output interaction.
        # We mock the core functions and print to verify arguments are passed correctly and output is generated.
        mock_scan_directory.return_value = {
            "/mock/repo/file.py": [
                {"type": "TODO", "line": 1, "message": "Test"}
            ]
        }
        mock_generate_report.return_value = '{"total_findings": 1}'

        from utils.nightly-code-comment-concierge.src.concierge import main
        main()

        mock_isdir.assert_called_once_with('/mock/repo')
        mock_scan_directory.assert_called_once_with('/mock/repo', COMMENT_PATTERNS, [], [])
        mock_generate_report.assert_called_once_with(mock_scan_directory.return_value, 'json')
        mock_print.assert_any_call("Scanning '/mock/repo' for code comments...")
        mock_print.assert_any_call('{"total_findings": 1}')

    @patch('sys.argv', ['concierge.py', '--path', '/nonexistent/path'])
    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_cli_invalid_path(self, mock_exit, mock_print, mock_isdir):
        # Mock rationale: Test error handling for an invalid path without exiting the test runner.
        from utils.nightly-code-comment-concierge.src.concierge import main
        main()

        mock_isdir.assert_called_once_with('/nonexistent/path')
        mock_print.assert_any_call("Error: Directory not found at '/nonexistent/path'")
        mock_exit.assert_called_once_with(1)
