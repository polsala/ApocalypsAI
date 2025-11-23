import unittest
import os
import sys
from unittest.mock import patch, mock_open, MagicMock

# Add the src directory to the path to allow importing link_checker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import link_checker

class TestLinkChecker(unittest.TestCase):

    @patch('os.walk')
    def test_find_markdown_files(self, mock_os_walk):
        # Mock rationale: Simulate a file system structure without actually creating files.
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['file.txt', 'README.md']),
            ('/root/dir1', [], ['doc.markdown', 'image.png']),
            ('/root/dir2', [], ['another.md'])
        ]
        expected_files = [
            os.path.join('/root', 'README.md'),
            os.path.join('/root/dir1', 'doc.markdown'),
            os.path.join('/root/dir2', 'another.md')
        ]
        self.assertEqual(sorted(link_checker.find_markdown_files('/root')), sorted(expected_files))

        mock_os_walk.return_value = [] # No files
        self.assertEqual(link_checker.find_markdown_files('/empty'), [])

    def test_extract_urls_from_markdown(self):
        # Test cases for URL extraction from markdown content.
        content1 = "This is a [link to Google](https://www.google.com) and another [link](http://example.com/path)."
        expected1 = ["https://www.google.com", "http://example.com/path"]
        self.assertEqual(link_checker.extract_urls_from_markdown(content1), expected1)

        content2 = "No links here."
        expected2 = []
        self.assertEqual(link_checker.extract_urls_from_markdown(content2), expected2)

        content3 = "Link with query params: [params](https://example.com/search?q=test&page=1)"
        expected3 = ["https://example.com/search?q=test&page=1"]
        self.assertEqual(link_checker.extract_urls_from_markdown(content3), expected3)

        content4 = "Link with fragment: [fragment](https://example.com/page#section)"
        expected4 = ["https://example.com/page#section"]
        self.assertEqual(link_checker.extract_urls_from_markdown(content4), expected4)

        content5 = "Mixed content: [internal](/local/path) and [external](https://external.com)"
        expected5 = ["https://external.com"]
        self.assertEqual(link_checker.extract_urls_from_markdown(content5), expected5)

    @patch('requests.head')
    def test_check_url_status_ok(self, mock_head):
        # Mock rationale: Simulate a successful HTTP response (200 OK) without actual network calls.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.reason = "OK"
        mock_head.return_value = mock_response

        is_ok, msg = link_checker.check_url_status("https://example.com/valid")
        self.assertTrue(is_ok)
        self.assertEqual(msg, "OK")
        mock_head.assert_called_once_with("https://example.com/valid", timeout=5, allow_redirects=True)

    @patch('requests.head')
    def test_check_url_status_not_found(self, mock_head):
        # Mock rationale: Simulate a 404 Not Found HTTP response without actual network calls.
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_head.return_value = mock_response

        is_ok, msg = link_checker.check_url_status("https://example.com/404")
        self.assertFalse(is_ok)
        self.assertEqual(msg, "404 Not Found")

    @patch('requests.head')
    def test_check_url_status_connection_error(self, mock_head):
        # Mock rationale: Simulate a network connection error without actual network calls.
        mock_head.side_effect = link_checker.requests.exceptions.ConnectionError("Failed to connect")

        is_ok, msg = link_checker.check_url_status("https://example.com/error")
        self.assertFalse(is_ok)
        self.assertEqual(msg, "Connection Error")

    @patch('requests.head')
    def test_check_url_status_timeout(self, mock_head):
        # Mock rationale: Simulate a request timeout without actual network calls.
        mock_head.side_effect = link_checker.requests.exceptions.Timeout("Request timed out")

        is_ok, msg = link_checker.check_url_status("https://example.com/timeout")
        self.assertFalse(is_ok)
        self.assertEqual(msg, "Timeout")

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('requests.head')
    @patch('sys.stdout', new_callable=MagicMock) # Mock stdout to capture print statements
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during tests
    def test_main_no_broken_links(self, mock_exit, mock_stdout, mock_head, mock_open_file, mock_os_walk, mock_isdir):
        # Mock rationale: Simulate a full run where all links are valid.
        # Mock os.walk to find markdown files.
        mock_os_walk.return_value = [
            ('/root', [], ['doc1.md'])
        ]
        # Mock open to provide content for doc1.md.
        mock_open_file.return_value.__enter__.return_value.read.return_value = \
            "This is a [valid link](https://good.example.com)."

        # Mock requests.head for the valid link.
        mock_response_ok = MagicMock()
        mock_response_ok.status_code = 200
        mock_response_ok.reason = "OK"
        mock_head.return_value = mock_response_ok

        # Run main function
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(dir='/root', timeout=5)):
            link_checker.main()

        # Assertions
        mock_exit.assert_called_once_with(0) # Expect successful exit
        output = mock_stdout.getvalue()
        self.assertIn("[✅] https://good.example.com", output)
        self.assertIn("No broken links found. All clear!", output)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('requests.head')
    @patch('sys.stdout', new_callable=MagicMock) # Mock stdout to capture print statements
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during tests
    def test_main_with_broken_links(self, mock_exit, mock_stdout, mock_head, mock_open_file, mock_os_walk, mock_isdir):
        # Mock rationale: Simulate a full run where some links are broken.
        # Mock os.walk to find markdown files.
        mock_os_walk.return_value = [
            ('/root', [], ['doc1.md', 'doc2.md'])
        ]

        # Mock open to provide content for doc1.md and doc2.md.
        # Use a side_effect for read() to return different content for different files.
        mock_open_file.side_effect = [
            mock_open(read_data="[Good Link](https://good.example.com)\n[Bad Link 1](https://bad1.example.com)").return_value,
            mock_open(read_data="[Bad Link 2](https://bad2.example.com)").return_value
        ]

        # Mock requests.head for different URLs.
        mock_response_ok = MagicMock(status_code=200, reason="OK")
        mock_response_bad1 = MagicMock(status_code=404, reason="Not Found")
        mock_response_bad2 = MagicMock(status_code=500, reason="Internal Server Error")

        mock_head.side_effect = [
            mock_response_ok,   # For https://good.example.com
            mock_response_bad1, # For https://bad1.example.com
            mock_response_bad2  # For https://bad2.example.com
        ]

        # Run main function
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(dir='/root', timeout=5)):
            link_checker.main()

        # Assertions
        mock_exit.assert_called_once_with(1) # Expect error exit due to broken links
        output = mock_stdout.getvalue()
        self.assertIn("[✅] https://good.example.com", output)
        self.assertIn("[❌] https://bad1.example.com (Status: 404 Not Found)", output)
        self.assertIn("-> Found in: /root/doc1.md", output)
        self.assertIn("[❌] https://bad2.example.com (Status: 500 Internal Server Error)", output)
        self.assertIn("-> Found in: /root/doc2.md", output)
        self.assertIn("Found 2 broken links:", output)

    @patch('os.path.isdir', return_value=False)
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_main_invalid_directory(self, mock_exit, mock_stdout, mock_isdir):
        # Mock rationale: Simulate an invalid directory path provided to the script.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(dir='/nonexistent', timeout=5)):
            link_checker.main()
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Directory '/nonexistent' not found.", mock_stdout.getvalue())

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[]) # No markdown files found
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_main_no_markdown_files(self, mock_exit, mock_stdout, mock_os_walk, mock_isdir):
        # Mock rationale: Simulate a directory with no markdown files.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(dir='/root', timeout=5)):
            link_checker.main()
        mock_exit.assert_called_once_with(0)
        self.assertIn("No markdown files found.", mock_stdout.getvalue())
