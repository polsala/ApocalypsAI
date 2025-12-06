import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import requests

# Store original sys.argv to restore it after tests
original_argv = sys.argv

# Mock response object for requests.head
class MockResponse:
    def __init__(self, status_code, content=b''):
        self.status_code = status_code
        self.content = content

    def raise_for_status(self):
        if 400 <= self.status_code < 600:
            raise requests.exceptions.HTTPError(f"Mock HTTP Error: {self.status_code}")

class TestLinkLoomer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Temporarily add the src directory to the Python path to allow importing link_loomer
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
        # Import the module after modifying sys.path
        global link_loomer
        import link_loomer

    @classmethod
    def tearDownClass(cls):
        # Clean up sys.path
        sys.path.pop(0)

    def setUp(self):
        # Reset sys.argv before each test that calls main to ensure isolation
        sys.argv = original_argv[:]

    @patch('os.walk')
    def test_find_markdown_files(self, mock_os_walk):
        # Mock rationale: Simulate a file system structure without actual disk access.
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['file.txt', 'doc.md']),
            ('/root/dir1', [], ['another.md', 'image.png']),
            ('/root/dir2', [], ['report.pdf'])
        ]
        files = link_loomer.find_markdown_files('/root')
        expected_files = [
            os.path.join('/root', 'doc.md'),
            os.path.join('/root/dir1', 'another.md')
        ]
        self.assertCountEqual(files, expected_files)

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_extract_external_links_no_links(self, mock_open):
        # Mock rationale: Simulate reading a file with no external links.
        mock_open.return_value.read.return_value = "# Header\nSome text here.\n[Local Link](/path/to/local)."
        links = link_loomer.extract_external_links('dummy.md')
        self.assertEqual(links, [])

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_extract_external_links_valid_formats(self, mock_open):
        # Mock rationale: Simulate reading a file with various external link formats.
        markdown_content = """
        # My Document
        This is a [link to Google](https://www.google.com).
        Another link: <http://example.com/page>.
        A secure link: [Secure Site](https://secure.org/path?q=test).
        Internal link: [Local](/local/path).
        Relative link: [Relative](./relative.md).
        Link with spaces in text [Link with spaces](https://spaces.com/path).
        """
        mock_open.return_value.read.return_value = markdown_content
        links = link_loomer.extract_external_links('dummy.md')
        expected_links = sorted([
            'https://www.google.com',
            'http://example.com/page',
            'https://secure.org/path?q=test',
            'https://spaces.com/path'
        ])
        self.assertEqual(links, expected_links)

    @patch('requests.head')
    def test_check_link_success(self, mock_head):
        # Mock rationale: Simulate a successful HTTP HEAD request (200 OK).
        mock_head.return_value = MockResponse(200)
        is_valid, status = link_loomer.check_link('http://valid.com')
        self.assertTrue(is_valid)
        self.assertEqual(status, 200)
        mock_head.assert_called_once_with(
            'http://valid.com', timeout=5, allow_redirects=True,
            headers={'User-Agent': 'ApocalypsAI/NightlyLinkLoomer (https://github.com/polsala/ApocalypsAI)'}
        )

    @patch('requests.head')
    def test_check_link_redirect_success(self, mock_head):
        # Mock rationale: Simulate a successful HTTP HEAD request with a redirect (301 Moved Permanently).
        mock_head.return_value = MockResponse(301)
        is_valid, status = link_loomer.check_link('http://redirect.com')
        self.assertTrue(is_valid)
        self.assertEqual(status, 301)

    @patch('requests.head')
    def test_check_link_not_found(self, mock_head):
        # Mock rationale: Simulate a 404 Not Found error.
        mock_head.return_value = MockResponse(404)
        is_valid, status = link_loomer.check_link('http://notfound.com')
        self.assertFalse(is_valid)
        self.assertEqual(status, 404)

    @patch('requests.head')
    def test_check_link_server_error(self, mock_head):
        # Mock rationale: Simulate a 500 Internal Server Error.
        mock_head.return_value = MockResponse(500)
        is_valid, status = link_loomer.check_link('http://servererror.com')
        self.assertFalse(is_valid)
        self.assertEqual(status, 500)

    @patch('requests.head')
    def test_check_link_network_error(self, mock_head):
        # Mock rationale: Simulate a network-related exception (e.g., connection refused, timeout).
        mock_head.side_effect = requests.exceptions.ConnectionError("Mock Connection Error")
        is_valid, status = link_loomer.check_link('http://networkerror.com')
        self.assertFalse(is_valid)
        self.assertEqual(status, 0) # 0 indicates network error

    @patch('link_loomer.find_markdown_files')
    @patch('link_loomer.extract_external_links')
    @patch('link_loomer.check_link')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_main_no_markdown_files(self, mock_exit, mock_stdout, mock_check_link, mock_extract_links, mock_find_files):
        # Mock rationale: Simulate a scenario where no Markdown files are found in the target directory.
        sys.argv = ['link_loomer.py', '/test/dir']
        mock_find_files.return_value = []
        link_loomer.main()
        mock_exit.assert_called_once_with(0)
        mock_stdout.write.assert_any_call('No Markdown files found to scan.\n')

    @patch('link_loomer.find_markdown_files')
    @patch('link_loomer.extract_external_links')
    @patch('link_loomer.check_link')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_main_all_links_valid(self, mock_exit, mock_stdout, mock_check_link, mock_extract_links, mock_find_files):
        # Mock rationale: Simulate a scenario where all extracted links are valid.
        sys.argv = ['link_loomer.py', '/test/dir']
        mock_find_files.return_value = ['/test/dir/doc.md']
        mock_extract_links.return_value = ['http://valid1.com', 'https://valid2.org']
        mock_check_link.side_effect = [
            (True, 200), # for http://valid1.com
            (True, 200)  # for https://valid2.org
        ]
        link_loomer.main()
        mock_exit.assert_called_once_with(0)
        mock_stdout.write.assert_any_call('All external links are robust! The digital fabric holds strong. ✅\n')

    @patch('link_loomer.find_markdown_files')
    @patch('link_loomer.extract_external_links')
    @patch('link_loomer.check_link')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_main_broken_links_found(self, mock_exit, mock_stdout, mock_check_link, mock_extract_links, mock_find_files):
        # Mock rationale: Simulate a scenario where some links are broken, leading to a non-zero exit code.
        sys.argv = ['link_loomer.py', '/test/dir']
        mock_find_files.return_value = ['/test/dir/doc.md', '/test/dir/another.md']
        mock_extract_links.side_effect = [
            ['http://valid.com', 'http://broken1.com'], # for doc.md
            ['https://broken2.org'] # for another.md
        ]
        mock_check_link.side_effect = [
            (True, 200),  # http://valid.com
            (False, 404), # http://broken1.com
            (False, 0)    # https://broken2.org (network error)
        ]
        link_loomer.main()
        mock_exit.assert_called_once_with(1)
        mock_stdout.write.assert_any_call('The Nightly Link-Loomer has detected the following digital decay:\n\n')
        mock_stdout.write.assert_any_call('File: /test/dir/doc.md\n')
        mock_stdout.write.assert_any_call('  - http://broken1.com (Status: 404)\n')
        mock_stdout.write.assert_any_call('File: /test/dir/another.md\n')
        mock_stdout.write.assert_any_call('  - https://broken2.org (Network Error)\n')

    @patch('os.path.isdir')
    @patch('sys.exit')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_invalid_directory(self, mock_stdout, mock_exit, mock_isdir):
        # Mock rationale: Simulate providing an invalid directory path as an argument.
        sys.argv = ['link_loomer.py', '/nonexistent/dir']
        mock_isdir.return_value = False
        link_loomer.main()
        mock_exit.assert_called_once_with(1)
        mock_stdout.write.assert_any_call('Error: Directory not found: /nonexistent/dir\n')

    @patch('sys.exit')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_no_arguments(self, mock_stdout, mock_exit):
        # Mock rationale: Simulate running the script without any arguments.
        sys.argv = ['link_loomer.py']
        link_loomer.main()
        mock_exit.assert_called_once_with(1)
        mock_stdout.write.assert_any_call('Usage: python src/link_loomer.py <directory_path>\n')
