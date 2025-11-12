import unittest
from unittest.mock import patch, mock_open
import os
import sys

# Add the src directory to the Python path to allow importing whisperer.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from whisperer import lint_workflow_file, find_workflow_files

class TestWorkflowWhisperer(unittest.TestCase):

    def setUp(self):
        # Mock rationale: Simulate os.getcwd for consistent testing environment.
        self.mock_getcwd_patch = patch('os.getcwd', return_value='/mock/repo')
        self.mock_getcwd = self.mock_getcwd_patch.start()

    def tearDown(self):
        self.mock_getcwd_patch.stop()

    @patch('os.path.isdir')
    @patch('os.listdir')
    def test_find_workflow_files(self, mock_listdir, mock_isdir):
        # Mock rationale: Simulate file system structure for finding workflow files.
        mock_isdir.side_effect = lambda path: path == '/mock/repo/.github/workflows'
        mock_listdir.return_value = ['ci.yml', 'deploy.yaml', 'README.md']

        files = find_workflow_files('/mock/repo')
        expected_files = [
            '/mock/repo/.github/workflows/ci.yml',
            '/mock/repo/.github/workflows/deploy.yaml'
        ]
        self.assertEqual(sorted(files), sorted(expected_files))

        mock_isdir.reset_mock()
        mock_listdir.reset_mock()
        mock_isdir.return_value = False # No workflows dir
        self.assertEqual(find_workflow_files('/mock/repo'), [])

    @patch('builtins.open', new_callable=mock_open)
    def test_lint_workflow_file_no_issues(self, mock_file_open):
        # Mock rationale: Provide a valid workflow YAML content without any issues.
        mock_file_open.return_value.read.return_value = """
name: Good Workflow
on: [push]
jobs:
  build:
    name: Build Job
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo 'Hello'
  test:
    name: Test Job
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: echo 'Test'
concurrency: my-concurrency-group
"""
        issues = lint_workflow_file('good-workflow.yml')
        self.assertEqual(issues, [])

    @patch('builtins.open', new_callable=mock_open)
    def test_lint_workflow_file_missing_workflow_name(self, mock_file_open):
        # Mock rationale: Simulate a workflow file missing the top-level 'name' key.
        mock_file_open.return_value.read.return_value = """
on: [push]
jobs:
  build:
    name: Build Job
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
"""
        issues = lint_workflow_file('missing-name.yml')
        self.assertEqual(len(issues), 1)
        self.assertIn("[WARNING] Workflow 'missing-name.yml' is missing a top-level 'name'.", issues[0])

    @patch('builtins.open', new_callable=mock_open)
    def test_lint_workflow_file_missing_job_name(self, mock_file_open):
        # Mock rationale: Simulate a workflow file where a job is missing its 'name' key.
        mock_file_open.return_value.read.return_value = """
name: Workflow with unnamed job
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
"""
        issues = lint_workflow_file('unnamed-job.yml')
        self.assertEqual(len(issues), 1)
        self.assertIn("[WARNING] Job 'build' is missing a 'name'.", issues[0])

    @patch('builtins.open', new_callable=mock_open)
    def test_lint_workflow_file_missing_runs_on(self, mock_file_open):
        # Mock rationale: Simulate a workflow file where a job is missing 'runs-on'.
        mock_file_open.return_value.read.return_value = """
name: Workflow with missing runs-on
on: [push]
jobs:
  build:
    name: Build Job
    steps:
      - uses: actions/checkout@v4
"""
        issues = lint_workflow_file('missing-runs-on.yml')
        self.assertEqual(len(issues), 1)
        self.assertIn("[WARNING] Job 'build' is missing 'runs-on'.", issues[0])

    @patch('builtins.open', new_callable=mock_open)
    def test_lint_workflow_file_outdated_checkout(self, mock_file_open):
        # Mock rationale: Simulate a workflow file using an outdated actions/checkout version.
        mock_file_open.return_value.read.return_value = """
name: Outdated Checkout Workflow
on: [push]
jobs:
  build:
    name: Build Job
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v1
      - run: echo 'Hello'
  test:
    name: Test Job
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: echo 'Test'
"""
        issues = lint_workflow_file('outdated-checkout.yml')
        self.assertEqual(len(issues), 2)
        self.assertIn("[SUGGESTION] Job 'build' uses 'actions/checkout@v1'.", issues[0])
        self.assertIn("[SUGGESTION] Job 'test' uses 'actions/checkout@v2'.", issues[1])

    @patch('builtins.open', new_callable=mock_open)
    def test_lint_workflow_file_unfiltered_triggers(self, mock_file_open):
        # Mock rationale: Simulate workflow files with unfiltered push/pull_request triggers.
        # Case 1: List of events
        mock_file_open.return_value.read.side_effect = [
            """
name: Unfiltered Push List
on: [push, pull_request]
jobs:
  build:
    name: Build Job
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
""",
            # Case 2: Dict with push, no branches/paths
            """
name: Unfiltered Push Dict
on:
  push:
  pull_request:
    types: [opened]
jobs:
  build:
    name: Build Job
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
""",
            # Case 3: Dict with pull_request, no branches/paths
            """
name: Unfiltered PR Dict
on:
  pull_request:
  push:
    branches: [main]
jobs:
  build:
    name: Build Job
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
"""
        ]

        issues1 = lint_workflow_file('unfiltered-list.yml')
        self.assertEqual(len(issues1), 1)
        self.assertIn("[SUGGESTION] Workflow 'unfiltered-list.yml' triggers on 'push' or 'pull_request' without 'branches' or 'paths'.", issues1[0])

        issues2 = lint_workflow_file('unfiltered-dict-push.yml')
        self.assertEqual(len(issues2), 1)
        self.assertIn("[SUGGESTION] Workflow 'unfiltered-dict-push.yml' triggers on 'push' without 'branches' or 'paths'.", issues2[0])

        issues3 = lint_workflow_file('unfiltered-dict-pr.yml')
        self.assertEqual(len(issues3), 1)
        self.assertIn("[SUGGESTION] Workflow 'unfiltered-dict-pr.yml' triggers on 'pull_request' without 'branches' or 'paths'.", issues3[0])

    @patch('builtins.open', new_callable=mock_open)
    def test_lint_workflow_file_missing_concurrency(self, mock_file_open):
        # Mock rationale: Simulate a workflow file with multiple jobs but no concurrency key.
        mock_file_open.return_value.read.return_value = """
name: Multi-job Workflow
on: [push]
jobs:
  build:
    name: Build Job
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
  test:
    name: Test Job
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
"""
        issues = lint_workflow_file('multi-job-no-concurrency.yml')
        self.assertEqual(len(issues), 1)
        self.assertIn("[SUGGESTION] Workflow 'multi-job-no-concurrency.yml' has multiple jobs but no 'concurrency' key.", issues[0])

    @patch('builtins.open', new_callable=mock_open)
    def test_lint_workflow_file_yaml_error(self, mock_file_open):
        # Mock rationale: Simulate a malformed YAML file.
        mock_file_open.return_value.read.return_value = """
name: Bad YAML
on: [push]
jobs:
  build:
    name: Build Job
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
  - this is not valid yaml
"""
        issues = lint_workflow_file('bad-yaml.yml')
        self.assertEqual(len(issues), 1)
        self.assertIn("[ERROR] YAML parsing error in 'bad-yaml.yml':", issues[0])

    @patch('builtins.open', new_callable=mock_open)
    def test_lint_workflow_file_empty_file(self, mock_file_open):
        # Mock rationale: Simulate an empty workflow file.
        mock_file_open.return_value.read.return_value = ""
        issues = lint_workflow_file('empty.yml')
        self.assertEqual(len(issues), 1)
        self.assertIn("[ERROR] File 'empty.yml' is empty.", issues[0])

    @patch('builtins.open', new_callable=mock_open)
    def test_lint_workflow_file_no_jobs(self, mock_file_open):
        # Mock rationale: Simulate a workflow file with no jobs defined.
        mock_file_open.return_value.read.return_value = """
name: No Jobs Workflow
on: [push]
"""
        issues = lint_workflow_file('no-jobs.yml')
        self.assertEqual(len(issues), 1)
        self.assertIn("[WARNING] Workflow 'no-jobs.yml' has no jobs defined.", issues[0])

    @patch('builtins.open', new_callable=mock_open)
    def test_lint_workflow_file_invalid_yaml_type(self, mock_file_open):
        # Mock rationale: Simulate a workflow file that is valid YAML but not a dictionary.
        mock_file_open.return_value.read.return_value = "- item1\n- item2"
        issues = lint_workflow_file('list-yaml.yml')
        self.assertEqual(len(issues), 1)
        self.assertIn("[ERROR] File 'list-yaml.yml' is not a valid YAML dictionary.", issues[0])

    @patch('builtins.open', new_callable=mock_open)
    def test_lint_workflow_file_invalid_job_type(self, mock_file_open):
        # Mock rationale: Simulate a workflow file with an invalid job definition (not a dictionary).
        mock_file_open.return_value.read.return_value = """
name: Invalid Job Type
on: [push]
jobs:
  build: "this is a string, not a dict"
"""
        issues = lint_workflow_file('invalid-job.yml')
        self.assertEqual(len(issues), 1)
        self.assertIn("[ERROR] Job 'build' in 'invalid-job.yml' is not a valid dictionary.", issues[0])

    @patch('builtins.open', new_callable=mock_open)
    def test_lint_workflow_file_invalid_steps_type(self, mock_file_open):
        # Mock rationale: Simulate a workflow file with an invalid steps definition (not a list).
        mock_file_open.return_value.read.return_value = """
name: Invalid Steps Type
on: [push]
jobs:
  build:
    name: Build Job
    runs-on: ubuntu-latest
    steps: "this is a string, not a list"
"""
        issues = lint_workflow_file('invalid-steps.yml')
        self.assertEqual(len(issues), 1)
        self.assertIn("[ERROR] Steps for job 'build' in 'invalid-steps.yml' is not a valid list.", issues[0])
