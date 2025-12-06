import unittest
import sys
import os
from unittest.mock import patch, mock_open

# Add the src directory to the path to allow importing forecaster
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import forecaster

class TestForecaster(unittest.TestCase):

    def test_calculate_depletion(self):
        # Test normal depletion
        self.assertAlmostEqual(forecaster.calculate_depletion(100, 10), 10.0)
        self.assertAlmostEqual(forecaster.calculate_depletion(50, 2.5), 20.0)
        # Test zero consumption
        self.assertEqual(forecaster.calculate_depletion(100, 0), float('inf'))
        # Test negative consumption (should also be infinite, as it implies growth/gain)
        self.assertEqual(forecaster.calculate_depletion(100, -5), float('inf'))
        # Test zero current amount, positive consumption
        self.assertAlmostEqual(forecaster.calculate_depletion(0, 10), 0.0)
        # Test negative current amount, positive consumption
        self.assertAlmostEqual(forecaster.calculate_depletion(-10, 10), -1.0)

    def test_get_status_emoji(self):
        # Test 'Plenty' status
        self.assertEqual(forecaster.get_status_emoji(float('inf')), ("🟢", "Plenty"))
        self.assertEqual(forecaster.get_status_emoji(31), ("🟢", "Plenty"))
        # Test 'Stable' status
        self.assertEqual(forecaster.get_status_emoji(15), ("🟡", "Stable"))
        self.assertEqual(forecaster.get_status_emoji(25), ("🟡", "Stable"))
        self.assertEqual(forecaster.get_status_emoji(14.9), ("🟠", "Warning")) # Edge case
        # Test 'Warning' status
        self.assertEqual(forecaster.get_status_emoji(5), ("🟠", "Warning"))
        self.assertEqual(forecaster.get_status_emoji(10), ("🟠", "Warning"))
        self.assertEqual(forecaster.get_status_emoji(4.9), ("🔴", "Critical")) # Edge case
        # Test 'Critical' status
        self.assertEqual(forecaster.get_status_emoji(1), ("🔴", "Critical"))
        self.assertEqual(forecaster.get_status_emoji(3), ("🔴", "Critical"))
        self.assertEqual(forecaster.get_status_emoji(0.9), ("💀", "Depleted")) # Edge case
        # Test 'Depleted' status
        self.assertEqual(forecaster.get_status_emoji(0), ("💀", "Depleted"))
        self.assertEqual(forecaster.get_status_emoji(-5), ("💀", "Depleted"))

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner
    @patch('sys.stderr') # Mock rationale: Capture stderr output for assertion
    def test_load_config_yaml(self, mock_stderr, mock_exit, mock_file_open):
        mock_file_open.return_value.read.return_value = "resources:\n  - name: Test\n    current_amount: 10\n    daily_consumption: 1\n"
        config = forecaster.load_config("test.yaml")
        self.assertEqual(config, {'resources': [{'name': 'Test', 'current_amount': 10, 'daily_consumption': 1}]})
        mock_file_open.assert_called_with("test.yaml", 'r')

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner
    @patch('sys.stderr') # Mock rationale: Capture stderr output for assertion
    def test_load_config_json(self, mock_stderr, mock_exit, mock_file_open):
        mock_file_open.return_value.read.return_value = '{"resources": [{"name": "Test", "current_amount": 10, "daily_consumption": 1}]}'
        config = forecaster.load_config("test.json")
        self.assertEqual(config, {'resources': [{'name': 'Test', 'current_amount': 10, 'daily_consumption': 1}]})
        mock_file_open.assert_called_with("test.json", 'r')

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner
    @patch('sys.stderr') # Mock rationale: Capture stderr output for assertion
    def test_load_config_file_not_found(self, mock_stderr, mock_exit, mock_file_open):
        forecaster.load_config("non_existent.yaml")
        mock_exit.assert_called_with(1)
        self.assertIn("Error: Config file not found", mock_stderr.write.call_args[0][0])

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner
    @patch('sys.stderr') # Mock rationale: Capture stderr output for assertion
    def test_load_config_invalid_yaml(self, mock_stderr, mock_exit, mock_file_open):
        mock_file_open.return_value.read.return_value = "resources: - name: Test\n  invalid_yaml_structure"
        forecaster.load_config("invalid.yaml")
        mock_exit.assert_called_with(1)
        self.assertIn("Error: Failed to parse config file", mock_stderr.write.call_args[0][0])

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner
    @patch('sys.stderr') # Mock rationale: Capture stderr output for assertion
    def test_load_config_unsupported_format(self, mock_stderr, mock_exit, mock_file_open):
        forecaster.load_config("unsupported.txt")
        mock_exit.assert_called_with(1)
        self.assertIn("Error: Unsupported config file format", mock_stderr.write.call_args[0][0])

    @patch('argparse.ArgumentParser.parse_args')
    @patch('forecaster.load_config')
    @patch('sys.stdout') # Mock rationale: Capture stdout output for assertion
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner
    def test_main_functionality(self, mock_exit, mock_stdout, mock_load_config, mock_parse_args):
        # Mock command line arguments
        mock_parse_args.return_value.config = "mock_config.yaml"

        # Mock config content
        mock_load_config.return_value = {
            'resources': [
                {'name': 'Water', 'current_amount': 100, 'daily_consumption': 10},
                {'name': 'Food', 'current_amount': 50, 'daily_consumption': 0},
                {'name': 'Ammo', 'current_amount': 5, 'daily_consumption': 2},
                {'name': 'Scrap', 'current_amount': 0, 'daily_consumption': 1}
            ]
        }

        forecaster.main()

        output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)

        self.assertIn("Resource                  | Current | Consump. | Days Left | Status", output)
        self.assertIn("Water                     | 100.0   | 10.0     | 10.0      | 🟠 Warning", output)
        self.assertIn("Food                      | 50.0    | 0.0      | ∞         | 🟢 Plenty", output)
        self.assertIn("Ammo                      | 5.0     | 2.0      | 2.5       | 🔴 Critical", output)
        self.assertIn("Scrap                     | 0.0     | 1.0      | 0.0       | 💀 Depleted", output)
        mock_exit.assert_not_called() # Should not exit on successful run

    @patch('argparse.ArgumentParser.parse_args')
    @patch('forecaster.load_config')
    @patch('sys.stdout') # Mock rationale: Capture stdout output for assertion
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner
    def test_main_no_resources(self, mock_exit, mock_stdout, mock_load_config, mock_parse_args):
        mock_parse_args.return_value.config = "mock_config.yaml"
        mock_load_config.return_value = {'resources': []}

        forecaster.main()

        output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
        self.assertIn("No resources defined in the configuration file.", output)
        mock_exit.assert_called_with(0) # Should exit with 0 if no resources, as it's not an error

    @patch('argparse.ArgumentParser.parse_args')
    @patch('forecaster.load_config')
    @patch('sys.stdout') # Mock rationale: Capture stdout output for assertion
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner
    def test_main_missing_resource_keys(self, mock_exit, mock_stdout, mock_load_config, mock_parse_args):
        mock_parse_args.return_value.config = "mock_config.yaml"
        mock_load_config.return_value = {
            'resources': [
                {'name': 'Partial Resource'},
                {'current_amount': 10, 'daily_consumption': 1}
            ]
        }

        forecaster.main()

        output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
        self.assertIn("Unknown Resource", output)
        self.assertIn("0.0", output) # Default current_amount
        self.assertIn("0.0", output) # Default daily_consumption
        self.assertIn("∞", output) # Default daily_consumption 0 leads to inf
        mock_exit.assert_not_called()
