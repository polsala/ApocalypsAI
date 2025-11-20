import unittest
import os
import sys
from unittest.mock import patch, mock_open, MagicMock

# Add the src directory to the path to allow importing scavenger.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import scavenger

class TestScavenger(unittest.TestCase):

    def test_find_urls_in_file_basic(self):
        # Mock rationale: Simulate reading a file with URLs without actual file I/O.
        mock_file_content = "This is a test file with a link: https://example.com/page1 and another http://test.org/path."
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as mock_file:
            urls = scavenger.find_urls_in_file("dummy.txt")
            self.assertIn("https://example.com/page1", urls)
            self.assertIn("http://test.org/path", urls)
            self.assertEqual(len(urls), 2)
            mock_file.assert_called_once_with("dummy.txt", 'r', encoding='utf-8', errors='ignore')

    def test_find_urls_in_file_no_urls(self):
        # Mock rationale: Simulate reading a file with no URLs.
        mock_file_content = "No links here, just plain text."
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            urls = scavenger.find_urls_in_file("dummy.txt")
            self.assertEqual(len(urls), 0)

    def test_find_urls_in_file_malformed_urls(self):
        # Mock rationale: Ensure only valid HTTP/HTTPS URLs are captured.
        mock_file_content = "ftp://bad.com and just.a.domain.com and https://good.com/path"
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            urls = scavenger.find_urls_in_file("dummy.txt")
            self.assertIn("https://good.com/path", urls)
            self.assertEqual(len(urls), 1)

    @patch('requests.get')
    def test_check_url_ok(self, mock_get):
        # Mock rationale: Simulate a successful HTTP request without actual network access.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        is_ok, status_msg = scavenger.check_url("https://good.com")
        self.assertTrue(is_ok)
        self.assertEqual(status_msg, "OK")
        mock_get.assert_called_once_with("https://good.com", timeout=5, allow_redirects=True)

    @patch('requests.get')
    def test_check_url_not_found(self, mock_get):
        # Mock rationale: Simulate a 404 Not Found HTTP response.
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        is_ok, status_msg = scavenger.check_url("https://bad.com/404")
        self.assertFalse(is_ok)
        self.assertEqual(status_msg, "Status: 404")

    @patch('requests.get')
    def test_check_url_connection_error(self, mock_get):
        # Mock rationale: Simulate a network connection error.
        mock_get.side_effect = requests.exceptions.ConnectionError

        is_ok, status_msg = scavenger.check_url("https://unreachable.com")
        self.assertFalse(is_ok)
        self.assertEqual(status_msg, "Error: ConnectionError")

    @patch('requests.get')
    def test_check_url_timeout(self, mock_get):
        # Mock rationale: Simulate a request timeout.
        mock_get.side_effect = requests.exceptions.Timeout

        is_ok, status_msg = scavenger.check_url("https://slow.com")
        self.assertFalse(is_ok)
        self.assertEqual(status_msg, "Error: Timeout")

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('scavenger.check_url')
    @patch('sys.stdout', new_callable=MagicMock) # Mock stdout to capture prints
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during test
    def test_main_no_broken_links(self, mock_exit, mock_stdout, mock_check_url, mock_open_file, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure and file content, and control URL check outcomes.
        # This allows testing the main logic without actual file system or network interaction.
        mock_walk.return_value = [
            ('/tmp/test_dir', [], ['file1.md', 'file2.py'])
        ]
        
        # Mock file content for file1.md and file2.py
        mock_open_file.side_effect = [
            mock_open(read_data="Link: https://good.com/page1").return_value,
            mock_open(read_data="Another link: https://good.com/page2").return_value
        ]

        # Mock check_url to always return OK
        mock_check_url.side_effect = [
            (True, "OK"), # for https://good.com/page1
            (True, "OK")  # for https://good.com/page2
        ]

        # Simulate command line arguments
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/tmp/test_dir', file_extensions='md,py', timeout=5)):
            scavenger.main()
            mock_exit.assert_called_once_with(0) # Expect successful exit
            output = mock_stdout.getvalue()
            self.assertIn("No broken links found. All systems nominal!", output)
            self.assertIn("Checking URL: https://good.com/page1 (OK)", output)
            self.assertIn("Checking URL: https://good.com/page2 (OK)", output)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('scavenger.check_url')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_main_with_broken_links(self, mock_exit, mock_stdout, mock_check_url, mock_open_file, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure and file content, and control URL check outcomes
        # to include broken links. This tests the reporting and error exit behavior.
        mock_walk.return_value = [
            ('/tmp/test_dir', [], ['doc.md', 'config.json'])
        ]

        # Mock file content
        mock_open_file.side_effect = [
            mock_open(read_data="Docs link: https://good.com/page1 and https://broken.com/page").return_value,
            mock_open(read_data="Config API: https://api.example.com/v1 and https://broken.com/page").return_value # Same broken link
        ]

        # Mock check_url to return one broken link (https://broken.com/page)
        # The order of side_effect corresponds to the order unique URLs are processed.
        mock_check_url.side_effect = [
            (True, "OK"), # for https://api.example.com/v1
            (False, "Status: 404"), # for https://broken.com/page
            (True, "OK") # for https://good.com/page1
        ]

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/tmp/test_dir', file_extensions='md,json', timeout=5)):
            scavenger.main()
            mock_exit.assert_called_once_with(1) # Expect exit with error code 1
            output = mock_stdout.getvalue()
            self.assertIn("--- Broken Links Report ---", output)
            self.assertIn("https://broken.com/page (Source: /tmp/test_dir/doc.md) (Status: Status: 404)", output)
            self.assertIn("https://broken.com/page (Source: /tmp/test_dir/config.json) (Status: Status: 404)", output)
            self.assertIn("Scan complete. Found 2 broken links.", output) # 2 entries in report because found in 2 files
            self.assertIn("Checking URL: https://broken.com/page (Status: 404)", output)

    @patch('os.path.isdir', return_value=False)
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_exit, mock_stdout, mock_isdir):
        # Mock rationale: Test the error handling for an invalid directory path.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/nonexistent', file_extensions='md', timeout=5)):
            scavenger.main()
            mock_exit.assert_called_once_with(1)
            self.assertIn("Error: Directory '/nonexistent' not found.", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
