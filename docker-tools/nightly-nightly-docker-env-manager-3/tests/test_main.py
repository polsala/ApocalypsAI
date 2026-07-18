import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Mock the docker library to avoid actual Docker operations during tests
class MockDockerClient:
    def __init__(self):
        self.images = MagicMock()
        self.containers = MagicMock()

class MockImageCollection:
    def build(self, path, tag, rm):
        # Mock rationale: Simulate a successful image build.
        mock_image = MagicMock()
        mock_image.tags = [tag]
        return mock_image, ["build log line"]

class MockContainerCollection:
    def get(self, name):
        # Mock rationale: Simulate finding a container.
        mock_container = MagicMock()
        mock_container.name = name
        mock_container.id = f"mock_id_for_{name}"
        mock_container.logs.return_value = b"Mock log output"
        return mock_container

    def list(self, filters=None):
        # Mock rationale: Simulate an empty list of containers for 'list' command.
        # For 'up' command, we'll mock the creation of a container with a label.
        if filters and filters.get('label') == 'apoc-env-manager=true':
            return [] # No containers with this label initially
        return []

    def run(self, image_tag, detach, name, volumes):
        # Mock rationale: Simulate starting a container.
        mock_container = MagicMock()
        mock_container.name = name
        mock_container.id = f"mock_id_for_{name}"
        mock_container.stop = MagicMock()
        mock_container.remove = MagicMock()
        return mock_container

class MockContainer:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.stop = MagicMock()
        self.remove = MagicMock()
        self.logs = MagicMock(return_value=b"Mock log output")


class TestDockerEnvManager(unittest.TestCase):

    @patch('docker.from_env', return_value=MockDockerClient())
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('os.path.isdir', return_value=True)
    def test_start_environment_success(self, mock_isdir, mock_stderr, mock_stdout, mock_docker_from_env):
        # Mock rationale: Ensure the Docker client and its methods are mocked.
        mock_client = mock_docker_from_env()
        mock_client.images.build.return_value = (MagicMock(tags=['test-env']), ["build log"])
        mock_client.containers.run.return_value = MockContainer('test-env', 'mock_id_123')

        # Mock sys.argv to simulate command line arguments
        original_argv = sys.argv
        sys.argv = ["main.py", "up", "test-env", "./path/to/dockerfile"]

        # Mock os.environ to simulate the label being set
        original_environ = os.environ.copy()
        os.environ['APOC_ENV_MANAGER_LABEL'] = 'true'

        try:
            import main # Import after mocking sys.argv
            main.main()

            mock_client.images.build.assert_called_once_with(path="./path/to/dockerfile", tag="test-env", rm=True)
            mock_client.containers.run.assert_called_once_with("test-env", detach=True, name="test-env", volumes={'var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'}})
            mock_stdout.write.assert_any_call("Image 'test-env' built successfully.\n")
            mock_stdout.write.assert_any_call("Environment 'test-env' started with container ID: mock_id_123\n")
        finally:
            sys.argv = original_argv
            os.environ = original_environ

    @patch('docker.from_env', return_value=MockDockerClient())
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('os.path.isdir', return_value=False)
    def test_start_environment_invalid_path(self, mock_isdir, mock_stderr, mock_stdout, mock_docker_from_env):
        # Mock rationale: Ensure error handling for invalid Dockerfile paths.
        original_argv = sys.argv
        sys.argv = ["main.py", "up", "test-env", "./invalid/path"]
        try:
            import main
            main.main()
            mock_stderr.write.assert_called_once_with("Error: Dockerfile path './invalid/path' is not a valid directory.\n")
        finally:
            sys.argv = original_argv

    @patch('docker.from_env', return_value=MockDockerClient())
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('os.path.isdir', return_value=True)
    def test_stop_environment_success(self, mock_isdir, mock_stderr, mock_stdout, mock_docker_from_env):
        # Mock rationale: Ensure stopping and removing a container works.
        mock_client = mock_docker_from_env()
        mock_container = MockContainer('test-env', 'mock_id_123')
        mock_client.containers.get.return_value = mock_container

        original_argv = sys.argv
        sys.argv = ["main.py", "down", "test-env"]
        try:
            import main
            main.main()
            mock_container.stop.assert_called_once()
            mock_container.remove.assert_called_once()
            mock_stdout.write.assert_called_once_with("Environment 'test-env' stopped and removed.\n")
        finally:
            sys.argv = original_argv

    @patch('docker.from_env', return_value=MockDockerClient())
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    def test_stop_environment_not_found(self, mock_stderr, mock_stdout, mock_docker_from_env):
        # Mock rationale: Ensure error handling when environment is not found.
        mock_client = mock_docker_from_env()
        mock_client.containers.get.side_effect = docker.errors.NotFound("No such container")

        original_argv = sys.argv
        sys.argv = ["main.py", "down", "non-existent-env"]
        try:
            import main
            main.main()
            mock_stderr.write.assert_called_once_with("Error: Environment 'non-existent-env' not found.\n")
        finally:
            sys.argv = original_argv

    @patch('docker.from_env', return_value=MockDockerClient())
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    def test_list_environments_empty(self, mock_stderr, mock_stdout, mock_docker_from_env):
        # Mock rationale: Ensure 'list' command handles no running environments.
        mock_client = mock_docker_from_env()
        mock_client.containers.list.return_value = []

        original_argv = sys.argv
        sys.argv = ["main.py", "list"]
        try:
            import main
            main.main()
            mock_stdout.write.assert_called_once_with("No managed environments running.\n")
        finally:
            sys.argv = original_argv

    @patch('docker.from_env', return_value=MockDockerClient())
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    def test_list_environments_with_containers(self, mock_stderr, mock_stdout, mock_docker_from_env):
        # Mock rationale: Ensure 'list' command shows running environments.
        mock_client = mock_docker_from_env()
        mock_container1 = MockContainer('env1', 'mock_id_abc')
        mock_container2 = MockContainer('env2', 'mock_id_def')
        mock_client.containers.list.return_value = [mock_container1, mock_container2]

        original_argv = sys.argv
        sys.argv = ["main.py", "list"]
        try:
            import main
            main.main()
            mock_stdout.write.assert_any_call("Running managed environments:\n")
            mock_stdout.write.assert_any_call("- env1 (ID: mock_id_abc)\n")
            mock_stdout.write.assert_any_call("- env2 (ID: mock_id_def)\n")
        finally:
            sys.argv = original_argv

    @patch('docker.from_env', return_value=MockDockerClient())
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    def test_show_logs_success(self, mock_stderr, mock_stdout, mock_docker_from_env):
        # Mock rationale: Ensure logs are fetched and displayed correctly.
        mock_client = mock_docker_from_env()
        mock_container = MockContainer('test-env', 'mock_id_123')
        mock_container.logs.return_value = b"Log line 1\nLog line 2"
        mock_client.containers.get.return_value = mock_container

        original_argv = sys.argv
        sys.argv = ["main.py", "logs", "test-env"]
        try:
            import main
            main.main()
            mock_container.logs.assert_called_once()
            mock_stdout.write.assert_any_call("Logs for 'test-env':\n")
            mock_stdout.write.assert_any_call("Log line 1\nLog line 2")
        finally:
            sys.argv = original_argv

    @patch('docker.from_env', return_value=MockDockerClient())
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    def test_unknown_command(self, mock_stderr, mock_stdout, mock_docker_from_env):
        # Mock rationale: Ensure handling of unknown commands.
        original_argv = sys.argv
        sys.argv = ["main.py", "unknown-command"]
        try:
            import main
            main.main()
            mock_stderr.write.assert_called_once_with("Unknown command: unknown-command\n")
        finally:
            sys.argv = original_argv

if __name__ == '__main__':
    unittest.main()
