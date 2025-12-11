import unittest
from unittest.mock import patch, mock_open
import yaml

# Assuming the script is named workflow_guardian_angel.py
# If it's in a subdirectory, adjust the import path accordingly
from scripts.workflow_guardian_angel import analyze_workflow, get_workflow_files

class TestWorkflowGuardianAngel(unittest.TestCase):

    @patch('glob.glob')
    def test_get_workflow_files_found(self, mock_glob):
        """Test that get_workflow_files returns correct paths when files are found."""
        mock_glob.return_value = ['.github/workflows/test1.yml', '.github/workflows/test2.yml']
        files = get_workflow_files()
        self.assertEqual(files, ['.github/workflows/test1.yml', '.github/workflows/test2.yml'])
        mock_glob.assert_called_once_with('.github/workflows/*.yml')

    @patch('glob.glob')
    def test_get_workflow_files_not_found(self, mock_glob):
        """Test that get_workflow_files returns empty list when no files are found."""
        mock_glob.return_value = []
        files = get_workflow_files()
        self.assertEqual(files, [])
        mock_glob.assert_called_once_with('.github/workflows/*.yml')

    def test_analyze_workflow_no_issues(self):
        """Test analysis of a clean workflow file."""
        workflow_content = {
            'name': 'My Awesome Workflow',
            'on': 'push',
            'jobs': {
                'build': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'actions/checkout@v4'}
                    ]
                }
            }
        }
        with patch('builtins.open', mock_open(read_data=yaml.dump(workflow_content))):
            findings = analyze_workflow('test_workflow.yml')
            self.assertEqual(findings, [])

    def test_analyze_workflow_missing_runs_on(self):
        """Test analysis of a workflow missing 'runs-on' key."""
        workflow_content = {
            'name': 'Wandering Job Workflow',
            'on': 'push',
            'jobs': {
                'wanderer': {
                    'steps': [
                        {'uses': 'actions/checkout@v4'}
                    ]
                }
            }
        }
        with patch('builtins.open', mock_open(read_data=yaml.dump(workflow_content))):
            findings = analyze_workflow('wandering_job.yml')
            self.assertIn("Job 'wanderer' in 'wandering_job.yml' is missing a 'runs-on' key. It might wander aimlessly!", findings)
            self.assertEqual(len(findings), 1)

    def test_analyze_workflow_frequent_cron(self):
        """Test analysis of a workflow with a very frequent cron schedule."""
        workflow_content = {
            'name': 'Apocalypse Runner',
            'on': {
                'schedule': [
                    {'cron': '* * * * *'}
                ]
            },
            'jobs': {
                'run_fast': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'run': 'echo "Running too fast!"'}
                    ]
                }
            }
        }
        with patch('builtins.open', mock_open(read_data=yaml.dump(workflow_content))):
            findings = analyze_workflow('apocalypse_runner.yml')
            self.assertIn("Workflow 'apocalypse_runner.yml' has a very frequent cron schedule ('* * * * *'). Is it trying to outrun the apocalypse? Consider a less frantic pace.", findings)
            self.assertEqual(len(findings), 1)

    def test_analyze_workflow_yaml_error(self):
        """Test analysis of a malformed YAML workflow file."""
        malformed_yaml = "name: Bad Workflow\n  on: push\njobs:\n  bad_job: \n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n        invalid_syntax: this is not valid yaml"
        with patch('builtins.open', mock_open(read_data=malformed_yaml)):
            findings = analyze_workflow('bad_workflow.yml')
            self.assertIn("Could not parse 'bad_workflow.yml': ... It might be speaking an ancient dialect?", findings)
            self.assertEqual(len(findings), 1)

    def test_analyze_workflow_multiple_issues(self):
        """Test analysis of a workflow with multiple issues."""
        workflow_content = {
            'name': 'Multi-Issue Workflow',
            'on': {
                'schedule': [
                    {'cron': '0 * * * *'}
                ]
            },
            'jobs': {
                'job1': {
                    'steps': [
                        {'uses': 'actions/checkout@v4'}
                    ]
                },
                'job2': {
                    'runs-on': 'windows-latest',
                    'steps': [
                        {'run': 'echo "Hello"'}
                    ]
                }
            }
        }
        with patch('builtins.open', mock_open(read_data=yaml.dump(workflow_content))):
            findings = analyze_workflow('multi_issue.yml')
            self.assertIn("Job 'job1' in 'multi_issue.yml' is missing a 'runs-on' key. It might wander aimlessly!", findings)
            self.assertIn("Workflow 'multi_issue.yml' has a very frequent cron schedule ('* * * * *'). Is it trying to outrun the apocalypse? Consider a less frantic pace.", findings)
            self.assertEqual(len(findings), 2)

    @patch('scripts.workflow_guardian_angel.get_workflow_files')
    @patch('scripts.workflow_guardian_angel.analyze_workflow')
    @patch('builtins.print')
    def test_main_no_findings(self, mock_print, mock_analyze, mock_get_files):
        """Test main function when no findings are reported."""
        mock_get_files.return_value = ['.github/workflows/clean.yml']
        mock_analyze.return_value = []
        
        # Mocking the set-output command for GitHub Actions
        with patch('builtins.print') as mock_print_output:
            # Simulate the print statement that sets output
            def side_effect(text):
                if text.startswith('::set-output'):
                    pass # Do nothing, just prevent it from printing to console
                else:
                    print(text) # Default print behavior for other messages
            mock_print_output.side_effect = side_effect

            # Call the main function
            from scripts.workflow_guardian_angel import main
            main()

            mock_print.assert_any_call("[bold green]Guardian Angel is surveying your workflows...[/bold green]")
            mock_print.assert_any_call("[bold green]All workflows appear to be in good spirits! The Guardian Angel is pleased.[/bold green]")

    @patch('scripts.workflow_guardian_angel.get_workflow_files')
    @patch('scripts.workflow_guardian_angel.analyze_workflow')
    @patch('builtins.print')
    def test_main_with_findings(self, mock_print, mock_analyze, mock_get_files):
        """Test main function when findings are reported."""
        mock_get_files.return_value = ['.github/workflows/issue.yml']
        mock_analyze.return_value = ["- Issue found in issue.yml"]
        
        # Mocking the set-output command for GitHub Actions
        with patch('builtins.print') as mock_print_output:
            # Simulate the print statement that sets output
            def side_effect(text):
                if text.startswith('::set-output'):
                    pass # Do nothing, just prevent it from printing to console
                else:
                    print(text) # Default print behavior for other messages
            mock_print_output.side_effect = side_effect

            # Call the main function
            from scripts.workflow_guardian_angel import main
            main()

            mock_print.assert_any_call("[bold green]Guardian Angel is surveying your workflows...[/bold green]")
            mock_print.assert_any_call("[bold yellow]Guardian Angel found some points of interest![/bold yellow]")

if __name__ == '__main__':
    unittest.main()
