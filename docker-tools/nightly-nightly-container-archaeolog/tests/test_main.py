import unittest
from unittest.mock import MagicMock, patch
import sys
import io
import re

# Mock rationale: We need to test the logic of scanning container environment variables
# without actually running Docker containers or requiring a Docker daemon.
# Mocking the 'docker' client allows for deterministic and offline testing.

# Temporarily add src to path to import main.py
sys.path.insert(0, 'src')
from main import scan_containers_for_secrets
sys.path.pop(0)


class TestContainerArchaeologist(unittest.TestCase):

    @patch('docker.from_env')
    def test_no_containers_running(self, mock_from_env):
        mock_client = MagicMock()
        mock_client.containers.list.return_value = []
        mock_from_env.return_value = mock_client

        captured_output = io.StringIO()
        sys.stdout = captured_output

        scan_containers_for_secrets()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Excavation Initiated", output)
        self.assertIn("Excavation Complete: 0 digital artifacts unearthed.", output)
        self.assertNotIn("Artifact Found!", output)

    @patch('docker.from_env')
    def test_containers_with_no_secrets(self, mock_from_env):
        mock_container_1 = MagicMock()
        mock_container_1.short_id = "abcde1"
        mock_container_1.name = "safe-app"
        mock_container_1.image.tags = ["safe-image:1.0"]
        mock_container_1.attrs = {'Config': {'Env': ['VAR1=value1', 'VAR2=value2']}}

        mock_container_2 = MagicMock()
        mock_container_2.short_id = "fghij2"
        mock_container_2.name = "another-safe-app"
        mock_container_2.image.tags = ["another-safe-image:latest"]
        mock_container_2.attrs = {'Config': {'Env': ['APP_ENV=production']}}

        mock_client = MagicMock()
        mock_client.containers.list.return_value = [mock_container_1, mock_container_2]
        mock_from_env.return_value = mock_client

        captured_output = io.StringIO()
        sys.stdout = captured_output

        scan_containers_for_secrets()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Excavation Initiated", output)
        self.assertIn("Excavation Complete: 0 digital artifacts unearthed.", output)
        self.assertNotIn("Artifact Found!", output)

    @patch('docker.from_env')
    def test_containers_with_secrets(self, mock_from_env):
        mock_container_1 = MagicMock()
        mock_container_1.short_id = "abcde1"
        mock_container_1.name = "secret-app"
        mock_container_1.image.tags = ["secret-image:1.0"]
        mock_container_1.attrs = {'Config': {'Env': ['DB_PASSWORD=supersecret', 'USER=admin']}}

        mock_container_2 = MagicMock()
        mock_container_2.short_id = "fghij2"
        mock_container_2.name = "api-service"
        mock_container_2.image.tags = ["api-image:latest"]
        mock_container_2.attrs = {'Config': {'Env': ['API_KEY=xyz123', 'APP_ENV=production', 'STRIPE_TOKEN=tok_abc']}}

        mock_client = MagicMock()
        mock_client.containers.list.return_value = [mock_container_1, mock_container_2]
        mock_from_env.return_value = mock_client

        captured_output = io.StringIO()
        sys.stdout = captured_output

        scan_containers_for_secrets()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Excavation Initiated", output)
        self.assertIn("Excavation Complete: 3 digital artifacts unearthed.", output)
        self.assertIn("Artifact Found!", output)
        self.assertIn("Container Name: secret-app", output)
        self.assertIn("Artifact: DB_PASSWORD (Potential secret)", output)
        self.assertIn("Container Name: api-service", output)
        self.assertIn("Artifact: API_KEY (Potential secret)", output)
        self.assertIn("Artifact: STRIPE_TOKEN (Potential secret)", output)
        self.assertNotIn("Artifact: USER (Potential secret)", output) # Should not be flagged

    @patch('docker.from_env')
    def test_docker_connection_error(self, mock_from_env):
        mock_from_env.side_effect = Exception("Cannot connect to Docker daemon")

        captured_output = io.StringIO()
        sys.stdout = captured_output

        scan_containers_for_secrets()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Error connecting to Docker daemon: Cannot connect to Docker daemon", output)
        self.assertIn("Please ensure Docker is running and the Docker socket is accessible", output)
        self.assertNotIn("Excavation Complete", output) # Should not complete if connection fails

    @patch('docker.from_env')
    def test_container_with_empty_env(self, mock_from_env):
        mock_container = MagicMock()
        mock_container.short_id = "empty1"
        mock_container.name = "empty-env-app"
        mock_container.image.tags = ["empty-image:1.0"]
        mock_container.attrs = {'Config': {'Env': []}}

        mock_client = MagicMock()
        mock_client.containers.list.return_value = [mock_container]
        mock_from_env.return_value = mock_client

        captured_output = io.StringIO()
        sys.stdout = captured_output

        scan_containers_for_secrets()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Excavation Complete: 0 digital artifacts unearthed.", output)
        self.assertNotIn("Artifact Found!", output)

    @patch('docker.from_env')
    def test_container_with_no_tags(self, mock_from_env):
        mock_container = MagicMock()
        mock_container.short_id = "notag1"
        mock_container.name = "no-tag-app"
        mock_container.image.tags = [] # No tags
        mock_container.attrs = {'Config': {'Env': ['API_KEY=secret']}}

        mock_client = MagicMock()
        mock_client.containers.list.return_value = [mock_container]
        mock_from_env.return_value = mock_client

        captured_output = io.StringIO()
        sys.stdout = captured_output

        scan_containers_for_secrets()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Artifact Found!", output)
        self.assertIn("Image:          unknown", output) # Should default to 'unknown'
        self.assertIn("Artifact: API_KEY (Potential secret)", output)
        self.assertIn("Excavation Complete: 1 digital artifacts unearthed.", output)


if __name__ == '__main__':
    unittest.main()
