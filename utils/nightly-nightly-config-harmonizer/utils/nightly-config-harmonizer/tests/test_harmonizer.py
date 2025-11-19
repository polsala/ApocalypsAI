import unittest
import os
import yaml
from unittest.mock import patch, mock_open
from io import StringIO

# Import functions from the harmonizer script
# Assuming the test runner correctly adds src to sys.path or runs from the parent directory.
from src.harmonizer import load_yaml, save_yaml, find_discrepancies, apply_defaults, main

class TestHarmonizer(unittest.TestCase):

    def setUp(self):
        self.template_content = """
api_key: "default_api_key"
log_level: "INFO"
database:
  host: "localhost"
  port: 5432
  user: "admin"
server:
  port: 8080
  timeout: 30
"""
        self.target_content_missing_keys = """
api_key: "my_secret_key"
database:
  host: "db.example.com"
  port: 5432
"""
        self.target_content_extra_key = """
api_key: "default_api_key"
log_level: "INFO"
database:
  host: "localhost"
  port: 5432
  user: "admin"
new_feature: true
"""
        self.target_content_mismatch = """
api_key: "my_secret_key"
log_level: "DEBUG"
database:
  host: "localhost"
  port: 8000 # Mismatch
  user: "admin"
server:
  port: 8080
  timeout: 60 # Mismatch
"""
        self.target_content_harmonized = """
api_key: "my_secret_key"
log_level: "INFO"
database:
  host: "db.example.com"
  port: 5432
  user: "admin"
server:
  port: 8080
  timeout: 30
"""
        self.template_config = yaml.safe_load(self.template_content)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='key: value')
    def test_load_yaml_success(self, mock_file, mock_exists):
        # Mock rationale: Simulate successful file reading for YAML content.
        result = load_yaml('dummy.yaml')
        self.assertEqual(result, {'key': 'value'})
        mock_exists.assert_called_once_with('dummy.yaml')
        mock_file.assert_called_once_with('dummy.yaml', 'r')

    @patch('os.path.exists', return_value=False)
    def test_load_yaml_file_not_found(self, mock_exists):
        # Mock rationale: Simulate a non-existent file to test error handling.
        with self.assertRaises(FileNotFoundError):
            load_yaml('non_existent.yaml')
        mock_exists.assert_called_once_with('non_existent.yaml')

    @patch('builtins.open', new_callable=mock_open)
    def test_save_yaml(self, mock_file):
        # Mock rationale: Simulate writing data to a file without actual disk I/O.
        data = {'key': 'value'}
        save_yaml('output.yaml', data)
        mock_file.assert_called_once_with('output.yaml', 'w')
        handle = mock_file()
        handle.write.assert_called_once_with(yaml.safe_dump(data, default_flow_style=False))

    def test_find_discrepancies_missing_keys(self):
        target_config = yaml.safe_load(self.target_content_missing_keys)
        discrepancies = find_discrepancies(self.template_config, target_config)
        self.assertIn(('log_level', 'INFO'), discrepancies['missing_keys'])
        self.assertIn(('database.user', 'admin'), discrepancies['missing_keys'])
        self.assertIn(('server.port', 8080), discrepancies['missing_keys'])
        self.assertIn(('server.timeout', 30), discrepancies['missing_keys'])
        self.assertEqual(len(discrepancies['extra_keys']), 0)
        self.assertIn(('api_key', 'my_secret_key', 'default_api_key'), discrepancies['value_mismatches'])

    def test_find_discrepancies_extra_key(self):
        target_config = yaml.safe_load(self.target_content_extra_key)
        discrepancies = find_discrepancies(self.template_config, target_config)
        self.assertIn('new_feature', discrepancies['extra_keys'])
        self.assertEqual(len(discrepancies['missing_keys']), 0)
        self.assertEqual(len(discrepancies['value_mismatches']), 0)

    def test_find_discrepancies_value_mismatches(self):
        target_config = yaml.safe_load(self.target_content_mismatch)
        discrepancies = find_discrepancies(self.template_config, target_config)
        self.assertIn(('api_key', 'my_secret_key', 'default_api_key'), discrepancies['value_mismatches'])
        self.assertIn(('log_level', 'DEBUG', 'INFO'), discrepancies['value_mismatches'])
        self.assertIn(('database.port', 8000, 5432), discrepancies['value_mismatches'])
        self.assertIn(('server.timeout', 60, 30), discrepancies['value_mismatches'])
        self.assertEqual(len(discrepancies['missing_keys']), 0)
        self.assertEqual(len(discrepancies['extra_keys']), 0)

    def test_find_discrepancies_no_discrepancies(self):
        target_config = yaml.safe_load(self.template_content)
        discrepancies = find_discrepancies(self.template_config, target_config)
        self.assertEqual(len(discrepancies['missing_keys']), 0)
        self.assertEqual(len(discrepancies['extra_keys']), 0)
        self.assertEqual(len(discrepancies['value_mismatches']), 0)

    def test_apply_defaults(self):
        target_config = yaml.safe_load(self.target_content_missing_keys)
        updated_config = apply_defaults(self.template_config, target_config)
        expected_config = yaml.safe_load(self.target_content_harmonized)
        self.assertEqual(updated_config, expected_config)

    @patch('src.harmonizer.load_yaml')
    @patch('src.harmonizer.save_yaml')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_report_only(self, mock_stdout, mock_save, mock_load):
        # Mock rationale: Simulate file loading and prevent actual file saving.
        # Capture stdout to verify printed messages.
        mock_load.side_effect = [
            self.template_config, # For template.yaml
            yaml.safe_load(self.target_content_missing_keys) # For target.yaml
        ]
        
        # Simulate command line arguments
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(
            template='template.yaml', target='target.yaml', apply=False
        )):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn('Discrepancies found in target.yaml:', output)
        self.assertIn('- Missing key: log_level (default: INFO)', output)
        self.assertIn('- Missing key: database.user (default: admin)', output)
        self.assertIn('- Missing key: server.port (default: 8080)', output)
        self.assertIn('- Missing key: server.timeout (default: 30)', output)
        self.assertIn("- Value mismatch for api_key: target='my_secret_key', template='default_api_key'", output)
        self.assertIn('Run with --apply to update the target file with missing defaults.', output)
        mock_save.assert_not_called()

    @patch('src.harmonizer.load_yaml')
    @patch('src.harmonizer.save_yaml')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_apply_changes(self, mock_stdout, mock_save, mock_load):
        # Mock rationale: Simulate file loading and verify file saving with updated content.
        # Capture stdout to verify printed messages.
        mock_load.side_effect = [
            self.template_config, # For template.yaml
            yaml.safe_load(self.target_content_missing_keys) # For target.yaml
        ]
        
        # Simulate command line arguments
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(
            template='template.yaml', target='target.yaml', apply=True
        )):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn('Discrepancies found in target.yaml:', output)
        self.assertIn('Applying missing defaults to target.yaml...', output)
        self.assertIn('Harmonization complete. Target file updated.', output)
        mock_save.assert_called_once()
        # Verify the content passed to save_yaml
        expected_saved_config = yaml.safe_load(self.target_content_harmonized)
        mock_save.assert_called_once_with('target.yaml', expected_saved_config)

    @patch('src.harmonizer.load_yaml')
    @patch('src.harmonizer.save_yaml')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_discrepancies(self, mock_stdout, mock_save, mock_load):
        # Mock rationale: Simulate file loading where no discrepancies exist.
        # Capture stdout to verify printed messages.
        mock_load.side_effect = [
            self.template_config, # For template.yaml
            self.template_config # For target.yaml (identical)
        ]
        
        # Simulate command line arguments
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(
            template='template.yaml', target='target.yaml', apply=False
        )):
            main()
        
        output = mock_stdout.getvalue()
        self.assertIn('No discrepancies found in target.yaml. Configuration is harmonized.', output)
        mock_save.assert_not_called()

    @patch('src.harmonizer.load_yaml', side_effect=FileNotFoundError('test_file.yaml'))
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_file_not_found_error(self, mock_exit, mock_stdout, mock_load):
        # Mock rationale: Simulate a FileNotFoundError during YAML loading.
        # Capture stdout and sys.exit to verify error handling.
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(
            template='template.yaml', target='target.yaml', apply=False
        )):
            main()
        output = mock_stdout.getvalue()
        self.assertIn('Error: File not found: test_file.yaml', output)
        mock_exit.assert_called_once_with(1)

    @patch('src.harmonizer.load_yaml', side_effect=yaml.YAMLError('bad yaml'))
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_yaml_error(self, mock_exit, mock_stdout, mock_load):
        # Mock rationale: Simulate a YAML parsing error during loading.
        # Capture stdout and sys.exit to verify error handling.
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(
            template='template.yaml', target='target.yaml', apply=False
        )):
            main()
        output = mock_stdout.getvalue()
        self.assertIn('Error parsing YAML: bad yaml', output)
        mock_exit.assert_called_once_with(1)
