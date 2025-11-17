import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import requests # Import requests to catch its exceptions

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import beacon

class TestBeacon(unittest.TestCase):

    @patch('os.walk')
    def test_find_markdown_files(self, mock_os_walk):
        # Mock rationale: Simulate file system traversal without actual disk access.
        mock_os_walk.return_value = [
            ('/repo', ['agents', 'docs', 'utils'], ['README.md', 'LICENSE']),
            ('/repo/agents', [], ['AGENTS.md', 'agent.py']),
            ('/repo/docs', [], ['CONTRIBUTING.md']),
            ('/repo/utils', ['nightly-timer'], ['config.txt'])
        ]
        
        expected_files = [
            os.path.join('/repo', 'README.md'),
            os.path.join('/repo/agents', 'AGENTS.md'),
            os.path.join('/repo/docs', 'CONTRIBUTING.md')
        ]
        
        found_files = beacon.find_markdown_files('/repo')
        self.assertCountEqual(found_files, expected_files)
        mock_os_walk.assert_called_once_with('/repo')

    def test_extract_links(self):
        # Mock rationale: Provide controlled Markdown content as if read from a file.
        mock_md_content = """
# My Doc

This is a [link to Google](https://www.google.com).
And an [internal file](./path/to/file.md).
Another [external link](http://example.com/page).
No link here.
[Link with anchor](/some/path.md#section).
[Empty link]()
"""
        
        # Patch open to return our mock content
        with patch('builtins.open', unittest.mock.mock_open(read_data=mock_md_content)) as mock_file:
            links = beacon.extract_links('/fake/path/doc.md')
            expected_links = [
                'https://www.google.com',
                './path/to/file.md',
                'http://example.com/page',
                '/some/path.md#section',
                '' # Empty link should still be extracted
            ]
            self.assertCountEqual(links, expected_links)
            mock_file.assert_called_once_with('/fake/path/doc.md', 'r', encoding='utf-8')

    @patch('requests.head')
    def test_check_external_link(self, mock_head):
        # Mock rationale: Simulate network responses without making actual HTTP requests.
        
        # Test valid link (200 OK)
        mock_response_ok = MagicMock()
        mock_response_ok.status_code = 200
        mock_head.return_value = mock_response_ok
        is_valid, status = beacon.check_external_link('https://valid.com')
        self.assertTrue(is_valid)
        self.assertEqual(status, 200)
        mock_head.assert_called_with('https://valid.com', timeout=5, allow_redirects=True)

        # Test broken link (404 Not Found)
        mock_response_404 = MagicMock()
        mock_response_404.status_code = 404
        mock_head.return_value = mock_response_404
        is_valid, status = beacon.check_external_link('https://broken.com/404')
        self.assertFalse(is_valid)
        self.assertEqual(status, 404)

        # Test server error (500 Internal Server Error)
        mock_response_500 = MagicMock()
        mock_response_500.status_code = 500
        mock_head.return_value = mock_response_500
        is_valid, status = beacon.check_external_link('https://server-error.com')
        self.assertFalse(is_valid)
        self.assertEqual(status, 500)

        # Test network error (requests.exceptions.RequestException)
        mock_head.side_effect = requests.exceptions.ConnectionError('DNS lookup failed')
        is_valid, status = beacon.check_external_link('https://no-network.com')
        self.assertFalse(is_valid)
        self.assertIn('DNS lookup failed', status)

    @patch('os.path.exists')
    @patch('os.getcwd', return_value='/repo') # Mock rationale: Fix current working directory for absolute path resolution
    def test_check_internal_link(self, mock_getcwd, mock_exists):
        # Mock rationale: Simulate file system existence checks without actual disk access.
        
        base_filepath = '/repo/docs/README.md'

        # Test valid relative link
        mock_exists.return_value = True
        is_valid = beacon.check_internal_link(base_filepath, './images/pic.png')
        self.assertTrue(is_valid)
        mock_exists.assert_called_with(os.path.normpath('/repo/docs/images/pic.png'))

        # Test valid parent directory link
        mock_exists.return_value = True
        is_valid = beacon.check_internal_link(base_filepath, '../AGENTS.md')
        self.assertTrue(is_valid)
        mock_exists.assert_called_with(os.path.normpath('/repo/AGENTS.md'))

        # Test broken relative link
        mock_exists.return_value = False
        is_valid = beacon.check_internal_link(base_filepath, './non-existent.md')
        self.assertFalse(is_valid)
        mock_exists.assert_called_with(os.path.normpath('/repo/docs/non-existent.md'))

        # Test valid absolute link (relative to repo root, indicated by leading /)
        mock_exists.return_value = True
        is_valid = beacon.check_internal_link(base_filepath, '/agents/agent_builder.py')
        self.assertTrue(is_valid)
        mock_exists.assert_called_with(os.path.normpath('/repo/agents/agent_builder.py'))

        # Test broken absolute link
        mock_exists.return_value = False
        is_valid = beacon.check_internal_link(base_filepath, '/non-existent-root-file.txt')
        self.assertFalse(is_valid)
        mock_exists.assert_called_with(os.path.normpath('/repo/non-existent-root-file.txt'))

        # Test link with anchor (should ignore anchor for existence check)
        mock_exists.return_value = True
        is_valid = beacon.check_internal_link(base_filepath, './another.md#section')
        self.assertTrue(is_valid)
        mock_exists.assert_called_with(os.path.normpath('/repo/docs/another.md'))

        # Test empty link (e.g., just an anchor like '[](#section)')
        is_valid = beacon.check_internal_link(base_filepath, '#section')
        self.assertTrue(is_valid) # Should be considered valid as it's an internal anchor

        is_valid = beacon.check_internal_link(base_filepath, '')
        self.assertTrue(is_valid) # Empty link, assume valid (e.g., for JS-driven links)


    @patch('beacon.find_markdown_files')
    @patch('beacon.extract_links')
    @patch('beacon.check_external_link')
    @patch('beacon.check_internal_link')
    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    @patch('os.getcwd', return_value='/repo') # Mock rationale: Fix current working directory for consistent paths.
    @patch('os.path.relpath', side_effect=lambda path, start: path.replace(start + '/', '')) # Mock rationale: Simplify relative path for consistent output.
    def test_main_flow(self, mock_relpath, mock_getcwd, mock_print, mock_check_internal, mock_check_external, mock_extract_links, mock_find_markdown_files):
        # Mock rationale: Simulate the entire utility's execution without actual file system or network interaction.
        
        mock_find_markdown_files.return_value = [
            '/repo/README.md',
            '/repo/docs/CONTRIBUTING.md'
        ]

        mock_extract_links.side_effect = [
            # Links for README.md
            ['https://valid-external.com', './internal-valid.md', 'https://broken-external.com', '/root-valid.md', '#anchor-only'],
            # Links for CONTRIBUTING.md
            ['../README.md', 'http://another-broken.org']
        ]

        mock_check_external.side_effect = [
            (True, 200),   # valid-external.com
            (False, 404),  # broken-external.com
            (False, 500)   # another-broken.org
        ]

        mock_check_internal.side_effect = [
            True,  # internal-valid.md
            True,  # root-valid.md
            True,  # #anchor-only (handled by check_internal_link logic)
            True   # ../README.md
        ]

        beacon.main()

        # Verify calls and output
        mock_find_markdown_files.assert_called_once_with('/repo')
        self.assertEqual(mock_extract_links.call_count, 2)
        self.assertEqual(mock_check_external.call_count, 3)
        self.assertEqual(mock_check_internal.call_count, 4)

        # Check print calls for expected output
        mock_print.assert_any_call('Scanning for broken links in the repository...')
        mock_print.assert_any_call('\nFound 2 Markdown files.\n')
        mock_print.assert_any_call('--- File: README.md ---')
        mock_print.assert_any_call('  ✅ Valid External: https://valid-external.com')
        mock_print.assert_any_call('  ✅ Valid Internal: ./internal-valid.md')
        mock_print.assert_any_call('  ❌ Broken External: https://broken-external.com (Status: 404)')
        mock_print.assert_any_call('  ✅ Valid Internal: /root-valid.md')
        mock_print.assert_any_call('  ✅ Valid Internal: #anchor-only')
        mock_print.assert_any_call('--- File: docs/CONTRIBUTING.md ---')
        mock_print.assert_any_call('  ✅ Valid Internal: ../README.md')
        mock_print.assert_any_call('  ❌ Broken External: http://another-broken.org (Status: 500)')
        
        # Ensure the total broken links count is correct
        last_print_call_args = mock_print.call_args_list[-1].args[0]
        self.assertIn('2 broken links found.', last_print_call_args)


if __name__ == '__main__':
    unittest.main()
