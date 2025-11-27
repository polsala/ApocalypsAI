import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import requests
from src import scavenger

class TestScavenger(unittest.TestCase):

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_success(self, mock_get, mock_head):
        # Mock rationale: Simulate a successful HTTP HEAD request.
        mock_head.return_value = MagicMock(status_code=200, reason='OK', request=MagicMock(method='HEAD'))
        is_ok, status_message = scavenger.check_link("https://example.com/valid")
        self.assertTrue(is_ok)
        self.assertIn("200 OK", status_message)
        mock_head.assert_called_once_with("https://example.com/valid", allow_redirects=True, timeout=5)
        mock_get.assert_not_called()

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_broken_404(self, mock_get, mock_head):
        # Mock rationale: Simulate a broken link (HTTP 404) with HEAD request.
        mock_head.return_value = MagicMock(status_code=404, reason='Not Found', request=MagicMock(method='HEAD'))
        is_ok, status_message = scavenger.check_link("https://example.com/broken")
        self.assertFalse(is_ok)
        self.assertIn("404 Not Found", status_message)
        mock_head.assert_called_once_with("https://example.com/broken", allow_redirects=True, timeout=5)
        mock_get.assert_called_once_with("https://example.com/broken", allow_redirects=True, timeout=5) # Fallback to GET

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_broken_500(self, mock_get, mock_head):
        # Mock rationale: Simulate a server error (HTTP 500) with HEAD request.
        mock_head.return_value = MagicMock(status_code=500, reason='Internal Server Error', request=MagicMock(method='HEAD'))
        is_ok, status_message = scavenger.check_link("https://example.com/server-error")
        self.assertFalse(is_ok)
        self.assertIn("500 Internal Server Error", status_message)
        mock_head.assert_called_once_with("https://example.com/server-error", allow_redirects=True, timeout=5)
        mock_get.assert_called_once_with("https://example.com/server-error", allow_redirects=True, timeout=5) # Fallback to GET

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_timeout(self, mock_get, mock_head):
        # Mock rationale: Simulate a network timeout during the request.
        mock_head.side_effect = requests.exceptions.Timeout("Connection timed out")
        is_ok, status_message = scavenger.check_link("https://example.com/timeout")
        self.assertFalse(is_ok)
        self.assertIn("Connection timed out", status_message)
        mock_head.assert_called_once_with("https://example.com/timeout", allow_redirects=True, timeout=5)
        mock_get.assert_not_called()

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_connection_error(self, mock_get, mock_head):
        # Mock rationale: Simulate a general connection error.
        mock_head.side_effect = requests.exceptions.ConnectionError("Failed to connect")
        is_ok, status_message = scavenger.check_link("https://example.com/no-connection")
        self.assertFalse(is_ok)
        self.assertIn("Connection failed", status_message)
        mock_head.assert_called_once_with("https://example.com/no-connection", allow_redirects=True, timeout=5)
        mock_get.assert_not_called()

    def test_find_links(self):
        content = """
        This is a [link to Google](https://www.google.com).
        Another link: [GitHub](https://github.com/polsala/ApocalypsAI).
        No link here.
        [Invalid link](ftp://not-http.com).
        [Relative link](/path/to/file).
        """
        links = scavenger.find_links(content)
        self.assertEqual(len(links), 2)
        self.assertIn("https://www.google.com", links)
        self.assertIn("https://github.com/polsala/ApocalypsAI", links)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.scavenger.check_link')
    def test_scan_directory_no_broken_links(self, mock_check_link, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate file system traversal and all links being valid.
        mock_os_walk.return_value = [
            ('/repo', ('dir1',), ('README.md', 'file.txt')),
            ('/repo/dir1', (), ('DOC.markdown',))
        ]
        mock_file_open.side_effect = [
            mock_open(read_data="[Valid Link](https://good.com)").return_value,
            mock_open(read_data="[Another Valid Link](https://another.good.com)").return_value
        ]
        mock_check_link.side_effect = [
            (True, "Status: 200 OK"),
            (True, "Status: 200 OK")
        ]

        broken_links = scavenger.scan_directory('./repo', ['.md', '.markdown'])
        self.assertEqual(len(broken_links), 0)
        self.assertEqual(mock_check_link.call_count, 2)
        mock_os_walk.assert_called_once_with('./repo')
        self.assertEqual(mock_file_open.call_count, 2)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.scavenger.check_link')
    def test_scan_directory_with_broken_links(self, mock_check_link, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate file system traversal and some links being broken.
        mock_os_walk.return_value = [
            ('/repo', (), ('README.md',))
        ]
        mock_file_open.return_value = mock_open(read_data="[Valid Link](https://good.com)\n[Broken Link](https://bad.com)").return_value
        mock_check_link.side_effect = [
            (True, "Status: 200 OK"),
            (False, "Status: 404 Not Found")
        ]

        broken_links = scavenger.scan_directory('./repo', ['.md'])
        self.assertEqual(len(broken_links), 1)
        self.assertIn('./repo/README.md', broken_links)
        self.assertEqual(len(broken_links['./repo/README.md']), 1)
        self.assertEqual(broken_links['./repo/README.md'][0], ('https://bad.com', 'Status: 404 Not Found'))
        self.assertEqual(mock_check_link.call_count, 2)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.scavenger.check_link')
    def test_scan_directory_file_read_error(self, mock_check_link, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a file that cannot be read (e.g., permissions error).
        mock_os_walk.return_value = [
            ('/repo', (), ('README.md',))
        ]
        mock_file_open.side_effect = IOError("Permission denied")

        broken_links = scavenger.scan_directory('./repo', ['.md'])
        self.assertEqual(len(broken_links), 0) # No links processed, so no broken links reported
        mock_check_link.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.scavenger.scan_directory')
    @patch('sys.exit')
    def test_main_no_broken_links(self, mock_sys_exit, mock_scan_directory, mock_parse_args):
        # Mock rationale: Simulate main execution path where no broken links are found.
        mock_parse_args.return_value = MagicMock(root_dir='./test_repo', file_extensions=['.md'])
        mock_scan_directory.return_value = {}

        scavenger.main()
        mock_scan_directory.assert_called_once_with('./test_repo', ['.md'])
        mock_sys_exit.assert_called_once_with(0)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.scavenger.scan_directory')
    @patch('sys.exit')
    def test_main_with_broken_links(self, mock_sys_exit, mock_scan_directory, mock_parse_args):
        # Mock rationale: Simulate main execution path where broken links are found.
        mock_parse_args.return_value = MagicMock(root_dir='./test_repo', file_extensions=['.md'])
        mock_scan_directory.return_value = {
            './test_repo/README.md': [('https://bad.com', 'Status: 404 Not Found')]
        }

        scavenger.main()
        mock_scan_directory.assert_called_once_with('./test_repo', ['.md'])
        mock_sys_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
