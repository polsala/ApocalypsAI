import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO
import requests

# Adjust path to import the module from src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import link_checker

class TestLinkChecker(unittest.TestCase):

    def test_extract_links_from_markdown(self):
        markdown_content = """
        # My Document

        This is a [link to Google](https://www.google.com).
        Another link: [GitHub](https://github.com/polsala/ApocalypsAI).
        A reference link:
        [Python Docs]: https://docs.python.org/3/
        And a bare URL: https://example.com/path/to/resource.html

        No link here.
        [Local link](/local/path) should not be extracted.
        ftp://ftp.example.com should not be extracted.
        """
        expected_links = [
            "https://www.google.com",
            "https://github.com/polsala/ApocalypsAI",
            "https://docs.python.org/3/",
            "https://example.com/path/to/resource.html"
        ]
        extracted = link_checker.extract_links_from_markdown(markdown_content)
        self.assertCountEqual(extracted, expected_links) # Use assertCountEqual for order-independent comparison

    @patch('requests.head')
    def test_check_link_success(self, mock_head):
        # Mock rationale: Simulate a successful HTTP HEAD request (status 200 OK)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.reason = "OK"
        mock_head.return_value = mock_response

        is_ok, message = link_checker.check_link("https://www.valid.com")
        self.assertTrue(is_ok)
        self.assertEqual(message, "OK")
        mock_head.assert_called_once_with("https://www.valid.com", timeout=10, headers=link_checker.HEADERS, allow_redirects=True)

    @patch('requests.head')
    def test_check_link_not_found(self, mock_head):
        # Mock rationale: Simulate an HTTP HEAD request resulting in a 404 Not Found error
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_head.return_value = mock_response

        is_ok, message = link_checker.check_link("https://www.notfound.com")
        self.assertFalse(is_ok)
        self.assertEqual(message, "Status: 404 Not Found")

    @patch('requests.head')
    def test_check_link_connection_error(self, mock_head):
        # Mock rationale: Simulate a network connection error during the HTTP HEAD request
        mock_head.side_effect = requests.exceptions.ConnectionError("Connection refused")

        is_ok, message = link_checker.check_link("https://www.error.com")
        self.assertFalse(is_ok)
        self.assertEqual(message, "Error: Connection refused/failed")

    @patch('requests.head')
    def test_check_link_timeout_error(self, mock_head):
        # Mock rationale: Simulate a timeout error during the HTTP HEAD request
        mock_head.side_effect = requests.exceptions.Timeout("Request timed out")

        is_ok, message = link_checker.check_link("https://www.timeout.com")
        self.assertFalse(is_ok)
        self.assertEqual(message, "Error: Timeout")

    @patch('builtins.open', new_callable=MagicMock)
    @patch('os.path.exists', return_value=True)
    @patch('link_checker.check_link')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_all_links_ok(self, mock_stderr, mock_stdout, mock_check_link, mock_exists, mock_open):
        # Mock rationale: Simulate file existence and content, and mock network calls for links.
        # This allows testing the main logic without actual file I/O or network requests.
        mock_open.return_value.__enter__.return_value.read.return_value = """
        [Valid Link](https://valid.com)
        """
        mock_check_link.return_value = (True, "OK") # All links are OK

        # Simulate command line arguments
        with patch('sys.argv', ['link_checker.py', 'test_file.md']):
            link_checker.main()

        self.assertIn("Scanning: test_file.md", mock_stdout.getvalue())
        self.assertIn("[✓] https://valid.com", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "") # No errors should be printed to stderr

    @patch('builtins.open', new_callable=MagicMock)
    @patch('os.path.exists', return_value=True)
    @patch('link_checker.check_link')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_some_links_broken(self, mock_stderr, mock_stdout, mock_check_link, mock_exists, mock_open):
        # Mock rationale: Simulate file existence and content, and mock network calls for links,
        # including a broken one, to test error reporting and exit code.
        mock_open.return_value.__enter__.return_value.read.return_value = """
        [Valid Link](https://valid.com)
        [Broken Link](https://broken.com)
        """
        # Configure check_link to return success for the first, failure for the second
        mock_check_link.side_effect = [(True, "OK"), (False, "Status: 404 Not Found")]

        # Simulate command line arguments and expect a SystemExit due to broken link
        with patch('sys.argv', ['link_checker.py', 'test_file.md']):
            with self.assertRaises(SystemExit) as cm:
                link_checker.main()
            self.assertEqual(cm.exception.code, 1) # Expect exit code 1 for failure

        output = mock_stdout.getvalue()
        self.assertIn("Scanning: test_file.md", output)
        self.assertIn("[✓] https://valid.com", output)
        self.assertIn("[✗] https://broken.com (Status: 404 Not Found)", output)
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('os.path.exists', return_value=False)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_file_not_found(self, mock_stderr, mock_stdout, mock_exists):
        # Mock rationale: Simulate a scenario where the input file does not exist,
        # to test the error handling for missing files.
        with patch('sys.argv', ['link_checker.py', 'non_existent_file.md']):
            with self.assertRaises(SystemExit) as cm:
                link_checker.main()
            self.assertEqual(cm.exception.code, 1)

        self.assertIn("Error: File not found: non_existent_file.md", mock_stderr.getvalue())
        self.assertEqual(mock_stdout.getvalue(), "")

    @patch('builtins.open', new_callable=MagicMock)
    @patch('os.path.exists', return_value=True)
    @patch('link_checker.extract_links_from_markdown', return_value=[])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_no_links_found(self, mock_stderr, mock_stdout, mock_extract_links, mock_exists, mock_open):
        # Mock rationale: Simulate a Markdown file with no external links,
        # to ensure the utility handles this case gracefully without errors.
        mock_open.return_value.__enter__.return_value.read.return_value = "No links here."

        with patch('sys.argv', ['link_checker.py', 'no_links.md']):
            link_checker.main()

        self.assertIn("Scanning: no_links.md", mock_stdout.getvalue())
        self.assertIn("  No external links found.", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "")

if __name__ == '__main__':
    unittest.main()
