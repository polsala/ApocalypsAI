import unittest
from unittest.mock import Mock, patch
import sys
import io
import docker
from src.main import get_container_garden_data, render_garden, main

# Mock rationale: We need to simulate Docker daemon responses without actually
# running Docker containers or connecting to a real daemon.
# This involves mocking the docker client and container objects.

class MockContainer:
    """A mock Docker container object."""
    def __init__(self, name, status, health=None):
        self.name = name
        self.status = status
        self._health = health # Store health as a private attribute

    @property
    def health(self):
        """Mock health property."""
        if self._health:
            return {'Status': self._health}
        return None

class TestContainerGardenMonitor(unittest.TestCase):

    def test_get_container_garden_data_healthy(self):
        mock_client = Mock()
        mock_container_healthy = MockContainer("web-app", "running", "healthy")
        mock_client.containers.list.return_value = [mock_container_healthy]

        data = get_container_garden_data(mock_client)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "web-app")
        self.assertEqual(data[0]["plant_type"], "🌱")
        self.assertEqual(data[0]["health"], "healthy")

    def test_get_container_garden_data_unhealthy(self):
        mock_client = Mock()
        mock_container_unhealthy = MockContainer("db-service", "running", "unhealthy")
        mock_client.containers.list.return_value = [mock_container_unhealthy]

        data = get_container_garden_data(mock_client)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "db-service")
        self.assertEqual(data[0]["plant_type"], "🥀")
        self.assertEqual(data[0]["health"], "unhealthy")

    def test_get_container_garden_data_exited(self):
        mock_client = Mock()
        mock_container_exited = MockContainer("old-job", "exited")
        mock_client.containers.list.return_value = [mock_container_exited]

        data = get_container_garden_data(mock_client)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "old-job")
        self.assertEqual(data[0]["plant_type"], "💀")
        self.assertEqual(data[0]["health"], "N/A")

    def test_get_container_garden_data_running_no_health_check(self):
        mock_client = Mock()
        mock_container_running = MockContainer("api-gateway", "running")
        mock_client.containers.list.return_value = [mock_container_running]

        data = get_container_garden_data(mock_client)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "api-gateway")
        self.assertEqual(data[0]["plant_type"], "🌿")
        self.assertEqual(data[0]["health"], "N/A")

    def test_get_container_garden_data_restarting(self):
        mock_client = Mock()
        mock_container_restarting = MockContainer("worker", "restarting")
        mock_client.containers.list.return_value = [mock_container_restarting]

        data = get_container_garden_data(mock_client)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "worker")
        self.assertEqual(data[0]["plant_type"], "🐛")
        self.assertEqual(data[0]["health"], "N/A")

    def test_get_container_garden_data_empty(self):
        mock_client = Mock()
        mock_client.containers.list.return_value = []

        data = get_container_garden_data(mock_client)
        self.assertEqual(len(data), 0)

    def test_render_garden_multiple_plants(self):
        plants_data = [
            {"name": "web-app", "status": "running", "health": "healthy", "plant_type": "🌱"},
            {"name": "db-service", "status": "running", "health": "unhealthy", "plant_type": "🥀"},
            {"name": "old-job", "status": "exited", "health": "N/A", "plant_type": "💀"}
        ]
        output = render_garden(plants_data)
        self.assertIn("🌱 web-app", output)
        self.assertIn("🥀 db-service", output)
        self.assertIn("💀 old-job", output)
        self.assertIn("Garden Legend:", output)

    def test_render_garden_empty(self):
        output = render_garden([])
        self.assertIn("Your container garden is currently empty.", output)

    @patch('src.main.docker.from_env')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_function_success(self, mock_stdout, mock_from_env):
        # Mock rationale: We need to mock the Docker client creation and its
        # subsequent calls to simulate a successful run without a real Docker daemon.
        mock_client = Mock()
        mock_from_env.return_value = mock_client
        mock_container_healthy = MockContainer("test-web", "running", "healthy")
        mock_client.containers.list.return_value = [mock_container_healthy]

        main()
        output = mock_stdout.getvalue()
        self.assertIn("🌱 Nightly Container Garden Monitor 🌿", output)
        self.assertIn("🌱       test-web", output)
        self.assertIn("running", output)
        self.assertIn("healthy", output)

    @patch('src.main.docker.from_env')
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_function_docker_connection_error(self, mock_exit, mock_stderr, mock_from_env):
        # Mock rationale: Simulate a failure to connect to the Docker daemon.
        mock_from_env.side_effect = docker.errors.DockerException("Cannot connect")

        main()
        error_output = mock_stderr.getvalue()
        self.assertIn("Could not connect to Docker daemon: Cannot connect", error_output)
        mock_exit.assert_called_with(1)

    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_get_container_garden_data_api_error_handling(self, mock_exit, mock_stderr):
        # Mock rationale: Simulate an API error when listing containers.
        mock_client = Mock()
        mock_client.containers.list.side_effect = docker.errors.APIError("API error", response=Mock(status_code=500))

        get_container_garden_data(mock_client)

        error_output = mock_stderr.getvalue()
        self.assertIn("Error connecting to Docker daemon: API error", error_output)
        mock_exit.assert_called_with(1)

    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_get_container_garden_data_unexpected_error_handling(self, mock_exit, mock_stderr):
        # Mock rationale: Simulate an unexpected error during container listing.
        mock_client = Mock()
        mock_client.containers.list.side_effect = ValueError("Unexpected issue")

        get_container_garden_data(mock_client)

        error_output = mock_stderr.getvalue()
        self.assertIn("An unexpected error occurred: Unexpected issue", error_output)
        mock_exit.assert_called_with(1)


if __name__ == '__main__':
    unittest.main()
