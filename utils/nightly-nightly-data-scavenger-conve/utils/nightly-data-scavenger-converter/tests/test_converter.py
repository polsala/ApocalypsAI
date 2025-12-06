import unittest
from unittest.mock import patch, mock_open
import sys
import io

# Mock PyYAML and tomli/tomli_w if not installed, to ensure tests run offline.
# Mock rationale: The utility explicitly states these are optional dependencies
# and raises ImportError if not found. For testing, we want to control their presence
# and provide simplified, deterministic mock implementations for conversion logic.

# --- Mock Implementations for YAML and TOML --- #
class MockYAML:
    def safe_load(self, s):
        # Simple mock for YAML loading: handles basic key-value pairs and types.
        if s.strip() == '': return {}
        data = {}
        for line in s.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if value.lower() == 'true': value = True
                elif value.lower() == 'false': value = False
                elif value.isdigit(): value = int(value)
                elif value.replace('.', '', 1).isdigit(): value = float(value)
                data[key] = value
        return data

    def safe_dump(self, data, **kwargs):
        # Simple mock for YAML dumping: outputs key-value pairs, preserving order.
        output = []
        for k, v in data.items():
            # Convert Python bool to YAML-style True/False
            if isinstance(v, bool): v = str(v).lower().capitalize()
            output.append(f"{k}: {v}")
        return '\n'.join(output)

class MockTomli:
    def loads(self, s):
        # Simple mock for TOML loading: handles basic key-value pairs and types.
        if s.strip() == '': return {}
        data = {}
        for line in s.strip().split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                if value.startswith('"') and value.endswith('"'): value = value[1:-1]
                elif value.lower() == 'true': value = True
                elif value.lower() == 'false': value = False
                elif value.isdigit(): value = int(value)
                elif value.replace('.', '', 1).isdigit(): value = float(value)
                data[key] = value
        return data

class MockTomliW:
    def dumps(self, data):
        # Simple mock for TOML dumping: outputs key-value pairs, preserving order.
        output = []
        for k, v in data.items():
            if isinstance(v, str): output.append(f"{k} = \"{v}\"")
            elif isinstance(v, bool): output.append(f"{k} = {str(v).lower()}")
            else: output.append(f"{k} = {v}")
        return '\n'.join(output)

# Patch sys.modules to inject our mocks before importing converter.py
sys.modules['yaml'] = MockYAML()
sys.modules['tomli'] = MockTomli()
sys.modules['tomli_w'] = MockTomliW()

# Now import the converter module, which will use our mocked dependencies
from src.converter import convert_data, FORMAT_HANDLERS

class TestConverter(unittest.TestCase):

    def setUp(self):
        # Ensure FORMAT_HANDLERS uses our mock implementations for each test run.
        # This is crucial if converter.py was imported before mocks were fully set up.
        FORMAT_HANDLERS['yaml'] = {'load': sys.modules['yaml'].safe_load, 'dump': sys.modules['yaml'].safe_dump}
        FORMAT_HANDLERS['toml'] = {'load': sys.modules['tomli'].loads, 'dump': sys.modules['tomli_w'].dumps}

    # Sample data for testing various conversions
    json_input = '{\n  "name": "ApocalypsAI",\n  "version": 1.0,\n  "active": true\n}'
    yaml_output = 'name: ApocalypsAI\nversion: 1.0\nactive: True'
    toml_output = 'name = "ApocalypsAI"\nversion = 1.0\nactive = true'

    yaml_input = 'project: \"ApocalypsAI\"\nstatus: active\nid: 123'
    json_output_from_yaml = '{\n  "project": "ApocalypsAI",\n  "status": "active",\n  "id": 123\n}'
    toml_output_from_yaml = 'project = "ApocalypsAI"\nstatus = "active"\nid = 123'

    toml_input = 'title = "ApocalypsAI Config"\nport = 8080\nenabled = true'
    json_output_from_toml = '{\n  "title": "ApocalypsAI Config",\n  "port": 8080,\n  "enabled": true\n}'
    yaml_output_from_toml = 'title: ApocalypsAI Config\nport: 8080\nenabled: True'

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_json_to_yaml_conversion(self, mock_exists, mock_file_open):
        # Mock rationale: Simulate file read and write operations without touching the filesystem.
        # mock_open handles both 'r' and 'w' modes. os.path.exists is mocked to ensure the input file is considered present.
        mock_file_open.side_effect = [
            io.StringIO(self.json_input), # For reading input_file
            io.StringIO()                # For writing output_file
        ]

        input_path = 'input.json'
        output_path = 'output.yaml'
        convert_data(input_path, output_path, 'json', 'yaml')

        mock_file_open.assert_any_call(input_path, 'r', encoding='utf-8')
        mock_file_open.assert_any_call(output_path, 'w', encoding='utf-8')

        written_content = mock_file_open().write.call_args[0][0]
        self.assertEqual(written_content.strip(), self.yaml_output.strip())

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_yaml_to_json_conversion(self, mock_exists, mock_file_open):
        # Mock rationale: Simulate file read and write operations without touching the filesystem.
        mock_file_open.side_effect = [
            io.StringIO(self.yaml_input),
            io.StringIO()
        ]

        input_path = 'input.yaml'
        output_path = 'output.json'
        convert_data(input_path, output_path, 'yaml', 'json')

        written_content = mock_file_open().write.call_args[0][0]
        self.assertEqual(written_content.strip(), self.json_output_from_yaml.strip())

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_json_to_toml_conversion(self, mock_exists, mock_file_open):
        # Mock rationale: Simulate file read and write operations without touching the filesystem.
        mock_file_open.side_effect = [
            io.StringIO(self.json_input),
            io.StringIO()
        ]

        input_path = 'input.json'
        output_path = 'output.toml'
        convert_data(input_path, output_path, 'json', 'toml')

        written_content = mock_file_open().write.call_args[0][0]
        self.assertEqual(written_content.strip(), self.toml_output.strip())

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_toml_to_json_conversion(self, mock_exists, mock_file_open):
        # Mock rationale: Simulate file read and write operations without touching the filesystem.
        mock_file_open.side_effect = [
            io.StringIO(self.toml_input),
            io.StringIO()
        ]

        input_path = 'input.toml'
        output_path = 'output.json'
        convert_data(input_path, output_path, 'toml', 'json')

        written_content = mock_file_open().write.call_args[0][0]
        self.assertEqual(written_content.strip(), self.json_output_from_toml.strip())

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_yaml_to_toml_conversion(self, mock_exists, mock_file_open):
        # Mock rationale: Simulate file read and write operations without touching the filesystem.
        mock_file_open.side_effect = [
            io.StringIO(self.yaml_input),
            io.StringIO()
        ]

        input_path = 'input.yaml'
        output_path = 'output.toml'
        convert_data(input_path, output_path, 'yaml', 'toml')

        written_content = mock_file_open().write.call_args[0][0]
        self.assertEqual(written_content.strip(), self.toml_output_from_yaml.strip())

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_toml_to_yaml_conversion(self, mock_exists, mock_file_open):
        # Mock rationale: Simulate file read and write operations without touching the filesystem.
        mock_file_open.side_effect = [
            io.StringIO(self.toml_input),
            io.StringIO()
        ]

        input_path = 'input.toml'
        output_path = 'output.yaml'
        convert_data(input_path, output_path, 'toml', 'yaml')

        written_content = mock_file_open().write.call_args[0][0]
        self.assertEqual(written_content.strip(), self.yaml_output_from_toml.strip())

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_input_file_not_found(self, mock_exists, mock_file_open):
        # Mock rationale: Simulate a scenario where the input file does not exist.
        with self.assertRaisesRegex(FileNotFoundError, "Input file not found: non_existent.json"):
            convert_data('non_existent.json', 'output.yaml', 'json', 'yaml')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_invalid_input_format_content(self, mock_exists, mock_file_open):
        # Mock rationale: Simulate an input file with malformed content for the specified format.
        mock_file_open.side_effect = [
            io.StringIO('This is not valid JSON'),
            io.StringIO()
        ]
        with self.assertRaisesRegex(ValueError, "Error parsing input file as json"):
            convert_data('invalid.json', 'output.yaml', 'json', 'yaml')

    def test_unsupported_input_format(self):
        # Mock rationale: Test the utility's handling of explicitly unsupported formats.
        with self.assertRaisesRegex(ValueError, "Unsupported input format: xml"):
            convert_data('input.xml', 'output.json', 'xml', 'json')

    def test_unsupported_output_format(self):
        # Mock rationale: Test the utility's handling of explicitly unsupported formats.
        with self.assertRaisesRegex(ValueError, "Unsupported output format: csv"):
            convert_data('input.json', 'output.csv', 'json', 'csv')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_io_error_on_write(self, mock_exists, mock_file_open):
        # Mock rationale: Simulate an IOError during the writing process.
        mock_file_open.side_effect = [
            io.StringIO(self.json_input),
            io.StringIO() # This will be the mock for the output file
        ]
        # Make the write operation raise an exception on the output file mock
        mock_file_open.return_value.__enter__.return_value.write.side_effect = IOError("Disk full")

        with self.assertRaisesRegex(IOError, "Error writing output file output.yaml: Disk full"):
            convert_data('input.json', 'output.yaml', 'json', 'yaml')
