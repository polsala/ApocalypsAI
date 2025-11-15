import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os
import requests

# Add the src directory to the Python path for importing link_auditor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import link_auditor

class TestLinkAuditor(unittest.TestCase):

    def test_extract_links(self):
        markdown_content = """
        # My Project

        This is a link to [GitHub](https://github.com/user/repo).
        Another link: <https://example.com/docs>.
        A broken link: [Broken](http://bad.link/404).
        A duplicate link: [GitHub again](https://github.com/user/repo).
        No link here.
        Link with query params: [Query](https://example.com/search?q=test&page=1).
        Link with hash: [Hash](https://example.com/page#section).
        """
        expected_links = sorted([
            "https://github.com/user/repo",
            "https://example.com/docs",
            "http://bad.link/404",
            "https://example.com/search?q=test&page=1",
            "https://example.com/page#section"
        ])
        self.assertEqual(link_auditor.extract_links(markdown_content), expected_links)

    @patch('requests.get')
    def test_check_link_success(self, mock_get):
        # Mock rationale: Simulate a successful HTTP request (200 OK).
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.reason = "OK"
        mock_get.return_value = mock_response

        status, error = link_auditor.check_link("https://example.com/good")
        self.assertEqual(status, 200)
        self.assertIsNone(error)
        mock_get.assert_called_once_with("https://example.com/good", timeout=5, allow_redirects=True)

    @patch('requests.get')
    def test_check_link_404(self, mock_get):
        # Mock rationale: Simulate an HTTP 404 Not Found error.
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_get.return_value = mock_response

        status, error = link_auditor.check_link("https://example.com/bad")
        self.assertEqual(status, 404)
        self.assertEqual(error, "404 Not Found")

    @patch('requests.get')
    def test_check_link_connection_error(self, mock_get):
        # Mock rationale: Simulate a network connection error (e.g., DNS failure, host unreachable).
        mock_get.side_effect = requests.exceptions.ConnectionError("Failed to connect")

        status, error = link_auditor.check_link("https://nonexistent.domain")
        self.assertEqual(status, 0)
        self.assertEqual(error, "Connection failed")

    @patch('requests.get')
    def test_check_link_timeout(self, mock_get):
        # Mock rationale: Simulate a request timeout.
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

        status, error = link_auditor.check_link("https://slow.server")
        self.assertEqual(status, 0)
        self.assertEqual(error, "Timeout")

    @patch('builtins.open', new_callable=mock_open)
    @patch('link_auditor.check_link')
    def test_audit_readme_full_flow(self, mock_check_link, mock_file_open):
        # Mock rationale: Simulate reading a README file and the results of link checks.
        mock_file_open.return_value.read.return_value = """
        [Good Link](https://good.com)
        <https://bad.com/404>
        [Unreachable Link](https://unreachable.com)
        """

        # Configure mock_check_link to return different results for different URLs
        def mock_check_link_side_effect(url):
            if url == "https://good.com":
                return 200, None
            elif url == "https://bad.com/404":
                return 404, "404 Not Found"
            elif url == "https://unreachable.com":
                # Simulate a ConnectionError directly from check_link
                return 0, "Connection failed"
            return 0, "Unexpected URL" # Should not happen with these inputs

        mock_check_link.side_effect = mock_check_link_side_effect

        results = link_auditor.audit_readme("dummy_readme.md")

        self.assertEqual(len(results["valid"]), 1)
        self.assertEqual(results["valid"][0][0], "https://good.com")
        self.assertEqual(results["valid"][0][1], 200)

        self.assertEqual(len(results["broken"]), 1)
        self.assertEqual(results["broken"][0][0], "https://bad.com/404")
        self.assertEqual(results["broken"][0][1], 404)
        self.assertEqual(results["broken"][0][2], "404 Not Found")

        self.assertEqual(len(results["unreachable"]), 1)
        self.assertEqual(results["unreachable"][0][0], "https://unreachable.com")
        self.assertEqual(results["unreachable"][0][1], 0)
        self.assertEqual(results["unreachable"][0][2], "Connection failed")

    @patch('builtins.open', new_callable=mock_open)
    @patch('link_auditor.check_link')
    def test_audit_readme_no_links(self, mock_check_link, mock_file_open):
        # Mock rationale: Simulate a README file with no links.
        mock_file_open.return_value.read.return_value = "Just some plain text."
        
        results = link_auditor.audit_readme("dummy_readme.md")
        
        self.assertEqual(len(results["valid"]), 0)
        self.assertEqual(len(results["broken"]), 0)
        self.assertEqual(len(results["unreachable"]), 0)
        mock_check_link.assert_not_called() # No links, so no checks should be made

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_audit_readme_file_not_found(self, mock_file_open):
        # Mock rationale: Simulate the scenario where the README file does not exist.
        results = link_auditor.audit_readme("non_existent_file.md")
        self.assertEqual(results, {}) # Expect an empty dict on error

    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('link_auditor.audit_readme')
    def test_main_success(self, mock_audit_readme, mock_parse_args, mock_exit):
        # Mock rationale: Simulate a successful audit run via main(), expecting exit code 0.
        mock_parse_args.return_value.file = "test_readme.md"
        mock_audit_readme.return_value = {
            "valid": [("https://good.com", 200, None)],
            "broken": [],
            "unreachable": []
        }
        link_auditor.main()
        mock_exit.assert_called_once_with(0)

    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('link_auditor.audit_readme')
    def test_main_failure_broken_links(self, mock_audit_readme, mock_parse_args, mock_exit):
        # Mock rationale: Simulate an audit run with broken links, expecting exit code 1.
        mock_parse_args.return_value.file = "test_readme.md"
        mock_audit_readme.return_value = {
            "valid": [],
            "broken": [("https://bad.com", 404, "404 Not Found")],
            "unreachable": []
        }
        link_auditor.main()
        mock_exit.assert_called_once_with(1)

    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('link_auditor.audit_readme')
    def test_main_failure_unreachable_links(self, mock_audit_readme, mock_parse_args, mock_exit):
        # Mock rationale: Simulate an audit run with unreachable links, expecting exit code 1.
        mock_parse_args.return_value.file = "test_readme.md"
        mock_audit_readme.return_value = {
            "valid": [],
            "broken": [],
            "unreachable": [("https://unreachable.com", 0, "Connection failed")]
        }
        link_auditor.main()
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
