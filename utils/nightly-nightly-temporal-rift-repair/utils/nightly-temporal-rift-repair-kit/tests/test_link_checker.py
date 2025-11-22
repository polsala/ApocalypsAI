import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
import sys
from io import StringIO

# Add the src directory to the Python path to import the module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from link_checker import find_markdown_files, extract_links, check_external_link, check_internal_link, main

class TestLinkChecker(unittest.TestCase):

    @patch('os.walk')
    def test_find_markdown_files(self, mock_os_walk):
        # Mock rationale: Simulate file system traversal without actual disk access.
        mock_os_walk.return_value = [
            ('/root', ['dir1'], ['file.md', 'other.txt']),
            ('/root/dir1', [], ['another.markdown', 'image.png'])
        ]
        files = find_markdown_files('/root')
        expected = [
            os.path.join('/root', 'file.md'),
            os.path.join('/root/dir1', 'another.markdown')
        ]
        self.assertEqual(sorted(files), sorted(expected))

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.relpath', side_effect=lambda x, start=None: x) # Mock relpath for consistent test paths
    def test_extract_links(self, mock_relpath, mock_file_open):
        # Mock rationale: Simulate reading file content without actual disk access.
        mock_file_open.return_value.read.return_value = (
            "# My Doc\n\n"
            "This is a [link to Google](https://www.google.com).\n"
            "Another link: <https://example.com/test>.\n"
            "Internal link: [local file](./local.md).\n"
            "Anchor link: [section](#section-1).\n"
            "No link here."
        )
        links = extract_links('/path/to/doc.md')
        self.assertEqual(len(links), 4)
        self.assertEqual(links[0]['url'], 'https://www.google.com')
        self.assertEqual(links[1]['url'], 'https://example.com/test')
        self.assertEqual(links[2]['url'], './local.md')
        self.assertEqual(links[3]['url'], '#section-1')

    @patch('requests.head')
    @patch('requests.get')
    def test_check_external_link_success(self, mock_requests_get, mock_requests_head):
        # Mock rationale: Simulate successful HTTP requests without actual network calls.
        mock_response_head = MagicMock()
        mock_response_head.status_code = 200
        mock_response_head.raise_for_status.return_value = None
        mock_requests_head.return_value = mock_response_head

        is_valid, reason = check_external_link('https://valid.com')
        self.assertTrue(is_valid)
        self.assertIsNone(reason)
        mock_requests_head.assert_called_once_with('https://valid.com', timeout=5, allow_redirects=True)
        mock_requests_get.assert_not_called() # Should not call GET if HEAD is 200

    @patch('requests.head')
    @patch('requests.get')
    def test_check_external_link_head_fail_get_success(self, mock_requests_get, mock_requests_head):
        # Mock rationale: Simulate a server rejecting HEAD (e.g., 405) but accepting GET.
        mock_response_head = MagicMock()
        mock_response_head.status_code = 405 # Method Not Allowed
        mock_requests_head.return_value = mock_response_head

        mock_response_get = MagicMock()
        mock_response_get.status_code = 200
        mock_response_get.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response_get

        is_valid, reason = check_external_link('https://valid.com/head-fail')
        self.assertTrue(is_valid)
        self.assertIsNone(reason)
        mock_requests_head.assert_called_once()
        mock_requests_get.assert_called_once_with('https://valid.com/head-fail', timeout=5, allow_redirects=True)

    @patch('requests.head')
    @patch('requests.get')
    def test_check_external_link_failure(self, mock_requests_get, mock_requests_head):
        # Mock rationale: Simulate a failed HTTP request (e.g., 404, network error) for both HEAD and GET.
        mock_requests_head.side_effect = requests.exceptions.RequestException("404 Not Found")
        mock_requests_get.side_effect = requests.exceptions.RequestException("404 Not Found") 

        is_valid, reason = check_external_link('https://invalid.com')
        self.assertFalse(is_valid)
        self.assertIsNotNone(reason)
        self.assertIn('404 Not Found', reason)

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.dirname', return_value='/root') # Mock dirname for consistent path resolution
    @patch('os.path.normpath', side_effect=lambda x: x) # Mock normpath to simplify path handling in tests
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args)) # Mock join for consistent path handling
    def test_check_internal_link_file_exists(self, mock_os_path_join, mock_os_path_normpath, mock_os_path_dirname, mock_file_open, mock_os_path_isdir, mock_os_path_exists):
        # Mock rationale: Simulate file system checks and file content reading for internal links.
        mock_os_path_exists.return_value = True
        mock_os_path_isdir.return_value = False
        is_valid, reason = check_internal_link('/root/doc.md', './target.md', [])
        self.assertTrue(is_valid)
        self.assertIsNone(reason)

    @patch('os.path.exists', return_value=False)
    @patch('os.path.dirname', return_value='/root')
    @patch('os.path.normpath', side_effect=lambda x: x)
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_check_internal_link_file_not_exists(self, mock_os_path_join, mock_os_path_normpath, mock_os_path_dirname, mock_os_path_exists):
        # Mock rationale: Simulate a non-existent internal file.
        is_valid, reason = check_internal_link('/root/doc.md', './non-existent.md', [])
        self.assertFalse(is_valid)
        self.assertIn('not found', reason)

    @patch('os.path.exists')
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.dirname', return_value='/root')
    @patch('os.path.normpath', side_effect=lambda x: x)
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_check_internal_link_directory_without_index(self, mock_os_path_join, mock_os_path_normpath, mock_os_path_dirname, mock_file_open, mock_os_path_isdir, mock_os_path_exists):
        # Mock rationale: Simulate linking to a directory that lacks a common index file.
        mock_os_path_exists.side_effect = lambda p: p == '/root/target_dir' # Directory exists, but no index.md/README.md
        is_valid, reason = check_internal_link('/root/doc.md', './target_dir', [])
        self.assertFalse(is_valid)
        self.assertIn('directory', reason)

    @patch('os.path.exists')
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.dirname', return_value='/root')
    @patch('os.path.normpath', side_effect=lambda x: x)
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_check_internal_link_directory_with_index(self, mock_os_path_join, mock_os_path_normpath, mock_os_path_dirname, mock_file_open, mock_os_path_isdir, mock_os_path_exists):
        # Mock rationale: Simulate linking to a directory that has a common index file.
        mock_os_path_exists.side_effect = lambda p: p in ['/root/target_dir', '/root/target_dir/README.md']
        is_valid, reason = check_internal_link('/root/doc.md', './target_dir', [])
        self.assertTrue(is_valid)
        self.assertIsNone(reason)

    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.dirname', return_value='/root')
    @patch('os.path.normpath', side_effect=lambda x: x)
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_check_internal_link_anchor_exists(self, mock_os_path_join, mock_os_path_normpath, mock_os_path_dirname, mock_file_open, mock_os_path_isdir, mock_os_path_exists):
        # Mock rationale: Simulate checking for an anchor within a file, covering both explicit IDs and generated heading IDs.
        mock_file_open.return_value.read.return_value = (
            "# My Document\n\n"
            "## Section One\n"
            "Content here.\n"
            "<a id=\"section-two\"></a>\n"
            "### Section Two With Spaces\n"
        )
        is_valid, reason = check_internal_link('/root/doc.md', './target.md#section-one', [])
        self.assertTrue(is_valid)
        self.assertIsNone(reason)

        is_valid, reason = check_internal_link('/root/doc.md', './target.md#section-two', [])
        self.assertTrue(is_valid)
        self.assertIsNone(reason)

        is_valid, reason = check_internal_link('/root/doc.md', './target.md#section-two-with-spaces', [])
        self.assertTrue(is_valid)
        self.assertIsNone(reason)

    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.dirname', return_value='/root')
    @patch('os.path.normpath', side_effect=lambda x: x)
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_check_internal_link_anchor_not_exists(self, mock_os_path_join, mock_os_path_normpath, mock_os_path_dirname, mock_file_open, mock_os_path_isdir, mock_os_path_exists):
        # Mock rationale: Simulate checking for a non-existent anchor within a file.
        mock_file_open.return_value.read.return_value = (
            "# My Document\n\n"
            "## Existing Section\n"
        )
        is_valid, reason = check_internal_link('/root/doc.md', './target.md#non-existent-anchor', [])
        self.assertFalse(is_valid)
        self.assertIn('Anchor', reason)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    @patch('link_checker.find_markdown_files')
    @patch('link_checker.extract_links')
    @patch('link_checker.check_external_link')
    @patch('link_checker.check_internal_link')
    def test_main_no_broken_links(self, mock_check_internal, mock_check_external, mock_extract_links, mock_find_md_files, mock_sys_exit, mock_stdout):
        # Mock rationale: Simulate a full run where no broken links are found.
        mock_find_md_files.return_value = ['/root/file1.md']
        mock_extract_links.return_value = [
            {'file': 'file1.md', 'line': 1, 'link_text': 'Google', 'url': 'https://google.com'},
            {'file': 'file1.md', 'line': 2, 'link_text': 'Local', 'url': './local.md'}
        ]
        mock_check_external.return_value = (True, None)
        mock_check_internal.return_value = (True, None)

        main()

        self.assertEqual(mock_stdout.getvalue().strip(), '[]')
        mock_sys_exit.assert_called_once_with(0)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    @patch('link_checker.find_markdown_files')
    @patch('link_checker.extract_links')
    @patch('link_checker.check_external_link')
    @patch('link_checker.check_internal_link')
    def test_main_with_broken_links(self, mock_check_internal, mock_check_external, mock_extract_links, mock_find_md_files, mock_sys_exit, mock_stdout):
        # Mock rationale: Simulate a full run where broken links are found.
        mock_find_md_files.return_value = ['/root/file1.md']
        mock_extract_links.return_value = [
            {'file': 'file1.md', 'line': 1, 'link_text': 'Broken External', 'url': 'https://broken.com'},
            {'file': 'file1.md', 'line': 2, 'link_text': 'Broken Internal', 'url': './non-existent.md'}
        ]
        mock_check_external.return_value = (False, 'External link failed: 404')
        mock_check_internal.return_value = (False, 'Internal file not found: /root/non-existent.md')

        main()

        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0]['url'], 'https://broken.com')
        self.assertEqual(output[0]['reason'], 'External link failed: 404')
        self.assertEqual(output[1]['url'], './non-existent.md')
        self.assertEqual(output[1]['reason'], 'Internal file not found: /root/non-existent.md')
        mock_sys_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
