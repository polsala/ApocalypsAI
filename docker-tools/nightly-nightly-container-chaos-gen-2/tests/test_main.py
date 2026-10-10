import unittest
import yaml
from unittest.mock import patch, MagicMock

# Assuming src/main.py is in the same directory or accessible
from src.main import generate_chaos_compose

class TestContainerChaosGenerator(unittest.TestCase):

    def test_default_generation(self):
        """Test that default parameters generate a valid compose structure."""
        compose_data = generate_chaos_compose()

        self.assertIsInstance(compose_data, dict)
        self.assertIn("version", compose_data)
        self.assertEqual(compose_data["version"], "3.8")
        self.assertIn("services", compose_data)
        self.assertIn("networks", compose_data)
        self.assertEqual(len(compose_data["services"]), 3 * 2 + 1) # 3 app services + 3 chaos services + 1 base chaos_network

        # Check for a specific app service and its chaos counterpart
        self.assertIn("app_service_1", compose_data["services"])
        self.assertIn("chaos_for_app_service_1", compose_data["services"])

        # Check network configuration
        self.assertIn("chaos_net", compose_data["networks"])
        self.assertEqual(compose_data["networks"]["chaos_net"]["driver"], "bridge")

    def test_custom_parameters(self):
        """Test generation with custom parameters."""
        num_services = 5
        latency = 100
        loss = 10
        cpu = 1.0
        memory = 256

        compose_data = generate_chaos_compose(
            num_services=num_services,
            network_latency=latency,
            network_loss=loss,
            resource_cpu=cpu,
            resource_memory=memory
        )

        self.assertEqual(len(compose_data["services"]), num_services * 2 + 1)

        # Check resource limits for one of the app services
        app_service_1 = compose_data["services"]["app_service_1"]
        self.assertEqual(app_service_1["deploy"]["resources"]["limits"]["cpus"], str(cpu))
        self.assertEqual(app_service_1["deploy"]["resources"]["limits"]["memory"], f"{memory}M")

        # Check network settings in chaos service
        chaos_service_1 = compose_data["services"]["chaos_for_app_service_1"]
        self.assertIn(f"delay {latency}ms", chaos_service_1["entrypoint"])
        self.assertIn(f"loss {loss}%", chaos_service_1["entrypoint"])

    @patch('src.main.yaml.dump')
    @patch('builtins.open', new_callable=MagicMock)
    def test_output_to_file(self, mock_open, mock_yaml_dump):
        """Test that the output is written to the specified file."""
        mock_file_handle = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file_handle

        # Mock the generate_chaos_compose to return a fixed structure
        fixed_compose_data = {"version": "3.8", "services": {}}
        with patch('src.main.generate_chaos_compose', return_value=fixed_compose_data):
            # Simulate running the script with --output
            import sys
            from io import StringIO
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            try:
                # Simulate command line arguments
                with patch.object(yaml, 'dump') as mock_dump:
                    from src.main import main
                    # Temporarily modify sys.argv to simulate command line args
                    original_argv = sys.argv
                    sys.argv = ['src/main.py', '--output', 'test_output.yml']
                    main()
                    sys.argv = original_argv # Restore sys.argv

                    mock_open.assert_called_once_with('test_output.yml', 'w')
                    mock_dump.assert_called_once_with(fixed_compose_data, mock_file_handle, indent=2)
                    self.assertIn("Generated chaotic compose file: test_output.yml", captured_output.getvalue())
            finally:
                sys.stdout = old_stdout

    def test_entrypoint_command_structure(self):
        """Verify the structure of the entrypoint command for chaos service."""
        compose_data = generate_chaos_compose(network_latency=75, network_loss=8)
        chaos_service = compose_data["services"]["chaos_for_app_service_1"]
        command = chaos_service["entrypoint"]

        self.assertIn("tc qdisc add dev eth0 root netem", command)
        self.assertIn("delay 75ms", command)
        self.assertIn("loss 8%", command)
        self.assertIn("exec /usr/bin/socat", command)

if __name__ == '__main__':
    unittest.main()
