import unittest
from unittest import mock
import sys
import io
import json
import time

# Import the functions to be tested
from src.monitor import get_container_stats, analyze_plant_health, main

class MockContainer:
    """Mock Docker container object."""
    def __init__(self, name, stats_data):
        self.name = name
        self._stats_data = stats_data

    def stats(self, stream=False):
        # Mock rationale: Simulate Docker API's container.stats() method.
        # It returns a dictionary of stats for a container.
        return self._stats_data

class TestContainerGardenMonitor(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print output
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = io.StringIO()
        self.held_stderr = sys.stderr
        sys.stderr = self.mock_stderr = io.StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    # Mock data for container stats
    MOCK_STATS_HEALTHY = {
        "cpu_stats": {
            "cpu_usage": {"total_usage": 100000000, "percpu_usage": [50000000, 50000000]},
            "system_cpu_usage": 200000000,
            "online_cpus": 2
        },
        "precpu_stats": {
            "cpu_usage": {"total_usage": 50000000, "percpu_usage": [25000000, 25000000]},
            "system_cpu_usage": 100000000,
            "online_cpus": 2
        },
        "memory_stats": {"usage": 100 * 1024 * 1024, "limit": 1024 * 1024 * 1024}, # 100MB / 1GB
        "networks": {"eth0": {"rx_bytes": 1000000, "tx_bytes": 500000}}, # 1MB RX, 0.5MB TX
        "blkio_stats": {"io_service_bytes_recursive": []}
    }

    MOCK_STATS_HIGH_CPU = {
        "cpu_stats": {
            "cpu_usage": {"total_usage": 1000000000, "percpu_usage": [500000000, 500000000]},
            "system_cpu_usage": 200000000,
            "online_cpus": 2
        },
        "precpu_stats": {
            "cpu_usage": {"total_usage": 50000000, "percpu_usage": [25000000, 25000000]},
            "system_cpu_usage": 100000000,
            "online_cpus": 2
        },
        "memory_stats": {"usage": 100 * 1024 * 1024, "limit": 1024 * 1024 * 1024},
        "networks": {"eth0": {"rx_bytes": 1000000, "tx_bytes": 500000}},
        "blkio_stats": {"io_service_bytes_recursive": []}
    }

    MOCK_STATS_HIGH_MEM = {
        "cpu_stats": {
            "cpu_usage": {"total_usage": 100000000, "percpu_usage": [50000000, 50000000]},
            "system_cpu_usage": 200000000,
            "online_cpus": 2
        },
        "precpu_stats": {
            "cpu_usage": {"total_usage": 50000000, "percpu_usage": [25000000, 25000000]},
            "system_cpu_usage": 100000000,
            "online_cpus": 2
        },
        "memory_stats": {"usage": 950 * 1024 * 1024, "limit": 1024 * 1024 * 1024}, # 950MB / 1GB
        "networks": {"eth0": {"rx_bytes": 1000000, "tx_bytes": 500000}},
        "blkio_stats": {"io_service_bytes_recursive": []}
    }

    MOCK_STATS_HIGH_IO = {
        "cpu_stats": {
            "cpu_usage": {"total_usage": 100000000, "percpu_usage": [50000000, 50000000]},
            "system_cpu_usage": 200000000,
            "online_cpus": 2
        },
        "precpu_stats": {
            "cpu_usage": {"total_usage": 50000000, "percpu_usage": [25000000, 25000000]},
            "system_cpu_usage": 100000000,
            "online_cpus": 2
        },
        "memory_stats": {"usage": 100 * 1024 * 1024, "limit": 1024 * 1024 * 1024},
        "networks": {"eth0": {"rx_bytes": 1000000, "tx_bytes": 500000}},
        "blkio_stats": {"io_service_bytes_recursive": [
            {"major": 253, "minor": 0, "op": "Read", "value": 120 * 1024 * 1024}, # 120MB Read
            {"major": 253, "minor": 0, "op": "Write", "value": 10 * 1024 * 1024}  # 10MB Write
        ]}
    }

    MOCK_STATS_HIGH_NET = {
        "cpu_stats": {
            "cpu_usage": {"total_usage": 100000000, "percpu_usage": [50000000, 50000000]},
            "system_cpu_usage": 200000000,
            "online_cpus": 2
        },
        "precpu_stats": {
            "cpu_usage": {"total_usage": 50000000, "percpu_usage": [25000000, 25000000]},
            "system_cpu_usage": 100000000,
            "online_cpus": 2
        },
        "memory_stats": {"usage": 100 * 1024 * 1024, "limit": 1024 * 1024 * 1024},
        "networks": {"eth0": {"rx_bytes": 15 * 1024 * 1024, "tx_bytes": 10 * 1024 * 1024}}, # 15MB RX, 10MB TX
        "blkio_stats": {"io_service_bytes_recursive": []}
    }

    def test_get_container_stats(self):
        mock_container = MockContainer("test-plant", self.MOCK_STATS_HEALTHY)
        stats = get_container_stats(mock_container)
        self.assertEqual(stats, self.MOCK_STATS_HEALTHY)

    def test_analyze_plant_health_healthy(self):
        report = analyze_plant_health("healthy-plant", self.MOCK_STATS_HEALTHY)
        self.assertEqual(report["name"], "healthy-plant")
        self.assertEqual(report["status"], "Thriving")
        self.assertEqual(report["emoji"], "🌱")
        self.assertIn("50.00% CPU", report["sunlight"])
        self.assertIn("9.77% MEM", report["water"])
        self.assertIn("R:0.00MB W:0.00MB", report["soil_nutrients"])
        self.assertIn("RX:0.95MB TX:0.48MB", report["pollination"])

    def test_analyze_plant_health_high_cpu(self):
        report = analyze_plant_health("sun-scorched-plant", self.MOCK_STATS_HIGH_CPU)
        self.assertEqual(report["status"], "Sun-scorched")
        self.assertEqual(report["emoji"], "☀️")
        self.assertIn("950.00% CPU", report["sunlight"]) # This is expected due to the large delta in mock data

    def test_analyze_plant_health_high_mem(self):
        report = analyze_plant_health("parched-plant", self.MOCK_STATS_HIGH_MEM)
        self.assertEqual(report["status"], "Parched")
        self.assertEqual(report["emoji"], "💧")
        self.assertIn("92.77% MEM", report["water"])

    def test_analyze_plant_health_high_io(self):
        report = analyze_plant_health("soil-churning-plant", self.MOCK_STATS_HIGH_IO)
        self.assertEqual(report["status"], "Soil-churning")
        self.assertEqual(report["emoji"], "🪱")
        self.assertIn("R:120.00MB W:10.00MB", report["soil_nutrients"])

    def test_analyze_plant_health_high_net(self):
        report = analyze_plant_health("buzzing-plant", self.MOCK_STATS_HIGH_NET)
        self.assertEqual(report["status"], "Buzzing with Pollinators")
        self.assertEqual(report["emoji"], "🐝")
        self.assertIn("RX:15.00MB TX:10.00MB", report["pollination"])

    def test_analyze_plant_health_no_stats(self):
        report = analyze_plant_health("no-data-plant", None)
        self.assertEqual(report["status"], "Wilted (No Data)")
        self.assertEqual(report["emoji"], "🥀")

    @mock.patch('docker.from_env')
    def test_main_no_containers(self, mock_from_env):
        # Mock rationale: Simulate no running containers.
        mock_client = mock.Mock()
        mock_client.containers.list.return_value = []
        mock_from_env.return_value = mock_client

        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("The container garden is empty. No plants to monitor! 🌻", output)

    @mock.patch('docker.from_env')
    def test_main_with_containers(self, mock_from_env):
        # Mock rationale: Simulate two containers with different health states.
        mock_client = mock.Mock()
        mock_container1 = MockContainer("my-web-app", self.MOCK_STATS_HEALTHY)
        mock_container2 = MockContainer("my-db", self.MOCK_STATS_HIGH_MEM)
        mock_client.containers.list.return_value = [mock_container1, mock_container2]
        mock_from_env.return_value = mock_client

        # Mock time.strftime to make output deterministic
        with mock.patch('time.strftime', return_value="2023-10-27 10:00:00"):
            main()

        output = self.mock_stdout.getvalue()
        self.assertIn("--- ApocalypsAI Container Garden Report ---", output)
        self.assertIn("Report generated: 2023-10-27 10:00:00", output)
        self.assertIn("🌱 my-web-app (Thriving)", output)
        self.assertIn("Sunlight: 50.00% CPU", output)
        self.assertIn("Water: 9.77% MEM (100.00MB)", output)
        self.assertIn("💧 my-db (Parched)", output)
        self.assertIn("Water: 92.77% MEM (950.00MB)", output)
        self.assertIn("-------------------------------------------", output)

    @mock.patch('docker.from_env')
    def test_main_docker_exception(self, mock_from_env):
        # Mock rationale: Simulate a Docker connection error.
        mock_from_env.side_effect = docker.errors.DockerException("Cannot connect to Docker daemon")

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        error_output = self.mock_stderr.getvalue()
        self.assertIn("Error connecting to Docker daemon: Cannot connect to Docker daemon", error_output)
        self.assertIn("Please ensure Docker is running and the Docker socket is accessible.", error_output)
