import unittest
from unittest.mock import MagicMock, patch
import re
import os
from src.main import detect_quirk, quench_quirk, parse_patterns, parse_labels, main
import docker

class TestQuantumQuirkQuencher(unittest.TestCase):

    def setUp(self):
        # Store original environment variables to restore them after tests
        self._original_env = {
            'QUIRK_PATTERNS': os.getenv('QUIRK_PATTERNS'),
            'QUENCH_ACTION': os.getenv('QUENCH_ACTION'),
            'MONITORED_LABELS': os.getenv('MONITORED_LABELS'),
            'LOG_LEVEL': os.getenv('LOG_LEVEL')
        }
        # Set a default log level for tests to avoid excessive output
        os.environ['LOG_LEVEL'] = 'CRITICAL'

    def tearDown(self):
        # Restore original environment variables
        for key, value in self._original_env.items():
            if value is not None:
                os.environ[key] = value
            else:
                if key in os.environ:
                    del os.environ[key]

    def test_parse_patterns(self):
        patterns_str = "error|fail|exception"
        patterns = parse_patterns(patterns_str)
        self.assertEqual(len(patterns), 3)
        self.assertTrue(patterns[0].match("This is an error message"))
        self.assertFalse(patterns[0].match("No problem here"))

        patterns_str_empty = ""
        patterns_empty = parse_patterns(patterns_str_empty)
        self.assertEqual(len(patterns_empty), 0)

        patterns_str_spaces = "  error |  fail  "
        patterns_spaces = parse_patterns(patterns_str_spaces)
        self.assertEqual(len(patterns_spaces), 2)
        self.assertTrue(patterns_spaces[0].match("error"))

    def test_parse_labels(self):
        labels_str = "app=backend,env=prod"
        labels = parse_labels(labels_str)
        self.assertEqual(labels, {"app": "backend", "env": "prod"})

        labels_str_single = "monitor=true"
        labels_single = parse_labels(labels_str_single)
        self.assertEqual(labels_single, {"monitor": "true"})

        labels_str_empty = ""
        labels_empty = parse_labels(labels_str_empty)
        self.assertEqual(labels_empty, {})

        labels_str_spaces = "  app =  frontend ,  env = dev  "
        labels_spaces = parse_labels(labels_str_spaces)
        self.assertEqual(labels_spaces, {"app": "frontend", "env": "dev"})

    def test_detect_quirk(self):
        quirk_patterns = parse_patterns("error|fail")
        self.assertTrue(detect_quirk("This log has an error.", quirk_patterns))
        self.assertTrue(detect_quirk("Failed to connect.", quirk_patterns))
        self.assertFalse(detect_quirk("All good here.", quirk_patterns))
        self.assertTrue(detect_quirk("ERROR: Something went wrong.", quirk_patterns)) # Case insensitive

    @patch('src.main.logging')
    def test_quench_quirk_restart(self, mock_logging):
        mock_container = MagicMock()
        mock_container.name = "test_container"
        quench_quirk(mock_container, 'restart', 'test log line')
        mock_container.restart.assert_called_once()
        mock_logging.info.assert_any_call("Quirk detected in container 'test_container'. Initiating quench action: restart")
        mock_logging.info.assert_any_call("Container 'test_container' restarted successfully.")
        # Mock rationale: Avoids actual Docker container restarts during tests.

    @patch('src.main.logging')
    def test_quench_quirk_notify(self, mock_logging):
        mock_container = MagicMock()
        mock_container.name = "test_container"
        quench_quirk(mock_container, 'notify', 'test log line')
        mock_container.restart.assert_not_called()
        mock_logging.info.assert_any_call("Quirk detected in container 'test_container'. Initiating quench action: notify")
        mock_logging.info.assert_any_call("Notification: Quirk in 'test_container' detected. Log snippet: test log line")
        # Mock rationale: Avoids actual notification sending during tests.

    @patch('src.main.logging')
    def test_quench_quirk_unknown_action(self, mock_logging):
        mock_container = MagicMock()
        mock_container.name = "test_container"
        quench_quirk(mock_container, 'unknown', 'test log line')
        mock_container.restart.assert_not_called()
        mock_logging.warning.assert_any_call("Unknown quench action: unknown. No action taken for 'test_container'.")
        # Mock rationale: Tests error handling for invalid actions without side effects.

    @patch('src.main.docker.from_env')
    @patch('src.main.time.sleep', return_value=None) # Mock sleep to speed up tests
    @patch('src.main.logging')
    def test_main_loop_detects_and_quenches(self, mock_logging, mock_sleep, mock_docker_from_env):
        # Mock rationale:
        # - docker.from_env: Avoids needing a live Docker daemon.
        # - time.sleep: Prevents tests from waiting for actual delays.
        # - logging: Captures log output for assertions.

        mock_client = MagicMock()
        mock_docker_from_env.return_value = mock_client

        mock_container_1 = MagicMock()
        mock_container_1.name = "app_backend"
        mock_container_1.labels = {"apocalypsai.monitor": "true", "env": "prod"}
        mock_container_1.logs.return_value = iter([
            b"INFO: Starting service...\n",
            b"WARN: Minor issue detected.\n",
            b"ERROR: Critical failure! Aborting.\n", # This should trigger a quench
            b"INFO: Service stopped.\n" # This log line will not be processed due to break
        ])

        mock_container_2 = MagicMock()
        mock_container_2.name = "app_frontend"
        mock_container_2.labels = {"apocalypsai.monitor": "true"} # Does not match all monitored labels
        mock_container_2.logs.return_value = iter([
            b"INFO: Frontend running.\n"
        ])

        mock_container_3 = MagicMock()
        mock_container_3.name = "unmonitored_service"
        mock_container_3.labels = {} # No monitoring label
        mock_container_3.logs.return_value = iter([
            b"INFO: Unmonitored service running.\n"
        ])

        # Simulate one pass of containers, then an empty list to break the main loop
        mock_client.containers.list.side_effect = [[mock_container_1, mock_container_2, mock_container_3], []]

        # Set environment variables for the test
        os.environ['QUIRK_PATTERNS'] = 'error|critical'
        os.environ['QUENCH_ACTION'] = 'restart'
        os.environ['MONITORED_LABELS'] = 'apocalypsai.monitor=true,env=prod'

        # The main loop is infinite, but with `containers.list.side_effect` returning `[]`
        # on the second call, the outer loop will effectively terminate after one pass.
        # The inner `for line_bytes in container.logs` loop will exhaust its iterator.
        # The `break` after `quench_quirk` will exit the inner loop, allowing the outer loop
        # to proceed to the next container or re-list containers.
        try:
            main()
        except StopIteration: # Expected when all mocked iterators are exhausted
            pass

        mock_client.containers.list.assert_called()
        mock_container_1.logs.assert_called_once_with(stream=True, follow=True)
        mock_container_1.restart.assert_called_once()
        mock_logging.warning.assert_any_call("Quirk detected in 'app_backend': ERROR: Critical failure! Aborting.")
        mock_logging.info.assert_any_call("Container 'app_backend' restarted successfully.")

        # Ensure container_2 and container_3 were not processed for logs or restarted
        mock_container_2.logs.assert_not_called()
        mock_container_2.restart.assert_not_called()
        mock_container_3.logs.assert_not_called()
        mock_container_3.restart.assert_not_called()

    @patch('src.main.docker.from_env')
    @patch('src.main.time.sleep', return_value=None)
    @patch('src.main.logging')
    def test_main_loop_no_quirk(self, mock_logging, mock_sleep, mock_docker_from_env):
        mock_client = MagicMock()
        mock_docker_from_env.return_value = mock_client

        mock_container_1 = MagicMock()
        mock_container_1.name = "app_backend"
        mock_container_1.labels = {"apocalypsai.monitor": "true", "env": "prod"}
        mock_container_1.logs.return_value = iter([
            b"INFO: All systems nominal.\n",
            b"DEBUG: Processing data.\n"
        ])

        mock_client.containers.list.side_effect = [[mock_container_1], []]

        os.environ['QUIRK_PATTERNS'] = 'error|fail'
        os.environ['QUENCH_ACTION'] = 'restart'
        os.environ['MONITORED_LABELS'] = 'apocalypsai.monitor=true,env=prod'

        try:
            main()
        except StopIteration:
            pass

        mock_container_1.logs.assert_called_once_with(stream=True, follow=True)
        mock_container_1.restart.assert_not_called()
        mock_logging.warning.assert_not_called() # No quirk detected, no warning

    @patch('src.main.docker.from_env')
    @patch('src.main.time.sleep', return_value=None)
    @patch('src.main.logging')
    def test_main_loop_docker_api_error_handling(self, mock_logging, mock_sleep, mock_docker_from_env):
        mock_client = MagicMock()
        mock_docker_from_env.return_value = mock_client
        mock_client.containers.list.side_effect = [
            docker.errors.APIError("Connection refused", 500, "Server Error"),
            [], # After error, it should retry and then exit
        ]

        os.environ['QUIRK_PATTERNS'] = 'error'
        os.environ['QUENCH_ACTION'] = 'restart'
        os.environ['MONITORED_LABELS'] = 'apocalypsai.monitor=true'

        try:
            main()
        except StopIteration:
            pass

        mock_logging.error.assert_any_call("Docker API error: Connection refused. Retrying in 10 seconds.")
        # One sleep for the error, one for the end of the main loop
        self.assertEqual(mock_sleep.call_count, 2)

    @patch('src.main.docker.from_env')
    @patch('src.main.time.sleep', return_value=None)
    @patch('src.main.logging')
    def test_main_loop_general_exception_handling(self, mock_logging, mock_sleep, mock_docker_from_env):
        mock_client = MagicMock()
        mock_docker_from_env.return_value = mock_client
        mock_client.containers.list.side_effect = [
            Exception("Something truly unexpected happened!"),
            [], # After error, it should retry and then exit
        ]

        os.environ['QUIRK_PATTERNS'] = 'error'
        os.environ['QUENCH_ACTION'] = 'restart'
        os.environ['MONITORED_LABELS'] = 'apocalypsai.monitor=true'

        try:
            main()
        except StopIteration:
            pass

        mock_logging.critical.assert_any_call("An unexpected error occurred in main loop: Something truly unexpected happened!. Restarting monitoring in 10 seconds.")
        self.assertEqual(mock_sleep.call_count, 2)

    @patch('src.main.docker.from_env')
    @patch('src.main.time.sleep', return_value=None)
    @patch('src.main.logging')
    def test_main_loop_no_monitored_containers(self, mock_logging, mock_sleep, mock_docker_from_env):
        mock_client = MagicMock()
        mock_docker_from_env.return_value = mock_client
        mock_client.containers.list.side_effect = [[], []] # No containers found

        os.environ['QUIRK_PATTERNS'] = 'error'
        os.environ['QUENCH_ACTION'] = 'restart'
        os.environ['MONITORED_LABELS'] = 'apocalypsai.monitor=true'

        try:
            main()
        except StopIteration:
            pass

        mock_client.containers.list.assert_called()
        mock_logging.debug.assert_not_called() # No containers to debug
        mock_sleep.assert_called_once_with(5) # Only the sleep at the end of the loop

    @patch('src.main.docker.from_env')
    @patch('src.main.time.sleep', return_value=None)
    @patch('src.main.logging')
    def test_main_loop_container_log_stream_error(self, mock_logging, mock_sleep, mock_docker_from_env):
        mock_client = MagicMock()
        mock_docker_from_env.return_value = mock_client

        mock_container_1 = MagicMock()
        mock_container_1.name = "flaky_app"
        mock_container_1.labels = {"apocalypsai.monitor": "true"}
        # Simulate an error during log streaming for one container
        mock_container_1.logs.side_effect = docker.errors.APIError("Log stream broken", 500, "Server Error")

        mock_client.containers.list.side_effect = [[mock_container_1], []]

        os.environ['QUIRK_PATTERNS'] = 'error'
        os.environ['QUENCH_ACTION'] = 'restart'
        os.environ['MONITORED_LABELS'] = 'apocalypsai.monitor=true'

        try:
            main()
        except StopIteration:
            pass

        mock_logging.error.assert_any_call("Error streaming logs from 'flaky_app': Log stream broken")
        mock_container_1.restart.assert_not_called() # No quirk detected, just a log stream error
        self.assertEqual(mock_sleep.call_count, 1) # Only the sleep at the end of the main loop
