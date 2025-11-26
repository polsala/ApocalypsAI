import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import requests
from src.scavenger import find_markdown_files, extract_links_from_markdown, check_link_status

# Mock rationale: We need to simulate file system traversal (os.walk) and file reading (open)
# without actually touching the disk. This ensures tests are fast, deterministic, and isolated.
# We also need to mock network requests (requests.head) to avoid actual network calls,
# making tests offline and preventing external dependencies from affecting test results.

class TestScavenger(unittest.TestCase):

    @patch('os.walk')
    def test_find_markdown_files(self, mock_os_walk):
        # Mock rationale: Simulate a directory structure with Markdown files.
        mock_os_walk.return_value = [
            ('/repo', ['docs', 'src'], ['README.md', 'LICENSE']),
            ('/repo/docs', [], ['guide.md', 'api.markdown']),
            ('/repo/src', [], ['main.py'])
        ]
        
        expected_files = [
            os.path.join('/repo', 'README.md'),
            os.path.join('/repo/docs', 'guide.md'),
            os.path.join('/repo/docs', 'api.markdown'),
        ]
        
        found_files = find_markdown_files('/repo')
        self.assertCountEqual(expected_files, found_files)
        mock_os_walk.assert_called_once_with('/repo')

    @patch('builtins.open', new_callable=mock_open)
    def test_extract_links_from_markdown(self, mock_file_open):
        # Mock rationale: Simulate reading content from a Markdown file.
        mock_file_content = (
            "# My Doc\n\n"
            "This is a [link to Google](https://www.google.com).\n"
            "Another link: <https://example.com/path/to/resource?id=123>.\n"
            "A relative link: [local](/local/path).\n"
            "An image link: ![alt text](https://picsum.photos/200/300).\n"
            "Just a URL: https://standalone.org/page.\n"
            "No link here."
        )
        mock_file_open.return_value.read.return_value = mock_file_content

        expected_links = sorted([
            "https://www.google.com",
            "https://example.com/path/to/resource?id=123",
            "https://picsum.photos/200/300",
            "https://standalone.org/page"
        ])
        
        extracted_links = extract_links_from_markdown('/fake/path/doc.md')
        self.assertEqual(expected_links, extracted_links)
        mock_file_open.assert_called_once_with('/fake/path/doc.md', 'r', encoding='utf-8')

    @patch('requests.head')
    def test_check_link_status_success(self, mock_head):
        # Mock rationale: Simulate a successful HTTP HEAD request.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None # No exception
        mock_head.return_value = mock_response

        is_ok, status_msg = check_link_status('https://good.com')
        self.assertTrue(is_ok)
        self.assertEqual(status_msg, 'OK (Status: 200)')
        mock_head.assert_called_once_with('https://good.com', timeout=5, allow_redirects=True)

    @patch('requests.head')
    def test_check_link_status_404(self, mock_head):
        # Mock rationale: Simulate a 404 Not Found HTTP response.
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.reason = 'Not Found'
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_head.return_value = mock_response

        is_ok, status_msg = check_link_status('https://bad.com/404')
        self.assertFalse(is_ok)
        self.assertEqual(status_msg, 'Status: 404 Not Found')

    @patch('requests.head')
    def test_check_link_status_connection_error(self, mock_head):
        # Mock rationale: Simulate a network connection error.
        mock_head.side_effect = requests.exceptions.ConnectionError('Failed to connect')

        is_ok, status_msg = check_link_status('https://no-internet.com')
        self.assertFalse(is_ok)
        self.assertEqual(status_msg, 'Error: Connection Error')

    @patch('requests.head')
    def test_check_link_status_timeout(self, mock_head):
        # Mock rationale: Simulate a request timeout.
        mock_head.side_effect = requests.exceptions.Timeout('Request timed out')

        is_ok, status_msg = check_link_status('https://slow-server.com')
        self.assertFalse(is_ok)
        self.assertEqual(status_msg, 'Error: Timeout')

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.scavenger.check_link_status') # Patch the function directly for integration-like test
    def test_main_functionality(self, mock_check_link_status, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate the entire flow from file discovery to link checking and reporting.
        # This tests the integration of find_markdown_files, extract_links_from_markdown, and check_link_status
        # without actual file I/O or network requests.

        # Setup mock file system
        mock_os_walk.return_value = [
            ('/repo', [], ['README.md'])
        ]

        # Setup mock file content
        mock_file_content = (
            "# Project README\n\n"
            "Visit our [website](https://good.com).\n"
            "Check out the [old docs](https://bad.com/404).\n"
            "Another good link: https://another-good.com/."
        )
        mock_file_open.return_value.read.return_value = mock_file_content

        # Setup mock link status checks
        mock_check_link_status.side_effect = [
            (True, 'OK (Status: 200)'), # https://good.com
            (False, 'Status: 404 Not Found'), # https://bad.com/404
            (True, 'OK (Status: 200)') # https://another-good.com/
        ]

        # Capture print output
        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/repo')):
                from src.scavenger import main
                main()
                
                output = mock_stdout.getvalue()
                self.assertIn('Scanning for broken links in:', output)
                self.assertIn('Found 1 Markdown files.', output)
                self.assertIn('--- Broken Links Found ---', output)
                self.assertIn(f'File: {os.path.abspath('/repo/README.md')}', output)
                self.assertIn('  - https://bad.com/404 (Status: 404 Not Found)', output)
                self.assertIn('--- Scan Complete ---', output)
                self.assertNotIn('No broken links found. All clear!', output)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.scavenger.check_link_status')
    def test_main_no_broken_links(self, mock_check_link_status, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a scenario where all links are valid.
        mock_os_walk.return_value = [
            ('/repo', [], ['README.md'])
        ]
        mock_file_content = "# Project README\n\nVisit our [website](https://good.com)."
        mock_file_open.return_value.read.return_value = mock_file_content
        mock_check_link_status.return_value = (True, 'OK (Status: 200)')

        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/repo')):
                from src.scavenger import main
                main()
                output = mock_stdout.getvalue()
                self.assertIn('--- Scan Complete ---', output)
                self.assertIn('No broken links found. All clear!', output)
                self.assertNotIn('--- Broken Links Found ---', output)
