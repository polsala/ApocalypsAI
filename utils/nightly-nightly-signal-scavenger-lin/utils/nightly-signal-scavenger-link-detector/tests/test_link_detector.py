import unittest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO
import os
import requests # Import requests to access its exception types

# Add the src directory to the Python path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import link_detector

class MockResponse:
    """A mock class to simulate requests.Response objects."""
    def __init__(self, status_code, content=""):
        self.status_code = status_code
        self.content = content
        self.ok = status_code >= 200 and status_code < 400

    def raise_for_status(self):
        if not self.ok:
            raise requests.exceptions.HTTPError(f"HTTP Error: {self.status_code}")

class TestLinkDetector(unittest.TestCase):

    @patch('requests.get')
    def test_check_single_link_success(self, mock_get):
        # Mock rationale: Simulate a successful HTTP GET request (status 200 OK).
        mock_get.return_value = MockResponse(200)
        url = "http://example.com/good"
        result_url, status_code, message = link_detector._check_single_link(url)
        self.assertEqual(result_url, url)
        self.assertEqual(status_code, 200)
        self.assertEqual(message, "OK")
        mock_get.assert_called_once_with(url, timeout=5.0, allow_redirects=True)

    @patch('requests.get')
    def test_check_single_link_not_found(self, mock_get):
        # Mock rationale: Simulate an HTTP GET request resulting in a 404 Not Found error.
        mock_get.return_value = MockResponse(404)
        url = "http://example.com/bad"
        result_url, status_code, message = link_detector._check_single_link(url)
        self.assertEqual(result_url, url)
        self.assertEqual(status_code, 404)
        self.assertEqual(message, "Client/Server Error")

    @patch('requests.get')
    def test_check_single_link_timeout(self, mock_get):
        # Mock rationale: Simulate a network request timing out.
        mock_get.side_effect = requests.exceptions.Timeout
        url = "http://example.com/timeout"
        result_url, status_code, message = link_detector._check_single_link(url)
        self.assertEqual(result_url, url)
        self.assertEqual(status_code, 0)
        self.assertEqual(message, "Timeout")

    @patch('requests.get')
    def test_check_single_link_connection_error(self, mock_get):
        # Mock rationale: Simulate a network connection error (e.g., DNS failure, host unreachable).
        mock_get.side_effect = requests.exceptions.ConnectionError
        url = "http://example.com/no-connection"
        result_url, status_code, message = link_detector._check_single_link(url)
        self.assertEqual(result_url, url)
        self.assertEqual(status_code, 0)
        self.assertEqual(message, "Connection Error")

    @patch('requests.get')
    def test_check_links_multiple_urls(self, mock_get):
        # Mock rationale: Simulate checking multiple URLs with mixed results (success, 404, timeout).
        def mock_get_side_effect(url, **kwargs):
            if "good" in url:
                return MockResponse(200)
            elif "bad" in url:
                return MockResponse(404)
            elif "timeout" in url:
                raise requests.exceptions.Timeout
            return MockResponse(200) # Default for unexpected URLs

        mock_get.side_effect = mock_get_side_effect

        urls = ["http://example.com/good", "http://example.com/bad", "http://example.com/timeout"]
        results = link_detector.check_links(urls)

        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["url"], "http://example.com/good")
        self.assertEqual(results[0]["status_code"], 200)
        self.assertEqual(results[1]["url"], "http://example.com/bad")
        self.assertEqual(results[1]["status_code"], 404)
        self.assertEqual(results[2]["url"], "http://example.com/timeout")
        self.assertEqual(results[2]["status_code"], 0)
        self.assertEqual(results[2]["message"], "Timeout")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('requests.get')
    def test_main_from_file_success(self, mock_get, mock_open, mock_stderr, mock_stdout):
        # Mock rationale: Simulate reading URLs from a file and all links being reachable.
        mock_open.return_value.read.return_value = "http://example.com/good1\nhttp://example.com/good2\n"
        mock_get.return_value = MockResponse(200) # All links are good

        # Mock command-line arguments
        with patch('sys.argv', ['link_detector.py', 'test_file.txt']):
            with self.assertRaises(SystemExit) as cm:
                link_detector.main()
            self.assertEqual(cm.exception.code, 0) # Expect success exit code

        output = mock_stdout.getvalue()
        self.assertIn("Checking 2 URLs", output)
        self.assertIn("✅ REACHABLE | 200 | http://example.com/good1 (OK)", output)
        self.assertIn("✅ REACHABLE | 200 | http://example.com/good2 (OK)", output)
        self.assertNotIn("❌ UNREACHABLE", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('requests.get')
    def test_main_from_file_failure(self, mock_get, mock_open, mock_stderr, mock_stdout):
        # Mock rationale: Simulate reading URLs from a file with some unreachable links.
        mock_open.return_value.read.return_value = "http://example.com/good\nhttp://example.com/bad\n"
        def mock_get_side_effect(url, **kwargs):
            if "good" in url:
                return MockResponse(200)
            elif "bad" in url:
                return MockResponse(404)
            return MockResponse(200)

        mock_get.side_effect = mock_get_side_effect

        # Mock command-line arguments
        with patch('sys.argv', ['link_detector.py', 'test_file.txt']):
            with self.assertRaises(SystemExit) as cm:
                link_detector.main()
            self.assertEqual(cm.exception.code, 1) # Expect failure exit code

        output = mock_stdout.getvalue()
        self.assertIn("Checking 2 URLs", output)
        self.assertIn("✅ REACHABLE | 200 | http://example.com/good (OK)", output)
        self.assertIn("❌ UNREACHABLE | 404 | http://example.com/bad (Client/Server Error)", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.stdin', new_callable=StringIO)
    @patch('requests.get')
    def test_main_from_stdin_success(self, mock_get, mock_stdin, mock_stderr, mock_stdout):
        # Mock rationale: Simulate reading URLs from stdin and all links being reachable.
        mock_stdin.write("http://example.com/stdin_good1\nhttp://example.com/stdin_good2\n")
        mock_stdin.seek(0) # Reset stdin buffer to read from start
        mock_get.return_value = MockResponse(200)

        with patch('sys.argv', ['link_detector.py']): # No file argument
            with self.assertRaises(SystemExit) as cm:
                link_detector.main()
            self.assertEqual(cm.exception.code, 0)

        output = mock_stdout.getvalue()
        self.assertIn("Reading URLs from stdin", output)
        self.assertIn("✅ REACHABLE | 200 | http://example.com/stdin_good1 (OK)", output)
        self.assertIn("✅ REACHABLE | 200 | http://example.com/stdin_good2 (OK)", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_main_file_not_found(self, mock_open, mock_stderr, mock_stdout):
        # Mock rationale: Simulate the scenario where the specified input file does not exist.
        with patch('sys.argv', ['link_detector.py', 'non_existent_file.txt']):
            with self.assertRaises(SystemExit) as cm:
                link_detector.main()
            self.assertEqual(cm.exception.code, 1) # Expect failure exit code

        error_output = mock_stderr.getvalue()
        self.assertIn("Error: Input file 'non_existent_file.txt' not found.", error_output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.stdin', new_callable=StringIO)
    def test_main_no_urls_provided(self, mock_stdin, mock_stderr, mock_stdout):
        # Mock rationale: Simulate the scenario where no URLs are provided via file or stdin.
        mock_stdin.write("\n \n") # Empty lines
        mock_stdin.seek(0)

        with patch('sys.argv', ['link_detector.py']):
            with self.assertRaises(SystemExit) as cm:
                link_detector.main()
            self.assertEqual(cm.exception.code, 0) # Expect success (no dead links, just nothing to do)

        output = mock_stderr.getvalue()
        self.assertIn("No URLs provided to check.", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('requests.get')
    def test_main_custom_timeout(self, mock_get, mock_open, mock_stderr, mock_stdout):
        # Mock rationale: Test that the custom timeout argument is correctly passed to requests.get.
        mock_open.return_value.read.return_value = "http://example.com/timeout_test\n"
        mock_get.return_value = MockResponse(200)

        with patch('sys.argv', ['link_detector.py', 'test_file.txt', '--timeout', '10.0']):
            with self.assertRaises(SystemExit) as cm:
                link_detector.main()
            self.assertEqual(cm.exception.code, 0)

        mock_get.assert_called_once_with("http://example.com/timeout_test", timeout=10.0, allow_redirects=True)
