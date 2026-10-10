import unittest
import os
import sys
from unittest.mock import MagicMock, patch, call

# Add src directory to path for importing app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import ContainerWhisperer

class TestContainerWhisperer(unittest.TestCase):

    @patch('app.docker.from_env')
    def setUp(self, mock_docker_from_env):
        # Mock rationale: We don't want to connect to a real Docker daemon during tests.
        # We'll mock the entire docker client interaction.
        self.mock_client = MagicMock()
        self.mock_containers = MagicMock()
        self.mock_client.containers = self.mock_containers
        mock_docker_from_env.return_value = self.mock_client

        # Set up environment variables for the test
        os.environ["CONTAINER_NAMES"] = "test-container-1,test-container-2"
        os.environ["POLLING_INTERVAL_SECONDS"] = "1"

        self.whisperer = ContainerWhisperer(
            os.getenv("CONTAINER_NAMES"),
            os.getenv("POLLING_INTERVAL_SECONDS")
        )

    def tearDown(self):
        # Clean up environment variables
        del os.environ["CONTAINER_NAMES"]
        del os.environ["POLLING_INTERVAL_SECONDS"]

    def _mock_container(self, name, logs_content):
        mock_container = MagicMock()
        mock_container.name = name
        # Mock rationale: `container.logs()` returns bytes.
        mock_container.logs.return_value = logs_content.encode('utf-8')
        return mock_container

    def test_init_no_container_names(self):
        # Mock rationale: Test initialization without container names.
        os.environ["CONTAINER_NAMES"] = ""
        with self.assertLogs('app', level='WARNING') as cm:
            whisperer = ContainerWhisperer("", "1")
            self.assertIn("No container names specified", cm.output[0])
        self.assertEqual(whisperer.container_names, [])

    def test_get_container_by_name_found(self):
        # Mock rationale: Simulate finding a container.
        mock_container = self._mock_container("test-container-1", "")
        self.mock_containers.get.return_value = mock_container
        
        container = self.whisperer._get_container_by_name("test-container-1")
        self.assertEqual(container, mock_container)
        self.mock_containers.get.assert_called_once_with("test-container-1")

    def test_get_container_by_name_not_found(self):
        # Mock rationale: Simulate a container not being found.
        from docker.errors import NotFound
        self.mock_containers.get.side_effect = NotFound("Container not found")
        
        with self.assertLogs('app', level='WARNING') as cm:
            container = self.whisperer._get_container_by_name("non-existent")
            self.assertIsNone(container)
            self.assertIn("Container 'non-existent' not found", cm.output[0])

    def test_analyze_logs_grumpy_mood(self):
        # Mock rationale: Provide log content that should trigger a "Grumpy" mood.
        logs = "INFO: App started\nERROR: Something went wrong!\nWARNING: Disk space low"
        error_c, warning_c, info_c = self.whisperer._analyze_logs("test-container", logs)
        self.assertEqual(error_c, 1)
        self.assertEqual(warning_c, 1)
        self.assertEqual(info_c, 1)
        mood, desc = self.whisperer._determine_mood(error_c, warning_c, info_c)
        self.assertEqual(mood, "Grumpy 😠")
        self.assertIn("Multiple errors (1)", desc)

    def test_analyze_logs_anxious_mood(self):
        # Mock rationale: Provide log content that should trigger an "Anxious" mood.
        logs = "INFO: Processing data\nWARNING: High CPU usage detected"
        error_c, warning_c, info_c = self.whisperer._analyze_logs("test-container", logs)
        self.assertEqual(error_c, 0)
        self.assertEqual(warning_c, 1)
        self.assertEqual(info_c, 1)
        mood, desc = self.whisperer._determine_mood(error_c, warning_c, info_c)
        self.assertEqual(mood, "Anxious 😨")
        self.assertIn("A few warnings (1)", desc)

    def test_analyze_logs_chatty_mood(self):
        # Mock rationale: Provide log content that should trigger a "Chatty" mood.
        logs = "INFO: User logged in\nINFO: Data saved"
        error_c, warning_c, info_c = self.whisperer._analyze_logs("test-container", logs)
        self.assertEqual(error_c, 0)
        self.assertEqual(warning_c, 0)
        self.assertEqual(info_c, 2)
        mood, desc = self.whisperer._determine_mood(error_c, warning_c, info_c)
        self.assertEqual(mood, "Chatty 🗣️")
        self.assertIn("actively communicating, with 2 info messages", desc)

    def test_analyze_logs_serene_mood(self):
        # Mock rationale: Provide log content that should trigger a "Serene" mood.
        logs = "App is running smoothly\nAnother normal line"
        error_c, warning_c, info_c = self.whisperer._analyze_logs("test-container", logs)
        self.assertEqual(error_c, 0)
        self.assertEqual(warning_c, 0)
        self.assertEqual(info_c, 0)
        mood, desc = self.whisperer._determine_mood(error_c, warning_c, info_c)
        self.assertEqual(mood, "Serene 😌")
        self.assertIn("All is calm", desc)

    @patch('app.time.sleep', MagicMock()) # Mock rationale: Prevent actual sleep during tests.
    def test_whisper_loop_single_iteration(self):
        # Mock rationale: Simulate container logs and verify the output.
        mock_container_1 = self._mock_container("test-container-1", "INFO: All good here.")
        mock_container_2 = self._mock_container("test-container-2", "ERROR: Critical failure!")

        self.mock_containers.get.side_effect = [mock_container_1, mock_container_2]

        # Run the loop once
        with self.assertLogs('app', level='INFO') as cm:
            # We need to break the infinite loop after one iteration
            with patch('app.ContainerWhisperer.whisper_loop', side_effect=[None, StopIteration]):
                try:
                    self.whisperer.whisper_loop()
                except StopIteration:
                    pass # Expected to break the loop

            # Check if logs contain the expected mood reports
            output = "\n".join(cm.output)
            self.assertIn("Container 'test-container-1': Feeling Serene 😌. All is calm in its digital garden.", output)
            self.assertIn("Container 'test-container-2': Feeling Grumpy 😠. Multiple errors (1) indicate it's having a very bad day.", output)
            self.assertEqual(self.mock_containers.get.call_count, 2)
            self.mock_containers.get.assert_has_calls([
                call("test-container-1"),
                call("test-container-2")
            ])
            mock_container_1.logs.assert_called_once_with(tail=100)
            mock_container_2.logs.assert_called_once_with(tail=100)

    @patch('app.time.sleep', MagicMock()) # Mock rationale: Prevent actual sleep during tests.
    def test_whisper_loop_no_containers_configured(self):
        # Mock rationale: Test the behavior when no container names are provided.
        os.environ["CONTAINER_NAMES"] = ""
        whisperer_no_names = ContainerWhisperer("", "1")

        with self.assertLogs('app', level='INFO') as cm:
            with patch('app.ContainerWhisperer.whisper_loop', side_effect=[None, StopIteration]):
                try:
                    whisperer_no_names.whisper_loop()
                except StopIteration:
                    pass
            output = "\n".join(cm.output)
            self.assertIn("No containers to whisper to. Zzz...", output)
            self.mock_containers.get.assert_not_called() # Ensure no attempt to get containers

    @patch('app.docker.from_env', side_effect=Exception("Docker daemon not available"))
    def test_docker_client_connection_failure(self, mock_docker_from_env):
        # Mock rationale: Simulate a failure to connect to the Docker daemon.
        with self.assertLogs('app', level='ERROR') as cm:
            with self.assertRaises(Exception) as context:
                ContainerWhisperer("some-container", "1")
            self.assertIn("Could not connect to Docker daemon", cm.output[0])
            self.assertIn("Docker daemon not available", str(context.exception))


if __name__ == '__main__':
    unittest.main()
