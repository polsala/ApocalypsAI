import unittest
from unittest.mock import patch, mock_open
import os

# Mock rationale: We are mocking file system operations and YAML parsing
# to ensure deterministic and offline testing of the validation logic.

# Assuming the script is in the same directory or accessible via PYTHONPATH
# If not, adjust the import path accordingly.
from scripts.validate_github_actions import find_workflow_files, validate_workflow

class TestGitHubActionsValidator(unittest.TestCase):

    @patch('glob.glob')
    def test_find_workflow_files_found(self, mock_glob):
        """Test that find_workflow_files returns correct paths when files are found."""
        mock_glob.return_value = [
            '.github/workflows/main.yml',
            '.github/workflows/deploy.yml'
        ]
        files = find_workflow_files()
        self.assertEqual(files, ['.github/workflows/main.yml', '.github/workflows/deploy.yml'])
        mock_glob.assert_called_once_with('.github/workflows/*.yml')

    @patch('glob.glob')
    def test_find_workflow_files_not_found(self, mock_glob):
        """Test that find_workflow_files returns an empty list when no files are found."""
        mock_glob.return_value = []
        files = find_workflow_files()
        self.assertEqual(files, [])
        mock_glob.assert_called_once_with('.github/workflows/*.yml')

    @patch('builtins.open', new_callable=mock_open, read_data='''
name: Test Workflow

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Run script
        run: echo "Hello"
''')
    @patch('yaml.safe_load')
    def test_validate_workflow_no_errors(self, mock_safe_load, mock_file_open):
        """Test that validate_workflow returns no errors for a clean workflow."""
        mock_safe_load.return_value = {
            'name': 'Test Workflow',
            'on': ['push'],
            'jobs': {
                'build': {
                    'runs-on': 'ubuntu-latest',
                    'permissions': {'contents': 'read'},
                    'steps': [
                        {'name': 'Checkout', 'uses': 'actions/checkout@v4'},
                        {'name': 'Run script', 'run': 'echo "Hello"'}
                    ]
                }
            }
        }
        errors = validate_workflow('.github/workflows/test.yml')
        self.assertEqual(errors, [])
        mock_file_open.assert_called_once_with('.github/workflows/test.yml', 'r')

    @patch('builtins.open', new_callable=mock_open, read_data='''
name: Test Workflow with Issues

on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write # Problematic permission
      secrets: write # Problematic permission
    steps:
      - name: Deploy step
        run: echo "Deploying with ${{ secrets.ANY_SECRET }}" # Problematic secret usage
''')
    @patch('yaml.safe_load')
    def test_validate_workflow_with_errors(self, mock_safe_load, mock_file_open):
        """Test that validate_workflow catches common permission and secret issues."""
        mock_safe_load.return_value = {
            'name': 'Test Workflow with Issues',
            'on': ['push'],
            'jobs': {
                'deploy': {
                    'runs-on': 'ubuntu-latest',
                    'permissions': {'contents': 'write', 'secrets': 'write'},
                    'steps': [
                        {'name': 'Deploy step', 'run': 'echo "Deploying with ${{ secrets.ANY_SECRET }}"'} 
                    ]
                }
            }
        }
        errors = validate_workflow('.github/workflows/test_issues.yml')
        self.assertIn("`test_issues.yml`: Job 'deploy' grants `write` permissions to `contents`. Consider using more granular permissions.", errors)
        self.assertIn("`test_issues.yml`: Job 'deploy' grants `write` permissions to `secrets`. Consider using more granular permissions.", errors)
        self.assertIn("`test_issues.yml`: Job 'deploy' uses `secrets.ANY_SECRET`. This is generally discouraged. Consider using specific secrets.", errors)
        self.assertEqual(len(errors), 3)
        mock_file_open.assert_called_once_with('.github/workflows/test_issues.yml', 'r')

    @patch('builtins.open', new_callable=mock_open, read_data='''
name: Empty Workflow
''')
    @patch('yaml.safe_load')
    def test_validate_workflow_empty_file(self, mock_safe_load, mock_file_open):
        """Test that validate_workflow handles empty YAML content."""
        mock_safe_load.return_value = None
        errors = validate_workflow('.github/workflows/empty.yml')
        self.assertIn("Workflow file is empty.", errors)
        self.assertEqual(len(errors), 1)

    @patch('builtins.open', new_callable=mock_open, read_data='''
This is not YAML
''')
    @patch('yaml.safe_load')
    def test_validate_workflow_invalid_yaml(self, mock_safe_load, mock_file_open):
        """Test that validate_workflow handles invalid YAML content."""
        mock_safe_load.side_effect = yaml.YAMLError("Invalid YAML")
        errors = validate_workflow('.github/workflows/invalid.yml')
        self.assertIn("Could not parse YAML file: Invalid YAML", errors)
        self.assertEqual(len(errors), 1)

if __name__ == '__main__':
    unittest.main()
