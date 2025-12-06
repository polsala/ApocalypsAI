import unittest
import os
import sys
from unittest.mock import patch, mock_open
import yaml

# Add the src directory to the path to allow importing checker.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from checker import WorkflowSanityChecker

class TestWorkflowSanityChecker(unittest.TestCase):

    def setUp(self):
        # Mock rationale: We don't want to touch the actual filesystem during tests.
        # We simulate the directory structure and file contents.
        self.mock_workflow_dir = "/mock/repo/.github/workflows"
        self.mock_base_path = "/mock/repo"
        self.checker = WorkflowSanityChecker(base_path=self.mock_base_path)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_no_workflow_files_found(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate a scenario where the workflow directory exists but is empty.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            (self.mock_workflow_dir, [], []) # No files
        ]
        with patch('builtins.print') as mock_print:
            result = self.checker.run_checks()
            self.assertFalse(result)
            mock_print.assert_any_call("No workflow files found. Ensure you are in the repository root and .github/workflows exists.")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_valid_workflow(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate a perfectly valid workflow file.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            (self.mock_workflow_dir, [], ['valid.yml'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data="""
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
      name: Checkout repository
    - run: echo "Hello"
permissions:
  contents: read
""").return_value
        ]
        with patch('builtins.print') as mock_print:
            result = self.checker.run_checks()
            self.assertTrue(result)
            mock_print.assert_any_call("[SUCCESS] All workflows appear sane. The apocalypse can wait... for now.")
            self.assertEqual(len(self.checker.issues), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_workflow_missing_on_trigger(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate a workflow missing the 'on:' trigger.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            (self.mock_workflow_dir, [], ['no_on.yml'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data="""
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
""").return_value
        ]
        with patch('builtins.print') as mock_print:
            result = self.checker.run_checks()
            self.assertFalse(result)
            self.assertIn("[ERROR] /mock/repo/.github/workflows/no_on.yml: Missing 'on:' trigger.", self.checker.issues)
            mock_print.assert_any_call(f"\nFound {len(self.checker.issues)} issues. Please review.")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_workflow_missing_jobs_section(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate a workflow missing the 'jobs:' section.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            (self.mock_workflow_dir, [], ['no_jobs.yml'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data="""
on: [push]
""").return_value
        ]
        with patch('builtins.print') as mock_print:
            result = self.checker.run_checks()
            self.assertFalse(result)
            self.assertIn("[ERROR] /mock/repo/.github/workflows/no_jobs.yml: Missing 'jobs:' section.", self.checker.issues)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_workflow_job_missing_runs_on(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate a job missing the 'runs-on' key.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            (self.mock_workflow_dir, [], ['no_runs_on.yml'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data="""
on: [push]
jobs:
  build:
    steps:
    - uses: actions/checkout@v3
""").return_value
        ]
        with patch('builtins.print') as mock_print:
            result = self.checker.run_checks()
            self.assertFalse(result)
            self.assertIn("[ERROR] /mock/repo/.github/workflows/no_runs_on.yml: Job 'build': Missing 'runs-on' key.", self.checker.issues)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_workflow_job_missing_steps(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate a job missing the 'steps' key.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            (self.mock_workflow_dir, [], ['no_steps.yml'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data="""
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
""").return_value
        ]
        with patch('builtins.print') as mock_print:
            result = self.checker.run_checks()
            self.assertFalse(result)
            self.assertIn("[ERROR] /mock/repo/.github/workflows/no_steps.yml: Job 'build': Missing 'steps' key.", self.checker.issues)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_workflow_unversioned_action(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate a workflow using an unversioned action.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            (self.mock_workflow_dir, [], ['unversioned.yml'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data="""
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout
      name: Checkout repository
""").return_value
        ]
        with patch('builtins.print') as mock_print:
            result = self.checker.run_checks()
            self.assertFalse(result)
            self.assertIn("[WARNING] /mock/repo/.github/workflows/unversioned.yml: Job 'build': Step 'Checkout repository': Action 'actions/checkout' should specify a version (e.g., 'actions/checkout@v3').", self.checker.issues)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_workflow_missing_permissions_block(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate a workflow missing the 'permissions' block.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            (self.mock_workflow_dir, [], ['no_permissions.yml'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data="""
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
""").return_value
        ]
        with patch('builtins.print') as mock_print:
            result = self.checker.run_checks()
            self.assertFalse(result)
            self.assertIn("[INFO] /mock/repo/.github/workflows/no_permissions.yml: Consider adding an explicit 'permissions' block for better security.", self.checker.issues)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_malformed_yaml(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate a workflow file with invalid YAML syntax.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            (self.mock_workflow_dir, [], ['malformed.yml'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data="""
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
      - this is not valid yaml
""").return_value
        ]
        with patch('builtins.print') as mock_print:
            result = self.checker.run_checks()
            self.assertFalse(result)
            # Check for the specific error message from PyYAML
            self.assertTrue(any("Invalid YAML syntax" in issue for issue in self.checker.issues))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_multiple_issues_in_one_file(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate a workflow file with multiple issues.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            (self.mock_workflow_dir, [], ['multi_issue.yml'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data="""
jobs: # Missing 'on:'
  build:
    steps: # Missing 'runs-on'
    - uses: actions/checkout # Unversioned action
""").return_value
        ]
        with patch('builtins.print') as mock_print:
            result = self.checker.run_checks()
            self.assertFalse(result)
            self.assertIn("[ERROR] /mock/repo/.github/workflows/multi_issue.yml: Missing 'on:' trigger.", self.checker.issues)
            self.assertIn("[ERROR] /mock/repo/.github/workflows/multi_issue.yml: Job 'build': Missing 'runs-on' key.", self.checker.issues)
            self.assertIn("[WARNING] /mock/repo/.github/workflows/multi_issue.yml: Job 'build': Step 'Step 1': Action 'actions/checkout' should specify a version (e.g., 'actions/checkout@v3').", self.checker.issues)
            self.assertIn("[INFO] /mock/repo/.github/workflows/multi_issue.yml: Consider adding an explicit 'permissions' block for better security.", self.checker.issues)
            self.assertEqual(len(self.checker.issues), 4)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_multiple_files_with_issues(self, mock_file_open, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate multiple workflow files, some with issues, some valid.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            (self.mock_workflow_dir, [], ['valid.yml', 'no_on.yml'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data="""
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
permissions:
  contents: read
""").return_value, # Content for valid.yml
            mock_open(read_data="""
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
""").return_value  # Content for no_on.yml
        ]
        with patch('builtins.print') as mock_print:
            result = self.checker.run_checks()
            self.assertFalse(result)
            self.assertIn("[ERROR] /mock/repo/.github/workflows/no_on.yml: Missing 'on:' trigger.", self.checker.issues)
            self.assertIn("[INFO] /mock/repo/.github/workflows/no_on.yml: Consider adding an explicit 'permissions' block for better security.", self.checker.issues)
            self.assertEqual(len(self.checker.issues), 2)


if __name__ == '__main__':
    unittest.main()
