import unittest
from unittest.mock import patch, mock_open
import os
import json
import requests
from src.stabilizer import parse_simple_version, parse_requirements, get_latest_pypi_version, stabilize_dependencies

class TestStabilizer(unittest.TestCase):

    def test_parse_simple_version(self):
        self.assertEqual(parse_simple_version("1.0.0"), (1, 0, 0))
        self.assertEqual(parse_simple_version("2.1"), (2, 1))
        self.assertEqual(parse_simple_version("3"), (3,))
        self.assertEqual(parse_simple_version("1.0.0rc1"), (1, 0, 0)) # Should ignore release candidates for simple comparison
        self.assertEqual(parse_simple_version("1.0.0.post1"), (1, 0, 0))
        self.assertEqual(parse_simple_version("invalid-version"), (0,))
        self.assertEqual(parse_simple_version(""), (0,))

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_parse_requirements_simple(self, mock_exists, mock_file):
        # Mock rationale: Simulate reading a requirements.txt file without actual file I/O.
        mock_file.return_value.read.return_value = "requests==2.28.1\nrich\n# comment\n\nflask>=2.0.0\nmy-package" # my-package is just a name
        
        deps = parse_requirements("dummy/path/requirements.txt")
        self.assertEqual(len(deps), 4)
        self.assertIn({'name': 'requests', 'pinned_version': '2.28.1'}, deps)
        self.assertIn({'name': 'rich', 'pinned_version': None}, deps)
        self.assertIn({'name': 'flask', 'pinned_version': None}, deps) # >= is not a strict pin for this utility
        self.assertIn({'name': 'my-package', 'pinned_version': None}, deps)

    @patch('os.path.exists', return_value=False)
    def test_parse_requirements_no_file(self, mock_exists):
        # Mock rationale: Simulate a missing requirements.txt file.
        deps = parse_requirements("nonexistent/path/requirements.txt")
        self.assertEqual(len(deps), 0)

    @patch('requests.get')
    def test_get_latest_pypi_version_success(self, mock_get):
        # Mock rationale: Prevent actual network calls to PyPI, ensuring deterministic and offline tests.
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"info": {"version": "3.0.0"}}
        mock_response.raise_for_status.return_value = None # Ensure no HTTPError is raised
        mock_get.return_value = mock_response

        version = get_latest_pypi_version("some-package")
        self.assertEqual(version, "3.0.0")
        mock_get.assert_called_once_with("https://pypi.org/pypi/some-package/json", timeout=5)

    @patch('requests.get')
    def test_get_latest_pypi_version_not_found(self, mock_get):
        # Mock rationale: Simulate a package not found on PyPI (404 response).
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found")
        mock_get.return_value = mock_response

        version = get_latest_pypi_version("nonexistent-package")
        self.assertIsNone(version)

    @patch('requests.get')
    def test_get_latest_pypi_version_network_error(self, mock_get):
        # Mock rationale: Simulate a network connectivity issue or timeout.
        mock_get.side_effect = requests.exceptions.RequestException("Connection refused")

        version = get_latest_pypi_version("any-package")
        self.assertIsNone(version)

    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_stabilize_dependencies_updates_available(self, mock_exists, mock_file, mock_get):
        # Mock rationale: Simulate both file I/O and network requests for a full scenario.
        # This allows testing the core logic without external dependencies.
        mock_file.return_value.read.return_value = "requests==2.28.1\nflask==1.1.0\nrich"

        # Mock PyPI responses for requests, flask, and rich
        def mock_get_side_effect(url, **kwargs):
            mock_resp = unittest.mock.Mock()
            mock_resp.raise_for_status.return_value = None
            if "requests" in url:
                mock_resp.json.return_value = {"info": {"version": "2.29.0"}} # Newer version
            elif "flask" in url:
                mock_resp.json.return_value = {"info": {"version": "1.1.0"}} # Same version
            elif "rich" in url:
                mock_resp.json.return_value = {"info": {"version": "13.7.0"}} # Not pinned, just latest
            else:
                mock_resp.json.return_value = {"info": {"version": "0.0.0"}} # Default for unexpected
            return mock_resp
        
        mock_get.side_effect = mock_get_side_effect

        report = stabilize_dependencies("/mock/project")
        self.assertEqual(len(report), 3)
        
        requests_report = next(item for item in report if item['package'] == 'requests')
        self.assertEqual(requests_report['status'], 'UPDATE_AVAILABLE')
        self.assertEqual(requests_report['current_version'], '2.28.1')
        self.assertEqual(requests_report['latest_version'], '2.29.0')

        flask_report = next(item for item in report if item['package'] == 'flask')
        self.assertEqual(flask_report['status'], 'UP_TO_DATE')
        self.assertEqual(flask_report['current_version'], '1.1.0')
        self.assertEqual(flask_report['latest_version'], '1.1.0')

        rich_report = next(item for item in report if item['package'] == 'rich')
        self.assertEqual(rich_report['status'], 'LATEST_REPORTED')
        self.assertEqual(rich_report['current_version'], 'N/A (not pinned)')
        self.assertEqual(rich_report['latest_version'], '13.7.0')

    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_stabilize_dependencies_no_updates(self, mock_exists, mock_file, mock_get):
        # Mock rationale: Simulate a scenario where all dependencies are up-to-date or not pinned.
        mock_file.return_value.read.return_value = "requests==2.29.0\nflask"

        def mock_get_side_effect(url, **kwargs):
            mock_resp = unittest.mock.Mock()
            mock_resp.raise_for_status.return_value = None
            if "requests" in url:
                mock_resp.json.return_value = {"info": {"version": "2.29.0"}}
            elif "flask" in url:
                mock_resp.json.return_value = {"info": {"version": "2.0.0"}} # Not pinned, just latest
            return mock_resp
        
        mock_get.side_effect = mock_get_side_effect

        report = stabilize_dependencies("/mock/project")
        self.assertEqual(len(report), 2)
        
        requests_report = next(item for item in report if item['package'] == 'requests')
        self.assertEqual(requests_report['status'], 'UP_TO_DATE')

        flask_report = next(item for item in report if item['package'] == 'flask')
        self.assertEqual(flask_report['status'], 'LATEST_REPORTED') # Not pinned, so just reports latest

    @patch('os.path.exists', return_value=False)
    def test_stabilize_dependencies_no_requirements_file(self, mock_exists):
        # Mock rationale: Simulate the absence of a requirements.txt file.
        report = stabilize_dependencies("/mock/project")
        self.assertEqual(len(report), 0)

    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_stabilize_dependencies_pypi_unavailable_for_one(self, mock_exists, mock_file, mock_get):
        # Mock rationale: Simulate PyPI being unreachable for one package.
        mock_file.return_value.read.return_value = "requests==2.28.1\nnonexistent-package"

        def mock_get_side_effect(url, **kwargs):
            mock_resp = unittest.mock.Mock()
            if "requests" in url:
                mock_resp.json.return_value = {"info": {"version": "2.29.0"}}
                mock_resp.raise_for_status.return_value = None
            elif "nonexistent-package" in url:
                mock_resp.status_code = 404
                mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found")
            return mock_resp
        
        mock_get.side_effect = mock_get_side_effect

        report = stabilize_dependencies("/mock/project")
        self.assertEqual(len(report), 2)
        self.assertEqual(next(item for item in report if item['package'] == 'requests')['status'], 'UPDATE_AVAILABLE')
        self.assertEqual(next(item for item in report if item['package'] == 'nonexistent-package')['status'], 'UNAVAILABLE')

    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_stabilize_dependencies_empty_requirements(self, mock_exists, mock_file, mock_get):
        # Mock rationale: Simulate an empty or comment-only requirements.txt file.
        mock_file.return_value.read.return_value = "# This is a comment\n\n"
        report = stabilize_dependencies("/mock/project")
        self.assertEqual(len(report), 0)
