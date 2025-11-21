import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
from io import StringIO

# Add the src directory to the path to allow importing echo_locator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import echo_locator

class TestEchoLocator(unittest.TestCase):

    def test_find_urls_in_text(self):
        text = "Visit https://example.com and also http://test.org/path?q=1. Another one: https://sub.domain.net/file.pdf. No URL here."
        expected_urls = [
            "http://test.org/path?q=1",
            "https://example.com",
            "https://sub.domain.net/file.pdf"
        ]
        self.assertEqual(echo_locator.find_urls_in_text(text), expected_urls)

        text_no_urls = "This text has no URLs."
        self.assertEqual(echo_locator.find_urls_in_text(text_no_urls), [])

        text_duplicate_urls = "https://example.com and https://example.com again."
        self.assertEqual(echo_locator.find_urls_in_text(text_duplicate_urls), ["https://example.com"])

    @patch('requests.head')
    @patch('requests.get')
    def test_check_url_success(self, mock_get, mock_head):
        # Mock rationale: `requests.head` and `requests.get` perform network requests.
        # We need to mock them to ensure tests are deterministic and offline.
        mock_head.return_value.status_code = 200
        mock_head.return_value.raise_for_status.return_value = None
        
        is_reachable, status_code = echo_locator.check_url("https://good.com")
        self.assertTrue(is_reachable)
        self.assertEqual(status_code, 200)
        mock_head.assert_called_once_with("https://good.com", timeout=5, allow_redirects=True)
        mock_get.assert_not_called()

    @patch('requests.head')
    @patch('requests.get')
    def test_check_url_broken_head_then_get_success(self, mock_get, mock_head):
        # Mock rationale: Simulating a server that doesn't allow HEAD but allows GET.
        mock_head.return_value.status_code = 405 # Method Not Allowed
        mock_get.return_value.status_code = 200
        mock_get.return_value.raise_for_status.return_value = None

        is_reachable, status_code = echo_locator.check_url("https://head-fail-get-ok.com")
        self.assertTrue(is_reachable)
        self.assertEqual(status_code, 200)
        mock_head.assert_called_once()
        mock_get.assert_called_once_with("https://head-fail-get-ok.com", timeout=5, allow_redirects=True)

    @patch('requests.head')
    @patch('requests.get')
    def test_check_url_broken_head_then_get_fail(self, mock_get, mock_head):
        # Mock rationale: Simulating a server that doesn't allow HEAD and GET also fails.
        mock_head.return_value.status_code = 405 # Method Not Allowed
        mock_get.return_value.status_code = 404 # Not Found

        is_reachable, status_code = echo_locator.check_url("https://head-fail-get-fail.com")
        self.assertFalse(is_reachable)
        self.assertEqual(status_code, 404)
        mock_head.assert_called_once()
        mock_get.assert_called_once_with("https://head-fail-get-fail.com", timeout=5, allow_redirects=True)

    @patch('requests.head')
    @patch('requests.get')
    def test_check_url_broken_status(self, mock_get, mock_head):
        # Mock rationale: Simulating a server returning a non-2xx status code.
        mock_head.return_value.status_code = 404
        
        is_reachable, status_code = echo_locator.check_url("https://broken.com")
        self.assertFalse(is_reachable)
        self.assertEqual(status_code, 404)
        mock_head.assert_called_once()
        mock_get.assert_not_called()

    @patch('requests.head', side_effect=requests.exceptions.Timeout)
    @patch('requests.get')
    def test_check_url_timeout(self, mock_get, mock_head):
        # Mock rationale: Simulating a network timeout during the request.
        is_reachable, status_code = echo_locator.check_url("https://timeout.com")
        self.assertFalse(is_reachable)
        self.assertEqual(status_code, 408) # Request Timeout
        mock_head.assert_called_once()
        mock_get.assert_not_called()

    @patch('requests.head', side_effect=requests.exceptions.ConnectionError)
    @patch('requests.get')
    def test_check_url_connection_error(self, mock_get, mock_head):
        # Mock rationale: Simulating a network connection error.
        is_reachable, status_code = echo_locator.check_url("https://no-connection.com")
        self.assertFalse(is_reachable)
        self.assertEqual(status_code, 503) # Service Unavailable (or similar network issue)
        mock_head.assert_called_once()
        mock_get.assert_not_called()

    @patch('builtins.open', new_callable=mock_open, read_data="Link: https://ok.com\nBroken: https://bad.com")
    @patch('echo_locator.check_url')
    def test_scan_file(self, mock_check_url, mock_file_open):
        # Mock rationale: `builtins.open` for file I/O and `echo_locator.check_url` for network calls.
        # This ensures file content is controlled and network calls are simulated.
        mock_check_url.side_effect = [
            (True, 200),  # For https://ok.com
            (False, 404) # For https://bad.com
        ]

        broken_links = echo_locator.scan_file("dummy.md")
        self.assertEqual(len(broken_links), 1)
        self.assertEqual(broken_links[0], ("https://bad.com", 404))
        mock_file_open.assert_called_once_with("dummy.md", 'r', encoding='utf-8', errors='ignore')
        self.assertEqual(mock_check_url.call_count, 2)

    @patch('builtins.open', new_callable=mock_open, read_data="No links here.")
    @patch('echo_locator.check_url')
    def test_scan_file_no_urls(self, mock_check_url, mock_file_open):
        # Mock rationale: `builtins.open` for file I/O.
        broken_links = echo_locator.scan_file("no_urls.txt")
        self.assertEqual(len(broken_links), 0)
        mock_file_open.assert_called_once()
        mock_check_url.assert_not_called()

    @patch('os.path.isfile', return_value=True)
    @patch('os.path.isdir', return_value=False)
    @patch('echo_locator.scan_file', return_value=[("https://broken.com", 404)])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_single_file_broken_link(self, mock_exit, mock_stdout, mock_scan_file, mock_isdir, mock_isfile):
        # Mock rationale: `os.path.isfile` and `os.path.isdir` for file system checks.
        # `echo_locator.scan_file` to simulate file scanning results.
        # `sys.stdout` to capture printed output.
        # `sys.exit` to prevent actual program termination during test.
        test_args = ['echo_locator.py', '--path', 'test.md']
        with patch('sys.argv', test_args):
            echo_locator.main()
            output = mock_stdout.getvalue()
            self.assertIn("[BROKEN] https://broken.com (Status: 404)", output)
            self.assertIn("Found 1 broken links.", output)
            mock_scan_file.assert_called_once_with('test.md', 5, False)
            mock_exit.assert_called_once_with(1)

    @patch('os.path.isfile', return_value=True)
    @patch('os.path.isdir', return_value=False)
    @patch('echo_locator.scan_file', return_value=[])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_single_file_no_broken_link(self, mock_exit, mock_stdout, mock_scan_file, mock_isdir, mock_isfile):
        # Mock rationale: Same as above, but simulating no broken links.
        test_args = ['echo_locator.py', '--path', 'test.md']
        with patch('sys.argv', test_args):
            echo_locator.main()
            output = mock_stdout.getvalue()
            self.assertIn("All digital echoes are strong! No broken links found.", output)
            mock_scan_file.assert_called_once_with('test.md', 5, False)
            mock_exit.assert_called_once_with(0)

    @patch('os.path.isfile', return_value=False)
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('echo_locator.scan_file', side_effect=[[], [("https://broken-dir.com", 404)]])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_directory_scan(self, mock_exit, mock_stdout, mock_scan_file, mock_walk, mock_isdir, mock_isfile):
        # Mock rationale: `os.walk` to simulate directory structure.
        # `echo_locator.scan_file` to simulate scanning multiple files.
        mock_walk.return_value = [
            ('/tmp/test_dir', [], ['file1.md', 'file2.py'])
        ]
        test_args = ['echo_locator.py', '--path', '/tmp/test_dir', '--extensions', 'md,py']
        with patch('sys.argv', test_args):
            echo_locator.main()
            output = mock_stdout.getvalue()
            self.assertIn("[BROKEN] https://broken-dir.com (Status: 404)", output)
            self.assertIn("Found 1 broken links.", output)
            self.assertEqual(mock_scan_file.call_count, 2)
            mock_scan_file.assert_any_call(os.path.join('/tmp/test_dir', 'file1.md'), 5, False)
            mock_scan_file.assert_any_call(os.path.join('/tmp/test_dir', 'file2.py'), 5, False)
            mock_exit.assert_called_once_with(1)

    @patch('os.path.isfile', return_value=False)
    @patch('os.path.isdir', return_value=False)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_exit, mock_stdout, mock_isdir, mock_isfile):
        # Mock rationale: Simulating an invalid path input.
        test_args = ['echo_locator.py', '--path', '/nonexistent/path']
        with patch('sys.argv', test_args):
            echo_locator.main()
            output = mock_stdout.getvalue()
            self.assertIn("Error: Path '/nonexistent/path' does not exist or is not a valid file/directory.", output)
            mock_exit.assert_called_once_with(1)

    @patch('os.path.isfile', return_value=True)
    @patch('os.path.isdir', return_value=False)
    @patch('echo_locator.scan_file', return_value=[])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_verbose_output(self, mock_exit, mock_stdout, mock_scan_file, mock_isdir, mock_isfile):
        # Mock rationale: Testing verbose output.
        mock_scan_file.return_value = [] # No broken links for simplicity
        test_args = ['echo_locator.py', '--path', 'test.md', '--verbose']
        with patch('sys.argv', test_args):
            echo_locator.main()
            output = mock_stdout.getvalue()
            self.assertIn("Scanning file: test.md", output)
            self.assertIn("All digital echoes are strong! No broken links found.", output)
            mock_scan_file.assert_called_once_with('test.md', 5, True)
            mock_exit.assert_called_once_with(0)

if __name__ == '__main__':
    unittest.main()
