import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import requests
import sys
from src.link_checker import LinkChecker

class MockResponse:
    """A mock class for requests.Response objects."""
    def __init__(self, status_code, reason, url, content=b''):
        self.status_code = status_code
        self.reason = reason
        self.url = url # Final URL after redirects
        self.content = content
        self.ok = 200 <= status_code < 400
        self.headers = {'Content-Type': 'text/html'}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def raise_for_status(self):
        if not self.ok:
            # Create a mock response object for HTTPError to reference
            mock_http_error_response = MagicMock()
            mock_http_error_response.status_code = self.status_code
            mock_http_error_response.reason = self.reason
            raise requests.exceptions.HTTPError(f"{self.status_code} {self.reason}", response=mock_http_error_response)

class TestLinkChecker(unittest.TestCase):

    def setUp(self):
        self.checker = LinkChecker(timeout=1)

    def test_extract_links_from_markdown(self):
        markdown_content = """
# My Document

This is a [link to Google](https://www.google.com).
Another link: [GitHub](http://github.com/polsala/ApocalypsAI).
No link here.
[Relative link](/path/to/local).
[Malformed link](ftp://example.com/file.txt).
[Link with query](https://example.com/search?q=test&param=value).
[Link with hash](https://example.com/page#section).
"""
        expected_links = [
            "https://www.google.com",
            "http://github.com/polsala/ApocalypsAI",
            "https://example.com/search?q=test&param=value",
            "https://example.com/page#section"
        ]
        extracted = self.checker.extract_links_from_markdown(markdown_content)
        self.assertCountEqual(extracted, expected_links)

    @patch('requests.get')
    def test_check_link_status_success(self, mock_get):
        # Mock rationale: Simulate a successful HTTP request (200 OK).
        mock_get.return_value = MockResponse(200, 'OK', 'https://example.com/success')
        status, final_url = self.checker.check_link_status('https://example.com/success')
        self.assertEqual(status, '200 OK')
        self.assertEqual(final_url, 'https://example.com/success')
        mock_get.assert_called_once_with('https://example.com/success', timeout=1, stream=True, allow_redirects=True)

    @patch('requests.get')
    def test_check_link_status_not_found(self, mock_get):
        # Mock rationale: Simulate a 404 Not Found error.
        mock_get.return_value = MockResponse(404, 'Not Found', 'https://example.com/404')
        status, final_url = self.checker.check_link_status('https://example.com/404')
        self.assertEqual(status, '404 Not Found')
        self.assertEqual(final_url, 'https://example.com/404')

    @patch('requests.get')
    def test_check_link_status_redirect(self, mock_get):
        # Mock rationale: Simulate a 301 redirect. requests handles the redirect internally,
        # so the mock_get should return the final status and URL after the redirect.
        mock_get.return_value = MockResponse(200, 'OK', 'https://new-site.com/page')
        status, final_url = self.checker.check_link_status('https://old-site.com/page')
        self.assertEqual(status, '200 OK') # The final status is 200 after redirect
        self.assertEqual(final_url, 'https://new-site.com/page')

    @patch('requests.get')
    def test_check_link_status_connection_error(self, mock_get):
        # Mock rationale: Simulate a network connection error.
        mock_get.side_effect = requests.exceptions.ConnectionError("DNS lookup failed")
        status, final_url = self.checker.check_link_status('https://nonexistent.com')
        self.assertEqual(status, 'Connection Error')
        self.assertEqual(final_url, 'https://nonexistent.com')

    @patch('requests.get')
    def test_check_link_status_timeout(self, mock_get):
        # Mock rationale: Simulate a request timeout.
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        status, final_url = self.checker.check_link_status('https://slow-site.com')
        self.assertEqual(status, 'Timeout Error')
        self.assertEqual(final_url, 'https://slow-site.com')

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('src.link_checker.LinkChecker.check_link_status')
    def test_run_scan_basic(self, mock_check_link_status, mock_stdout, mock_open_file, mock_os_walk):
        # Mock rationale: Simulate file system traversal and file content, and link status checks.
        # This allows testing the orchestration logic without actual file I/O or network requests.

        # Simulate directory structure
        mock_os_walk.return_value = [
            ('/repo', ('docs',), ('README.md',)),
            ('/repo/docs', (), ('CONTRIBUTING.md',))
        ]

        # Simulate file content
        mock_open_file.side_effect = [
            mock_open(read_data="[Google](https://www.google.com)\n[Broken](https://broken.com)").return_value,
            mock_open(read_data="[GitHub](https://github.com)\n[Error](https://error.com)").return_value
        ]

        # Simulate link statuses
        mock_check_link_status.side_effect = [
            ('200 OK', 'https://www.google.com'),
            ('404 Not Found', 'https://broken.com'),
            ('200 OK', 'https://github.com'),
            ('Connection Error', 'https://error.com')
        ]

        self.checker.run_scan('/repo')

        # Assertions for output (simplified, checking for key phrases)
        output = mock_stdout.getvalue()
        self.assertIn("Scanning directory: /repo", output)
        self.assertIn("--- Checking links in README.md ---", output)
        self.assertIn("[SUCCESS] https://www.google.com (200 OK)", output)
        self.assertIn("[BROKEN ] https://broken.com (404 Not Found)", output)
        self.assertIn("--- Checking links in docs/CONTRIBUTING.md ---", output)
        self.assertIn("[SUCCESS] https://github.com (200 OK)", output)
        self.assertIn("[ERROR  ] https://error.com (Connection Error)", output)
        self.assertIn("Scan complete. Found 1 broken link(s) and 1 error(s).", output)

        # Ensure files were opened and links checked
        self.assertEqual(mock_open_file.call_count, 2)
        self.assertEqual(mock_check_link_status.call_count, 4)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('src.link_checker.LinkChecker.check_link_status')
    def test_run_scan_no_links(self, mock_check_link_status, mock_stdout, mock_open_file, mock_os_walk):
        # Mock rationale: Simulate a markdown file with no external links.
        mock_os_walk.return_value = [
            ('/repo', (), ('README.md',))
        ]
        mock_open_file.return_value = mock_open(read_data="# No Links Here\nThis document has no external links.").return_value

        self.checker.run_scan('/repo')

        output = mock_stdout.getvalue()
        self.assertIn("No external links found.", output)
        self.assertIn("Scan complete. Found 0 broken link(s) and 0 error(s).", output)
        mock_check_link_status.assert_not_called()

    @patch('os.walk')
    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_run_scan_file_not_found(self, mock_stdout, mock_open_file, mock_os_walk):
        # Mock rationale: Simulate a scenario where os.walk finds a file, but open() fails.
        mock_os_walk.return_value = [
            ('/repo', (), ('MISSING.md',))
        ]

        self.checker.run_scan('/repo')

        output = mock_stdout.getvalue()
        self.assertIn("Error: File not found: MISSING.md", output)
        self.assertIn("Scan complete. Found 0 broken link(s) and 0 error(s).", output)

    @patch('os.walk', return_value=[])
    @patch('sys.stdout', new_callable=MagicMock)
    def test_run_scan_no_markdown_files(self, mock_stdout, mock_os_walk):
        # Mock rationale: Simulate a directory with no markdown files.
        self.checker.run_scan('/empty_repo')
        output = mock_stdout.getvalue()
        self.assertIn("No markdown files found in the specified directory.", output)
        self.assertNotIn("Scan complete.", output) # Should exit early


if __name__ == '__main__':
    unittest.main()
