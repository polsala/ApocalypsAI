import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add the src directory to the path to allow importing app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import get_stack_health, main, COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_BLUE

class TestDockerMoodLamp(unittest.TestCase):

    def setUp(self):
        # Reset environment variables for each test
        if "COMPOSE_PROJECT_NAME" in os.environ:
            del os.environ["COMPOSE_PROJECT_NAME"]
        if "CHECK_INTERVAL_SECONDS" in os.environ:
            del os.environ["CHECK_INTERVAL_SECONDS"]

    # Mock rationale: We need to simulate Docker daemon responses without actually running Docker containers,
    # ensuring tests are deterministic and offline. This involves mocking the docker client and container objects.

    @patch('app.docker.from_env')
    def test_get_stack_health_all_healthy(self, mock_from_env):
        mock_client = MagicMock()
        mock_container1 = MagicMock()
        mock_container1.status = 'running'
        mock_container1.health = MagicMock(status='healthy')
        mock_container1.labels = {'com.docker.compose.project': 'test_project'}

        mock_container2 = MagicMock()
        mock_container2.status = 'running'
        mock_container2.health = MagicMock(status='healthy')
        mock_container2.labels = {'com.docker.compose.project': 'test_project'}

        mock_client.containers.list.return_value = [mock_container1, mock_container2]
        mock_from_env.return_value = mock_client

        color, message = get_stack_health(mock_client, 'test_project')
        self.assertEqual(color, 'green')
        self.assertIn('All Systems Go!', message)

    @patch('app.docker.from_env')
    def test_get_stack_health_one_unhealthy(self, mock_from_env):
        mock_client = MagicMock()
        mock_container1 = MagicMock()
        mock_container1.status = 'running'
        mock_container1.health = MagicMock(status='healthy')
        mock_container1.labels = {'com.docker.compose.project': 'test_project'}

        mock_container2 = MagicMock()
        mock_container2.status = 'running'
        mock_container2.health = MagicMock(status='unhealthy') # This one is unhealthy
        mock_container2.labels = {'com.docker.compose.project': 'test_project'}

        mock_client.containers.list.return_value = [mock_container1, mock_container2]
        mock_from_env.return_value = mock_client

        color, message = get_stack_health(mock_client, 'test_project')
        self.assertEqual(color, 'red')
        self.assertIn('Trouble in Paradise!', message)

    @patch('app.docker.from_env')
    def test_get_stack_health_one_exited(self, mock_from_env):
        mock_client = MagicMock()
        mock_container1 = MagicMock()
        mock_container1.status = 'running'
        mock_container1.health = MagicMock(status='healthy')
        mock_container1.labels = {'com.docker.compose.project': 'test_project'}

        mock_container2 = MagicMock()
        mock_container2.status = 'exited' # This one exited
        mock_container2.health = MagicMock(status='healthy') # Health status might still be 'healthy' from last check
        mock_container2.labels = {'com.docker.compose.project': 'test_project'}

        mock_client.containers.list.return_value = [mock_container1, mock_container2]
        mock_from_env.return_value = mock_client

        color, message = get_stack_health(mock_client, 'test_project')
        self.assertEqual(color, 'red')
        self.assertIn('Trouble in Paradise!', message)

    @patch('app.docker.from_env')
    def test_get_stack_health_one_restarting(self, mock_from_env):
        mock_client = MagicMock()
        mock_container1 = MagicMock()
        mock_container1.status = 'running'
        mock_container1.health = MagicMock(status='healthy')
        mock_container1.labels = {'com.docker.compose.project': 'test_project'}

        mock_container2 = MagicMock()
        mock_container2.status = 'restarting' # This one is restarting
        mock_container2.health = MagicMock(status='starting') # Health status might be 'starting'
        mock_container2.labels = {'com.docker.compose.project': 'test_project'}

        mock_client.containers.list.return_value = [mock_container1, mock_container2]
        mock_from_env.return_value = mock_client

        color, message = get_stack_health(mock_client, 'test_project')
        self.assertEqual(color, 'yellow')
        self.assertIn('A Bit Wobbly...', message)

    @patch('app.docker.from_env')
    def test_get_stack_health_no_containers(self, mock_from_env):
        mock_client = MagicMock()
        mock_client.containers.list.return_value = []
        mock_from_env.return_value = mock_client

        color, message = get_stack_health(mock_client, 'test_project')
        self.assertEqual(color, 'blue')
        self.assertIn('No containers found', message)

    @patch('app.docker.from_env')
    def test_get_stack_health_docker_exception(self, mock_from_env):
        mock_client = MagicMock()
        mock_client.containers.list.side_effect = docker.errors.DockerException("Connection error")
        mock_from_env.return_value = mock_client

        color, message = get_stack_health(mock_client, 'test_project')
        self.assertEqual(color, 'red')
        self.assertIn('Error connecting to Docker', message)

    @patch('app.docker.from_env')
    def test_get_stack_health_no_project_name(self, mock_from_env):
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        color, message = get_stack_health(mock_client, '')
        self.assertEqual(color, 'blue')
        self.assertIn('COMPOSE_PROJECT_NAME not set', message)

    @patch('app.time.sleep', MagicMock())
    @patch('app.print_mood')
    @patch('app.docker.from_env')
    @patch('app.os.getenv')
    def test_main_no_project_name_env(self, mock_getenv, mock_from_env, mock_print_mood):
        mock_getenv.side_effect = lambda key, default=None: {
            "COMPOSE_PROJECT_NAME": None, # Simulate not set
            "CHECK_INTERVAL_SECONDS": "1"
        }.get(key, default)

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        mock_print_mood.assert_any_call(COLOR_RED, "🔴 Error: COMPOSE_PROJECT_NAME environment variable is not set.")

    @patch('app.time.sleep', MagicMock())
    @patch('app.print_mood')
    @patch('app.docker.from_env')
    @patch('app.os.getenv')
    def test_main_docker_connection_failure(self, mock_getenv, mock_from_env, mock_print_mood):
        mock_getenv.side_effect = lambda key, default=None: {
            "COMPOSE_PROJECT_NAME": "test_project",
            "CHECK_INTERVAL_SECONDS": "1"
        }.get(key, default)
        mock_from_env.side_effect = docker.errors.DockerException("Cannot connect")

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        mock_print_mood.assert_any_call(COLOR_RED, "🔴 Failed to connect to Docker daemon: Cannot connect")

    @patch('app.time.sleep', MagicMock())
    @patch('app.print_mood')
    @patch('app.docker.from_env')
    @patch('app.os.getenv')
    def test_main_loop_and_exit(self, mock_getenv, mock_from_env, mock_print_mood):
        mock_getenv.side_effect = lambda key, default=None: {
            "COMPOSE_PROJECT_NAME": "test_project",
            "CHECK_INTERVAL_SECONDS": "1"
        }.get(key, default)

        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_container.status = 'running'
        mock_container.health = MagicMock(status='healthy')
        mock_container.labels = {'com.docker.compose.project': 'test_project'}
        mock_client.containers.list.return_value = [mock_container]
        mock_from_env.return_value = mock_client

        # Simulate KeyboardInterrupt after a few iterations
        mock_print_mood.side_effect = [None, None, None, KeyboardInterrupt]

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        mock_print_mood.assert_any_call(COLOR_BLUE, "🔵 Exiting Mood Lamp. Goodbye!")

    @patch('app.docker.from_env')
    def test_get_stack_health_no_healthcheck(self, mock_from_env):
        mock_client = MagicMock()
        mock_container1 = MagicMock()
        mock_container1.status = 'running'
        # No health attribute
        mock_container1.labels = {'com.docker.compose.project': 'test_project'}

        mock_client.containers.list.return_value = [mock_container1]
        mock_from_env.return_value = mock_client

        color, message = get_stack_health(mock_client, 'test_project')
        self.assertEqual(color, 'green') # Should still be green if running and no explicit issues
        self.assertIn('All Systems Go!', message)

    @patch('app.docker.from_env')
    def test_get_stack_health_mixed_states_priority(self, mock_from_env):
        mock_client = MagicMock()
        # Healthy container
        mock_container1 = MagicMock()
        mock_container1.status = 'running'
        mock_container1.health = MagicMock(status='healthy')
        mock_container1.labels = {'com.docker.compose.project': 'test_project'}

        # Restarting container
        mock_container2 = MagicMock()
        mock_container2.status = 'restarting'
        mock_container2.health = MagicMock(status='starting')
        mock_container2.labels = {'com.docker.compose.project': 'test_project'}

        # Unhealthy container (should trigger RED)
        mock_container3 = MagicMock()
        mock_container3.status = 'running'
        mock_container3.health = MagicMock(status='unhealthy')
        mock_container3.labels = {'com.docker.compose.project': 'test_project'}

        mock_client.containers.list.return_value = [mock_container1, mock_container2, mock_container3]
        mock_from_env.return_value = mock_client

        color, message = get_stack_health(mock_client, 'test_project')
        self.assertEqual(color, 'red')
        self.assertIn('Trouble in Paradise!', message)

    @patch('app.docker.from_env')
    def test_get_stack_health_paused_container(self, mock_from_env):
        mock_client = MagicMock()
        mock_container1 = MagicMock()
        mock_container1.status = 'running'
        mock_container1.health = MagicMock(status='healthy')
        mock_container1.labels = {'com.docker.compose.project': 'test_project'}

        mock_container2 = MagicMock()
        mock_container2.status = 'paused' # This one is paused
        mock_container2.health = MagicMock(status='healthy') # Health status might still be 'healthy' from last check
        mock_container2.labels = {'com.docker.compose.project': 'test_project'}

        mock_client.containers.list.return_value = [mock_container1, mock_container2]
        mock_from_env.return_value = mock_client

        color, message = get_stack_health(mock_client, 'test_project')
        self.assertEqual(color, 'yellow')
        self.assertIn('A Bit Wobbly...', message)


if __name__ == '__main__':
    unittest.main()
