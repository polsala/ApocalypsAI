import unittest
import os
import sys
import io
from unittest.mock import patch, MagicMock

# Add the src directory to the path to allow importing link_checker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import link_checker

class TestLinkChecker(unittest.TestCase):

    @patch('os.walk')
    def test_find_markdown_files(self, mock_os_walk):
        # Mock rationale: Simulate a file system structure without actual disk access.
        mock_os_walk.return_value = [
            ('/repo', ['docs', 'src'], ['README.md', 'LICENSE']),
            ('/repo/docs', [], ['guide.md', 'image.png']),
            ('/repo/src', [], ['main.py'])
        ]
        files = link_checker.find_markdown_files('/repo')
        expected_files = [
            os.path.join('/repo', 'README.md'),
            os.path.join('/repo/docs', 'guide.md')
        ]
        self.assertCountEqual(files, expected_files)

    def test_extract_links(self):
        markdown_content = """
# My Project

This is a [link to Google](https://www.google.com).
And another one: ![GitHub](https://github.com/polsala/ApocalypsAI/logo.png).
Visit our site at https://example.org/path/to/page.html?query=1#fragment.
No link here.
[Local link](/local/path).
"""
        links = link_checker.extract_links(markdown_content)
        expected_links = {
            "https://www.google.com",
            "https://github.com/polsala/ApocalypsAI/logo.png",
            "https://example.org/path/to/page.html?query=1#fragment"
        }
        self.assertSetEqual(links, expected_links)

    @patch('requests.get')
    def test_check_link_success(self, mock_requests_get):
        # Mock rationale: Simulate a successful HTTP request without actual network access.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None # No HTTPError
        mock_requests_get.return_value = mock_response

        url = "https://example.com/valid"
        result_url, status = link_checker.check_link(url)
        self.assertEqual(result_url, url)
        self.assertEqual(status, "200 OK")
        mock_requests_get.assert_called_once_with(url, timeout=5, stream=True, allow_redirects=True)

    @patch('requests.get')
    def test_check_link_failure_404(self, mock_requests_get):
        # Mock rationale: Simulate a 404 Not Found HTTP error.
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_requests_get.return_value = mock_response

        url = "https://example.com/404"
        result_url, status = link_checker.check_link(url)
        self.assertEqual(result_url, url)
        self.assertEqual(status, "404 Not Found")

    @patch('requests.get')
    def test_check_link_timeout(self, mock_requests_get):
        # Mock rationale: Simulate a network timeout during the request.
        mock_requests_get.side_effect = requests.exceptions.Timeout

        url = "https://example.com/timeout"
        result_url, status = link_checker.check_link(url)
        self.assertEqual(result_url, url)
        self.assertEqual(status, "Timeout")

    @patch('requests.get')
    def test_check_link_connection_error(self, mock_requests_get):
        # Mock rationale: Simulate a general connection error (e.g., DNS failure, no internet).
        mock_requests_get.side_effect = requests.exceptions.ConnectionError

        url = "https://example.com/no-connection"
        result_url, status = link_checker.check_link(url)
        self.assertEqual(result_url, url)
        self.assertEqual(status, "Connection Error")

    @patch('os.walk')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('requests.get')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_with_broken_links(self, mock_sys_exit, mock_stdout, mock_requests_get, mock_open, mock_os_walk):
        # Mock rationale: Simulate a full run with a mix of valid and broken links
        # without touching the file system or network, and capture stdout/exit code.

        # Setup mock file system
        mock_os_walk.return_value = [
            ('/repo', [], ['README.md'])
        ]

        # Setup mock file content
        mock_file_handle = MagicMock()
        mock_file_handle.read.return_value = """
# Project README
[Good Link](https://good.example.com)
[Bad Link](https://bad.example.com/404)
[Timeout Link](https://timeout.example.com)
"""
        mock_open.return_value.__enter__.return_value = mock_file_handle

        # Setup mock requests responses
        def mock_get_side_effect(url, **kwargs):
            mock_response = MagicMock()
            if url == "https://good.example.com":
                mock_response.status_code = 200
                mock_response.raise_for_status.return_value = None
            elif url == "https://bad.example.com/404":
                mock_response.status_code = 404
                mock_response.reason = "Not Found"
                mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
            elif url == "https://timeout.example.com":
                raise requests.exceptions.Timeout
            return mock_response

        mock_requests_get.side_effect = mock_get_side_effect

        # Run main function
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/repo')):
            link_checker.main()

        # Assertions
        output = mock_stdout.getvalue()
        self.assertIn("BROKEN LINKS DETECTED!", output)
        self.assertIn("[404 Not Found] https://bad.example.com/404", output)
        self.assertIn("  - Found in: README.md", output)
        self.assertIn("[Timeout] https://timeout.example.com", output)
        self.assertIn("  - Found in: README.md", output)
        self.assertNotIn("https://good.example.com", output)
        mock_sys_exit.assert_called_once_with(1) # Expect exit code 1 for broken links

    @patch('os.walk')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('requests.get')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_no_broken_links(self, mock_sys_exit, mock_stdout, mock_requests_get, mock_open, mock_os_walk):
        # Mock rationale: Simulate a full run where all links are valid.

        mock_os_walk.return_value = [
            ('/repo', [], ['README.md'])
        ]

        mock_file_handle = MagicMock()
        mock_file_handle.read.return_value = """
# Project README
[Good Link 1](https://good1.example.com)
[Good Link 2](https://good2.example.com)
"""
        mock_open.return_value.__enter__.return_value = mock_file_handle

        def mock_get_side_effect(url, **kwargs):
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            return mock_response

        mock_requests_get.side_effect = mock_get_side_effect

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/repo')):
            link_checker.main()

        output = mock_stdout.getvalue()
        self.assertIn("All links are holding strong! The web is perfectly intact!", output)
        self.assertNotIn("BROKEN LINKS DETECTED!", output)
        mock_sys_exit.assert_not_called() # Expect no exit code 1

    @patch('os.walk')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_no_markdown_files(self, mock_stdout, mock_os_walk):
        # Mock rationale: Simulate a directory with no Markdown files.
        mock_os_walk.return_value = [
            ('/repo', [], ['file.txt', 'image.png'])
        ]

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/repo')):
            link_checker.main()

        output = mock_stdout.getvalue()
        self.assertIn("No Markdown files found. The web is calm, for now.", output)

    @patch('os.walk')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_no_external_links(self, mock_stdout, mock_open, mock_os_walk):
        # Mock rationale: Simulate Markdown files that only contain local links.
        mock_os_walk.return_value = [
            ('/repo', [], ['README.md'])
        ]

        mock_file_handle = MagicMock()
        mock_file_handle.read.return_value = """
# Project README
[Local Link](/local/path)
"""
        mock_open.return_value.__enter__.return_value = mock_file_handle

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/repo')):
            link_checker.main()

        output = mock_stdout.getvalue()
        self.assertIn("No external links found to check. The web is perfectly spun!", output)

if __name__ == '__main__':
    unittest.main()
