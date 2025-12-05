import unittest
import os
import tempfile
from unittest.mock import patch
from src.config_checker import ConfigChecker, main # Import main to test CLI

class TestConfigChecker(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup) # Ensure cleanup even if tests fail

    def _create_file(self, filename, content):
        path = os.path.join(self.temp_dir.name, filename)
        with open(path, 'w') as f:
            f.write(content)
        return path

    def test_valid_yaml_config_no_rules(self):
        config_content = """
system:
    name: Alpha
    version: 1.0
settings:
    enabled: true
    threshold: 100
        """
        config_path = self._create_file("valid_config.yaml", config_content)
        checker = ConfigChecker(config_path)
        errors = checker.check()
        self.assertEqual(len(errors), 0)

    def test_valid_json_config_no_rules(self):
        config_content = """
{
    "system": {
        "name": "Beta",
        "version": 2.0
    },
    "settings": {
        "enabled": false,
        "threshold": 50
    }
}
        """
        config_path = self._create_file("valid_config.json", config_content)
        checker = ConfigChecker(config_path)
        errors = checker.check()
        self.assertEqual(len(errors), 0)

    def test_missing_config_file(self):
        checker = ConfigChecker("non_existent_config.yaml")
        errors = checker.check()
        self.assertEqual(len(errors), 1)
        self.assertIn("File not found", errors[0])

    def test_invalid_yaml_syntax(self):
        config_content = """
system:
  name: Alpha
settings:
  enabled: true
  threshold: 100
- this is invalid yaml
        """
        config_path = self._create_file("invalid_syntax.yaml", config_content)
        checker = ConfigChecker(config_path)
        errors = checker.check()
        self.assertEqual(len(errors), 1)
        self.assertIn("Error parsing", errors[0])

    def test_missing_required_key(self):
        config_content = """
system:
    name: Alpha
settings:
    enabled: true
        """
        rules_content = """
required_keys:
    system:
        name: {}
        version: {}
    settings:
        enabled: {}
        threshold: {}
        """
        config_path = self._create_file("config.yaml", config_content)
        rules_path = self._create_file("rules.yaml", rules_content)
        checker = ConfigChecker(config_path, rules_path)
        errors = checker.check()
        self.assertEqual(len(errors), 2) # Missing system.version, settings.threshold
        self.assertIn("Missing required key: 'system.version'", errors)
        self.assertIn("Missing required key: 'settings.threshold'", errors)

    def test_incorrect_type(self):
        config_content = """
system:
    name: Alpha
    version: "1.0" # Should be int
settings:
    enabled: "true" # Should be bool
    threshold: 100.5 # Should be int
        """
        rules_content = """
type_rules:
    system:
        version: integer
    settings:
        enabled: boolean
        threshold: integer
        """
        config_path = self._create_file("config.yaml", config_content)
        rules_path = self._create_file("rules.yaml", rules_content)
        checker = ConfigChecker(config_path, rules_path)
        errors = checker.check()
        self.assertEqual(len(errors), 3)
        self.assertIn("Incorrect type for 'system.version': Expected int, got str", errors)
        self.assertIn("Incorrect type for 'settings.enabled': Expected bool, got str", errors)
        self.assertIn("Incorrect type for 'settings.threshold': Expected int, got float", errors)

    def test_invalid_value_enum_and_range(self):
        config_content = """
system:
    name: Beta
    level: 5 # Max is 3
settings:
    mode: "debug" # Not in enum
        """
        rules_content = """
value_rules:
    system:
        level:
            min: 1
            max: 3
    settings:
        mode:
            enum: ["production", "staging"]
        """
        config_path = self._create_file("config.yaml", config_content)
        rules_path = self._create_file("rules.yaml", rules_content)
        checker = ConfigChecker(config_path, rules_path)
        errors = checker.check()
        self.assertEqual(len(errors), 2)
        self.assertIn("Value for 'system.level' is too high: 5 (max: 3)", errors)
        self.assertIn("Invalid value for 'settings.mode': 'debug' not in allowed list ['production', 'staging']", errors)

    def test_mixed_validation_success(self):
        config_content = """
system:
    name: Gamma
    version: 3
settings:
    enabled: true
    threshold: 75
    mode: "production"
        """
        rules_content = """
required_keys:
    system:
        name: {}
        version: {}
    settings:
        enabled: {}
        threshold: {}
        mode: {}
type_rules:
    system:
        version: integer
    settings:
        enabled: boolean
        threshold: integer
        mode: string
value_rules:
    system:
        version:
            min: 1
            max: 5
    settings:
        threshold:
            min: 0
            max: 100
        mode:
            enum: ["production", "staging"]
        """
        config_path = self._create_file("config.yaml", config_content)
        rules_path = self._create_file("rules.yaml", rules_content)
        checker = ConfigChecker(config_path, rules_path)
        errors = checker.check()
        self.assertEqual(len(errors), 0)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_success(self, mock_exit, mock_print, mock_parse_args):
        # Mock rationale: We are testing the CLI entry point. 
        # We need to mock argparse to control the arguments passed to main().
        # We also mock print and sys.exit to capture output and prevent actual exit during testing.
        config_content = """
system:
    name: Alpha
        """
        config_path = self._create_file("cli_config.yaml", config_content)

        mock_parse_args.return_value = type('obj', (object,), {
            'config_file': config_path,
            'rules_file': None
        })()

        main()
        mock_exit.assert_called_once_with(0)
        mock_print.assert_any_call(f"Configuration for {config_path} is perfectly calibrated. All systems nominal!")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_failure(self, mock_exit, mock_print, mock_parse_args):
        # Mock rationale: Similar to test_main_success, we mock CLI arguments, print, and sys.exit.
        # This test specifically checks the failure path of the CLI.
        config_content = """
system:
    name: Alpha
settings:
    enabled: "true" # Should be bool
        """
        rules_content = """
type_rules:
    settings:
        enabled: boolean
        """
        config_path = self._create_file("cli_config_fail.yaml", config_content)
        rules_path = self._create_file("cli_rules_fail.yaml", rules_content)

        mock_parse_args.return_value = type('obj', (object,), {
            'config_file': config_path,
            'rules_file': rules_path
        })()

        main()
        mock_exit.assert_called_once_with(1)
        mock_print.assert_any_call(f"Configuration check failed for {config_path}:")
        mock_print.assert_any_call("- Incorrect type for 'settings.enabled': Expected bool, got str")

    def test_unsupported_file_type(self):
        config_content = "This is not a YAML or JSON file."
        config_path = self._create_file("unsupported.txt", config_content)
        checker = ConfigChecker(config_path)
        errors = checker.check()
        self.assertEqual(len(errors), 1)
        self.assertIn("Unsupported file type", errors[0])

    def test_empty_rules_file(self):
        config_content = """
system:
    name: Alpha
        """
        rules_content = "" # Empty file
        config_path = self._create_file("config.yaml", config_content)
        rules_path = self._create_file("empty_rules.yaml", rules_content)
        checker = ConfigChecker(config_path, rules_path)
        errors = checker.check()
        # An empty rules file means no rules to apply, so if the config is valid YAML/JSON, it passes.
        self.assertEqual(len(errors), 0)

    def test_rules_file_not_found(self):
        config_content = """
system:
    name: Alpha
        """
        config_path = self._create_file("config.yaml", config_content)
        checker = ConfigChecker(config_path, "non_existent_rules.yaml")
        errors = checker.check()
        self.assertEqual(len(errors), 1)
        self.assertIn("File not found at non_existent_rules.yaml", errors[0])

    def test_empty_config_file(self):
        config_content = "" # Empty file
        config_path = self._create_file("empty_config.yaml", config_content)
        checker = ConfigChecker(config_path)
        errors = checker.check()
        self.assertEqual(len(errors), 1)
        self.assertIn("Error parsing empty_config.yaml: end of the stream or a document stream must contain at least one document", errors[0])

    def test_empty_json_config_file(self):
        config_content = "{}" # Empty JSON object
        config_path = self._create_file("empty_config.json", config_content)
        checker = ConfigChecker(config_path)
        errors = checker.check()
        self.assertEqual(len(errors), 0)

    def test_empty_json_config_file_with_rules(self):
        config_content = "{}" # Empty JSON object
        rules_content = """
required_keys:
    system:
        name: {}
        """
        config_path = self._create_file("empty_config.json", config_content)
        rules_path = self._create_file("rules.yaml", rules_content)
        checker = ConfigChecker(config_path, rules_path)
        errors = checker.check()
        self.assertEqual(len(errors), 1)
        self.assertIn("Missing required key: 'system'", errors)
