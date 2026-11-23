import unittest
from unittest.mock import MagicMock, patch
import sys
import io

# Mock rationale: We need to test the logic of `get_container_aura` and `main`
# without actually interacting with a live Docker daemon. This requires mocking
# the `docker` library and its client objects.

# Import the functions to be tested from the src directory
# This assumes the test is run from the utility's root directory
# (e.g., `python -m unittest tests/test_aura_reader.py`)
from src.aura_reader import get_container_aura, main

class TestContainerAuraReader(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = io.StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    def _create_mock_container(self, name, status, health_status=None, exit_code=None):
        """Helper to create a mock container object."""
        mock_container = MagicMock()
        mock_container.name = name
        mock_container.status = status
        mock_container.attrs = {'State': {'ExitCode': exit_code}} if exit_code is not None else {}

        if health_status:
            mock_health = MagicMock()
            mock_health.status = health_status
            mock_container.health = mock_health
        else:
            # Ensure health attribute is not present or None if not specified
            if hasattr(mock_container, 'health'):
                del mock_container.health
            mock_container.health = None # Explicitly set to None for consistent mocking

        return mock_container

    @patch('src.aura_reader.docker.from_env')
    def test_main_no_containers(self, mock_from_env):
        # Mock rationale: Simulate a scenario where no Docker containers are found.
        mock_client = MagicMock()
        mock_client.containers.list.return_value = []
        mock_from_env.return_value = mock_client

        main()
        self.assertIn("No Docker containers found.", self.mock_stdout.getvalue())

    @patch('src.aura_reader.docker.from_env')
    def test_main_multiple_containers(self, mock_from_env):
        # Mock rationale: Simulate multiple containers with different states.
        mock_client = MagicMock()
        mock_container_vibrant = self._create_mock_container("web-app", "running", "healthy")
        mock_container_anxious = self._create_mock_container("database", "running", "unhealthy")
        mock_container_serene = self._create_mock_container("old-service", "exited", exit_code=0)
        mock_container_grumpy = self._create_mock_container("failed-job", "exited", exit_code=1)
        mock_container_pondering = self._create_mock_container("new-service", "starting")
        mock_container_mysterious = self._create_mock_container("unknown-state", "paused") # 'paused' is not explicitly handled, should be mysterious

        mock_client.containers.list.return_value = [
            mock_container_vibrant,
            mock_container_anxious,
            mock_container_serene,
            mock_container_grumpy,
            mock_container_pondering,
            mock_container_mysterious
        ]
        mock_from_env.return_value = mock_client

        main()
        output = self.mock_stdout.getvalue()

        self.assertIn("Container 'web-app' is Vibrant.", output)
        self.assertIn("Container 'database' is Anxious.", output)
        self.assertIn("Container 'old-service' is Serene.", output)
        self.assertIn("Container 'failed-job' is Grumpy.", output)
        self.assertIn("Container 'new-service' is Pondering.", output)
        self.assertIn("Container 'unknown-state' is Mysterious.", output)

    @patch('src.aura_reader.docker.from_env')
    def test_main_docker_exception(self, mock_from_env):
        # Mock rationale: Simulate a Docker connection error.
        mock_from_env.side_effect = docker.errors.DockerException("Cannot connect")

        # Capture stderr for error messages
        held_stderr = sys.stderr
        sys.stderr = mock_stderr = io.StringIO()

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)

        sys.stderr = held_stderr # Restore stderr
        self.assertIn("Error connecting to Docker daemon: Cannot connect", mock_stderr.getvalue())

    def test_get_container_aura_vibrant(self):
        container = self._create_mock_container("test", "running", "healthy")
        self.assertEqual(get_container_aura(container), "Vibrant")

    def test_get_container_aura_anxious(self):
        container = self._create_mock_container("test", "running", "unhealthy")
        self.assertEqual(get_container_aura(container), "Anxious")

    def test_get_container_aura_pondering_starting(self):
        container = self._create_mock_container("test", "running", "starting")
        self.assertEqual(get_container_aura(container), "Pondering")

    def test_get_container_aura_pondering_restarting(self):
        container = self._create_mock_container("test", "restarting")
        self.assertEqual(get_container_aura(container), "Pondering")

    def test_get_container_aura_pondering_created(self):
        container = self._create_mock_container("test", "created")
        self.assertEqual(get_container_aura(container), "Pondering")

    def test_get_container_aura_serene(self):
        container = self._create_mock_container("test", "exited", exit_code=0)
        self.assertEqual(get_container_aura(container), "Serene")

    def test_get_container_aura_grumpy_exited_error(self):
        container = self._create_mock_container("test", "exited", exit_code=1)
        self.assertEqual(get_container_aura(container), "Grumpy")

    def test_get_container_aura_grumpy_dead(self):
        container = self._create_mock_container("test", "dead")
        self.assertEqual(get_container_aura(container), "Grumpy")

    def test_get_container_aura_mysterious_running_no_health(self):
        container = self._create_mock_container("test", "running") # No health status
        self.assertEqual(get_container_aura(container), "Mysterious")

    def test_get_container_aura_mysterious_unknown_status(self):
        container = self._create_mock_container("test", "paused") # 'paused' is not explicitly handled
        self.assertEqual(get_container_aura(container), "Mysterious")

if __name__ == '__main__':
    unittest.main()
