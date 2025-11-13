import unittest
import os
import sys
from unittest.mock import patch, mock_open
from io import StringIO

# Add the src directory to the path to allow importing workflow_hardener
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from workflow_hardener import WorkflowHardener

class TestWorkflowHardener(unittest.TestCase):

    def setUp(self):
        self.hardener = WorkflowHardener()
        self.mock_workflow_dir = '/mock/workflows'

    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir')
    def test_scan_workflow_directory_no_issues(self, mock_isdir, mock_file_open, mock_listdir):
        # Mock rationale: Simulate a directory with a valid workflow file.
        # Mock rationale: Simulate reading the content of a workflow file.
        # Mock rationale: Simulate checking if the directory exists.
        mock_isdir.return_value = True
        mock_listdir.return_value = ['good_workflow.yml']
        mock_file_open.side_effect = [
            mock_open(read_data="""
name: Good Workflow
on: [push, pull_request]
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - run: echo "Hello"
""").return_value
        ]

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            findings = self.hardener.scan_workflow_directory(self.mock_workflow_dir)
            self.assertEqual(len(findings), 0)
            self.assertIn("No hardening opportunities found.", mock_stdout.getvalue())

    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir')
    def test_scan_workflow_directory_with_concurrency_issue(self, mock_isdir, mock_file_open, mock_listdir):
        # Mock rationale: Simulate a directory with a workflow missing concurrency.
        # Mock rationale: Simulate reading the content of a workflow file.
        # Mock rationale: Simulate checking if the directory exists.
        mock_isdir.return_value = True
        mock_listdir.return_value = ['no_concurrency.yml']
        mock_file_open.side_effect = [
            mock_open(read_data="""
name: No Concurrency Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - run: echo "Hello"
""").return_value
        ]

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            findings = self.hardener.scan_workflow_directory(self.mock_workflow_dir)
            self.assertEqual(len(findings), 1)
            self.assertIn(f"{self.mock_workflow_dir}/no_concurrency.yml", findings)
            self.assertIn("could benefit from 'concurrency'", findings[f"{self.mock_workflow_dir}/no_concurrency.yml"][0])
            self.assertIn("--- Findings for /mock/workflows/no_concurrency.yml ---", mock_stdout.getvalue())

    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir')
    def test_scan_workflow_directory_with_checkout_version_issue(self, mock_isdir, mock_file_open, mock_listdir):
        # Mock rationale: Simulate a directory with a workflow using an old checkout version.
        # Mock rationale: Simulate reading the content of a workflow file.
        # Mock rationale: Simulate checking if the directory exists.
        mock_isdir.return_value = True
        mock_listdir.return_value = ['old_checkout.yml']
        mock_file_open.side_effect = [
            mock_open(read_data="""
name: Old Checkout Workflow
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - run: echo "Hello"
""").return_value
        ]

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            findings = self.hardener.scan_workflow_directory(self.mock_workflow_dir)
            self.assertEqual(len(findings), 1)
            self.assertIn(f"{self.mock_workflow_dir}/old_checkout.yml", findings)
            self.assertIn("uses 'actions/checkout@v2'. Consider updating to 'v3' or later", findings[f"{self.mock_workflow_dir}/old_checkout.yml"][0])
            self.assertIn("--- Findings for /mock/workflows/old_checkout.yml ---", mock_stdout.getvalue())

    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir')
    def test_scan_workflow_directory_with_permissions_issue(self, mock_isdir, mock_file_open, mock_listdir):
        # Mock rationale: Simulate a directory with a pull_request workflow missing explicit permissions.
        # Mock rationale: Simulate reading the content of a workflow file.
        # Mock rationale: Simulate checking if the directory exists.
        mock_isdir.return_value = True
        mock_listdir.return_value = ['no_permissions.yml']
        mock_file_open.side_effect = [
            mock_open(read_data="""
name: No Permissions Workflow
on: pull_request
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - run: echo "Hello"
""").return_value
        ]

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            findings = self.hardener.scan_workflow_directory(self.mock_workflow_dir)
            self.assertEqual(len(findings), 1)
            self.assertIn(f"{self.mock_workflow_dir}/no_permissions.yml", findings)
            self.assertIn("lacks an explicit 'permissions' block", findings[f"{self.mock_workflow_dir}/no_permissions.yml"][0])
            self.assertIn("--- Findings for /mock/workflows/no_permissions.yml ---", mock_stdout.getvalue())

    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir')
    def test_scan_workflow_directory_with_multiple_issues(self, mock_isdir, mock_file_open, mock_listdir):
        # Mock rationale: Simulate a directory with a workflow having multiple issues.
        # Mock rationale: Simulate reading the content of a workflow file.
        # Mock rationale: Simulate checking if the directory exists.
        mock_isdir.return_value = True
        mock_listdir.return_value = ['multiple_issues.yml']
        mock_file_open.side_effect = [
            mock_open(read_data="""
name: Multiple Issues Workflow
on: pull_request
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - run: echo "Hello"
""").return_value
        ]

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            findings = self.hardener.scan_workflow_directory(self.mock_workflow_dir)
            self.assertEqual(len(findings), 1)
            self.assertEqual(len(findings[f"{self.mock_workflow_dir}/multiple_issues.yml"]), 3)
            self.assertIn("could benefit from 'concurrency'", findings[f"{self.mock_workflow_dir}/multiple_issues.yml"][0])
            self.assertIn("uses 'actions/checkout@v2'. Consider updating to 'v3' or later", findings[f"{self.mock_workflow_dir}/multiple_issues.yml"][1])
            self.assertIn("lacks an explicit 'permissions' block", findings[f"{self.mock_workflow_dir}/multiple_issues.yml"][2])

    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir')
    def test_scan_workflow_directory_invalid_yaml(self, mock_isdir, mock_file_open, mock_listdir):
        # Mock rationale: Simulate a directory with an invalid YAML workflow file.
        # Mock rationale: Simulate reading the content of an invalid workflow file.
        # Mock rationale: Simulate checking if the directory exists.
        mock_isdir.return_value = True
        mock_listdir.return_value = ['invalid.yml']
        mock_file_open.side_effect = [
            mock_open(read_data="""
name: Invalid Workflow
on:
  push:
    branches:
      - main
jobs:
  build:
    steps:
      - uses: actions/checkout@v3
      - run: |
          echo "This is invalid YAML because of bad indentation"
        - another_step:
""").return_value
        ]

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            findings = self.hardener.scan_workflow_directory(self.mock_workflow_dir)
            self.assertEqual(len(findings), 1)
            self.assertIn(f"{self.mock_workflow_dir}/invalid.yml", findings)
            self.assertIn("[ERROR] Invalid YAML syntax:", findings[f"{self.mock_workflow_dir}/invalid.yml"][0])

    @patch('os.path.isdir')
    def test_scan_workflow_directory_not_found(self, mock_isdir):
        # Mock rationale: Simulate a non-existent workflow directory.
        mock_isdir.return_value = False
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            findings = self.hardener.scan_workflow_directory(self.mock_workflow_dir)
            self.assertEqual(len(findings), 0)
            self.assertIn(f"Error: Directory '{self.mock_workflow_dir}' not found.", mock_stdout.getvalue())

    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir')
    def test_main_functionality(self, mock_isdir, mock_file_open, mock_listdir):
        # Mock rationale: Test the main function's argument parsing and execution flow.
        mock_isdir.return_value = True
        mock_listdir.return_value = ['test_workflow.yml']
        mock_file_open.side_effect = [
            mock_open(read_data="""
name: Test Workflow
on: pull_request
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - run: echo "Test"
""").return_value
        ]

        test_args = ['workflow_hardener.py', '--workflow-dir', self.mock_workflow_dir]
        with patch('sys.argv', test_args):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                from workflow_hardener import main
                main()
                output = mock_stdout.getvalue()
                self.assertIn("Scanning workflows in /mock/workflows", output)
                self.assertIn("could benefit from 'concurrency'", output)
                self.assertIn("uses 'actions/checkout@v2'. Consider updating to 'v3' or later", output)
                self.assertIn("lacks an explicit 'permissions' block", output)


if __name__ == '__main__':
    unittest.main()
