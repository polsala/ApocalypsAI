import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add the src directory to the path to allow importing mood_ring
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from mood_ring import get_container_mood, main
import docker.errors

class TestMoodRing(unittest.TestCase):

    @patch('docker.from_env')
    def test_get_container_mood_running_healthy(self, mock_from_env):
        # Mock rationale: Simulate a healthy running container without needing a real Docker daemon.
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_container.status = 'running'
        mock_container.attrs = {'State': {'Health': {'Status': 'healthy'}}}.copy() # Use .copy() to prevent shared mutable state issues if attrs were modified in a test
        mock_client.containers.get.return_value = mock_container
        mock_from_env.return_value = mock_client

        mood = get_container_mood("my-healthy-app", mock_client)
        self.assertEqual(mood, "Serene 😌")
        mock_client.containers.get.assert_called_with("my-healthy-app")

    @patch('docker.from_env')
    def test_get_container_mood_running_unhealthy(self, mock_from_env):
        # Mock rationale: Simulate an unhealthy running container without needing a real Docker daemon.
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_container.status = 'running'
        mock_container.attrs = {'State': {'Health': {'Status': 'unhealthy'}}}.copy()
        mock_client.containers.get.return_value = mock_container
        mock_from_env.return_value = mock_client

        mood = get_container_mood("my-unhealthy-app", mock_client)
        self.assertEqual(mood, "Anxious 😨")

    @patch('docker.from_env')
    def test_get_container_mood_exited(self, mock_from_env):
        # Mock rationale: Simulate an exited container without needing a real Docker daemon.
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_container.status = 'exited'
        mock_container.attrs = {'State': {}}.copy() # No health info for exited
        mock_client.containers.get.return_value = mock_container
        mock_from_env.return_value = mock_client

        mood = get_container_mood("my-stopped-app", mock_client)
        self.assertEqual(mood, "Grumpy 😠")

    @patch('docker.from_env')
    def test_get_container_mood_restarting(self, mock_from_env):
        # Mock rationale: Simulate a restarting container without needing a real Docker daemon.
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_container.status = 'restarting'
        mock_container.attrs = {'State': {}}.copy() # No health info for restarting
        mock_client.containers.get.return_value = mock_container
        mock_from_env.return_value = mock_client

        mood = get_container_mood("my-restarting-app", mock_client)
        self.assertEqual(mood, "Anxious 😨")

    @patch('docker.from_env')
    def test_get_container_mood_not_found(self, mock_from_env):
        # Mock rationale: Simulate a container not being found without needing a real Docker daemon.
        mock_client = MagicMock()
        mock_client.containers.get.side_effect = docker.errors.NotFound("Container not found")
        mock_from_env.return_value = mock_client

        mood = get_container_mood("non-existent-app", mock_client)
        self.assertEqual(mood, "Invisible 👻 (Not Found)")

    @patch('docker.from_env')
    def test_get_container_mood_api_error(self, mock_from_env):
        # Mock rationale: Simulate a Docker API error without needing a real Docker daemon.
        mock_client = MagicMock()
        mock_client.containers.get.side_effect = docker.errors.APIError("API error", response=MagicMock(status_code=500))
        mock_from_env.return_value = mock_client

        mood = get_container_mood("problematic-app", mock_client)
        self.assertTrue("Troubled ⛈️ (API Error:" in mood)

    @patch('docker.from_env')
    def test_get_container_mood_running_no_health(self, mock_from_env):
        # Mock rationale: Simulate a running container without a health check defined.
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_container.status = 'running'
        mock_container.attrs = {'State': {}}.copy() # No Health key
        mock_client.containers.get.return_value = mock_container
        mock_from_env.return_value = mock_client

        mood = get_container_mood("my-simple-app", mock_client)
        self.assertEqual(mood, "Pensive 🧠")

    @patch('docker.from_env')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('os.getenv')
    def test_main_success(self, mock_getenv, mock_stdout, mock_from_env):
        # Mock rationale: Simulate successful execution of main without a real Docker daemon or actual environment variables.
        mock_getenv.return_value = "container1,container2"
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        # Mock container1
        mock_container1 = MagicMock()
        mock_container1.status = 'running'
        mock_container1.attrs = {'State': {'Health': {'Status': 'healthy'}}}.copy()

        # Mock container2
        mock_container2 = MagicMock()
        mock_container2.status = 'exited'
        mock_container2.attrs = {'State': {}}.copy()

        mock_client.containers.get.side_effect = [mock_container1, mock_container2]

        main()

        output = mock_stdout.getvalue()
        self.assertIn("Container 'container1': Serene 😌", output)
        self.assertIn("Container 'container2': Grumpy 😠", output)
        mock_client.containers.get.assert_any_call("container1")
        mock_client.containers.get.assert_any_call("container2")

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('os.getenv')
    def test_main_no_container_names_env(self, mock_getenv, mock_exit, mock_stdout):
        # Mock rationale: Simulate the scenario where CONTAINER_NAMES is not set, expecting an error and exit.
        mock_getenv.return_value = ""
        main()
        self.assertIn("Error: CONTAINER_NAMES environment variable not set.", mock_stdout.getvalue())
        mock_exit.assert_called_with(1)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('os.getenv')
    @patch('docker.from_env')
    def test_main_docker_connection_error(self, mock_from_env, mock_getenv, mock_exit, mock_stdout):
        # Mock rationale: Simulate a failure to connect to the Docker daemon, expecting an error and exit.
        mock_getenv.return_value = "container1"
        mock_from_env.side_effect = Exception("Cannot connect to Docker")
        main()
        self.assertIn("Error connecting to Docker daemon: Cannot connect to Docker", mock_stdout.getvalue())
        mock_exit.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
