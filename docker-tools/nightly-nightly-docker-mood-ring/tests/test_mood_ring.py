import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the src directory to the path for importing mood_ring
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import mood_ring
import docker.errors # Import for mocking specific exceptions

class TestDockerMoodRing(unittest.TestCase):

    @patch('mood_ring.docker.from_env')
    def test_get_container_mood_running_healthy(self, mock_from_env):
        # Mock rationale: Simulating a healthy running container without needing a live Docker daemon.
        mock_container = MagicMock()
        mock_container.status = 'running'
        mock_container.attrs = {'State': {'Health': {'Status': 'healthy'}}}.copy()
        self.assertEqual(mood_ring.get_container_mood(mock_container), "Joyful")

    @patch('mood_ring.docker.from_env')
    def test_get_container_mood_running_unhealthy(self, mock_from_env):
        # Mock rationale: Simulating an unhealthy running container without needing a live Docker daemon.
        mock_container = MagicMock()
        mock_container.status = 'running'
        mock_container.attrs = {'State': {'Health': {'Status': 'unhealthy'}}}.copy()
        self.assertEqual(mood_ring.get_container_mood(mock_container), "Grumpy")

    @patch('mood_ring.docker.from_env')
    def test_get_container_mood_running_no_healthcheck(self, mock_from_env):
        # Mock rationale: Simulating a running container without a healthcheck defined.
        mock_container = MagicMock()
        mock_container.status = 'running'
        mock_container.attrs = {'State': {}}.copy() # No 'Health' key
        self.assertEqual(mood_ring.get_container_mood(mock_container), "Content")

    @patch('mood_ring.docker.from_env')
    def test_get_container_mood_exited(self, mock_from_env):
        # Mock rationale: Simulating an exited container.
        mock_container = MagicMock()
        mock_container.status = 'exited'
        mock_container.attrs = {'State': {}}.copy()
        self.assertEqual(mood_ring.get_container_mood(mock_container), "Sleepy")

    @patch('mood_ring.docker.from_env')
    def test_get_container_mood_restarting(self, mock_from_env):
        # Mock rationale: Simulating a restarting container.
        mock_container = MagicMock()
        mock_container.status = 'restarting'
        mock_container.attrs = {'State': {}}.copy()
        self.assertEqual(mood_ring.get_container_mood(mock_container), "Anxious")

    @patch('mood_ring.docker.from_env')
    def test_get_container_mood_paused(self, mock_from_env):
        # Mock rationale: Simulating a paused container.
        mock_container = MagicMock()
        mock_container.status = 'paused'
        mock_container.attrs = {'State': {}}.copy()
        self.assertEqual(mood_ring.get_container_mood(mock_container), "Pensive")

    @patch('mood_ring.docker.from_env')
    def test_get_container_mood_dead(self, mock_from_env):
        # Mock rationale: Simulating a dead container.
        mock_container = MagicMock()
        mock_container.status = 'dead'
        mock_container.attrs = {'State': {}}.copy()
        self.assertEqual(mood_ring.get_container_mood(mock_container), "At Peace (Exited Permanently)")

    @patch('mood_ring.docker.from_env')
    def test_get_container_mood_unknown(self, mock_from_env):
        # Mock rationale: Simulating a container with an unknown status.
        mock_container = MagicMock()
        mock_container.status = 'unknown_status'
        mock_container.attrs = {'State': {}}.copy()
        self.assertEqual(mood_ring.get_container_mood(mock_container), "Mysterious")

    @patch('mood_ring.docker.from_env')
    @patch('mood_ring.time.sleep', MagicMock()) # Mock sleep to prevent actual delays
    @patch('builtins.print') # Mock print to capture output
    def test_monitor_containers_basic(self, mock_print, mock_from_env):
        # Mock rationale: Simulating Docker client and containers for a single monitoring cycle.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        mock_container1 = MagicMock()
        mock_container1.name = 'web-app'
        mock_container1.short_id = 'abc1'
        mock_container1.status = 'running'
        mock_container1.attrs = {'State': {'Health': {'Status': 'healthy'}}}.copy()

        mock_container2 = MagicMock()
        mock_container2.name = 'database'
        mock_container2.short_id = 'def2'
        mock_container2.status = 'exited'
        mock_container2.attrs = {'State': {}}.copy()

        mock_client.containers.list.return_value = [mock_container1, mock_container2]

        # Simulate one loop iteration then break
        with patch('mood_ring.time.sleep', side_effect=KeyboardInterrupt):
            mood_ring.monitor_containers(interval=1)

        mock_client.containers.list.assert_called_once_with(all=True)
        # Check if print was called with expected moods. The exact timestamp makes direct string comparison hard, so check for substrings.
        output_calls = [call.args[0] for call in mock_print.call_args_list if "Container" in call.args[0]]
        self.assertEqual(len(output_calls), 2)
        self.assertIn("Container 'web-app' (ID: abc1): Joyful", output_calls[0])
        self.assertIn("Container 'database' (ID: def2): Sleepy", output_calls[1])

    @patch('mood_ring.docker.from_env')
    @patch('mood_ring.time.sleep', MagicMock()) # Mock sleep to prevent actual delays
    @patch('builtins.print') # Mock print to capture output
    def test_monitor_containers_target_names(self, mock_print, mock_from_env):
        # Mock rationale: Testing the filtering of containers by name.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        mock_container1 = MagicMock()
        mock_container1.name = 'web-app'
        mock_container1.short_id = 'abc1'
        mock_container1.status = 'running'
        mock_container1.attrs = {'State': {'Health': {'Status': 'healthy'}}}.copy()

        mock_container2 = MagicMock()
        mock_container2.name = 'database'
        mock_container2.short_id = 'def2'
        mock_container2.status = 'exited'
        mock_container2.attrs = {'State': {}}.copy()

        mock_client.containers.list.return_value = [mock_container1, mock_container2]

        with patch('mood_ring.time.sleep', side_effect=KeyboardInterrupt):
            mood_ring.monitor_containers(interval=1, target_names=['web-app'])

        mock_client.containers.list.assert_called_once_with(all=True)
        output_calls = [call.args[0] for call in mock_print.call_args_list if "Container" in call.args[0]]
        self.assertEqual(len(output_calls), 1)
        self.assertIn("Container 'web-app' (ID: abc1): Joyful", output_calls[0])
        self.assertNotIn("database", output_calls[0])

    @patch('mood_ring.docker.from_env', side_effect=docker.errors.DockerException("Cannot connect"))
    @patch('builtins.print')
    def test_monitor_containers_docker_connection_error(self, mock_print, mock_from_env):
        # Mock rationale: Simulating a failure to connect to the Docker daemon.
        mood_ring.monitor_containers(interval=1)
        mock_print.assert_any_call(unittest.mock.ANY) # Check if print was called at all
        self.assertIn("Error connecting to Docker daemon: Cannot connect", mock_print.call_args_list[0].args[0])
        self.assertIn("Ensure Docker is running and /var/run/docker.sock is mounted.", mock_print.call_args_list[1].args[0])


if __name__ == '__main__':
    unittest.main()
