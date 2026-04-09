import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Mock rationale: Mocking the docker library to avoid actual Docker interactions during tests.
# This ensures tests are deterministic and offline.

# Add the src directory to the Python path to import main.py
# Mock rationale: This is a common practice for testing modules within a package structure.
# In a real project, this might be handled by setuptools or a proper package setup.
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "..", "src")
sys.path.insert(0, src_dir)

import main

class TestDockerEnvManager(unittest.TestCase):

    @patch('main.Console')
    @patch('main.from_env')
    def setUp(self, mock_from_env, mock_console):
        self.mock_console = mock_console.return_value
        self.mock_docker_client = mock_from_env.return_value
        self.mock_env_dir = MagicMock()
        self.mock_env_dir.glob.return_value = []
        self.mock_env_dir.exists.return_value = True
        self.mock_env_file = MagicMock()
        self.mock_env_file.exists.return_value = True
        self.mock_env_file.stem = "test-env"
        self.mock_env_dir.joinpath.return_value = self.mock_env_file

        # Mock sys.argv for command-line arguments
        self.original_argv = sys.argv

        # Mock subprocess for docker-compose calls
        self.mock_subprocess = patch('main.subprocess')
        self.mock_subprocess_module = self.mock_subprocess.start()
        self.mock_subprocess_module.run.return_value = MagicMock(stdout="", stderr="")

        # Patch the ENV_DIR to use our mock
        patcher = unittest.mock.patch('main.ENV_DIR', self.mock_env_dir)
        self.mock_env_dir_patcher = patcher.start()
        self.addCleanup(patcher.stop)

    def tearDown(self):
        sys.argv = self.original_argv
        self.mock_subprocess.stop()

    def test_get_environments_empty(self):
        self.mock_env_dir.glob.return_value = []
        self.assertEqual(main.get_environments(), [])

    @patch('main.Path')
    def test_get_environments_with_files(self, mock_path):
        mock_file1 = MagicMock()
        mock_file1.stem = "env1"
        mock_file1.is_file.return_value = True
        mock_file2 = MagicMock()
        mock_file2.stem = "env2"
        mock_file2.is_file.return_value = True
        mock_dir = MagicMock()
        mock_dir.glob.return_value = [mock_file1, mock_file2]
        mock_path.return_value = mock_dir
        self.assertEqual(main.get_environments(), ["env1", "env2"])

    def test_start_environment_success(self):
        sys.argv = ["main.py", "up", "test-env"]
        main.main()
        self.mock_subprocess_module.run.assert_called_once_with(
            ["docker-compose", "-f", "/app/environments/test-env.yaml", "up", "-d"],
            capture_output=True,
            text=True,
            check=True
        )
        self.mock_console.print.assert_any_call("[bold green]Starting environment: test-env...[/bold green]")
        self.mock_console.print.assert_any_call("[green]Successfully started test-env.[/green]")

    def test_start_environment_not_found(self):
        self.mock_env_file.exists.return_value = False
        sys.argv = ["main.py", "up", "nonexistent-env"]
        main.main()
        self.mock_console.print.assert_called_with("[bold red]Environment file not found: /app/environments/nonexistent-env.yaml[/bold red]")
        self.mock_subprocess_module.run.assert_not_called()

    def test_start_environment_docker_compose_not_found(self):
        self.mock_subprocess_module.run.side_effect = FileNotFoundError
        sys.argv = ["main.py", "up", "test-env"]
        main.main()
        self.mock_console.print.assert_any_call("[bold red]Error starting test-env:[/bold red]")
        self.mock_console.print.assert_any_call("[bold red]docker-compose command not found. Please ensure it is installed and in your PATH.[/bold red]")

    def test_stop_environment_success(self):
        sys.argv = ["main.py", "down", "test-env"]
        main.main()
        self.mock_subprocess_module.run.assert_called_once_with(
            ["docker-compose", "-f", "/app/environments/test-env.yaml", "down"],
            capture_output=True,
            text=True,
            check=True
        )
        self.mock_console.print.assert_any_call("[bold yellow]Stopping environment: test-env...[/bold yellow]")
        self.mock_console.print.assert_any_call("[yellow]Successfully stopped and removed test-env.[/yellow]")

    def test_stop_environment_not_found(self):
        self.mock_env_file.exists.return_value = False
        sys.argv = ["main.py", "down", "nonexistent-env"]
        main.main()
        self.mock_console.print.assert_called_with("[bold red]Environment file not found: /app/environments/nonexistent-env.yaml[/bold red]")
        self.mock_subprocess_module.run.assert_not_called()

    def test_list_environments_empty(self):
        sys.argv = ["main.py", "list"]
        main.main()
        self.mock_console.print.assert_called_with("[italic]No environments found. Create .yaml files in the environments/ directory.[/italic]")

    @patch('main.Table')
    def test_list_environments_with_running_containers(self, mock_table):
        mock_container_running = MagicMock()
        mock_container_running.name = "running_container"
        mock_container_running.image.tags = ["python:3.9-slim"]
        mock_container_running.status = "running"
        mock_container_running.ports = {"80/tcp": [{"HostIp": "0.0.0.0", "HostPort": "8080"}]}

        mock_container_stopped = MagicMock()
        mock_container_stopped.name = "stopped_container"
        mock_container_stopped.image.tags = ["ubuntu:latest"]
        mock_container_stopped.status = "exited"
        mock_container_stopped.ports = {}

        mock_project_containers = [mock_container_running, mock_container_stopped]
        self.mock_docker_client.containers.list.return_value = mock_project_containers

        self.mock_env_dir.glob.return_value = [self.mock_env_file]
        self.mock_env_file.stem = "test-env"

        sys.argv = ["main.py", "list"]
        main.main()

        self.mock_docker_client.containers.list.assert_called_once()
        mock_table.assert_called_once()
        self.mock_console.print.assert_any_call(mock_table())
        self.mock_console.print.assert_any_call("[bold green]Running[/bold green]")
        self.mock_console.print.assert_any_call("[bold red]Stopped[/bold red]")

    @patch('main.Table')
    def test_get_environment_status_running(self, mock_table):
        mock_container = MagicMock()
        mock_container.name = "my_app_container"
        mock_container.image.tags = ["my-app-image:latest"]
        mock_container.status = "running"
        mock_container.ports = {"8000/tcp": [{"HostIp": "0.0.0.0", "HostPort": "8000"}]}
        self.mock_docker_client.containers.list.return_value = [mock_container]

        sys.argv = ["main.py", "status", "test-env"]
        main.main()

        self.mock_docker_client.containers.list.assert_called_once_with(all=True, filters={'label': 'com.docker.compose.project=test-env'})
        mock_table.assert_called_once()
        self.mock_console.print.assert_any_call(mock_table())
        self.mock_console.print.assert_any_call("[bold green]running[/bold green]")

    def test_get_environment_status_not_running(self):
        self.mock_docker_client.containers.list.return_value = []
        sys.argv = ["main.py", "status", "test-env"]
        main.main()
        self.mock_console.print.assert_called_with("[bold red]Environment 'test-env' is not running.[/bold red]")

    def test_unknown_command(self):
        sys.argv = ["main.py", "foobar"]
        with self.assertRaises(SystemExit):
            main.main()
        self.mock_console.print.assert_called_with("[bold red]Unknown command: foobar[/bold red]")

if __name__ == '__main__':
    unittest.main()
