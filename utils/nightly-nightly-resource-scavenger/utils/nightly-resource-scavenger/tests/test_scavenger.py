import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
import requests

# Add the src directory to the path to allow importing scavenger.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import scavenger

class TestScavenger(unittest.TestCase):

    @patch('os.walk')
    def test_scan_directory_for_markdown_files(self, mock_os_walk):
        # Mock rationale: Simulate file system traversal without actual disk I/O.
        mock_os_walk.return_value = [
            ('/repo', ('docs', 'src'), ('README.md', 'LICENSE')),
            ('/repo/docs', (), ('guide.md', 'api.txt')),
            ('/repo/src', (), ('main.py',))
        ]
        expected_files = [
            os.path.join('/repo', 'README.md'),
            os.path.join('/repo/docs', 'guide.md')
        ]
        found_files = list(scavenger.scan_directory_for_markdown_files('/repo'))
        self.assertCountEqual(found_files, expected_files)

    def test_extract_links_from_markdown(self):
        # Mock rationale: Test Markdown parsing logic with various string inputs.
        markdown_content = """
# My Project

This is a [link to Google](https://www.google.com).
And another [link to Example](http://example.com/page).
No link here.
[Relative link](/path/to/local) should be ignored.
[FTP link](ftp://ftp.example.com) should be ignored.
"""
        expected_links = [
            {'url': 'https://www.google.com', 'line': 3},
            {'url': 'http://example.com/page', 'line': 4}
        ]
        extracted_links = scavenger.extract_links_from_markdown(markdown_content)
        self.assertCountEqual(extracted_links, expected_links)

        # Test with no links
        self.assertEqual(scavenger.extract_links_from_markdown("No links here."), [])

        # Test with only non-http links
        self.assertEqual(scavenger.extract_links_from_markdown("[Local](/local) [FTP](ftp://a.com)"), [])

    @patch('requests.head')
    def test_check_link_status_ok(self, mock_head):
        # Mock rationale: Simulate a successful HTTP HEAD request.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_head.return_value = mock_response

        status, detail = scavenger.check_link_status('http://valid.com')
        self.assertEqual(status, 'OK')
        self.assertEqual(detail, 200)
        mock_head.assert_called_once_with('http://valid.com', timeout=5, allow_redirects=True)

    @patch('requests.head')
    def test_check_link_status_broken_404(self, mock_head):
        # Mock rationale: Simulate a 404 Not Found HTTP error.
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_head.return_value = mock_response

        status, detail = scavenger.check_link_status('http://broken.com/404')
        self.assertEqual(status, 'BROKEN')
        self.assertEqual(detail, 404)

    @patch('requests.head')
    def test_check_link_status_connection_error(self, mock_head):
        # Mock rationale: Simulate a network connection error.
        mock_head.side_effect = requests.exceptions.ConnectionError

        status, detail = scavenger.check_link_status('http://no-connection.com')
        self.assertEqual(status, 'BROKEN')
        self.assertEqual(detail, 'Connection Error')

    @patch('requests.head')
    def test_check_link_status_timeout(self, mock_head):
        # Mock rationale: Simulate a request timeout.
        mock_head.side_effect = requests.exceptions.Timeout

        status, detail = scavenger.check_link_status('http://slow-server.com')
        self.assertEqual(status, 'BROKEN')
        self.assertEqual(detail, 'Timeout')

    @patch('scavenger.scan_directory_for_markdown_files')
    @patch('builtins.open', new_callable=mock_open)
    @patch('scavenger.check_link_status')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_main_all_healthy(self, mock_exit, mock_stdout, mock_check_link_status, mock_open_file, mock_scan_dir):
        # Mock rationale: Simulate a full run where all links are healthy.
        # Mock file system, link checking, and stdout to verify behavior without side effects.
        mock_scan_dir.return_value = ['/repo/README.md']
        mock_open_file.return_value.read.return_value = "[Healthy Link](http://healthy.com)"
        mock_check_link_status.return_value = ('OK', 200)

        scavenger.main()

        mock_scan_dir.assert_called_once_with('.')
        mock_open_file.assert_called_once_with('/repo/README.md', 'r', encoding='utf-8')
        mock_check_link_status.assert_called_once_with('http://healthy.com')
        # Check specific output for 'All links are healthy.'
        self.assertIn('All links are healthy.', mock_stdout.write.call_args_list[3].args[0])
        mock_exit.assert_called_once_with(0)

    @patch('scavenger.scan_directory_for_markdown_files')
    @patch('builtins.open', new_callable=mock_open)
    @patch('scavenger.check_link_status')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_main_with_broken_links(self, mock_exit, mock_stdout, mock_check_link_status, mock_open_file, mock_scan_dir):
        # Mock rationale: Simulate a full run where some links are broken.
        # Mock file system, link checking, and stdout to verify behavior without side effects.
        mock_scan_dir.return_value = ['/repo/docs/guide.md']
        mock_open_file.return_value.read.return_value = "[Broken Link](http://broken.com)\n[Healthy Link](http://healthy.com)"
        mock_check_link_status.side_effect = [
            ('BROKEN', 404), # First link is broken
            ('OK', 200)      # Second link is healthy
        ]

        scavenger.main()

        self.assertEqual(mock_check_link_status.call_count, 2)
        mock_check_link_status.assert_any_call('http://broken.com')
        mock_check_link_status.assert_any_call('http://healthy.com')
        # Check specific output for 'Found X broken links.'
        self.assertIn('Found 1 broken links.', mock_stdout.write.call_args_list[-1].args[0])
        mock_exit.assert_called_once_with(1)

    @patch('scavenger.scan_directory_for_markdown_files')
    @patch('builtins.open', new_callable=mock_open)
    @patch('scavenger.check_link_status')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_main_no_markdown_files(self, mock_exit, mock_stdout, mock_check_link_status, mock_open_file, mock_scan_dir):
        # Mock rationale: Simulate a scenario where no Markdown files are found.
        mock_scan_dir.return_value = []

        scavenger.main()

        mock_scan_dir.assert_called_once_with('.')
        mock_open_file.assert_not_called()
        mock_check_link_status.assert_not_called()
        # Check specific output for 'Found 0 Markdown files.' and 'All links are healthy.'
        self.assertIn('Found 0 Markdown files.', mock_stdout.write.call_args_list[1].args[0])
        self.assertIn('All links are healthy.', mock_stdout.write.call_args_list[-1].args[0])
        mock_exit.assert_called_once_with(0)

    @patch('scavenger.scan_directory_for_markdown_files')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_main_file_read_error(self, mock_exit, mock_stdout, mock_open_file, mock_scan_dir):
        # Mock rationale: Simulate an error when trying to read a Markdown file.
        mock_scan_dir.return_value = ['/repo/bad_file.md']
        mock_open_file.side_effect = IOError("Permission denied")

        scavenger.main()

        mock_open_file.assert_called_once_with('/repo/bad_file.md', 'r', encoding='utf-8')
        # Check specific output for the error message.
        self.assertIn('Could not process file /repo/bad_file.md: Permission denied', mock_stdout.write.call_args_list[2].args[0])
        # Exit 0 because no *broken links* were found, just a file processing error.
        self.assertIn('All links are healthy.', mock_stdout.write.call_args_list[-1].args[0])
        mock_exit.assert_called_once_with(0)
