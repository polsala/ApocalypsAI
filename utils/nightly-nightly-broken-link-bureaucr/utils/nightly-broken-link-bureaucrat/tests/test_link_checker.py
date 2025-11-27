import unittest
import os
from unittest.mock import patch, MagicMock
from src.link_checker import (
    find_markdown_files,
    extract_links,
    check_external_link,
    check_internal_link,
    main
)

class TestLinkChecker(unittest.TestCase):

    # Mock rationale: os.walk is a file system operation. Mocking it allows
    # us to simulate different directory structures without touching the actual disk.
    @patch('os.walk')
    def test_find_markdown_files(self, mock_os_walk):
        mock_os_walk.return_value = [
            ('/repo', ('dir1', 'dir2'), ('README.md', 'file.txt')),
            ('/repo/dir1', (), ('doc.md', 'image.png')),
            ('/repo/dir2', (), ('subdoc.md',)),
        ]
        
        files = find_markdown_files('/repo')
        expected_files = [
            os.path.join('/repo', 'README.md'),
            os.path.join('/repo/dir1', 'doc.md'),
            os.path.join('/repo/dir2', 'subdoc.md'),
        ]
        self.assertCountEqual(files, expected_files)

        mock_os_walk.return_value = []
        self.assertEqual(find_markdown_files('/empty'), [])

    def test_extract_links(self):
        markdown_content = """
        # My Document

        This is a [link to Google](https://www.google.com).
        Here's another [internal link](../docs/another.md).
        And an image: ![alt text](images/pic.png).
        A link with an anchor: [section](#section-id).
        A link to another file with an anchor: [other file](other.md#anchor).
        A broken external link: [bad link](http://nonexistent.com/page).
        """
        base_path = '/repo/current_doc.md'
        links = extract_links(markdown_content, base_path)
        
        expected_links = [
            {'url': 'https://www.google.com', 'type': 'external', 'base_path': base_path},
            {'url': '../docs/another.md', 'type': 'internal', 'base_path': base_path},
            {'url': 'images/pic.png', 'type': 'internal', 'base_path': base_path},
            {'url': 'other.md', 'type': 'internal', 'base_path': base_path},
            {'url': 'http://nonexistent.com/page', 'type': 'external', 'base_path': base_path},
        ]
        
        # Sort for deterministic comparison, as order might vary slightly based on regex
        sorted_links = sorted(links, key=lambda x: x['url'])
        sorted_expected = sorted(expected_links, key=lambda x: x['url'])
        
        self.assertEqual(sorted_links, sorted_expected)

    # Mock rationale: requests.head performs network I/O. Mocking it allows
    # us to simulate various HTTP responses (success, failure, redirects)
    # without making actual network calls, ensuring deterministic and fast tests.
    @patch('requests.head')
    def test_check_external_link(self, mock_head):
        # Test successful link
        mock_response_ok = MagicMock()
        mock_response_ok.status_code = 200
        mock_head.return_value = mock_response_ok
        self.assertTrue(check_external_link('http://example.com/ok'))

        # Test redirect link (still considered good)
        mock_response_redirect = MagicMock()
        mock_response_redirect.status_code = 301
        mock_head.return_value = mock_response_redirect
        self.assertTrue(check_external_link('http://example.com/redirect'))

        # Test broken link (404)
        mock_response_not_found = MagicMock()
        mock_response_not_found.status_code = 404
        mock_head.return_value = mock_response_not_found
        self.assertFalse(check_external_link('http://example.com/404'))

        # Test network error
        mock_head.side_effect = requests.exceptions.RequestException("Connection error")
        self.assertFalse(check_external_link('http://example.com/error'))

    # Mock rationale: os.path.exists is a file system operation. Mocking it allows
    # us to simulate the presence or absence of files on disk without
    # actually creating or deleting files, making tests fast and isolated.
    @patch('os.path.exists')
    @patch('os.path.normpath') # Mock rationale: os.path.normpath is a path manipulation function.
                               # Mocking it ensures consistent path resolution in tests,
                               # independent of the underlying OS path conventions.
    @patch('os.path.join')     # Mock rationale: os.path.join is a path manipulation function.
                               # Mocking it ensures consistent path construction in tests.
    @patch('os.path.dirname')  # Mock rationale: os.path.dirname is a path manipulation function.
                               # Mocking it ensures consistent directory extraction in tests.
    def test_check_internal_link(self, mock_dirname, mock_join, mock_normpath, mock_exists):
        root_dir = '/repo'
        
        # Setup mocks for path manipulation
        mock_dirname.return_value = '/repo/docs'
        mock_join.side_effect = lambda *args: os.path.join(*args) # Use real join for path construction
        mock_normpath.side_effect = lambda path: os.path.normpath(path) # Use real normpath

        # Test existing file
        mock_exists.return_value = True
        self.assertTrue(check_internal_link('sub/file.md', '/repo/docs/current.md', root_dir))
        mock_exists.assert_called_with(os.path.join('/repo/docs', 'sub/file.md'))

        # Test non-existing file
        mock_exists.return_value = False
        self.assertFalse(check_internal_link('nonexistent.md', '/repo/docs/current.md', root_dir))
        mock_exists.assert_called_with(os.path.join('/repo/docs', 'nonexistent.md'))

        # Test link outside root_dir (security check)
        mock_dirname.return_value = '/repo/docs'
        mock_join.side_effect = lambda base, rel: '/outside_repo/secret.txt' if rel == '../../secret.txt' else os.path.join(base, rel)
        mock_normpath.side_effect = lambda path: path # Assume normpath doesn't change it for this test
        mock_exists.return_value = True # Even if it exists, it should be rejected
        self.assertFalse(check_internal_link('../../secret.txt', '/repo/docs/current.md', root_dir))


    # Mock rationale: main involves file system access (os.getcwd, open, os.walk)
    # and network requests (requests.head). Mocking these allows us to run the
    # entire main logic in isolation, simulating a repository structure and
    # network responses without side effects or actual I/O.
    @patch('os.getcwd', return_value='/mock_repo')
    @patch('src.link_checker.find_markdown_files')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('src.link_checker.check_external_link')
    @patch('src.link_checker.check_internal_link')
    @patch('builtins.print') # Mock rationale: Capture print output for assertion.
    def test_main_with_broken_links(self, mock_print, mock_check_internal, mock_check_external, mock_open, mock_find_md_files, mock_getcwd):
        mock_find_md_files.return_value = ['/mock_repo/README.md', '/mock_repo/docs/guide.md']

        # Mock file content
        mock_file_content = {
            '/mock_repo/README.md': "[Google](https://www.google.com)\n[Broken External](http://bad.com)\n[Internal Doc](docs/guide.md)\n[Broken Internal](nonexistent.md)",
            '/mock_repo/docs/guide.md': "[Another External](https://example.com)\n[Relative Internal](../README.md)"
        }
        
        # Configure mock_open to return different content based on file path
        mock_open.side_effect = lambda filename, mode, encoding: MagicMock(
            __enter__=lambda *args: MagicMock(read=lambda: mock_file_content[filename]),
            __exit__=lambda *args: None
        )

        # Configure link checker mocks
        mock_check_external.side_effect = lambda url: url == 'https://www.google.com' or url == 'https://example.com'
        mock_check_internal.side_effect = lambda path, base_file_path, root_dir: path == 'docs/guide.md' or path == '../README.md'

        main()

        # Assertions on print calls
        mock_print.assert_any_call("\n--- Broken Link Report ---")
        mock_print.assert_any_call("File: README.md")
        mock_print.assert_any_call("  Link: http://bad.com")
        mock_print.assert_any_call("  Type: External")
        mock_print.assert_any_call("  Reason: Unreachable or invalid URL")
        mock_print.assert_any_call("File: README.md")
        mock_print.assert_any_call("  Link: nonexistent.md")
        mock_print.assert_any_call("  Type: Internal")
        mock_print.assert_any_call("  Reason: File does not exist")
        
        # Ensure 'All links checked...' is NOT called
        self.assertNotIn("\nAll links checked and found to be in perfect working order! Good job, Bureaucrat.", [call.args[0] for call.args in mock_print.call_args_list])

    @patch('os.getcwd', return_value='/mock_repo')
    @patch('src.link_checker.find_markdown_files')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('src.link_checker.check_external_link', return_value=True)
    @patch('src.link_checker.check_internal_link', return_value=True)
    @patch('builtins.print')
    def test_main_with_no_broken_links(self, mock_print, mock_check_internal, mock_check_external, mock_open, mock_find_md_files, mock_getcwd):
        mock_find_md_files.return_value = ['/mock_repo/README.md']
        mock_open.return_value.__enter__.return_value.read.return_value = "[Google](https://www.google.com)\n[Internal Doc](docs/guide.md)"

        main()

        mock_print.assert_any_call("\nAll links checked and found to be in perfect working order! Good job, Bureaucrat.")
        # Ensure 'Broken Link Report' is NOT called
        self.assertNotIn("\n--- Broken Link Report ---", [call.args[0] for call.args in mock_print.call_args_list])

    @patch('os.getcwd', return_value='/mock_repo')
    @patch('src.link_checker.find_markdown_files', return_value=[])
    @patch('builtins.print')
    def test_main_no_markdown_files(self, mock_print, mock_find_md_files, mock_getcwd):
        main()
        mock_print.assert_any_call("No Markdown files found to check.")


if __name__ == '__main__':
    unittest.main()
