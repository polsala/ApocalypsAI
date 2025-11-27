import unittest
import os
from unittest.mock import patch, mock_open
from utils.nightly-broken-link-beacon.src.link_checker import (
    find_markdown_files,
    extract_urls_from_markdown,
    check_url_reachability
)

class TestLinkChecker(unittest.TestCase):

    @patch('os.walk')
    def test_find_markdown_files(self, mock_os_walk):
        # Mock rationale: Simulate file system structure without actual disk I/O.
        mock_os_walk.return_value = [
            ('/repo', ['docs', 'src'], ['README.md', 'LICENSE']),
            ('/repo/docs', [], ['CONTRIBUTING.md', 'image.png']),
            ('/repo/src', [], ['main.py'])
        ]
        
        files = find_markdown_files('/repo')
        expected_files = [
            os.path.join('/repo', 'README.md'),
            os.path.join('/repo/docs', 'CONTRIBUTING.md')
        ]
        self.assertCountEqual(files, expected_files)

        mock_os_walk.return_value = [] # Test empty directory
        self.assertEqual(find_markdown_files('/empty'), [])

    @patch('builtins.open', new_callable=mock_open)
    def test_extract_urls_from_markdown(self, mock_file_open):
        # Mock rationale: Simulate reading file content without actual disk I/O.
        mock_file_open.return_value.read.side_effect = [
            """# My Project\n\nCheck out our [website](https://example.com/project).\nAlso, visit https://github.com/user/repo for code.\nAnother link: [docs](http://docs.example.org/guide)\nNo link here.\n""",
            """No links in this file.\n"""
        ]

        # Test with multiple links
        urls = extract_urls_from_markdown('dummy_path/README.md')
        expected_urls = [
            'https://example.com/project',
            'https://github.com/user/repo',
            'http://docs.example.org/guide'
        ]
        self.assertCountEqual(urls, expected_urls)

        # Test with no links
        urls_no_links = extract_urls_from_markdown('dummy_path/no_links.md')
        self.assertEqual(urls_no_links, [])

    @patch('requests.head')
    def test_check_url_reachability(self, mock_requests_head):
        # Mock rationale: Simulate network requests and responses without actual network calls.

        # Test successful link (200 OK)
        mock_requests_head.return_value.status_code = 200
        mock_requests_head.return_value.reason = 'OK'
        is_reachable, status = check_url_reachability('https://good.com')
        self.assertTrue(is_reachable)
        self.assertEqual(status, 'Status: 200')

        # Test successful link (301 Redirect)
        mock_requests_head.return_value.status_code = 301
        mock_requests_head.return_value.reason = 'Moved Permanently'
        is_reachable, status = check_url_reachability('https://redirect.com')
        self.assertTrue(is_reachable)
        self.assertEqual(status, 'Status: 301')

        # Test broken link (404 Not Found)
        mock_requests_head.return_value.status_code = 404
        mock_requests_head.return_value.reason = 'Not Found'
        is_reachable, status = check_url_reachability('https://bad.com/404')
        self.assertFalse(is_reachable)
        self.assertEqual(status, 'Status: 404 - Not Found')

        # Test server error (500 Internal Server Error)
        mock_requests_head.return_value.status_code = 500
        mock_requests_head.return_value.reason = 'Internal Server Error'
        is_reachable, status = check_url_reachability('https://server-error.com')
        self.assertFalse(is_reachable)
        self.assertEqual(status, 'Status: 500 - Internal Server Error')

        # Test connection error
        mock_requests_head.side_effect = requests.exceptions.ConnectionError('Connection refused')
        is_reachable, status = check_url_reachability('https://no-connection.com')
        self.assertFalse(is_reachable)
        self.assertEqual(status, 'Error: Connection refused or DNS error')
        mock_requests_head.side_effect = None # Reset side effect

        # Test timeout error
        mock_requests_head.side_effect = requests.exceptions.Timeout('Request timed out')
        is_reachable, status = check_url_reachability('https://slow-server.com')
        self.assertFalse(is_reachable)
        self.assertEqual(status, 'Error: Timeout')
        mock_requests_head.side_effect = None # Reset side effect

        # Test generic request exception
        mock_requests_head.side_effect = requests.exceptions.RequestException('Generic error')
        is_reachable, status = check_url_reachability('https://any-error.com')
        self.assertFalse(is_reachable)
        self.assertEqual(status, 'Error: Generic error')
        mock_requests_head.side_effect = None # Reset side effect

if __name__ == '__main__':
    unittest.main()
