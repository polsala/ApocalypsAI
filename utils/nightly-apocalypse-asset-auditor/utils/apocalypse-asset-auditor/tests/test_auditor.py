import unittest
from unittest.mock import patch, mock_open
import json
import os
from src.auditor import audit_repo

class TestApocalypseAssetAuditor(unittest.TestCase):

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_healthy_repo(self, mock_file_open, mock_getsize, mock_isdir, mock_exists):
        # Mock rationale: Simulate a repository where all critical assets exist and are healthy.
        mock_exists.side_effect = lambda p: True
        mock_isdir.side_effect = lambda p: p.endswith('.github/workflows') # Only workflows is a directory
        mock_getsize.side_effect = lambda p: 100 # All files have content
        mock_file_open.return_value.__enter__.return_value.read.return_value = "Some content"

        repo_path = "/mock/repo"
        results = audit_repo(repo_path)

        self.assertEqual(results["status"], "healthy")
        self.assertEqual(len(results["issues"]), 0)
        self.assertTrue(results["assets"]["README.md"]["exists"])
        self.assertFalse(results["assets"]["README.md"]["empty"])
        self.assertTrue(results["assets"]["LICENSE"]["exists"])
        self.assertFalse(results["assets"]["LICENSE"]["empty"])
        self.assertFalse(results["assets"]["LICENSE"].get("placeholder", False))
        self.assertTrue(results["assets"]["AGENTS.md"]["exists"])
        self.assertTrue(results["assets"][".github/workflows/"]["exists"])

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_missing_readme(self, mock_file_open, mock_getsize, mock_isdir, mock_exists):
        # Mock rationale: Simulate a repository where README.md is missing.
        def exists_side_effect(path):
            if path.endswith('README.md'):
                return False
            return True

        mock_exists.side_effect = exists_side_effect
        mock_isdir.side_effect = lambda p: p.endswith('.github/workflows')
        mock_getsize.side_effect = lambda p: 100
        mock_file_open.return_value.__enter__.return_value.read.return_value = "Some content"

        repo_path = "/mock/repo"
        results = audit_repo(repo_path)

        self.assertEqual(results["status"], "unhealthy")
        self.assertIn("Critical file 'README.md' is missing.", results["issues"])
        self.assertFalse(results["assets"]["README.md"]["exists"])

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_empty_license(self, mock_file_open, mock_getsize, mock_isdir, mock_exists):
        # Mock rationale: Simulate a repository where LICENSE exists but is empty.
        mock_exists.side_effect = lambda p: True
        mock_isdir.side_effect = lambda p: p.endswith('.github/workflows')
        def getsize_side_effect(path):
            if path.endswith('LICENSE'):
                return 0
            return 100
        mock_getsize.side_effect = getsize_side_effect
        mock_file_open.return_value.__enter__.return_value.read.return_value = ""

        repo_path = "/mock/repo"
        results = audit_repo(repo_path)

        self.assertEqual(results["status"], "unhealthy")
        self.assertIn("File 'LICENSE' exists but is empty.", results["issues"])
        self.assertTrue(results["assets"]["LICENSE"]["exists"])
        self.assertTrue(results["assets"]["LICENSE"]["empty"])

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_placeholder_license(self, mock_file_open, mock_getsize, mock_isdir, mock_exists):
        # Mock rationale: Simulate a repository where LICENSE exists but contains placeholder text.
        mock_exists.side_effect = lambda p: True
        mock_isdir.side_effect = lambda p: p.endswith('.github/workflows')
        mock_getsize.side_effect = lambda p: 150
        def read_side_effect(path):
            if path.endswith('LICENSE'):
                return "Copyright (c) [year] [fullname]"
            return "Some content"
        mock_file_open.return_value.__enter__.return_value.read.side_effect = read_side_effect

        repo_path = "/mock/repo"
        results = audit_repo(repo_path)

        self.assertEqual(results["status"], "unhealthy")
        self.assertIn("LICENSE file appears to be a placeholder.", results["issues"])
        self.assertTrue(results["assets"]["LICENSE"]["exists"])
        self.assertTrue(results["assets"]["LICENSE"]["placeholder"])

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_missing_workflows_dir(self, mock_file_open, mock_getsize, mock_isdir, mock_exists):
        # Mock rationale: Simulate a repository where .github/workflows/ directory is missing.
        def exists_side_effect(path):
            if path.endswith('.github/workflows'):
                return False
            return True

        mock_exists.side_effect = exists_side_effect
        mock_isdir.side_effect = lambda p: False # No directories exist for this test
        mock_getsize.side_effect = lambda p: 100
        mock_file_open.return_value.__enter__.return_value.read.return_value = "Some content"

        repo_path = "/mock/repo"
        results = audit_repo(repo_path)

        self.assertEqual(results["status"], "unhealthy")
        self.assertIn("Critical directory '.github/workflows' is missing.", results["issues"])
        self.assertFalse(results["assets"][".github/workflows/"]["exists"])

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_io_error_on_read(self, mock_file_open, mock_getsize, mock_isdir, mock_exists):
        # Mock rationale: Simulate an IOError when trying to read a file, ensuring graceful handling.
        # The _read_file_content helper should return an empty string on error.
        mock_exists.side_effect = lambda p: True
        mock_isdir.side_effect = lambda p: p.endswith('.github/workflows')
        mock_getsize.side_effect = lambda p: 100 # File exists and has size
        mock_file_open.side_effect = IOError("Permission denied") # Simulate read error

        repo_path = "/mock/repo"
        results = audit_repo(repo_path)

        # If _read_file_content fails, it returns empty string, making the file appear empty.
        self.assertEqual(results["status"], "unhealthy")
        self.assertIn("File 'README.md' exists but is empty.", results["issues"])
        self.assertTrue(results["assets"]["README.md"]["exists"])
        self.assertTrue(results["assets"]["README.md"]["empty"])
