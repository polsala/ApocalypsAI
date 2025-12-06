import unittest
from unittest.mock import patch, mock_open
import os
import sys

# Add the src directory to the path for importing oracle.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import oracle

class TestWorkflowWellnessOracle(unittest.TestCase):

    def test_empty_workflow_file(self):
        # Mock rationale: Simulate an empty workflow file.
        mock_yaml_content = ""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)) as m_open:
            issues = oracle.check_workflow_file('test.yml')
            self.assertIn("WARNING: Workflow file is empty or invalid YAML.", issues)
            m_open.assert_called_once_with('test.yml', 'r')

    def test_invalid_yaml_syntax(self):
        # Mock rationale: Simulate a workflow file with invalid YAML syntax.
        mock_yaml_content = "jobs:\n  - build: - invalid"
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)) as m_open:
            issues = oracle.check_workflow_file('test.yml')
            self.assertTrue(any("ERROR: Invalid YAML syntax:" in issue for issue in issues))
            m_open.assert_called_once_with('test.yml', 'r')

    def test_missing_on_trigger(self):
        # Mock rationale: Simulate a workflow missing the 'on' trigger.
        mock_yaml_content = """
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo 'Hello'
"""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)) as m_open:
            issues = oracle.check_workflow_file('test.yml')
            self.assertIn("WARNING: Workflow is missing an 'on' trigger.", issues)
            m_open.assert_called_once_with('test.yml', 'r')

    def test_valid_workflow(self):
        # Mock rationale: Simulate a perfectly valid workflow file.
        mock_yaml_content = """
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo 'Hello'
"""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)) as m_open:
            issues = oracle.check_workflow_file('test.yml')
            self.assertEqual(issues, [])
            m_open.assert_called_once_with('test.yml', 'r')

    def test_deprecated_set_output(self):
        # Mock rationale: Simulate a workflow using the deprecated '::set-output'.
        mock_yaml_content = """
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: set-var
        run: echo '::set-output name=my_var::value'
"""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)) as m_open:
            issues = oracle.check_workflow_file('test.yml')
            self.assertIn("DEPRECATION: Found '::set-output' in step 'set-var' in job 'test'. Consider using job outputs or environment files.", issues)
            m_open.assert_called_once_with('test.yml', 'r')

    def test_missing_runs_on(self):
        # Mock rationale: Simulate a job missing 'runs-on'.
        mock_yaml_content = """
on: [push]
jobs:
  build:
    steps:
      - run: echo 'Hello'
"""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)) as m_open:
            issues = oracle.check_workflow_file('test.yml')
            self.assertIn("WARNING: Job 'build' is missing 'runs-on'.", issues)
            m_open.assert_called_once_with('test.yml', 'r')

    def test_step_missing_uses_or_run(self):
        # Mock rationale: Simulate a step missing both 'uses' and 'run'.
        mock_yaml_content = """
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Empty Step
"""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)) as m_open:
            issues = oracle.check_workflow_file('test.yml')
            self.assertIn("WARNING: Step 'Empty Step' in job 'build' is missing 'uses' or 'run'.", issues)
            m_open.assert_called_once_with('test.yml', 'r')

    def test_hardcoded_secret_in_step_env(self):
        # Mock rationale: Simulate a hardcoded secret in a step's env block.
        mock_yaml_content = """
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy App
        env:
          MY_API_KEY: 'supersecretlongalphanumericstring12345'
        run: echo 'Deploying'
"""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)) as m_open:
            issues = oracle.check_workflow_file('test.yml')
            self.assertIn("WHIMSICAL WARNING: Potential hardcoded secret 'MY_API_KEY' found in step 'Deploy App' in job 'deploy' env. Consider using GitHub Secrets.", issues)
            m_open.assert_called_once_with('test.yml', 'r')

    def test_hardcoded_secret_in_job_env(self):
        # Mock rationale: Simulate a hardcoded secret in a job's env block.
        mock_yaml_content = """
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      MY_AUTH_TOKEN: 'anotherlongalphanumerictokenstringabcde'
    steps:
      - run: echo 'Deploying'
"""
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)) as m_open:
            issues = oracle.check_workflow_file('test.yml')
            self.assertIn("WHIMSICAL WARNING: Potential hardcoded secret 'MY_AUTH_TOKEN' found in job 'deploy' env. Consider using GitHub Secrets.", issues)
            m_open.assert_called_once_with('test.yml', 'r')

    def test_main_function_integration(self):
        # Mock rationale: Simulate multiple workflow files and test the main function's aggregation.
        mock_files = {
            'workflow1.yml': """
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo 'Hello'
""", # This workflow is valid
            'workflow2.yml': """
jobs:
  test:
    steps:
      - run: echo '::set-output name=var::val'
""" # This workflow has issues
        }

        def mock_walk(path):
            # Mock rationale: Simulate os.walk for finding workflow files.
            yield 'mock_workflows_dir', [], list(mock_files.keys())

        m_open = mock_open()
        m_open.side_effect = lambda filename, mode: unittest.mock.mock_open(read_data=mock_files[os.path.basename(filename)]).return_value

        with patch('builtins.open', m_open),
             patch('os.path.isdir', return_value=True),
             patch('os.walk', mock_walk),
             patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout:
            
            oracle.main('mock_workflows_dir')
            output = mock_stdout.getvalue()
            
            self.assertIn("Scanning workflows in mock_workflows_dir...", output)
            self.assertNotIn("File: mock_workflows_dir/workflow1.yml", output) # Valid workflow should not be reported
            self.assertIn("File: mock_workflows_dir/workflow2.yml", output)
            self.assertIn("WARNING: Workflow is missing an 'on' trigger.", output)
            self.assertIn("WARNING: Job 'test' is missing 'runs-on'.", output)
            self.assertIn("DEPRECATION: Found '::set-output' in step '#1' in job 'test'.", output)
            self.assertIn("All workflows scanned. May your automation be ever well!", output)
            self.assertNotIn("All workflows are in peak wellness! No issues found.", output) # Because workflow2 has issues

if __name__ == '__main__':
    unittest.main()
