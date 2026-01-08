import unittest
from unittest.mock import patch, MagicMock
import yaml
import os

# Mock the DockerEnvManager class to avoid actual Docker calls during tests
class MockDockerEnvManager:
    def __init__(self, env_dir="environments", dockerfile_dir="dockerfiles"):
        self.env_dir = env_dir
        self.dockerfile_dir = dockerfile_dir
        self.environments = {}
        self.load_environments()

    def load_environments(self):
        # Mock loading environments from a predefined structure
        self.environments = {
            "python-dev": {
                "name": "python-dev",
                "image": "python:3.10-slim",
                "ports": ["8000:8000"],
                "volumes": [".:/app"],
                "commands": ["pip install -r requirements.txt"]
            },
            "node-dev": {
                "name": "node-dev",
                "image": "node:18-alpine",
                "ports": ["3000:3000"],
                "volumes": ["./src:/usr/src/app"],
                "environment": ["NODE_ENV=development"]
            },
            "custom-build": {
                "name": "custom-build",
                "dockerfile": "my_custom.Dockerfile",
                "ports": ["9000:9000"]
            }
        }

    def get_env_config(self, env_name):
        return self.environments.get(env_name)

    def run_command(self, cmd_list):
        # Mock successful command execution
        print(f"Mock running command: {' '.join(cmd_list)}")
        return True

    def up(self, env_name):
        config = self.get_env_config(env_name)
        if not config:
            print(f"Mock: Environment '{env_name}' not found.")
            return
        print(f"Mock: Starting environment '{env_name}'...")
        if "commands" in config:
            print(f"Mock: Executing post-start commands for '{env_name}'...")
            for cmd in config["commands"]:
                print(f"Mock: Executing '{cmd}'")

    def down(self, env_name):
        print(f"Mock: Stopping and removing environment '{env_name}'...")

    def logs(self, env_name):
        print(f"Mock: Logs for environment '{env_name}':")

    def exec(self, env_name, command):
        print(f"Mock: Executing command in '{env_name}': {command}")


class TestDockerEnvManager(unittest.TestCase):

    @patch('src.main.DockerEnvManager', new=MockDockerEnvManager)
    def setUp(self):
        # Mock the main function to use our mock manager
        self.manager = MockDockerEnvManager()

    def test_load_environments(self):
        # Mock environments are pre-loaded in MockDockerEnvManager.__init__
        self.assertIn("python-dev", self.manager.environments)
        self.assertIn("node-dev", self.manager.environments)
        self.assertIn("custom-build", self.manager.environments)
        self.assertEqual(self.manager.environments["python-dev"]["image"], "python:3.10-slim")

    @patch('src.main.subprocess.run')
    def test_up_with_image(self, mock_run):
        # Mock rationale: Simulate successful Docker run command.
        mock_run.return_value = MagicMock(stdout="Container started", stderr="", returncode=0)
        self.manager.up("python-dev")
        # Check if docker run command was called with correct arguments
        mock_run.assert_any_call([
            'docker', 'run', '-d', '--name', 'apoc-env-python-dev',
            '-i', 'python:3.10-slim',
            '-p', '8000:8000',
            '-v', './:/app'
        ], capture_output=True, text=True, check=True)
        # Check if post-start command was executed
        mock_run.assert_any_call([
            'docker', 'exec', 'apoc-env-python-dev', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True, check=True)

    @patch('src.main.subprocess.run')
    def test_up_with_dockerfile(self, mock_run):
        # Mock rationale: Simulate successful Docker build and run commands.
        mock_run.side_effect = [
            MagicMock(stdout="Image built", stderr="", returncode=0), # Docker build
            MagicMock(stdout="Container started", stderr="", returncode=0) # Docker run
        ]
        self.manager.up("custom-build")
        # Check if docker build command was called
        mock_run.assert_any_call([
            'docker', 'build', '-t', 'apoc-env-custom-build-custom', '-f', 'my_custom.Dockerfile', 'dockerfiles'
        ], capture_output=True, text=True, check=True)
        # Check if docker run command was called with the custom image
        mock_run.assert_any_call([
            'docker', 'run', '-d', '--name', 'apoc-env-custom-build',
            '-i', 'apoc-env-custom-build-custom',
            '-p', '9000:9000'
        ], capture_output=True, text=True, check=True)

    @patch('src.main.subprocess.run')
    def test_down(self, mock_run):
        # Mock rationale: Simulate successful Docker stop and rm commands.
        mock_run.side_effect = [
            MagicMock(stdout="Container stopped", stderr="", returncode=0),
            MagicMock(stdout="Container removed", stderr="", returncode=0)
        ]
        self.manager.down("python-dev")
        mock_run.assert_any_call(['docker', 'stop', 'apoc-env-python-dev'], capture_output=True, text=True, check=True)
        mock_run.assert_any_call(['docker', 'rm', 'apoc-env-python-dev'], capture_output=True, text=True, check=True)

    @patch('src.main.subprocess.run')
    def test_logs(self, mock_run):
        # Mock rationale: Simulate successful Docker logs command.
        mock_run.return_value = MagicMock(stdout="Log line 1\nLog line 2", stderr="", returncode=0)
        self.manager.logs("node-dev")
        mock_run.assert_called_once_with(['docker', 'logs', 'apoc-env-node-dev'], capture_output=True, text=True, check=True)

    @patch('src.main.subprocess.run')
    def test_exec(self, mock_run):
        # Mock rationale: Simulate successful Docker exec command.
        mock_run.return_value = MagicMock(stdout="Command output", stderr="", returncode=0)
        self.manager.exec("python-dev", "ls -l")
        mock_run.assert_called_once_with(['docker', 'exec', 'apoc-env-python-dev', 'ls', '-l'], capture_output=True, text=True, check=True)

    def test_up_nonexistent_env(self):
        with self.assertLogs(level='ERROR') as cm:
            self.manager.up("nonexistent-env")
            self.assertIn("Environment 'nonexistent-env' not found.", cm.output[0])

if __name__ == '__main__':
    unittest.main()
