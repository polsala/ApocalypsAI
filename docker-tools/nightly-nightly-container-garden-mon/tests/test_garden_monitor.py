import unittest
from unittest.mock import MagicMock, patch
import json
from src.garden_monitor import get_container_garden_status, format_report

class TestContainerGardenMonitor(unittest.TestCase):

    @patch('src.garden_monitor.docker.from_env')
    def test_get_container_garden_status_no_containers(self, mock_from_env):
        # Mock rationale: Simulate a Docker environment with no running containers.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_client.containers.list.return_value = []

        result = get_container_garden_status()
        self.assertEqual(result, [])
        mock_client.containers.list.assert_called_once_with(all=True)

    @patch('src.garden_monitor.docker.from_env')
    def test_get_container_garden_status_running_healthy(self, mock_from_env):
        # Mock rationale: Simulate a Docker environment with one healthy, running container.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        mock_container = MagicMock()
        mock_container.name = "my-healthy-plant"
        mock_container.short_id = "abc1234"
        mock_container.status = "running"
        mock_container.id = "full_id_abc1234"

        # Mock inspect_container for health status
        mock_client.api.inspect_container.return_value = {
            'State': {'Health': {'Status': 'healthy'}}
        }

        # Mock stats for CPU/Memory
        mock_container.stats.return_value = {
            'cpu_stats': {
                'cpu_usage': {'total_usage': 62500000, 'percpu_usage': [31250000, 31250000]},
                'system_cpu_usage': 200000000,
                'online_cpus': 2
            },
            'precpu_stats': {
                'cpu_usage': {'total_usage': 50000000},
                'system_cpu_usage': 100000000
            },
            'memory_stats': {
                'usage': 50 * 1024 * 1024,  # 50 MB
                'limit': 100 * 1024 * 1024  # 100 MB
            }
        }
        mock_client.containers.list.return_value = [mock_container]

        result = get_container_garden_status()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "my-healthy-plant")
        self.assertEqual(result[0]["garden_status"], "Thriving Bloom")
        self.assertEqual(result[0]["health"], "healthy")
        self.assertEqual(result[0]["cpu_usage_percent"], "25.00%")
        self.assertEqual(result[0]["memory_usage_mb"], "50.00 MB / 100.00 MB")
        self.assertEqual(result[0]["foliage_condition"], "Lush & Green")
        mock_client.containers.list.assert_called_once_with(all=True)
        mock_container.stats.assert_called_once_with(stream=False)

    @patch('src.garden_monitor.docker.from_env')
    def test_get_container_garden_status_running_unhealthy(self, mock_from_env):
        # Mock rationale: Simulate a Docker environment with one unhealthy, running container.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        mock_container = MagicMock()
        mock_container.name = "my-wilting-plant"
        mock_container.short_id = "def5678"
        mock_container.status = "running"
        mock_container.id = "full_id_def5678"

        mock_client.api.inspect_container.return_value = {
            'State': {'Health': {'Status': 'unhealthy'}}
        }

        # Mock stats for CPU/Memory (high usage)
        mock_container.stats.return_value = {
            'cpu_stats': {
                'cpu_usage': {'total_usage': 1050000000, 'percpu_usage': [525000000, 525000000]},
                'system_cpu_usage': 1000000000,
                'online_cpus': 2
            },
            'precpu_stats': {
                'cpu_usage': {'total_usage': 50000000},
                'system_cpu_usage': 100000000
            },
            'memory_stats': {
                'usage': 90 * 1024 * 1024,  # 90 MB
                'limit': 100 * 1024 * 1024  # 100 MB
            }
        }
        mock_client.containers.list.return_value = [mock_container]

        result = get_container_garden_status()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "my-wilting-plant")
        self.assertEqual(result[0]["garden_status"], "Wilting Petal")
        self.assertEqual(result[0]["health"], "unhealthy")
        self.assertIn("MB", result[0]["memory_usage_mb"]) # Check format, specific value depends on mock
        self.assertEqual(result[0]["foliage_condition"], "Thirsty Roots & Overgrown Foliage")


    @patch('src.garden_monitor.docker.from_env')
    def test_get_container_garden_status_exited(self, mock_from_env):
        # Mock rationale: Simulate a Docker environment with one exited container.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        mock_container = MagicMock()
        mock_container.name = "my-dormant-seed"
        mock_container.short_id = "ghi9012"
        mock_container.status = "exited"
        mock_container.id = "full_id_ghi9012"

        mock_client.containers.list.return_value = [mock_container]

        result = get_container_garden_status()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "my-dormant-seed")
        self.assertEqual(result[0]["garden_status"], "Dormant Seed (Exited)")
        self.assertEqual(result[0]["health"], "Unknown") # No healthcheck for exited
        self.assertEqual(result[0]["cpu_usage_percent"], "N/A")
        self.assertEqual(result[0]["memory_usage_mb"], "N/A")
        self.assertEqual(result[0]["foliage_condition"], "N/A")
        mock_client.containers.list.assert_called_once_with(all=True)
        mock_container.stats.assert_not_called() # Stats should not be called for exited containers

    @patch('src.garden_monitor.docker.from_env')
    def test_get_container_garden_status_docker_error(self, mock_from_env):
        # Mock rationale: Simulate a failure to connect to the Docker daemon.
        mock_from_env.side_effect = Exception("Docker daemon not found")

        result = get_container_garden_status()
        self.assertIn("error", result)
        self.assertIn("Docker daemon not found", result["error"])

    def test_format_report_empty(self):
        report_data = []
        formatted_output = format_report(report_data)
        self.assertIn("The garden is empty", formatted_output)

    def test_format_report_with_data(self):
        report_data = [
            {
                "name": "test-plant-1",
                "id": "123",
                "status": "running",
                "health": "healthy",
                "cpu_usage_percent": "10.50%",
                "memory_usage_mb": "200.00 MB / 1024.00 MB",
                "foliage_condition": "Lush & Green",
                "garden_status": "Thriving Bloom"
            },
            {
                "name": "test-plant-2",
                "id": "456",
                "status": "exited",
                "health": "Unknown",
                "cpu_usage_percent": "N/A",
                "memory_usage_mb": "N/A",
                "foliage_condition": "N/A",
                "garden_status": "Dormant Seed (Exited)"
            }
        ]
        formatted_output = format_report(report_data)
        self.assertIn("Plant Name: test-plant-1", formatted_output)
        self.assertIn("Garden Status: Thriving Bloom", formatted_output)
        self.assertIn("Foliage Condition: Lush & Green", formatted_output)
        self.assertIn("Plant Name: test-plant-2", formatted_output)
        self.assertIn("Garden Status: Dormant Seed (Exited)", formatted_output)
        self.assertIn("(Plant is not active, no live stats available)", formatted_output)

    def test_format_report_error(self):
        report_data = {"error": "Failed to connect"}
        formatted_output = format_report(report_data)
        self.assertIn("Garden Report Error: Failed to connect", formatted_output)

    @patch('src.garden_monitor.docker.from_env')
    def test_get_container_garden_status_no_healthcheck(self, mock_from_env):
        # Mock rationale: Simulate a running container without a defined healthcheck.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        mock_container = MagicMock()
        mock_container.name = "no-healthcheck-plant"
        mock_container.short_id = "xyz7890"
        mock_container.status = "running"
        mock_container.id = "full_id_xyz7890"

        # Mock inspect_container to return no health status
        mock_client.api.inspect_container.return_value = {
            'State': {} # No 'Health' key
        }

        # Mock stats (low usage)
        mock_container.stats.return_value = {
            'cpu_stats': {
                'cpu_usage': {'total_usage': 62500000, 'percpu_usage': [31250000, 31250000]},
                'system_cpu_usage': 200000000,
                'online_cpus': 2
            },
            'precpu_stats': {
                'cpu_usage': {'total_usage': 50000000},
                'system_cpu_usage': 100000000
            },
            'memory_stats': {
                'usage': 20 * 1024 * 1024,  # 20 MB
                'limit': 100 * 1024 * 1024  # 100 MB
            }
        }
        mock_client.containers.list.return_value = [mock_container]

        result = get_container_garden_status()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "no-healthcheck-plant")
        self.assertEqual(result[0]["garden_status"], "Budding Sprout (Running)")
        self.assertEqual(result[0]["health"], "No Healthcheck")
        self.assertEqual(result[0]["foliage_condition"], "Lush & Green")

if __name__ == '__main__':
    unittest.main()
