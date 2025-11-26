import unittest
import os
import sys
from unittest.mock import patch, mock_open, MagicMock

# Add the src directory to the path to allow importing scavenger
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import scavenger

class TestScavenger(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_find_links_in_file_basic(self, mock_file):
        # Mock rationale: Simulate reading a file with various link types without actual file I/O.
        mock_file.return_value.read.return_value = (
            "This is a test file.\n"
            "Here's a link: https://example.com/page\n"
            "Another one: http://test.org/path/to/resource.html?query=1&param=2\n"
            "Link in parentheses (https://parentheses.net/)\n"
            "No link here.\n"
            "Invalid link: http://.com\n" # This regex might catch this, which is fine for basic check
            "Link with trailing slash: https://slash.com/\n"
            "Link with port: http://localhost:8080/api\n"
        )
        
        links = scavenger.find_links_in_file("dummy.md")
        expected_links = [
            "https://example.com/page",
            "http://test.org/path/to/resource.html?query=1&param=2",
            "https://parentheses.net/",
            "https://slash.com/",
            "http://localhost:8080/api"
        ]
        # The regex `[^\s)"\'\\]+` is designed to stop at common delimiters.
        # It correctly handles links within parentheses by stopping at the closing parenthesis.
        self.assertCountEqual(links, expected_links)

    @patch('builtins.open', new_callable=mock_open)
    def test_find_links_in_file_no_links(self, mock_file):
        # Mock rationale: Simulate reading a file with no links.
        mock_file.return_value.read.return_value = "This file has no links."
        links = scavenger.find_links_in_file("dummy.txt")
        self.assertEqual(links, [])

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_success(self, mock_get, mock_head):
        # Mock rationale: Simulate successful HTTP requests without actual network calls.
        mock_head.return_value = MagicMock(status_code=200, request=MagicMock(method='HEAD'))
        url, status, error = scavenger.check_link("https://good.com")
        self.assertEqual(status, 200)
        self.assertEqual(error, "")
        mock_head.assert_called_once_with("https://good.com", timeout=5, allow_redirects=True)
        mock_get.assert_not_called() # HEAD should be sufficient

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_not_found(self, mock_get, mock_head):
        # Mock rationale: Simulate a 404 Not Found response and HEAD fallback to GET.
        mock_head.return_value = MagicMock(status_code=404, request=MagicMock(method='HEAD'))
        mock_get.return_value = MagicMock(status_code=404, request=MagicMock(method='GET')) # Fallback to GET
        url, status, error = scavenger.check_link("https://bad.com/404")
        self.assertEqual(status, 404)
        self.assertEqual(error, "")
        mock_head.assert_called_once()
        mock_get.assert_called_once() # Should fall back to GET if HEAD returns 4xx/5xx

    @patch('requests.head', side_effect=requests.exceptions.ConnectionError)
    @patch('requests.get')
    def test_check_link_connection_error(self, mock_get, mock_head):
        # Mock rationale: Simulate a network connection error.
        url, status, error = scavenger.check_link("https://error.com")
        self.assertEqual(status, 0)
        self.assertEqual(error, "Connection Error")
        mock_head.assert_called_once()
        mock_get.assert_not_called()

    @patch('requests.head', side_effect=requests.exceptions.Timeout)
    @patch('requests.get')
    def test_check_link_timeout(self, mock_get, mock_head):
        # Mock rationale: Simulate a request timeout.
        url, status, error = scavenger.check_link("https://timeout.com")
        self.assertEqual(status, 0)
        self.assertEqual(error, "Timeout")
        mock_head.assert_called_once()
        mock_get.assert_not_called()

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('scavenger.check_link') # Mock the network call directly
    @patch('scavenger.find_links_in_file') # Mock link extraction
    def test_scavenge_directory_no_broken_links(self, mock_find_links, mock_check_link, mock_file, mock_os_walk):
        # Mock rationale: Simulate file system traversal and link checking without actual I/O or network.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['file1.md', 'file2.txt']),
            ('/test_dir/subdir', [], ['file3.md'])
        ]
        mock_find_links.side_effect = [
            ['https://good1.com'], # for file1.md
            [],                    # for file2.txt
            ['https://good2.com']  # for file3.md
        ]
        mock_check_link.side_effect = [
            ('https://good1.com', 200, ''),
            ('https://good2.com', 200, '')
        ]

        broken_links = scavenger.scavenge_directory('/test_dir', ['md', 'txt'])
        self.assertEqual(broken_links, {})
        self.assertEqual(mock_find_links.call_count, 3) # Called for file1.md, file2.txt, file3.md
        self.assertEqual(mock_check_link.call_count, 2) # Called for good1.com, good2.com

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('scavenger.check_link')
    @patch('scavenger.find_links_in_file')
    def test_scavenge_directory_with_broken_links(self, mock_find_links, mock_check_link, mock_file, mock_os_walk):
        # Mock rationale: Simulate file system traversal and link checking, including broken links.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['file1.md']),
        ]
        mock_find_links.return_value = ['https://good.com', 'https://broken.com']
        mock_check_link.side_effect = [
            ('https://good.com', 200, ''),
            ('https://broken.com', 404, '')
        ]

        broken_links = scavenger.scavenge_directory('/test_dir', ['md'])
        expected_broken = {
            os.path.join('/test_dir', 'file1.md'): [
                ('https://broken.com', 404, '')
            ]
        }
        self.assertEqual(broken_links, expected_broken)
        self.assertEqual(mock_find_links.call_count, 1)
        self.assertEqual(mock_check_link.call_count, 2)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('scavenger.check_link')
    @patch('scavenger.find_links_in_file')
    def test_scavenge_directory_ignore_patterns(self, mock_find_links, mock_check_link, mock_file, mock_os_walk):
        # Mock rationale: Test the ignore pattern functionality without actual I/O or network.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['file1.md']),
        ]
        mock_find_links.return_value = [
            'https://good.com',
            'https://ignore.me/path',
            'http://another.ignore.me'
        ]
        mock_check_link.side_effect = [
            ('https://good.com', 200, '')
        ]

        ignore_patterns = ['ignore.me', r'another\\.ignore\\.me'] # Escaped for regex
        broken_links = scavenger.scavenge_directory('/test_dir', ['md'], ignore_patterns=ignore_patterns)
        
        self.assertEqual(broken_links, {})
        self.assertEqual(mock_find_links.call_count, 1)
        # Only 'https://good.com' should be checked, the others are ignored
        mock_check_link.assert_called_once_with('https://good.com', 5)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('scavenger.scavenge_directory')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_no_broken_links(self, mock_exit, mock_print, mock_scavenge_directory, mock_parse_args):
        # Mock rationale: Test the main function's flow when no broken links are found.
        mock_parse_args.return_value = MagicMock(
            path='.', extensions=['md'], timeout=5, ignore_patterns=[]
        )
        mock_scavenge_directory.return_value = {}

        scavenger.main()

        mock_scavenge_directory.assert_called_once_with('.', ['md'], 5, [])
        mock_print.assert_any_call("\nScavenging complete. No broken links found. Repository is pristine!")
        mock_exit.assert_called_once_with(0)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('scavenger.scavenge_directory')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_with_broken_links(self, mock_exit, mock_print, mock_scavenge_directory, mock_parse_args):
        # Mock rationale: Test the main function's flow when broken links are found.
        mock_parse_args.return_value = MagicMock(
            path='.', extensions=['md'], timeout=5, ignore_patterns=[]
        )
        mock_scavenge_directory.return_value = {
            'file.md': [('https://broken.com', 404, '')]
        }

        scavenger.main()

        mock_scavenge_directory.assert_called_once_with('.', ['md'], 5, [])
        mock_print.assert_any_call("\n--- Broken Links Report ---")
        mock_print.assert_any_call("  - URL: https://broken.com")
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
