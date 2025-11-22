import unittest
from unittest.mock import patch, mock_open
import os
import sys

# Add the src directory to the Python path to import scavenger.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import scavenger

class TestScavenger(unittest.TestCase):

    def test_extract_urls_from_markdown_basic(self):
        content = "This is a [link](https://example.com/page1) and another <https://example.org/page2>."
        urls = scavenger.extract_urls_from_markdown(content)
        self.assertIn("https://example.com/page1", urls)
        self.assertIn("https://example.org/page2", urls)
        self.assertEqual(len(urls), 2)

    def test_extract_urls_from_markdown_no_links(self):
        content = "No links here, just plain text."
        urls = scavenger.extract_urls_from_markdown(content)
        self.assertEqual(len(urls), 0)

    def test_extract_urls_from_markdown_multiple_same_link(self):
        content = "[Link1](https://example.com/same) and [Link2](https://example.com/same)."
        urls = scavenger.extract_urls_from_markdown(content)
        self.assertEqual(len(urls), 1)
        self.assertIn("https://example.com/same", urls)

    def test_extract_urls_from_markdown_mixed_content(self):
        content = "Text with [link1](http://a.com) and <https://b.org> and more text [link2](https://c.net)."
        urls = scavenger.extract_urls_from_markdown(content)
        self.assertIn("http://a.com", urls)
        self.assertIn("https://b.org", urls)
        self.assertIn("https://c.net", urls)
        self.assertEqual(len(urls), 3)

    @patch('requests.head')
    def test_check_url_success(self, mock_head):
        # Mock rationale: Simulate a successful HTTP HEAD request (200 OK).
        mock_head.return_value.status_code = 200
        mock_head.return_value.raise_for_status.return_value = None
        is_ok, status = scavenger.check_url("https://example.com")
        self.assertTrue(is_ok)
        self.assertEqual(status, 200)

    @patch('requests.head')
    def test_check_url_not_found(self, mock_head):
        # Mock rationale: Simulate a 404 Not Found HTTP HEAD request.
        mock_head.return_value.status_code = 404
        is_ok, status = scavenger.check_url("https://example.com/404")
        self.assertFalse(is_ok)
        self.assertEqual(status, 404)

    @patch('requests.head')
    def test_check_url_server_error(self, mock_head):
        # Mock rationale: Simulate a 500 Internal Server Error HTTP HEAD request.
        mock_head.return_value.status_code = 500
        is_ok, status = scavenger.check_url("https://example.com/500")
        self.assertFalse(is_ok)
        self.assertEqual(status, 500)

    @patch('requests.head', side_effect=requests.exceptions.ConnectionError)
    def test_check_url_connection_error(self, mock_head):
        # Mock rationale: Simulate a network connection error.
        is_ok, status = scavenger.check_url("https://broken-domain.invalid")
        self.assertFalse(is_ok)
        self.assertEqual(status, "ConnectionError")

    @patch('requests.head', side_effect=requests.exceptions.Timeout)
    def test_check_url_timeout(self, mock_head):
        # Mock rationale: Simulate a request timeout.
        is_ok, status = scavenger.check_url("https://slow-server.com")
        self.assertFalse(is_ok)
        self.assertEqual(status, "Timeout")

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('scavenger.check_url')
    def test_scan_directory_no_broken_links(self, mock_check_url, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory structure and all links being OK.
        mock_os_walk.return_value = [
            ('/mock/repo', ['dir1'], ['README.md']),
            ('/mock/repo/dir1', [], ['file.md'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data="[Good Link](https://good.com)").return_value,
            mock_open(read_data="<https://another-good.org>").return_value
        ]
        mock_check_url.return_value = (True, 200)

        report = scavenger.scan_directory('/mock/repo', [])
        self.assertEqual(len(report), 0)
        self.assertEqual(mock_check_url.call_count, 2)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('scavenger.check_url')
    def test_scan_directory_with_broken_links(self, mock_check_url, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory structure with some broken links.
        mock_os_walk.return_value = [
            ('/mock/repo', [], ['README.md'])
        ]
        mock_file_open.return_value = mock_open(read_data="[Good Link](https://good.com) [Bad Link](https://bad.com)").return_value

        # First call for good.com, second for bad.com
        mock_check_url.side_effect = [
            (True, 200),
            (False, 404) # Bad link
        ]

        report = scavenger.scan_directory('/mock/repo', [])
        self.assertEqual(len(report), 1)
        self.assertIn('README.md', report)
        self.assertEqual(len(report['README.md']), 1)
        self.assertEqual(report['README.md'][0], ('https://bad.com', 404))
        self.assertEqual(mock_check_url.call_count, 2)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('scavenger.check_url')
    def test_scan_directory_with_exclusions(self, mock_check_url, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory structure with excluded directories and files.
        mock_os_walk.return_value = [
            ('/mock/repo', ['node_modules', 'src', '.git'], ['README.md', 'package.md']),
            ('/mock/repo/src', [], ['another.md']),
            ('/mock/repo/node_modules', [], ['ignored.md'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data="[Link](https://good.com)").return_value, # For README.md
            mock_open(read_data="[Link](https://good.com)").return_value  # For another.md
        ]
        mock_check_url.return_value = (True, 200)

        # Exclude 'node_modules' directory and files containing 'package'
        report = scavenger.scan_directory('/mock/repo', ['node_modules', 'package'])

        # Only README.md and another.md should be processed. 'package.md' and 'ignored.md' should be skipped.
        self.assertEqual(len(report), 0) # Assuming no broken links in processed files
        self.assertEqual(mock_check_url.call_count, 2) # One for README.md, one for another.md

    @patch('sys.stdout')
    @patch('scavenger.scan_directory')
    def test_main_no_broken_links(self, mock_scan_directory, mock_stdout):
        # Mock rationale: Simulate main execution where no broken links are found.
        mock_scan_directory.return_value = {}
        with self.assertRaises(SystemExit) as cm:
            scavenger.main()
        self.assertEqual(cm.exception.code, 0)
        mock_stdout.write.assert_any_call("\nNo broken links found. Repository documentation is healthy!\n")

    @patch('sys.stdout')
    @patch('scavenger.scan_directory')
    def test_main_with_broken_links(self, mock_scan_directory, mock_stdout):
        # Mock rationale: Simulate main execution where broken links are found.
        mock_scan_directory.return_value = {
            'README.md': [('https://bad.com', 404)]
        }
        with self.assertRaises(SystemExit) as cm:
            scavenger.main()
        self.assertEqual(cm.exception.code, 1)
        mock_stdout.write.assert_any_call("\nFound broken links:\n")
        mock_stdout.write.assert_any_call("  - https://bad.com (Status: 404)\n")

if __name__ == '__main__':
    unittest.main()
