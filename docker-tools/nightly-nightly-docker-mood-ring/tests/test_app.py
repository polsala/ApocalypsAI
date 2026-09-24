import unittest
from unittest.mock import Mock, patch
from src.app import assign_mood, get_container_metrics

class TestDockerMoodRing(unittest.TestCase):

    def test_assign_mood_lost_in_void(self):
        # Mock rationale: Test mood assignment for non-running containers.
        self.assertEqual(assign_mood(0, 0, 'exited'), "Lost in the Void 👻")
        self.assertEqual(assign_mood(0, 0, 'dead'), "Lost in the Void 👻")
        self.assertEqual(assign_mood(0, 0, 'created'), "Lost in the Void 👻")

    def test_assign_mood_overwhelmed(self):
        # Mock rationale: Test mood assignment for high resource usage.
        self.assertEqual(assign_mood(90, 10, 'running'), "Overwhelmed 🥵")
        self.assertEqual(assign_mood(10, 90, 'running'), "Overwhelmed 🥵")
        self.assertEqual(assign_mood(86, 86, 'running'), "Overwhelmed 🥵")

    def test_assign_mood_anxious(self):
        # Mock rationale: Test mood assignment for moderate resource usage.
        self.assertEqual(assign_mood(60, 10, 'running'), "Anxious 😬")
        self.assertEqual(assign_mood(10, 60, 'running'), "Anxious 😬")
        self.assertEqual(assign_mood(51, 51, 'running'), "Anxious 😬")

    def test_assign_mood_busy_bee(self):
        # Mock rationale: Test mood assignment for active but not stressed resource usage.
        self.assertEqual(assign_mood(15, 5, 'running'), "Busy Bee 🐝")
        self.assertEqual(assign_mood(5, 15, 'running'), "Busy Bee 🐝")
        self.assertEqual(assign_mood(10, 10, 'running'), "Busy Bee 🐝")
        self.assertEqual(assign_mood(49, 49, 'running'), "Busy Bee 🐝") # Just below anxious threshold

    def test_assign_mood_snoozing(self):
        # Mock rationale: Test mood assignment for very low resource usage.
        self.assertEqual(assign_mood(1, 1, 'running'), "Snoozing 😴")
        self.assertEqual(assign_mood(4, 4, 'running'), "Snoozing 😴")
        self.assertEqual(assign_mood(0, 0, 'running'), "Snoozing 😴")

    def test_assign_mood_zen(self):
        # Mock rationale: Test mood assignment for normal, healthy resource usage.
        self.assertEqual(assign_mood(7, 7, 'running'), "Zen 🙏")
        self.assertEqual(assign_mood(9.9, 9.9, 'running'), "Zen 🙏")

    @patch('src.app.docker.from_env')
    def test_get_container_metrics_success(self, mock_docker_from_env):
        # Mock rationale: Simulate a container with valid stats to test metric calculation.
        mock_container = Mock()
        mock_container.stats.return_value = {
            'cpu_stats': {
                'cpu_usage': {'total_usage': 200000000, 'percpu_usage': [100000000, 100000000]},
                'system_cpu_usage': 1000000000,
                'online_cpus': 2
            },
            'precpu_stats': {
                'cpu_usage': {'total_usage': 100000000, 'percpu_usage': [50000000, 50000000]},
                'system_cpu_usage': 500000000,
                'online_cpus': 2
            },
            'memory_stats': {
                'usage': 500000000, # 500MB
                'limit': 1000000000 # 1GB
            }
        }
        cpu, mem = get_container_metrics(mock_container)
        # Expected CPU: (200M-100M)/(1000M-500M) * 2 * 100 = (100M/500M) * 2 * 100 = 0.2 * 2 * 100 = 40.0
        # Expected Mem: 500M/1000M * 100 = 50.0
        self.assertAlmostEqual(cpu, 40.0, places=2)
        self.assertAlmostEqual(mem, 50.0, places=2)

    @patch('src.app.docker.from_env')
    def test_get_container_metrics_no_stats(self, mock_docker_from_env):
        # Mock rationale: Simulate a container with no stats available.
        mock_container = Mock()
        mock_container.stats.return_value = None # No stats available
        cpu, mem = get_container_metrics(mock_container)
        self.assertEqual(cpu, 0.0)
        self.assertEqual(mem, 0.0)

    @patch('src.app.docker.from_env')
    def test_get_container_metrics_partial_stats(self, mock_docker_from_env):
        # Mock rationale: Simulate a container with incomplete stats to ensure graceful handling.
        mock_container = Mock()
        mock_container.stats.return_value = {
            'cpu_stats': {
                'cpu_usage': {'total_usage': 200000000}
            },
            'precpu_stats': {
                'cpu_usage': {'total_usage': 100000000},
                'system_cpu_usage': 500000000,
                'online_cpus': 2
            },
            'memory_stats': {
                'usage': 500000000,
                'limit': 0 # Edge case for division by zero
            }
        }
        cpu, mem = get_container_metrics(mock_container)
        self.assertEqual(cpu, 0.0) # Should default to 0 if calculation fails due to missing keys or division by zero
        self.assertEqual(mem, 0.0) # Should default to 0 if calculation fails due to missing keys or division by zero
