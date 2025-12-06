import unittest
from unittest.mock import patch, MagicMock
import os
import requests
from src.collector import find_urls_in_text, check_url_reachability, collect_broken_links

class TestCollector(unittest.TestCase):

    def test_find_urls_in_text(self):
        text = "This is a [link](https://example.com/page) and a raw url https://another.org/path. Also, no link here."
        urls = find_urls_in_text(text)
        self.assertIn("https://example.com/page", urls)
        self.assertIn("https://another.org/path", urls)
        self.assertEqual(len(urls), 2)

        text_no_links = "Just plain text."
        urls_no_links = find_urls_in_text(text_no_links)
        self.assertEqual(len(urls_no_links), 0)

        text_multiple_same_link = "[Link1](https://same.com) and [Link2](https://same.com) and https://same.com"
        urls_multiple = find_urls_in_text(text_multiple_same_link)
        self.assertEqual(len(urls_multiple), 1)
        self.assertIn("https://same.com", urls_multiple)

        text_mixed_content = "Code comment: # See more at https://docs.example.com/api. Markdown link: [API Ref](https://api.example.com/v1)."
        urls_mixed = find_urls_in_text(text_mixed_content)
        self.assertEqual(len(urls_mixed), 2)
        self.assertIn("https://docs.example.com/api", urls_mixed)
        self.assertIn("https://api.example.com/v1", urls_mixed)

    @patch('requests.head')
    # Mock rationale: `requests.head` performs network I/O, which must be avoided in deterministic offline tests.
    @patch('requests.get')
    # Mock rationale: `requests.get` performs network I/O, used as a fallback, must be avoided in deterministic offline tests.
    def test_check_url_reachability_success(self, mock_get, mock_head):
        mock_head.return_value.status_code = 200
        mock_head.return_value.raise_for_status.return_value = None
        self.assertTrue(check_url_reachability("https://good.com"))
        mock_head.assert_called_once_with("https://good.com", timeout=5.0, allow_redirects=True)
        mock_get.assert_not_called()

    @patch('requests.head')
    # Mock rationale: `requests.head` performs network I/O, which must be avoided in deterministic offline tests.
    @patch('requests.get')
    # Mock rationale: `requests.get` performs network I/O, used as a fallback, must be avoided in deterministic offline tests.
    def test_check_url_reachability_http_error(self, mock_get, mock_head):
        mock_head.side_effect = requests.exceptions.HTTPError(response=MagicMock(status_code=404))
        self.assertFalse(check_url_reachability("https://bad.com/404"))
        mock_head.assert_called_once()
        mock_get.assert_not_called()

    @patch('requests.head')
    # Mock rationale: `requests.head` performs network I/O, which must be avoided in deterministic offline tests.
    @patch('requests.get')
    # Mock rationale: `requests.get` performs network I/O, used as a fallback, must be avoided in deterministic offline tests.
    def test_check_url_reachability_connection_error(self, mock_get, mock_head):
        mock_head.side_effect = requests.exceptions.ConnectionError
        self.assertFalse(check_url_reachability("https://unreachable.com"))
        mock_head.assert_called_once()
        mock_get.assert_not_called()

    @patch('requests.head')
    # Mock rationale: `requests.head` performs network I/O, which must be avoided in deterministic offline tests.
    @patch('requests.get')
    # Mock rationale: `requests.get` performs network I/O, used as a fallback, must be avoided in deterministic offline tests.
    def test_check_url_reachability_head_not_allowed_fallback_get_success(self, mock_get, mock_head):
        # Simulate HEAD returning 405, then GET succeeding
        mock_head.side_effect = requests.exceptions.HTTPError(response=MagicMock(status_code=405))
        mock_get.return_value.status_code = 200
        mock_get.return_value.raise_for_status.return_value = None

        self.assertTrue(check_url_reachability("https://head-forbidden.com"))
        mock_head.assert_called_once()
        mock_get.assert_called_once_with("https://head-forbidden.com", timeout=5.0, allow_redirects=True)

    @patch('requests.head')
    # Mock rationale: `requests.head` performs network I/O, which must be avoided in deterministic offline tests.
    @patch('requests.get')
    # Mock rationale: `requests.get` performs network I/O, used as a fallback, must be avoided in deterministic offline tests.
    def test_check_url_reachability_head_not_allowed_fallback_get_failure(self, mock_get, mock_head):
        # Simulate HEAD returning 405, then GET failing
        mock_head.side_effect = requests.exceptions.HTTPError(response=MagicMock(status_code=405))
        mock_get.side_effect = requests.exceptions.RequestException

        self.assertFalse(check_url_reachability("https://head-forbidden-get-fails.com"))
        mock_head.assert_called_once()
        mock_get.assert_called_once()

    @patch('os.walk')
    # Mock rationale: `os.walk` performs file system I/O, which must be avoided in deterministic offline tests.
    @patch('builtins.open', new_callable=MagicMock)
    # Mock rationale: `builtins.open` performs file system I/O, which must be avoided in deterministic offline tests.
    @patch('src.collector.check_url_reachability')
    # Mock rationale: `check_url_reachability` performs network I/O, which must be avoided in deterministic offline tests.
    def test_collect_broken_links(self, mock_check_url_reachability, mock_open, mock_os_walk):
        # Setup mock file system
        mock_os_walk.return_value = [
            ('/root', [], ['file1.md', 'file2.py']),
            ('/root/subdir', [], ['file3.txt', 'ignore.log'])
        ]

        # Setup mock file contents
        mock_file_contents = {
            os.path.join('/root', 'file1.md'): "[Good Link](https://good.com) and [Bad Link](https://bad.com)",
            os.path.join('/root', 'file2.py'): "# Comment with https://another-good.org and https://another-bad.org",
            os.path.join('/root/subdir', 'file3.txt'): "Plain text with https://good-txt.net and https://bad-txt.net"
        }

        def mock_open_side_effect(filepath, *args, **kwargs):
            mock_file = MagicMock()
            mock_file.read.return_value = mock_file_contents[filepath]
            return mock_file

        mock_open.side_effect = mock_open_side_effect

        # Setup mock URL reachability checks
        def mock_check_side_effect(url, *args, **kwargs):
            if 'good' in url:
                return True
            elif 'bad' in url:
                return False
            return True # Default to true for unexpected URLs

        mock_check_url_reachability.side_effect = mock_check_side_effect

        # Run the collector
        broken_links = collect_broken_links('/root', ['md', 'py', 'txt'])

        # Assertions
        expected_broken_links = {
            os.path.join('/root', 'file1.md'): ['https://bad.com'],
            os.path.join('/root', 'file2.py'): ['https://another-bad.org'],
            os.path.join('/root/subdir', 'file3.txt'): ['https://bad-txt.net']
        }

        self.assertDictEqual(broken_links, expected_broken_links)

        # Ensure all relevant URLs were checked
        expected_checked_urls = {
            'https://good.com',
            'https://bad.com',
            'https://another-good.org',
            'https://another-bad.org',
            'https://good-txt.net',
            'https://bad-txt.net'
        }
        actual_checked_urls = {call.args[0] for call in mock_check_url_reachability.call_args_list}
        self.assertSetEqual(actual_checked_urls, expected_checked_urls)

    @patch('os.walk')
    # Mock rationale: `os.walk` performs file system I/O, which must be avoided in deterministic offline tests.
    @patch('builtins.open', new_callable=MagicMock)
    # Mock rationale: `builtins.open` performs file system I/O, which must be avoided in deterministic offline tests.
    @patch('src.collector.check_url_reachability')
    # Mock rationale: `check_url_reachability` performs network I/O, which must be avoided in deterministic offline tests.
    def test_collect_broken_links_no_broken_links(self, mock_check_url_reachability, mock_open, mock_os_walk):
        mock_os_walk.return_value = [
            ('/root', [], ['file1.md'])
        ]
        mock_file_contents = {
            os.path.join('/root', 'file1.md'): "[Good Link](https://all-good.com)"
        }
        mock_open.side_effect = lambda filepath, *args, **kwargs: MagicMock(read=MagicMock(return_value=mock_file_contents[filepath]))
        mock_check_url_reachability.return_value = True # All links are good

        broken_links = collect_broken_links('/root', ['md'])
        self.assertEqual(len(broken_links), 0)

    @patch('os.walk')
    # Mock rationale: `os.walk` performs file system I/O, which must be avoided in deterministic offline tests.
    @patch('builtins.open', new_callable=MagicMock)
    # Mock rationale: `builtins.open` performs file system I/O, which must be avoided in deterministic offline tests.
    @patch('src.collector.check_url_reachability')
    # Mock rationale: `check_url_reachability` performs network I/O, which must be avoided in deterministic offline tests.
    def test_collect_broken_links_file_read_error(self, mock_check_url_reachability, mock_open, mock_os_walk):
        mock_os_walk.return_value = [
            ('/root', [], ['file1.md'])
        ]
        # Simulate file read error by making open raise an IOError
        mock_open.side_effect = IOError("Permission denied")

        # Ensure it doesn't crash and returns an empty dict (or handles gracefully)
        broken_links = collect_broken_links('/root', ['md'])
        self.assertEqual(len(broken_links), 0)
        mock_check_url_reachability.assert_not_called() # No URLs to check if file can't be read

if __name__ == '__main__':
    unittest.main()
