import unittest
import os
import json
from unittest.mock import patch
import argparse

# Mock rationale: We need to simulate the presence or absence of files
# in a directory without actually creating files on the filesystem.
# `os.path.exists` is the primary function to mock for this purpose.
# `os.path.isdir` is also mocked to ensure the input path is considered a valid directory.

class TestSurvivalKitChecker(unittest.TestCase):

    @patch('os.path.exists')
    @patch('os.path.isdir')
    def test_all_files_present(self, mock_isdir, mock_exists):
        # Mock rationale: Simulate a directory where all essential files exist.
        mock_isdir.return_value = True
        from src.checker import ESSENTIAL_FILES # Import the actual list
        mock_exists.side_effect = lambda path: os.path.basename(path) in ESSENTIAL_FILES
        
        from src.checker import check_survival_kit
        report = check_survival_kit("/mock/repo")

        self.assertEqual(report["directory"], "/mock/repo")
        self.assertCountEqual(report["files_found"], ESSENTIAL_FILES)
        self.assertEqual(report["files_missing"], [])
        self.assertEqual(report["survival_readiness_score"], 100.0)
        self.assertEqual(report["status"], "OK")
        self.assertIn("complete", report["message"])

    @patch('os.path.exists')
    @patch('os.path.isdir')
    def test_some_files_missing(self, mock_isdir, mock_exists):
        # Mock rationale: Simulate a directory where some essential files are missing.
        mock_isdir.return_value = True
        present_files = ["README.md", "LICENSE"]
        mock_exists.side_effect = lambda path: os.path.basename(path) in present_files
        
        from src.checker import check_survival_kit, ESSENTIAL_FILES
        report = check_survival_kit("/mock/repo")

        self.assertEqual(report["directory"], "/mock/repo")
        self.assertCountEqual(report["files_found"], present_files)
        self.assertCountEqual(report["files_missing"], [f for f in ESSENTIAL_FILES if f not in present_files])
        self.assertEqual(report["survival_readiness_score"], 40.0)
        self.assertEqual(report["status"], "WARNING")
        self.assertIn("missing", report["message"])

    @patch('os.path.exists')
    @patch('os.path.isdir')
    def test_all_files_missing(self, mock_isdir, mock_exists):
        # Mock rationale: Simulate an empty directory (no essential files).
        mock_isdir.return_value = True
        mock_exists.return_value = False # No files exist
        
        from src.checker import check_survival_kit, ESSENTIAL_FILES
        report = check_survival_kit("/mock/repo")

        self.assertEqual(report["directory"], "/mock/repo")
        self.assertEqual(report["files_found"], [])
        self.assertCountEqual(report["files_missing"], ESSENTIAL_FILES)
        self.assertEqual(report["survival_readiness_score"], 0.0)
        self.assertEqual(report["status"], "CRITICAL")
        self.assertIn("empty", report["message"])

    @patch('os.path.exists')
    @patch('os.path.isdir')
    def test_empty_essential_list(self, mock_isdir, mock_exists):
        # Mock rationale: Test behavior if the essential_files list were empty.
        # We directly patch the module-level ESSENTIAL_FILES for this test.
        mock_isdir.return_value = True
        mock_exists.return_value = False # No files exist

        from src import checker
        original_essential_files = checker.ESSENTIAL_FILES
        checker.ESSENTIAL_FILES = [] # Make it empty for this test

        try:
            report = checker.check_survival_kit("/mock/repo")
            self.assertEqual(report["survival_readiness_score"], 100.0)
            self.assertEqual(report["status"], "OK")
            self.assertIn("complete", report["message"])
            self.assertEqual(report["essential_files_checked"], [])
        finally:
            checker.ESSENTIAL_FILES = original_essential_files # Restore it

    @patch('os.path.isdir')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.exit')
    def test_main_directory_not_found(self, mock_exit, mock_stdout, mock_isdir):
        # Mock rationale: Simulate a scenario where the provided directory path does not exist.
        # We mock `sys.exit` to prevent the test runner from exiting prematurely
        # and `sys.stdout` to capture the printed error message.
        mock_isdir.return_value = False

        from src.checker import main
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(path='/nonexistent/path')):
            main()
        
        mock_exit.assert_called_once_with(1)
        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(output["error"], "Directory not found: /nonexistent/path")
        self.assertEqual(output["status"], "ERROR")

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_main_success_output(self, mock_stdout, mock_isdir, mock_exists):
        # Mock rationale: Simulate a successful run of the main function and capture its JSON output.
        mock_isdir.return_value = True
        present_files = ["README.md", "LICENSE"]
        mock_exists.side_effect = lambda path: os.path.basename(path) in present_files

        from src.checker import main
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(path='/mock/repo')):
            main()
        
        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(output["directory"], "/mock/repo")
        self.assertEqual(output["survival_readiness_score"], 40.0)
        self.assertEqual(output["status"], "WARNING")
