import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys
from io import StringIO

# Add the src directory to the Python path to import beacon.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import beacon

# Mock requests exceptions for testing
class MockConnectionError(Exception):
    pass
class MockTimeout(Exception):
    pass
class MockRequestException(Exception):
    pass

class TestBeacon(unittest.TestCase):

    def setUp(self):
        # Create a dummy directory structure for testing os.walk
        self.test_dir = 'test_root'
        os.makedirs(os.path.join(self.test_dir, 'subdir1'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'subdir2'), exist_ok=True)

        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()
        # Capture stderr for testing error print statements
        self.held_stderr = sys.stderr
        sys.stderr = self.mock_stderr = StringIO()

    def tearDown(self):
        # Clean up dummy directory structure
        if os.path.exists(self.test_dir):
            for root, dirs, files in os.walk(self.test_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.test_dir)
        
        # Restore stdout and stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_success(self, mock_get, mock_head):
        # Mock rationale: Simulate a successful HTTP HEAD request.
        mock_head.return_value = MagicMock(status_code=200)
        is_ok, msg = beacon.check_link('http://example.com')
        self.assertTrue(is_ok)
        self.assertEqual(msg, 'OK')
        mock_head.assert_called_once_with('http://example.com', timeout=5, allow_redirects=True)
        mock_get.assert_not_called()

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_404_head(self, mock_get, mock_head):
        # Mock rationale: Simulate a 404 Not Found response from an HTTP HEAD request.
        mock_head.return_value = MagicMock(status_code=404)
        is_ok, msg = beacon.check_link('http://broken.com')
        self.assertFalse(is_ok)
        self.assertEqual(msg, 'HTTP 404 (after GET fallback)') # Expect GET fallback for 4xx
        mock_head.assert_called_once()
        mock_get.assert_called_once_with('http://broken.com', timeout=5, allow_redirects=True)

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_head_method_not_allowed_fallback_get_success(self, mock_get, mock_head):
        # Mock rationale: Simulate a server that doesn't allow HEAD (405) but succeeds with GET.
        mock_head.return_value = MagicMock(status_code=405)
        mock_get.return_value = MagicMock(status_code=200)
        is_ok, msg = beacon.check_link('http://head-blocked.com')
        self.assertTrue(is_ok)
        self.assertEqual(msg, 'OK')
        mock_head.assert_called_once()
        mock_get.assert_called_once_with('http://head-blocked.com', timeout=5, allow_redirects=True)

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_head_method_not_allowed_fallback_get_failure(self, mock_get, mock_head):
        # Mock rationale: Simulate a server that doesn't allow HEAD (405) and also fails with GET (404).
        mock_head.return_value = MagicMock(status_code=405)
        mock_get.return_value = MagicMock(status_code=404)
        is_ok, msg = beacon.check_link('http://head-blocked-broken.com')
        self.assertFalse(is_ok)
        self.assertEqual(msg, 'HTTP 404 (after GET fallback)')
        mock_head.assert_called_once()
        mock_get.assert_called_once_with('http://head-blocked-broken.com', timeout=5, allow_redirects=True)

    @patch('requests.head', side_effect=MockConnectionError)
    @patch('requests.get') # Ensure get is also mocked if head fails before get is called
    def test_check_link_connection_error(self, mock_get, mock_head):
        # Mock rationale: Simulate a network connection error.
        is_ok, msg = beacon.check_link('http://no-connection.com')
        self.assertFalse(is_ok)
        self.assertEqual(msg, 'Connection Error')
        mock_head.assert_called_once()
        mock_get.assert_not_called()

    @patch('requests.head', side_effect=MockTimeout)
    @patch('requests.get') # Ensure get is also mocked if head fails before get is called
    def test_check_link_timeout(self, mock_get, mock_head):
        # Mock rationale: Simulate a request timeout.
        is_ok, msg = beacon.check_link('http://slow-server.com')
        self.assertFalse(is_ok)
        self.assertEqual(msg, 'Timeout')
        mock_head.assert_called_once()
        mock_get.assert_not_called()

    @patch('requests.head', side_effect=MockRequestException('Generic error'))
    @patch('requests.get')
    def test_check_link_request_exception(self, mock_get, mock_head):
        # Mock rationale: Simulate a generic requests.exceptions.RequestException.
        is_ok, msg = beacon.check_link('http://error.com')
        self.assertFalse(is_ok)
        self.assertEqual(msg, 'Request Error: Generic error')
        mock_head.assert_called_once()
        mock_get.assert_not_called()

    def test_find_links_in_file(self):
        # Mock rationale: Simulate reading file content from disk without actual file I/O.
        mock_file_content = """
        This is a test file.
        Here's a good link: http://good.com/path/to/resource
        And another: https://secure.org?param=value
        A broken one: http://bad.link
        No link here.
        A link with a semicolon: http://example.com/test;id=123
        """
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as m_open:
            links = beacon.find_links_in_file('dummy.md')
            self.assertIn('http://good.com/path/to/resource', links)
            self.assertIn('https://secure.org?param=value', links)
            self.assertIn('http://bad.link', links)
            self.assertIn('http://example.com/test;id=123', links)
            self.assertEqual(len(links), 4)
            m_open.assert_called_once_with('dummy.md', 'r', encoding='utf-8', errors='ignore')

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('beacon.check_link')
    def test_scan_directory_for_broken_links(self, mock_check_link, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate file system traversal and link checking without actual disk or network I/O.
        # Configure os.walk to return a specific directory structure.
        mock_os_walk.return_value = [
            (self.test_dir, ['subdir1'], ['file1.md', 'file2.txt']),
            (os.path.join(self.test_dir, 'subdir1'), [], ['subfile1.html'])
        ]

        # Configure mock_file_open to return specific content for each file.
        def mock_open_side_effect(filepath, *args, **kwargs):
            if 'file1.md' in filepath:
                return mock_open(read_data='Link: http://good.com\nAnother: http://bad.com').return_value
            elif 'subfile1.html' in filepath:
                return mock_open(read_data='<a href="http://another-bad.org"></a>').return_value
            return mock_open(read_data='').return_value # For other files like file2.txt
        mock_file_open.side_effect = mock_open_side_effect

        # Configure check_link to return specific results for each URL.
        mock_check_link.side_effect = [
            (True, 'OK'),      # http://good.com
            (False, 'HTTP 404 (after GET fallback)'), # http://bad.com
            (False, 'Timeout')  # http://another-bad.org
        ]

        report = beacon.scan_directory_for_broken_links(self.test_dir, ['md', 'html'], 5)

        expected_file1_path = os.path.join(self.test_dir, 'file1.md')
        expected_subfile1_path = os.path.join(self.test_dir, 'subdir1', 'subfile1.html')

        self.assertIn(expected_file1_path, report)
        self.assertIn(expected_subfile1_path, report)
        self.assertEqual(len(report[expected_file1_path]), 1)
        self.assertEqual(report[expected_file1_path][0], ('http://bad.com', 'HTTP 404 (after GET fallback)'))
        self.assertEqual(len(report[expected_subfile1_path]), 1)
        self.assertEqual(report[expected_subfile1_path][0], ('http://another-bad.org', 'Timeout'))
        self.assertEqual(mock_check_link.call_count, 3)

    @patch('os.path.isdir', return_value=True)
    @patch('beacon.scan_directory_for_broken_links', return_value={})
    @patch('sys.exit')
    def test_main_no_broken_links(self, mock_exit, mock_scan_dir, mock_isdir):
        # Mock rationale: Simulate a successful run of the main function where no broken links are found.
        # Mock argparse to control command-line arguments.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path=self.test_dir, file_types=['md'], timeout=5
        )):
            beacon.main()
            mock_scan_dir.assert_called_once_with(self.test_dir, ['md'], 5)
            mock_exit.assert_called_once_with(0)
            self.assertIn('No broken links found. All clear!', self.mock_stdout.getvalue())

    @patch('os.path.isdir', return_value=True)
    @patch('beacon.scan_directory_for_broken_links', return_value={
        'path/to/file.md': [('http://broken.com', 'HTTP 404 (after GET fallback)')]
    })
    @patch('sys.exit')
    def test_main_with_broken_links(self, mock_exit, mock_scan_dir, mock_isdir):
        # Mock rationale: Simulate a run of the main function where broken links are found.
        # Mock argparse to control command-line arguments.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path=self.test_dir, file_types=['md'], timeout=5
        )):
            beacon.main()
            mock_scan_dir.assert_called_once_with(self.test_dir, ['md'], 5)
            mock_exit.assert_called_once_with(1)
            output = self.mock_stdout.getvalue()
            self.assertIn('--- Broken Link Report ---', output)
            self.assertIn('File: path/to/file.md', output)
            self.assertIn('  - http://broken.com (HTTP 404 (after GET fallback))', output)

    @patch('os.path.isdir', return_value=False)
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_exit, mock_isdir):
        # Mock rationale: Simulate an invalid directory path provided to the main function.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path='non_existent_dir', file_types=['md'], timeout=5
        )):
            beacon.main()
            mock_isdir.assert_called_once_with('non_existent_dir')
            mock_exit.assert_called_once_with(1)
            self.assertIn('Error: Directory not found: non_existent_dir', self.mock_stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
