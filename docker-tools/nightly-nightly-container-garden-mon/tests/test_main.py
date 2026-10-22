import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Helper to make hash deterministic for testing purposes
# Mock rationale: Python's built-in hash() for strings can be randomized across runs
# (e.g., due to PYTHONHASHSEED). For deterministic tests of the whimsical resource
# checks, we temporarily override hash() for specific mock IDs to ensure consistent results.
_original_hash = __builtins__.hash
def _deterministic_hash(obj):
    if isinstance(obj, str) and obj.startswith(("db_id_thirsty_", "web_id_sunny_", "mix_")):
        # A simple sum of ordinals is deterministic and sufficient for testing this logic.
        return sum(ord(c) for c in obj)
    return _original_hash(obj)

# Temporarily replace the built-in hash for the test module
__builtins__.hash = _deterministic_hash

# Add the src directory to the path to allow importing main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from main import get_container_garden_report
import docker.errors # Import for APIError

class TestContainerGardenMonitor(unittest.TestCase):

    @patch('main.docker.from_env')
    def test_no_containers(self, mock_from_env):
        # Mock rationale: Simulate a Docker environment with no running containers.
        mock_client = MagicMock()
        mock_client.containers.list.return_value = []
        mock_from_env.return_value = mock_client

        report = get_container_garden_report(mock_client)
        self.assertIn("Your container garden is empty!", report)
        mock_client.containers.list.assert_called_once_with(all=True)

    @patch('main.docker.from_env')
    def test_running_container_no_issues(self, mock_from_env):
        # Mock rationale: Simulate a healthy, running container with no log errors.
        mock_container = MagicMock()
        mock_container.name = "healthy-web-app"
        mock_container.status = "running"
        mock_container.attrs = {'State': {'StartedAt': '2023-01-01T12:00:00Z'}}
        mock_container.logs.return_value = b"INFO: Application started successfully."
        mock_container.id = "abc123def456" # Needed for hash() in main.py, but won't trigger special conditions

        mock_client = MagicMock()
        mock_client.containers.list.return_value = [mock_container]
        mock_from_env.return_value = mock_client

        report = get_container_garden_report(mock_client)
        self.assertIn("[🌱] healthy-web-app (Running): Up 2023-01-01. Blooming beautifully! Logs are clear.", report)
        mock_container.logs.assert_called_once_with(tail=10, stream=False)

    @patch('main.docker.from_env')
    def test_running_container_with_errors_in_logs(self, mock_from_env):
        # Mock rationale: Simulate a running container that has errors in its logs.
        mock_container = MagicMock()
        mock_container.name = "flailing-worker"
        mock_container.status = "running"
        mock_container.attrs = {'State': {'StartedAt': '2023-01-02T10:00:00Z'}}
        mock_container.logs.return_value = b"ERROR: Failed to process item. Retrying...\nWARN: High memory usage."
        mock_container.id = "ghi789jkl012" # Needed for hash() in main.py, but won't trigger special conditions

        mock_client = MagicMock()
        mock_client.containers.list.return_value = [mock_container]
        mock_from_env.return_value = mock_client

        report = get_container_garden_report(mock_client)
        self.assertIn("[🍂] flailing-worker (Running): Up 2023-01-02. Showing some wilting leaves! Errors detected in logs.", report)
        mock_container.logs.assert_called_once_with(tail=10, stream=False)

    @patch('main.docker.from_env')
    def test_exited_container(self, mock_from_env):
        # Mock rationale: Simulate a container that has stopped.
        mock_container = MagicMock()
        mock_container.name = "old-batch-job"
        mock_container.status = "exited"
        mock_container.attrs = {'State': {'StartedAt': '2023-01-03T08:00:00Z'}} # StartedAt is still present even if exited
        mock_container.logs.return_value = b"" # No logs needed for exited status
        mock_container.id = "mno345pqr678" # Needed for hash() in main.py

        mock_client = MagicMock()
        mock_client.containers.list.return_value = [mock_container]
        mock_from_env.return_value = mock_client

        report = get_container_garden_report(mock_client)
        self.assertIn("[❌] old-batch-job (Exited): This plant has withered. It's no longer running.", report)

    @patch('main.docker.from_env')
    def test_docker_api_error(self, mock_from_env):
        # Mock rationale: Simulate a failure to connect to the Docker daemon.
        mock_client = MagicMock()
        mock_client.containers.list.side_effect = docker.errors.APIError("Cannot connect", 500, "Server Error")
        mock_from_env.return_value = mock_client

        report = get_container_garden_report(mock_client)
        self.assertIn("[🔥] The garden gate is locked! Could not connect to Docker daemon: Cannot connect", report)
        mock_client.containers.list.assert_called_once_with(all=True)

    @patch('main.docker.from_env')
    def test_database_container_thirsty_simulation(self, mock_from_env):
        # Mock rationale: Simulate a database container that is "thirsty" based on its name and deterministic ID hash.
        mock_container = MagicMock()
        mock_container.name = "my-database-service"
        mock_container.status = "running"
        mock_container.attrs = {'State': {'StartedAt': '2023-01-04T09:00:00Z'}}
        mock_container.logs.return_value = b"INFO: DB running."
        mock_container.id = "db_id_thirsty_0" # This ID's deterministic hash % 3 == 0
        
        mock_client = MagicMock()
        mock_client.containers.list.return_value = [mock_container]
        mock_from_env.return_value = mock_client

        report = get_container_garden_report(mock_client)
        self.assertIn("[💧] my-database-service (Running): Up 2023-01-04. Blooming beautifully! Logs are clear. A bit thirsty! High memory usage detected (simulated 85%). Consider watering it with more RAM.", report)

    @patch('main.docker.from_env')
    def test_web_container_sunny_simulation(self, mock_from_env):
        # Mock rationale: Simulate a web container that is "soaking up the sun" based on its name and deterministic ID hash.
        mock_container = MagicMock()
        mock_container.name = "nginx-proxy"
        mock_container.status = "running"
        mock_container.attrs = {'State': {'StartedAt': '2023-01-05T11:00:00Z'}}
        mock_container.logs.return_value = b"INFO: Nginx started."
        mock_container.id = "web_id_sunny_1" # This ID's deterministic hash % 5 == 0

        mock_client = MagicMock()
        mock_client.containers.list.return_value = [mock_container]
        mock_from_env.return_value = mock_client

        report = get_container_garden_report(mock_client)
        self.assertIn("[☀️] nginx-proxy (Running): Up 2023-01-05. Blooming beautifully! Logs are clear. Soaking up the sun! High CPU usage detected (simulated 70%). Ensure it has enough light.", report)

    @patch('main.docker.from_env')
    def test_mixed_containers(self, mock_from_env):
        # Mock rationale: Simulate a mix of healthy, error, and exited containers.
        mock_healthy = MagicMock()
        mock_healthy.name = "app-server"
        mock_healthy.status = "running"
        mock_healthy.attrs = {'State': {'StartedAt': '2023-01-06T13:00:00Z'}}
        mock_healthy.logs.return_value = b"INFO: All good."
        mock_healthy.id = "mix_healthy_id" # Won't trigger special resource conditions based on name

        mock_error = MagicMock()
        mock_error.name = "data-ingest"
        mock_error.status = "running"
        mock_error.attrs = {'State': {'StartedAt': '2023-01-07T14:00:00Z'}}
        mock_error.logs.return_value = b"ERROR: Connection lost."
        mock_error.id = "mix_error_id" # Won't trigger special resource conditions based on name

        mock_exited = MagicMock()
        mock_exited.name = "old-backup"
        mock_exited.status = "exited"
        mock_exited.attrs = {'State': {'StartedAt': '2023-01-08T15:00:00Z'}}
        mock_exited.logs.return_value = b""
        mock_exited.id = "mix_exited_id" # Won't trigger special resource conditions, as it's exited

        mock_client = MagicMock()
        mock_client.containers.list.return_value = [mock_healthy, mock_error, mock_exited]
        mock_from_env.return_value = mock_client

        report = get_container_garden_report(mock_client)
        self.assertIn("[🌱] app-server (Running): Up 2023-01-06. Blooming beautifully! Logs are clear.", report)
        self.assertIn("[🍂] data-ingest (Running): Up 2023-01-07. Showing some wilting leaves! Errors detected in logs.", report)
        self.assertIn("[❌] old-backup (Exited): This plant has withered. It's no longer running.", report)

    @patch('main.docker.from_env')
    def test_container_logs_permission_error(self, mock_from_env):
        # Mock rationale: Simulate a container where logs cannot be accessed due to permissions or other issues.
        mock_container = MagicMock()
        mock_container.name = "secure-app"
        mock_container.status = "running"
        mock_container.attrs = {'State': {'StartedAt': '2023-01-09T16:00:00Z'}}
        mock_container.logs.side_effect = docker.errors.APIError("Permission denied", 403, "Forbidden")
        mock_container.id = "secure_id" # Won't trigger special resource conditions

        mock_client = MagicMock()
        mock_client.containers.list.return_value = [mock_container]
        mock_from_env.return_value = mock_client

        report = get_container_garden_report(mock_client)
        self.assertIn("secure-app (Running): Up 2023-01-09. Couldn't check logs (perhaps no logs or permissions): Permission denied", report)


if __name__ == '__main__':
    unittest.main()
