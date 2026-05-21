import unittest
from unittest.mock import MagicMock, patch
import sys
from io import StringIO
import docker.errors
from src.critter_caretaker import get_container_status, get_care_instructions, main

class TestCritterCaretaker(unittest.TestCase):

    def test_get_container_status_healthy(self):
        mock_container = MagicMock()
        mock_container.attrs = {
            'State': {
                'Status': 'running',
                'Health': {'Status': 'healthy'}
            }
        }
        whimsical, actual = get_container_status(mock_container)
        self.assertEqual(whimsical, "purring happily")
        self.assertEqual(actual, "healthy")

    def test_get_container_status_unhealthy(self):
        mock_container = MagicMock()
        mock_container.attrs = {
            'State': {
                'Status': 'running',
                'Health': {'Status': 'unhealthy'}
            }
        }
        whimsical, actual = get_container_status(mock_container)
        self.assertEqual(whimsical, "looking a bit green")
        self.assertEqual(actual, "unhealthy")

    def test_get_container_status_running_no_healthcheck(self):
        mock_container = MagicMock()
        mock_container.attrs = {
            'State': {
                'Status': 'running'
            }
        }
        whimsical, actual = get_container_status(mock_container)
        self.assertEqual(whimsical, "idling contentedly")
        self.assertEqual(actual, "running")

    def test_get_container_status_exited(self):
        mock_container = MagicMock()
        mock_container.attrs = {
            'State': {
                'Status': 'exited'
            }
        }
        whimsical, actual = get_container_status(mock_container)
        self.assertEqual(whimsical, "wandered off")
        self.assertEqual(actual, "exited")

    def test_get_container_status_paused(self):
        mock_container = MagicMock()
        mock_container.attrs = {
            'State': {
                'Status': 'paused'
            }
        }
        whimsical, actual = get_container_status(mock_container)
        self.assertEqual(whimsical, "taking a nap")
        self.assertEqual(actual, "paused")

    def test_get_container_status_created(self):
        mock_container = MagicMock()
        mock_container.attrs = {
            'State': {
                'Status': 'created'
            }
        }
        whimsical, actual = get_container_status(mock_container)
        self.assertEqual(whimsical, "just hatched")
        self.assertEqual(actual, "created")

    def test_get_container_status_unknown(self):
        mock_container = MagicMock()
        mock_container.attrs = {
            'State': {
                'Status': 'restarting' # Example of an unknown/other status
            }
        }
        whimsical, actual = get_container_status(mock_container)
        self.assertEqual(whimsical, "in an unusual state (restarting)")
        self.assertEqual(actual, "unknown")

    def test_get_care_instructions_healthy(self):
        instructions, command = get_care_instructions("my-app", "purring happily", "healthy")
        self.assertIn("purring happily", instructions)
        self.assertEqual(command, "docker logs my-app")

    def test_get_care_instructions_unhealthy(self):
        instructions, command = get_care_instructions("db-server", "looking a bit green", "unhealthy")
        self.assertIn("looking a bit green", instructions)
        self.assertEqual(command, "docker inspect db-server --format '{{json .State.Health}}'")

    def test_get_care_instructions_exited(self):
        instructions, command = get_care_instructions("old-service", "wandered off", "exited")
        self.assertIn("wandered off", instructions)
        self.assertEqual(command, "docker start old-service")

    def test_get_care_instructions_paused(self):
        instructions, command = get_care_instructions("suspended-task", "taking a nap", "paused")
        self.assertIn("taking a nap", instructions)
        self.assertEqual(command, "docker unpause suspended-task")

    def test_get_care_instructions_created(self):
        instructions, command = get_care_instructions("new-critter", "just hatched", "created")
        self.assertIn("just hatched", instructions)
        self.assertEqual(command, "docker start new-critter")

    def test_get_care_instructions_unknown(self):
        instructions, command = get_care_instructions("mystery-box", "in an unusual state (restarting)", "unknown")
        self.assertIn("unusual state", instructions)
        self.assertEqual(command, "docker inspect mystery-box")

    @patch('src.critter_caretaker.docker.from_env')
    def test_main_no_containers(self, mock_from_env):
        # Mock rationale: We don't want to interact with a real Docker daemon during tests.
        # This mock simulates a scenario where no containers are found.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_client.containers.list.return_value = []

        captured_output = StringIO()
        sys.stdout = captured_output
        
        main()
        
        sys.stdout = sys.__stdout__ # Reset stdout
        self.assertIn("No container critters found", captured_output.getvalue())
        mock_client.containers.list.assert_called_once_with(all=True)

    @patch('src.critter_caretaker.docker.from_env')
    def test_main_with_containers(self, mock_from_env):
        # Mock rationale: Simulates a Docker daemon with specific container states
        # to test the main logic without actual Docker interaction.
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        mock_container_healthy = MagicMock()
        mock_container_healthy.name = "healthy-critter"
        mock_container_healthy.attrs = {
            'State': {'Status': 'running', 'Health': {'Status': 'healthy'}}
        }

        mock_container_exited = MagicMock()
        mock_container_exited.name = "sleepy-critter"
        mock_container_exited.attrs = {
            'State': {'Status': 'exited'}
        }

        mock_client.containers.list.return_value = [mock_container_healthy, mock_container_exited]

        captured_output = StringIO()
        sys.stdout = captured_output
        
        main()
        
        sys.stdout = sys.__stdout__ # Reset stdout
        output = captured_output.getvalue()

        self.assertIn("--- Container Critter Care Report ---", output)
        self.assertIn("Critter: healthy-critter", output)
        self.assertIn("Status: Purring happily", output)
        self.assertIn("Care Tip: Your healthy-critter critter is purring happily!", output)
        self.assertIn("Suggested Action: docker logs healthy-critter", output)

        self.assertIn("Critter: sleepy-critter", output)
        self.assertIn("Status: Wandered off", output)
        self.assertIn("Care Tip: Your sleepy-critter critter has wandered off. Time to coax it back into action!", output)
        self.assertIn("Suggested Action: docker start sleepy-critter", output)
        self.assertIn("--- End of Report ---", output)
        mock_client.containers.list.assert_called_once_with(all=True)

    @patch('src.critter_caretaker.docker.from_env')
    def test_main_docker_error(self, mock_from_env):
        # Mock rationale: Simulates a Docker connection error to ensure the utility handles it gracefully.
        mock_from_env.side_effect = docker.errors.DockerException("Cannot connect to the Docker daemon")

        captured_output = StringIO()
        sys.stderr = captured_output
        
        with self.assertRaises(SystemExit) as cm:
            main()
        
        sys.stderr = sys.__stderr__ # Reset stderr
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error connecting to Docker daemon: Cannot connect to the Docker daemon", captured_output.getvalue())
        self.assertIn("Please ensure Docker is running and the Docker socket is accessible.", captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()
