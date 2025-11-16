import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
from io import StringIO
import requests.exceptions

# Add the src directory to the path to allow importing scavenger
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from scavenger import find_urls_in_file, check_url, main

class TestScavenger(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_find_urls_in_file_no_urls(self, mock_file):
        # Mock rationale: Simulate a file with no URLs to test the regex and file reading.
        mock_file.return_value.read.return_value = "This is a test file with no URLs."
        urls = find_urls_in_file("dummy.txt")
        self.assertEqual(len(urls), 0)

    @patch('builtins.open', new_callable=mock_open)
    def test_find_urls_in_file_with_urls(self, mock_file):
        # Mock rationale: Simulate a file with multiple URLs on different lines.
        file_content = (
            "Line 1: https://example.com/page1\n"
            "Line 2: No URL here.\n"
            "Line 3: Another URL: http://test.org/path?q=1 and https://anothersite.net\n"
        )
        mock_file.return_value.read.return_value = file_content
        urls = find_urls_in_file("dummy.md")
        self.assertEqual(len(urls), 3)
        self.assertIn(('https://example.com/page1', 1, 'Line 1: https://example.com/page1'), urls)
        self.assertIn(('http://test.org/path?q=1', 3, 'Line 3: Another URL: http://test.org/path?q=1 and https://anothersite.net'), urls)
        self.assertIn(('https://anothersite.net', 3, 'Line 3: Another URL: http://test.org/path?q=1 and https://anothersite.net'), urls)

    @patch('requests.head')
    @patch('requests.get')
    def test_check_url_success(self, mock_get, mock_head):
        # Mock rationale: Simulate a successful HTTP HEAD request (status 200).
        mock_head.return_value = MagicMock(status_code=200, reason='OK')
        status, reason = check_url("https://valid.com")
        self.assertEqual(status, 200)
        self.assertEqual(reason, 'OK')
        mock_head.assert_called_once_with("https://valid.com", timeout=5, allow_redirects=True)
        mock_get.assert_not_called()

    @patch('requests.head')
    @patch('requests.get')
    def test_check_url_not_found(self, mock_get, mock_head):
        # Mock rationale: Simulate a 404 Not Found response from HTTP HEAD.
        mock_head.return_value = MagicMock(status_code=404, reason='Not Found')
        status, reason = check_url("https://broken.com/404")
        self.assertEqual(status, 404)
        self.assertEqual(reason, 'Not Found')
        mock_head.assert_called_once()
        mock_get.assert_not_called()

    @patch('requests.head')
    @patch('requests.get')
    def test_check_url_connection_error(self, mock_get, mock_head):
        # Mock rationale: Simulate a network connection error during the request.
        mock_head.side_effect = requests.exceptions.ConnectionError("Mock connection error")
        status, reason = check_url("https://error.com")
        self.assertEqual(status, 0)
        self.assertEqual(reason, 'Connection Error')
        mock_head.assert_called_once()
        mock_get.assert_not_called()

    @patch('requests.head')
    @patch('requests.get')
    def test_check_url_timeout(self, mock_get, mock_head):
        # Mock rationale: Simulate a request timeout.
        mock_head.side_effect = requests.exceptions.Timeout("Mock timeout")
        status, reason = check_url("https://timeout.com")
        self.assertEqual(status, 0)
        self.assertEqual(reason, 'Timeout')
        mock_head.assert_called_once()
        mock_get.assert_not_called()

    @patch('requests.head')
    @patch('requests.get')
    def test_check_url_head_not_allowed_fallback_to_get(self, mock_get, mock_head):
        # Mock rationale: Simulate a server that doesn't allow HEAD requests (405), forcing a GET fallback.
        mock_head.return_value = MagicMock(status_code=405, reason='Method Not Allowed')

        mock_get.return_value = MagicMock(status_code=200, reason='OK')
        mock_get.return_value.close = MagicMock() # Mock close method for stream=True

        status, reason = check_url("https://head-forbidden.com")
        self.assertEqual(status, 200)
        self.assertEqual(reason, 'OK')
        mock_head.assert_called_once()
        mock_get.assert_called_once_with("https://head-forbidden.com", timeout=5, allow_redirects=True, stream=True)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('requests.head')
    @patch('requests.get')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_broken_links(self, mock_stdout, mock_get, mock_head, mock_file, mock_walk):
        # Mock rationale: Simulate a file system with a valid file and all links working.
        mock_walk.return_value = [('./', [], ['test.md'])]
        mock_file.return_value.read.return_value = "Valid link: https://good.com"
        mock_head.return_value = MagicMock(status_code=200, reason='OK')

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        output = mock_stdout.getvalue()
        self.assertIn("No broken links found", output)
        self.assertIn("Found 1 URLs in 1 files.", output)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('requests.head')
    @patch('requests.get')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_broken_links(self, mock_stdout, mock_get, mock_head, mock_file, mock_walk):
        # Mock rationale: Simulate a file system with a file containing a broken link.
        mock_walk.return_value = [('./', [], ['test.md'])]
        mock_file.return_value.read.return_value = "Broken link: https://bad.com/404"

        # Configure mock_head to return 404 for 'https://bad.com/404'
        mock_head.return_value = MagicMock(status_code=404, reason='Not Found')

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        output = mock_stdout.getvalue()
        self.assertIn("Broken Links:", output)
        self.assertIn("[404 NOT FOUND] https://bad.com/404 (./test.md:1)", output)
        self.assertIn("1 broken links found.", output)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('requests.head')
    @patch('requests.get')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_multiple_files_and_urls(self, mock_stdout, mock_get, mock_head, mock_file, mock_walk):
        # Mock rationale: Simulate multiple files with a mix of good and bad links.
        mock_walk.return_value = [
            ('./', [], ['file1.md', 'file2.py']),
            ('./subdir', [], ['file3.md'])
        ]

        # Set up mock_open to return different content for different files
        def mock_open_side_effect(filepath, *args, **kwargs):
            if 'file1.md' in filepath:
                return mock_open(read_data="Good: https://good.com\nBad: https://bad.com/404").return_value
            elif 'file2.py' in filepath:
                return mock_open(read_data="Another good: https://another-good.com").return_value
            elif 'file3.md' in filepath:
                return mock_open(read_data="Error: https://error.com").return_value
            return mock_open().return_value
        mock_file.side_effect = mock_open_side_effect

        # Set up mock_head to return different statuses for different URLs
        def mock_head_side_effect(url, *args, **kwargs):
            mock_response = MagicMock()
            if "good.com" in url or "another-good.com" in url:
                mock_response.status_code = 200
                mock_response.reason = 'OK'
            elif "bad.com" in url:
                mock_response.status_code = 404
                mock_response.reason = 'Not Found'
            elif "error.com" in url:
                raise requests.exceptions.ConnectionError("Mock connection error")
            return mock_response
        mock_head.side_effect = mock_head_side_effect

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        output = mock_stdout.getvalue()
        self.assertIn("Found 4 URLs in 3 files.", output)
        self.assertIn("Broken Links:", output)
        self.assertIn("[404 NOT FOUND] https://bad.com/404 (./file1.md:2)", output)
        self.assertIn("[ERROR: Connection Error] https://error.com (./subdir/file3.md:1)", output)
        self.assertIn("2 broken links found.", output)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('requests.head')
    @patch('requests.get')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_unique_url_checking(self, mock_stdout, mock_get, mock_head, mock_file, mock_walk):
        # Mock rationale: Test that a URL appearing multiple times is only checked once via HTTP.
        mock_walk.return_value = [('./', [], ['test.md'])]
        mock_file.return_value.read.return_value = (
            "Link 1: https://unique.com/page\n"
            "Link 2: https://unique.com/page\n"
            "Link 3: https://another.com"
        )
        
        def mock_head_side_effect(url, *args, **kwargs):
            mock_response = MagicMock()
            if "unique.com" in url:
                mock_response.status_code = 404
                mock_response.reason = 'Not Found'
            elif "another.com" in url:
                mock_response.status_code = 200
                mock_response.reason = 'OK'
            return mock_response
        mock_head.side_effect = mock_head_side_effect

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        output = mock_stdout.getvalue()
        self.assertIn("Found 3 URLs in 1 files.", output)
        self.assertIn("[404 NOT FOUND] https://unique.com/page (./test.md:1)", output)
        self.assertIn("[404 NOT FOUND] https://unique.com/page (./test.md:2)", output)
        self.assertIn("2 broken links found.", output)
        # Ensure requests.head was called only once for each unique URL
        self.assertEqual(mock_head.call_count, 2) # Once for unique.com, once for another.com
        mock_head.assert_any_call("https://unique.com/page", timeout=5, allow_redirects=True)
        mock_head.assert_any_call("https://another.com", timeout=5, allow_redirects=True)
