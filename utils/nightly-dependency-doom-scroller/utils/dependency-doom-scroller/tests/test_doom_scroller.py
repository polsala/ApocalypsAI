import unittest
from unittest.mock import patch, mock_open
import os
import tempfile
import json
import io
import requests # Import requests to mock its exceptions
from src.doom_scroller import main, _get_latest_version, _parse_requirements

# Mock rationale: We need to simulate network responses from PyPI without making actual HTTP requests.
# This ensures tests are fast, deterministic, and can run offline. `requests.get` is patched
# to return mock Response objects with predefined JSON content and status codes.

# Mock rationale: File system operations (reading requirements.txt) must be controlled
# for testing. `tempfile` is used to create and manage temporary requirements.txt files
# with controlled content, ensuring isolation and determinism.

class TestDoomScroller(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = io.StringIO()
        self.stdout_patch = patch('sys.stdout', self.held_stdout)
        self.stdout_patch.start()

        # Create a temporary directory for requirements.txt files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

    def tearDown(self):
        self.stdout_patch.stop()

    def _create_requirements_file(self, content):
        file_path = os.path.join(self.temp_dir.name, 'requirements.txt')
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path

    @patch('requests.get')
    def test_get_latest_version_success(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'info': {'version': '2.28.1'}}
        mock_get.return_value = mock_response

        version = _get_latest_version('requests')
        self.assertEqual(version, '2.28.1')
        mock_get.assert_called_once_with('https://pypi.org/pypi/requests/json', timeout=5)

    @patch('requests.get')
    def test_get_latest_version_not_found(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('404 Client Error')
        mock_get.return_value = mock_response

        version = _get_latest_version('nonexistent-package')
        self.assertIsNone(version)
        self.assertIn("Error fetching latest version for nonexistent-package", self.held_stdout.getvalue())

    @patch('requests.get')
    def test_get_latest_version_network_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError('Network is down')

        version = _get_latest_version('requests')
        self.assertIsNone(version)
        self.assertIn("Error fetching latest version for requests", self.held_stdout.getvalue())

    @patch('requests.get')
    def test_get_latest_version_malformed_json(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'bad_key': 'no_version'}
        mock_get.return_value = mock_response

        version = _get_latest_version('requests')
        self.assertIsNone(version)
        self.assertIn("Could not find version info for requests on PyPI or JSON structure is unexpected.", self.held_stdout.getvalue())

    def test_parse_requirements_basic(self):
        content = "requests==2.25.1\npyyaml==5.4.1\n"
        file_path = self._create_requirements_file(content)
        packages = _parse_requirements(file_path)
        self.assertEqual(packages, [('requests', '2.25.1'), ('pyyaml', '5.4.1')])

    def test_parse_requirements_with_comments_and_blank_lines(self):
        content = "# This is a comment\nrequests==2.25.1\n\n  # Another comment\npyyaml==5.4.1  \n"
        file_path = self._create_requirements_file(content)
        packages = _parse_requirements(file_path)
        self.assertEqual(packages, [('requests', '2.25.1'), ('pyyaml', '5.4.1')])

    def test_parse_requirements_no_version(self):
        content = "requests\npyyaml>=5.4.1\n"
        file_path = self._create_requirements_file(content)
        packages = _parse_requirements(file_path)
        self.assertEqual(packages, [('requests', None), ('pyyaml', '5.4.1')])

    def test_parse_requirements_file_not_found(self):
        packages = _parse_requirements('/nonexistent/path/reqs.txt')
        self.assertEqual(packages, [])
        self.assertIn("Error: requirements file not found", self.held_stdout.getvalue())

    @patch('src.doom_scroller._get_latest_version')
    def test_main_no_requirements_file(self, mock_get_latest_version):
        # Ensure no requirements.txt in temp_dir
        main(directory=self.temp_dir.name)
        self.assertIn(f"No 'requirements.txt' found in '{self.temp_dir.name}'.", self.held_stdout.getvalue())
        mock_get_latest_version.assert_not_called()

    @patch('src.doom_scroller._get_latest_version')
    def test_main_up_to_date_package(self, mock_get_latest_version):
        content = "requests==2.28.1\n"
        self._create_requirements_file(content)
        mock_get_latest_version.return_value = '2.28.1'

        main(directory=self.temp_dir.name)
        output = self.held_stdout.getvalue()
        self.assertIn("✅ All clear for 'requests'. Its cosmic alignment is stable (v2.28.1).", output)
        mock_get_latest_version.assert_called_once_with('requests')

    @patch('src.doom_scroller._get_latest_version')
    def test_main_outdated_package(self, mock_get_latest_version):
        content = "requests==2.25.1\n"
        self._create_requirements_file(content)
        mock_get_latest_version.return_value = '2.28.1'

        main(directory=self.temp_dir.name)
        output = self.held_stdout.getvalue()
        self.assertIn("🚨 WARNING: The ancient scroll for 'requests' (v2.25.1) is crumbling! A newer, more powerful version (v2.28.1) has emerged from the cosmic dust. Upgrade to avoid the 'Dependency Collapse'!", output)
        mock_get_latest_version.assert_called_once_with('requests')

    @patch('src.doom_scroller._get_latest_version')
    def test_main_package_not_found_on_pypi(self, mock_get_latest_version):
        content = "nonexistent-package==1.0.0\n"
        self._create_requirements_file(content)
        mock_get_latest_version.return_value = None # Simulate PyPI not finding it

        main(directory=self.temp_dir.name)
        output = self.held_stdout.getvalue()
        self.assertIn("❓ UNKNOWN: Could not determine the fate of 'nonexistent-package'. Its cosmic signature is elusive.", output)
        mock_get_latest_version.assert_called_once_with('nonexistent-package')

    @patch('src.doom_scroller._get_latest_version')
    def test_main_mixed_packages(self, mock_get_latest_version):
        content = "requests==2.25.1\npyyaml==5.4.1\nblack==21.10b0\n"
        self._create_requirements_file(content)

        # Configure mock for different packages
        def mock_get_latest_version_side_effect(package_name):
            if package_name == 'requests':
                return '2.28.1'
            elif package_name == 'pyyaml':
                return '5.4.1'
            elif package_name == 'black':
                return '22.3.0'
            return None

        mock_get_latest_version.side_effect = mock_get_latest_version_side_effect

        main(directory=self.temp_dir.name)
        output = self.held_stdout.getvalue()

        self.assertIn("🚨 WARNING: The ancient scroll for 'requests' (v2.25.1) is crumbling! A newer, more powerful version (v2.28.1) has emerged from the cosmic dust. Upgrade to avoid the 'Dependency Collapse'!", output)
        self.assertIn("✅ All clear for 'pyyaml'. Its cosmic alignment is stable (v5.4.1).", output)
        self.assertIn("🚨 WARNING: The ancient scroll for 'black' (v21.10b0) is crumbling! A newer, more powerful version (v22.3.0) has emerged from the cosmic dust. Upgrade to avoid the 'Dependency Collapse'!", output)
        self.assertEqual(mock_get_latest_version.call_count, 3)

    @patch('src.doom_scroller._get_latest_version')
    def test_main_package_no_version_specified(self, mock_get_latest_version):
        content = "unpinned-package\n"
        self._create_requirements_file(content)

        main(directory=self.temp_dir.name)
        output = self.held_stdout.getvalue()
        self.assertIn("⚠️ CAUTION: 'unpinned-package' has no version specified. The future is uncertain! (Consider pinning a version)", output)
        mock_get_latest_version.assert_not_called()

    @patch('src.doom_scroller._get_latest_version')
    def test_main_empty_requirements_file(self, mock_get_latest_version):
        content = "# Just comments\n\n"
        self._create_requirements_file(content)

        main(directory=self.temp_dir.name)
        output = self.held_stdout.getvalue()
        self.assertIn("The scrolls are blank. No dependencies found to scrutinize.", output)
        mock_get_latest_version.assert_not_called()

    @patch('src.doom_scroller._get_latest_version')
    def test_main_with_packaging_version_parse(self, mock_get_latest_version):
        # Test with packaging.version.parse if available
        content = "requests==2.25.1\n"
        self._create_requirements_file(content)
        mock_get_latest_version.return_value = '2.28.1'

        # Mock the import to ensure it's used if available
        with patch.dict('sys.modules', {'packaging.version': __import__('packaging.version')}): # Ensure packaging is importable
            main(directory=self.temp_dir.name)
            output = self.held_stdout.getvalue()
            self.assertIn("🚨 WARNING: The ancient scroll for 'requests' (v2.25.1) is crumbling! A newer, more powerful version (v2.28.1) has emerged from the cosmic dust. Upgrade to avoid the 'Dependency Collapse'!", output)

    @patch('src.doom_scroller._get_latest_version')
    def test_main_without_packaging_version_parse(self, mock_get_latest_version):
        # Test fallback to string comparison if packaging is not available
        content = "requests==2.25.1\n"
        self._create_requirements_file(content)
        mock_get_latest_version.return_value = '2.28.1'

        # Mock packaging.version to be unavailable
        with patch.dict('sys.modules', {'packaging.version': None}):
            main(directory=self.temp_dir.name)
            output = self.held_stdout.getvalue()
            self.assertIn("🚨 WARNING: The ancient scroll for 'requests' (v2.25.1) is crumbling! A newer, more powerful version (v2.28.1) has emerged from the cosmic dust. Upgrade to avoid the 'Dependency Collapse'!", output)
