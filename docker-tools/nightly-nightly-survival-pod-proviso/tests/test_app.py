import unittest
from unittest.mock import patch, mock_open
import os
from src.app import load_manifest, render_template, validate_compose_yaml, main

class TestSurvivalPodProvisor(unittest.TestCase):

    def setUp(self):
        self.test_blueprint_content = """
version: '3.8'
services:
  {{ pod_name }}:
    image: {{ image_name }}:{{ image_tag | default('latest') }}
    ports:
      - "{{ host_port }}:{{ container_port }}"
    environment:
      POD_ENV_VAR: "{{ env_var_value }}"
      SECRET_KEY: "{{ secrets.secret_key }}"
    volumes:
      - {{ volume_path }}:/data
"""
        self.test_manifest_json_content = """{
  "pod_name": "test-web",
  "image_name": "httpd",
  "image_tag": "2.4",
  "host_port": 80,
  "container_port": 8080,
  "env_var_value": "test-env",
  "volume_path": "./test-data",
  "secrets": {
    "secret_key": "test-secret"
  }
}"""
        self.test_manifest_yaml_content = """
pod_name: test-db
image_name: postgres
image_tag: 13
host_port: 5432
container_port: 5432
env_var_value: db-env
volume_path: ./db-data
secrets:
  secret_key: db-secret
"""

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.splitext', return_value=('manifest', '.json'))
    def test_load_manifest_json(self, mock_splitext, mock_file):
        # Mock rationale: Simulates reading a JSON manifest file from disk without actual file I/O.
        mock_file.return_value.read.return_value = self.test_manifest_json_content
        manifest = load_manifest('manifest.json')
        self.assertEqual(manifest['pod_name'], 'test-web')
        self.assertEqual(manifest['secrets']['secret_key'], 'test-secret')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.splitext', return_value=('manifest', '.yaml'))
    def test_load_manifest_yaml(self, mock_splitext, mock_file):
        # Mock rationale: Simulates reading a YAML manifest file from disk without actual file I/O.
        mock_file.return_value.read.return_value = self.test_manifest_yaml_content
        manifest = load_manifest('manifest.yaml')
        self.assertEqual(manifest['pod_name'], 'test-db')
        self.assertEqual(manifest['secrets']['secret_key'], 'db-secret')

    def test_render_template(self):
        # Mock rationale: Jinja2 rendering is deterministic and doesn't require file I/O if template content is provided.
        context = {
            "pod_name": "rendered-pod",
            "image_name": "ubuntu",
            "image_tag": "20.04",
            "host_port": 2222,
            "container_port": 22,
            "env_var_value": "rendered-env",
            "volume_path": "./rendered-data",
            "secrets": {"secret_key": "rendered-secret"}
        }
        # We need to mock FileSystemLoader to provide the template content directly
        with patch('jinja2.FileSystemLoader') as MockLoader:
            MockLoader.return_value.get_source.return_value = (self.test_blueprint_content, None, None)
            rendered = render_template('blueprint.yml', context)
            self.assertIn('container_name: rendered-pod', rendered)
            self.assertIn('image: ubuntu:20.04', rendered)
            self.assertIn('ports:\n      - "2222:22"', rendered)
            self.assertIn('POD_ENV_VAR: "rendered-env"', rendered)
            self.assertIn('SECRET_KEY: "rendered-secret"', rendered)
            self.assertIn('volumes:\n      - ./rendered-data:/data', rendered)

    def test_validate_compose_yaml_valid(self):
        # Mock rationale: Input is a string, no file I/O or external calls needed.
        valid_yaml = """
version: '3.8'
services:
  web:
    image: nginx
"""
        self.assertTrue(validate_compose_yaml(valid_yaml))

    def test_validate_compose_yaml_no_services(self):
        # Mock rationale: Input is a string, no file I/O or external calls needed.
        invalid_yaml = """
version: '3.8'
"""
        with self.assertRaisesRegex(ValueError, "must contain a 'services' section."):
            validate_compose_yaml(invalid_yaml)

    def test_validate_compose_yaml_invalid_syntax(self):
        # Mock rationale: Input is a string, no file I/O or external calls needed.
        invalid_yaml = """
version: '3.8'
services:
  web:
  - image: nginx # Invalid YAML structure
"""
        with self.assertRaisesRegex(ValueError, "Invalid YAML syntax"):
            validate_compose_yaml(invalid_yaml)

    @patch('src.app.load_manifest')
    @patch('src.app.render_template')
    @patch('src.app.validate_compose_yaml')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_success(self, mock_parse_args, mock_stdout, mock_validate, mock_render, mock_load):
        # Mock rationale: Mocks all external dependencies (file I/O, argparse, stdout) to isolate main function logic.
        mock_parse_args.return_value.blueprint = 'blueprint.yml'
        mock_parse_args.return_value.manifest = 'manifest.json'
        mock_load.return_value = {'key': 'value'}
        mock_render.return_value = "version: '3.8'\nservices:\n  test: {image: 'test'}"
        mock_validate.return_value = True

        main()

        mock_load.assert_called_once_with('manifest.json')
        mock_render.assert_called_once_with('blueprint.yml', {'key': 'value'})
        mock_validate.assert_called_once_with("version: '3.8'\nservices:\n  test: {image: 'test'}")
        self.assertIn("version: '3.8'\nservices:\n  test: {image: 'test'}", mock_stdout.getvalue())

    @patch('src.app.load_manifest', side_effect=ValueError("Bad manifest"))
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_failure(self, mock_exit, mock_parse_args, mock_stdout, mock_load):
        # Mock rationale: Mocks external dependencies and forces an error to test error handling and exit behavior.
        mock_parse_args.return_value.blueprint = 'blueprint.yml'
        mock_parse_args.return_value.manifest = 'manifest.json'

        main()

        self.assertIn("Error provisioning pod: Bad manifest", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
