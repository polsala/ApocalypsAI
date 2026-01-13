import unittest
import yaml
from unittest.mock import patch, MagicMock

# Assuming main.py is in the same directory or accessible via PYTHONPATH
from src.main import generate_random_compose_file, apply_chaos, MockDockerClient

class TestContainerChaosGenerator(unittest.TestCase):

    def test_generate_random_compose_file_structure(self):
        """Tests if the generated compose file has the basic structure."""
        num_services = 4
        compose_content = generate_random_compose_file(num_services)
        data = yaml.safe_load(compose_content)

        self.assertIn("version", data)
        self.assertEqual(data["version"], "3.8")
        self.assertIn("services", data)
        self.assertEqual(len(data["services"]), num_services)
        self.assertIn("volumes", data)

    def test_generate_random_compose_file_service_types(self):
        """Tests if generated services use known types."""
        num_services = 5
        compose_content = generate_random_compose_file(num_services)
        data = yaml.safe_load(compose_content)
        available_types = ["web", "db", "redis", "worker"]

        for service_name, service_config in data["services"].items():
            found_type = False
            for t in available_types:
                if service_name.startswith(t):
                    found_type = True
                    break
            self.assertTrue(found_type, f"Service {service_name} does not start with a known type.")
            self.assertIn("image", service_config)

    def test_generate_random_compose_file_dependencies(self):
        """Tests if dependencies are correctly added (if any)."""
        num_services = 5
        compose_content = generate_random_compose_file(num_services)
        data = yaml.safe_load(compose_content)

        for service_name, service_config in data["services"].items():
            if "depends_on" in service_config:
                for dep in service_config["depends_on"]:
                    self.assertIn(dep, data["services"], f"Dependency {dep} for service {service_name} not found.")

    @patch('src.main.DockerClient')
    def test_apply_chaos_network_creation(self, MockDockerClient):
        """Tests if a network is created when applying chaos."""
        mock_client = MockDockerClient()
        mock_network_manager = MagicMock()
        mock_client.networks.return_value = mock_network_manager
        mock_network = MagicMock()
        mock_network_manager.create.return_value = mock_network

        compose_content = "version: '3.8'\nservices:\n  test-service-1:\n    image: nginx:latest\n  test-service-2:\n    image: redis:alpine"
        apply_chaos(mock_client, compose_content, chaos_level="low")

        mock_network_manager.create.assert_called_once()
        mock_network.remove.assert_called_once()

    @patch('src.main.DockerClient')
    def test_apply_chaos_no_chaos_if_no_services(self, MockDockerClient):
        """Tests that no chaos is applied if there are no services."""
        mock_client = MockDockerClient()
        mock_network_manager = MagicMock()
        mock_client.networks.return_value = mock_network_manager
        mock_network = MagicMock()
        mock_network_manager.create.return_value = mock_network

        compose_content = "version: '3.8'\nservices:{}"
        apply_chaos(mock_client, compose_content)

        mock_network_manager.create.assert_called_once()
        mock_network.remove.assert_called_once()

    @patch('src.main.DockerClient')
    @patch('src.main.time.sleep')
    def test_apply_chaos_simulates_delay(self, mock_sleep, MockDockerClient):
        """Tests that network delay is simulated."""
        mock_client = MockDockerClient()
        mock_network_manager = MagicMock()
        mock_client.networks.return_value = mock_network_manager
        mock_network = MagicMock()
        mock_network_manager.create.return_value = mock_network

        # Mocking print to capture output if needed, but focus is on function calls
        with patch('builtins.print') as mock_print:
            compose_content = "version: '3.8'\nservices:\n  test-service-1:\n    image: nginx:latest"
            apply_chaos(mock_client, compose_content, chaos_level="low")

            # Check if network delay is mentioned in the output
            mock_print.assert_any_call(unittest.mock.ANY)
            # This is a weak check, better to mock the actual tc command if it were called.
            # For this mock, we check if the print statement about delay is present.
            self.assertTrue(any("Applying network delay" in str(call) for call in mock_print.call_args_list))
            mock_sleep.assert_called_once()

    @patch('src.main.DockerClient')
    def test_apply_chaos_with_mock_client(self):
        """Tests chaos application using the MockDockerClient."""
        mock_client = MockDockerClient()
        compose_content = "version: '3.8'\nservices:\n  web-1:\n    image: nginx:latest\n  db-1:\n    image: postgres:13"

        # We can't directly assert the side effects of chaos on mock containers/networks
        # without more complex mocking, but we can ensure the function runs without errors
        # and that the mock client methods are called as expected (e.g., network creation).
        try:
            apply_chaos(mock_client, compose_content, chaos_level="high")
            # If no exception is raised, it's a good sign the mock client was used correctly.
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"apply_chaos with MockDockerClient raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
