import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add the src directory to the path to import mood_ring
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import mood_ring

class TestMoodRing(unittest.TestCase):

    @patch('mood_ring.docker.from_env')
    def test_container_not_found(self, mock_from_env):
        # Mock rationale: Simulates a Docker client that raises NotFound when getting a container.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_client.containers.get.side_effect = mood_ring.docker.errors.NotFound("No such container")

        mood = mood_ring.get_container_mood("non_existent_container")
        self.assertEqual(mood, "Vanished 👻")

    @patch('mood_ring.docker.from_env')
    def test_container_asleep(self, mock_from_env):
        # Mock rationale: Simulates a Docker client returning a stopped container.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_container = MagicMock()
        mock_container.status = 'exited'
        mock_container.attrs = {'State': {'ExitCode': 0}}
        mock_client.containers.get.return_value = mock_container

        mood = mood_ring.get_container_mood("stopped_container")
        self.assertEqual(mood, "Asleep 😴")

    @patch('mood_ring.docker.from_env')
    def test_container_furious_exit_code(self, mock_from_env):
        # Mock rationale: Simulates a Docker client returning an exited container with a non-zero exit code.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_container = MagicMock()
        mock_container.status = 'exited'
        mock_container.attrs = {'State': {'ExitCode': 137}}
        mock_client.containers.get.return_value = mock_container

        mood = mood_ring.get_container_mood("crashed_container")
        self.assertEqual(mood, "Furious 😡")

    @patch('mood_ring.docker.from_env')
    def test_container_furious_restarting(self, mock_from_env):
        # Mock rationale: Simulates a Docker client returning a container in 'restarting' status.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_container = MagicMock()
        mock_container.status = 'restarting'
        mock_client.containers.get.return_value = mock_container

        mood = mood_ring.get_container_mood("restarting_container")
        self.assertEqual(mood, "Furious 😡")

    @patch('mood_ring.docker.from_env')
    def test_container_grumpy_unhealthy(self, mock_from_env):
        # Mock rationale: Simulates a Docker client returning a running container with an 'unhealthy' health status.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_container = MagicMock()
        mock_container.status = 'running'
        mock_container.attrs = {'State': {'Health': {'Status': 'unhealthy'}}},
        mock_container.stats.return_value = iter([self._mock_stats(cpu_percent=10, mem_percent=10)]) # Stats don't matter if unhealthy
        mock_client.containers.get.return_value = mock_container

        mood = mood_ring.get_container_mood("unhealthy_container")
        self.assertEqual(mood, "Grumpy 😠")

    @patch('mood_ring.docker.from_env')
    def test_container_serene(self, mock_from_env):
        # Mock rationale: Simulates a Docker client returning a healthy, low-resource-usage container.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_container = MagicMock()
        mock_container.status = 'running'
        mock_container.attrs = {'State': {'Health': {'Status': 'healthy'}}},
        mock_container.stats.return_value = iter([self._mock_stats(cpu_percent=5, mem_percent=5)])
        mock_client.containers.get.return_value = mock_container

        mood = mood_ring.get_container_mood("serene_container")
        self.assertEqual(mood, "Serene 😌")

    @patch('mood_ring.docker.from_env')
    def test_container_content(self, mock_from_env):
        # Mock rationale: Simulates a Docker client returning a healthy, moderate-resource-usage container.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_container = MagicMock()
        mock_container.status = 'running'
        mock_container.attrs = {'State': {'Health': {'Status': 'healthy'}}},
        mock_container.stats.return_value = iter([self._mock_stats(cpu_percent=30, mem_percent=30)])
        mock_client.containers.get.return_value = mock_container

        mood = mood_ring.get_container_mood("content_container")
        self.assertEqual(mood, "Content 😊")

    @patch('mood_ring.docker.from_env')
    def test_container_anxious_cpu(self, mock_from_env):
        # Mock rationale: Simulates a Docker client returning a healthy, high-CPU-usage container.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_container = MagicMock()
        mock_container.status = 'running'
        mock_container.attrs = {'State': {'Health': {'Status': 'healthy'}}},
        mock_container.stats.return_value = iter([self._mock_stats(cpu_percent=60, mem_percent=10)])
        mock_client.containers.get.return_value = mock_container

        mood = mood_ring.get_container_mood("anxious_cpu_container")
        self.assertEqual(mood, "Anxious 😟")

    @patch('mood_ring.docker.from_env')
    def test_container_anxious_mem(self, mock_from_env):
        # Mock rationale: Simulates a Docker client returning a healthy, high-memory-usage container.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_container = MagicMock()
        mock_container.status = 'running'
        mock_container.attrs = {'State': {'Health': {'Status': 'healthy'}}},
        mock_container.stats.return_value = iter([self._mock_stats(cpu_percent=10, mem_percent=70)])
        mock_client.containers.get.return_value = mock_container

        mood = mood_ring.get_container_mood("anxious_mem_container")
        self.assertEqual(mood, "Anxious 😟")

    @patch('mood_ring.docker.from_env')
    def test_container_anxious_custom_thresholds(self, mock_from_env):
        # Mock rationale: Simulates a Docker client returning a healthy container with usage above custom thresholds.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_container = MagicMock()
        mock_container.status = 'running'
        mock_container.attrs = {'State': {'Health': {'Status': 'healthy'}}},
        mock_container.stats.return_value = iter([self._mock_stats(cpu_percent=60, mem_percent=60)])
        mock_client.containers.get.return_value = mock_container

        with patch.dict(os.environ, {'CPU_ANXIOUS_THRESHOLD': '55', 'MEM_ANXIOUS_THRESHOLD': '55'}):
            mood = mood_ring.get_container_mood("anxious_custom_container")
            self.assertEqual(mood, "Anxious 😟")

    @patch('mood_ring.docker.from_env')
    def test_container_content_custom_thresholds(self, mock_from_env):
        # Mock rationale: Simulates a Docker client returning a healthy container with usage below custom thresholds.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_container = MagicMock()
        mock_container.status = 'running'
        mock_container.attrs = {'State': {'Health': {'Status': 'healthy'}}},
        mock_container.stats.return_value = iter([self._mock_stats(cpu_percent=50, mem_percent=50)])
        mock_client.containers.get.return_value = mock_container

        with patch.dict(os.environ, {'CPU_ANXIOUS_THRESHOLD': '55', 'MEM_ANXIOUS_THRESHOLD': '55'}):
            mood = mood_ring.get_container_mood("content_custom_container")
            self.assertEqual(mood, "Content 😊")

    @patch('mood_ring.docker.from_env')
    def test_container_confused_no_stats(self, mock_from_env):
        # Mock rationale: Simulates a Docker client returning a running container but no stats are available.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_container = MagicMock()
        mock_container.status = 'running'
        mock_container.attrs = {'State': {'Health': {'Status': 'healthy'}}},
        mock_container.stats.return_value = iter([]) # No stats available
        mock_client.containers.get.return_value = mock_container

        mood = mood_ring.get_container_mood("confused_container")
        self.assertEqual(mood, "Confused 🤔")

    def _mock_stats(self, cpu_percent, mem_percent):
        # Helper to create mock stats for CPU and Memory calculations
        # These values are simplified to directly control the calculated percentages
        # In reality, Docker stats are more complex, but for mocking, we control the outcome.
        mock_stats = {
            'cpu_stats': {
                'cpu_usage': {'total_usage': int(1000000000 * cpu_percent), 'percpu_usage': [1,1,1,1]},
                'system_cpu_usage': int(1000000000 * 100),
                'online_cpus': 4
            },
            'precpu_stats': {
                'cpu_usage': {'total_usage': int(1000000000 * cpu_percent / 2)},
                'system_cpu_usage': int(1000000000 * 100 / 2)
            },
            'memory_stats': {
                'usage': int(1000000000 * (mem_percent / 100.0)),
                'limit': 1000000000
            }
        }
        return mock_stats

    @patch('mood_ring.docker.from_env')
    def test_calculate_cpu_percent(self, mock_from_env):
        # Mock rationale: Test the CPU calculation logic in isolation.
        stats = {
            'cpu_stats': {
                'cpu_usage': {'total_usage': 2000000000, 'percpu_usage': [1,1,1,1]},
                'system_cpu_usage': 4000000000,
                'online_cpus': 2
            },
            'precpu_stats': {
                'cpu_usage': {'total_usage': 1000000000},
                'system_cpu_usage': 2000000000
            }
        }
        # (2000M - 1000M) / (4000M - 2000M) * 2 * 100 = (1000M / 2000M) * 2 * 100 = 0.5 * 2 * 100 = 100%
        self.assertAlmostEqual(mood_ring.calculate_cpu_percent(stats), 100.0)

        stats_low_cpu = {
            'cpu_stats': {
                'cpu_usage': {'total_usage': 100000000, 'percpu_usage': [1,1,1,1]},
                'system_cpu_usage': 4000000000,
                'online_cpus': 2
            },
            'precpu_stats': {
                'cpu_usage': {'total_usage': 50000000},
                'system_cpu_usage': 2000000000
            }
        }
        # (100M - 50M) / (4000M - 2000M) * 2 * 100 = (50M / 2000M) * 2 * 100 = 0.025 * 2 * 100 = 5%
        self.assertAlmostEqual(mood_ring.calculate_cpu_percent(stats_low_cpu), 5.0)

    @patch('mood_ring.docker.from_env')
    def test_calculate_mem_percent(self, mock_from_env):
        # Mock rationale: Test the memory calculation logic in isolation.
        stats = {
            'memory_stats': {
                'usage': 500000000,
                'limit': 1000000000
            }
        }
        self.assertAlmostEqual(mood_ring.calculate_mem_percent(stats), 50.0)

        stats_high_mem = {
            'memory_stats': {
                'usage': 900000000,
                'limit': 1000000000
            }
        }
        self.assertAlmostEqual(mood_ring.calculate_mem_percent(stats_high_mem), 90.0)

        stats_no_limit = {
            'memory_stats': {
                'usage': 100000000,
                'limit': 0
            }
        }
        self.assertAlmostEqual(mood_ring.calculate_mem_percent(stats_no_limit), 0.0)

if __name__ == '__main__':
    unittest.main()
