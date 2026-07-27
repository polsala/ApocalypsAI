import unittest
from unittest.mock import patch, MagicMock, call
import os
import sys

# Mock the main script to avoid actual subprocess calls during tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from main import get_random_name, run_command, start_environment, list_environments, stop_environment_by_name, stop_all_environments


class TestDockerEnvManager(unittest.TestCase):

    @patch('main.random.choice')
    def test_get_random_name(self, mock_choice):
        # Mock rationale: Ensure the random name selection works as expected.
        mock_choice.return_value = "wasteland-workbench"
        self.assertEqual(get_random_name(), "wasteland-workbench")
        mock_choice.assert_called_once()

    @patch('main.subprocess.run')
    def test_run_command_success(self, mock_run):
        # Mock rationale: Verify that subprocess.run is called correctly and its output is processed.
        mock_run.return_value.stdout = "output line 1\noutput line 2"
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        result = run_command(['echo', 'hello'])
        mock_run.assert_called_once_with(['echo', 'hello'], capture_output=True, text=True, check=True)
        self.assertEqual(result, "output line 1\noutput line 2")

    @patch('main.subprocess.run')
    def test_run_command_failure(self, mock_run):
        # Mock rationale: Ensure that command failures are handled and reported.
        mock_run.side_effect = subprocess.CalledProcessError(1, ['echo', 'fail'], stderr="error message")
        with self.assertLogs(level='ERROR') as log:
            with self.assertRaises(SystemExit) as cm:
                run_command(['echo', 'fail'])
            self.assertEqual(cm.exception.code, 1)
        self.assertIn("Command failed:", "".join(log.output))
        self.assertIn("error message", "".join(log.output))

    @patch('main.os.path.exists')
    @patch('main.run_command')
    @patch('main.get_random_name')
    def test_start_environment_success(self, mock_get_random_name, mock_run_command, mock_os_exists):
        # Mock rationale: Simulate a successful environment start.
        mock_os_exists.return_value = True
        mock_get_random_name.return_value = "bunker-builder"
        mock_run_command.return_value = ""
        
        # Mocking the check for existing projects to return no running projects
        mock_run_command.side_effect = [
            "", # For the initial ps -q check
            ""
        ]

        start_environment("my-dev-env.yml")

        mock_os_exists.assert_called_once_with("my-dev-env.yml")
        mock_get_random_name.assert_called_once()
        expected_calls = [
            call(['docker-compose', '-f', 'my-dev-env.yml', 'ps', '-q'], check=False),
            call(['docker-compose', '-f', 'my-dev-env.yml', '-p', 'bunker-builder', 'up', '-d'])
        ]
        mock_run_command.assert_has_calls(expected_calls, any_order=False)

    @patch('main.os.path.exists')
    @patch('main.run_command')
    @patch('main.get_random_name')
    def test_start_environment_file_not_found(self, mock_get_random_name, mock_run_command, mock_os_exists):
        # Mock rationale: Ensure error handling when the compose file is missing.
        mock_os_exists.return_value = False
        with self.assertRaises(SystemExit) as cm:
            start_environment("non-existent-env.yml")
        self.assertEqual(cm.exception.code, 1)
        mock_os_exists.assert_called_once_with("non-existent-env.yml")
        mock_get_random_name.assert_not_called()
        mock_run_command.assert_not_called()

    @patch('main.run_command')
    def test_list_environments_no_running(self, mock_run_command):
        # Mock rationale: Test the case where no Docker Compose environments are running.
        mock_run_command.return_value = ""
        with unittest.mock.patch('builtins.print') as mock_print:
            list_environments()
            mock_print.assert_any_call("No Docker Compose environments found running.")
        mock_run_command.assert_called_once_with(['docker', 'ps', '--format', '{{.Names}}'], check=False)

    @patch('main.run_command')
    @unittest.mock.patch('builtins.print')
    def test_list_environments_with_running(self, mock_print, mock_run_command):
        # Mock rationale: Test listing environments when some are running.
        mock_run_command.return_value = "my-project-web-1\nmy-project-db-1\nanother-project-app-1"
        list_environments()
        mock_print.assert_any_call("Running environments (inferred project names):")
        mock_print.assert_any_call("- another-project")
        mock_print.assert_any_call("- my-project")
        mock_run_command.assert_called_once_with(['docker', 'ps', '--format', '{{.Names}}'], check=False)

    @patch('main.run_command')
    def test_stop_all_environments(self, mock_run_command):
        # Mock rationale: Verify that the stop-all command correctly calls docker-compose down.
        stop_all_environments()
        mock_run_command.assert_called_once_with(['docker-compose', 'down'], check=False)

    @patch('main.os.listdir')
    @patch('main.open', new_callable=unittest.mock.mock_open, read_data='version: \'3.8\'\nservices:\n  web:\n    image: nginx:latest')
    @patch('main.run_command')
    def test_stop_environment_by_name_success(self, mock_run_command, mock_open, mock_listdir):
        # Mock rationale: Simulate stopping a specific environment by name.
        mock_listdir.return_value = ['my-dev-env.yml', 'other.txt']
        mock_run_command.return_value = ""
        stop_environment_by_name("my-dev-env")
        mock_run_command.assert_called_once_with(['docker-compose', '-f', 'my-dev-env.yml', '-p', 'my-dev-env', 'down'], check=False)

    @patch('main.os.listdir')
    @patch('main.run_command')
    def test_stop_environment_by_name_no_compose_file(self, mock_run_command, mock_listdir):
        # Mock rationale: Test stopping an environment when no suitable compose file is found.
        mock_listdir.return_value = ['some_file.txt', 'another.log']
        with unittest.mock.patch('builtins.print') as mock_print:
            stop_environment_by_name("non-existent-env")
            mock_print.assert_any_call("Could not find a suitable compose file to stop environment 'non-existent-env'.", file=sys.stderr)
        mock_run_command.assert_not_called()

if __name__ == '__main__':
    unittest.main()
