import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
import requests

# Add the src directory to the path to allow importing scavenger.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import scavenger

class TestScavenger(unittest.TestCase):

    @patch('scavenger.requests.head')
    @patch('scavenger.requests.get')
    def test_check_url_success(self, mock_get, mock_head):
        # Mock rationale: Simulate a successful HTTP HEAD request to a URL.
        mock_head.return_value = MagicMock(status_code=200, reason='OK')
        is_reachable, status = scavenger.check_url("http://example.com/valid")
        self.assertTrue(is_reachable)
        self.assertEqual(status, "200 OK")
        mock_head.assert_called_once_with("http://example.com/valid", timeout=5, allow_redirects=True)
        mock_get.assert_not_called()

    @patch('scavenger.requests.head')
    @patch('scavenger.requests.get')
    def test_check_url_broken_404(self, mock_get, mock_head):
        # Mock rationale: Simulate a 404 Not Found response for a URL.
        mock_head.return_value = MagicMock(status_code=404, reason='Not Found')
        mock_get.return_value = MagicMock(status_code=404, reason='Not Found') # Fallback GET also fails
        is_reachable, status = scavenger.check_url("http://example.com/broken")
        self.assertFalse(is_reachable)
        self.assertEqual(status, "404 Not Found")
        mock_head.assert_called_once()
        mock_get.assert_called_once() # Should try GET after HEAD 4xx

    @patch('scavenger.requests.head')
    @patch('scavenger.requests.get')
    def test_check_url_connection_error(self, mock_get, mock_head):
        # Mock rationale: Simulate a network connection error when trying to reach a URL.
        mock_head.side_effect = requests.exceptions.ConnectionError("DNS lookup failed")
        is_reachable, status = scavenger.check_url("http://nonexistent.com")
        self.assertFalse(is_reachable)
        self.assertEqual(status, "Connection Error")
        mock_head.assert_called_once()
        mock_get.assert_not_called() # No GET if HEAD fails with connection error

    @patch('builtins.open', new_callable=mock_open)
    def test_find_urls_in_markdown_file(self, mock_file):
        # Mock rationale: Simulate reading a Markdown file with various link types.
        mock_file.return_value.read.return_value = (
            "# My Doc\n\n"
            "This is a [valid link](https://example.com/doc1).\n"
            "Another link: [GitHub](https://github.com/polsala/ApocalypsAI).\n"
            "No link here.\n"
            "A raw URL: https://www.python.org/downloads/\n"
            "[Broken link](http://bad.link/page.html)\n"
        )
        urls = scavenger.find_urls_in_file("test.md")
        expected_urls = [
            ("https://example.com/doc1", 3, "test.md"),
            ("https://github.com/polsala/ApocalypsAI", 4, "test.md"),
            ("https://www.python.org/downloads/", 6, "test.md"),
            ("http://bad.link/page.html", 7, "test.md"),
        ]
        self.assertEqual(len(urls), len(expected_urls))
        self.assertListEqual(sorted(urls), sorted(expected_urls))

    @patch('builtins.open', new_callable=mock_open)
    def test_find_urls_in_python_file(self, mock_file):
        # Mock rationale: Simulate reading a Python file with URLs in comments or strings.
        mock_file.return_value.read.return_value = (
            "import os # See docs at https://docs.python.org/3/library/os.html\n"
            "URL = 'https://api.example.com/v1'\n"
            "# Another comment with a link: [PEP 8](https://www.python.org/dev/peps/pep-0008/)\n"
            "def func():\n"
            "    pass\n"
        )
        urls = scavenger.find_urls_in_file("test.py")
        expected_urls = [
            ("https://docs.python.org/3/library/os.html", 1, "test.py"),
            ("https://api.example.com/v1", 2, "test.py"),
            ("https://www.python.org/dev/peps/pep-0008/", 3, "test.py"),
        ]
        self.assertEqual(len(urls), len(expected_urls))
        self.assertListEqual(sorted(urls), sorted(expected_urls))

    @patch('os.path.isfile', return_value=False)
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('scavenger.check_url', return_value=(True, '200 OK'))
    @patch('sys.stdout', new_callable=MagicMock) # Mock stdout to capture print calls
    def test_main_directory_scan(self, mock_stdout, mock_check_url, mock_file, mock_walk, mock_isdir, mock_isfile):
        # Mock rationale: Simulate directory traversal and file content reading for a full scan.
        # Mock os.walk to return a predefined directory structure.
        mock_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['file1.md', 'file2.py']),
            ('/root/dir1', [], ['subfile.txt']),
            ('/root/dir2', [], ['excluded.log'])
        ]
        # Mock file content for each file
        mock_file.side_effect = [
            mock_open(read_data='[Link1](http://link1.com)').return_value,
            mock_open(read_data='import sys # http://link2.com').return_value,
            mock_open(read_data='http://link3.com').return_value,
            mock_open(read_data='log content').return_value # For excluded.log, though it shouldn't be opened
        ]

        # Simulate command line arguments
        with patch('sys.argv', ['scavenger.py', '--path', '/root', '--exclude', '*.log']):
            scavenger.main()
        
        # Assert that check_url was called for expected links
        mock_check_url.assert_any_call('http://link1.com')
        mock_check_url.assert_any_call('http://link2.com')
        mock_check_url.assert_any_call('http://link3.com')
        self.assertEqual(mock_check_url.call_count, 3)

        # Assert that excluded.log was not processed (or its content not read for URLs)
        # We can also check stdout for specific messages
        output = mock_stdout.write.call_args_list
        output_str = "".join(call.args[0] for call in output)
        self.assertIn("Scanning: /root/file1.md", output_str)
        self.assertIn("Scanning: /root/dir1/subfile.txt", output_str)
        self.assertIn("Scanning: /root/file2.py", output_str)
        self.assertNotIn("Scanning: /root/dir2/excluded.log", output_str)
        self.assertIn("Scan complete. Found 0 broken links.", output_str)

    @patch('os.path.isfile', return_value=True)
    @patch('os.path.isdir', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    @patch('scavenger.check_url', return_value=(False, '404 Not Found'))
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_single_file_broken_link(self, mock_stdout, mock_check_url, mock_file, mock_isdir, mock_isfile):
        # Mock rationale: Simulate scanning a single file with a broken link.
        mock_file.return_value.read.return_value = "[Broken](http://broken.com/page)\n"

        with patch('sys.argv', ['scavenger.py', '--path', 'single.md']):
            scavenger.main()
        
        mock_check_url.assert_called_once_with('http://broken.com/page')
        output = mock_stdout.write.call_args_list
        output_str = "".join(call.args[0] for call in output)
        self.assertIn("Scanning: single.md", output_str)
        self.assertIn("[BROKEN] http://broken.com/page (404 Not Found) (Found in single.md:1)", output_str)
        self.assertIn("Scan complete. Found 1 broken links.", output_str)

    @patch('os.path.isfile', return_value=False)
    @patch('os.path.isdir', return_value=False)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_invalid_path(self, mock_stdout, mock_isdir, mock_isfile):
        # Mock rationale: Simulate providing an invalid path to the script.
        with patch('sys.argv', ['scavenger.py', '--path', 'nonexistent/path']):
            scavenger.main()
        
        output = mock_stdout.write.call_args_list
        output_str = "".join(call.args[0] for call in output)
        self.assertIn("Error: Path 'nonexistent/path' does not exist or is not a file/directory.", output_str)

if __name__ == '__main__':
    unittest.main()
