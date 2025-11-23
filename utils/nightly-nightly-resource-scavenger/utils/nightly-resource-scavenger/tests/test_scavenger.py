import unittest
import os
from unittest.mock import patch, MagicMock
from src.scavenger import LinkChecker, main
import requests.exceptions

# Mock rationale: We need to simulate network responses without actually making HTTP requests
# to ensure tests are deterministic, fast, and offline.
# Mock rationale: We need to simulate file system interactions (reading files, walking directories)
# without touching the actual disk, to ensure tests are isolated and deterministic.

class TestLinkChecker(unittest.TestCase):

    def setUp(self):
        self.checker = LinkChecker(timeout=1) # Shorter timeout for tests

    def test_extract_links_from_markdown(self):
        md_content = """
        # My Awesome Project

        Check out our website: [ApocalypsAI](https://polsala.github.io/ApocalypsAI/)
        Also, a broken link: [Broken](http://example.com/broken)
        Another valid one: <https://google.com>
        Local link: [Local](./local.md)
        No link here.
        """
        links = self.checker.extract_links_from_markdown(md_content)
        self.assertIn("https://polsala.github.io/ApocalypsAI/", links)
        self.assertIn("http://example.com/broken", links)
        self.assertIn("https://google.com", links)
        self.assertNotIn("./local.md", links) # Should only extract http/https
        self.assertEqual(len(links), 3)

        md_no_links = "Just some text with no links."
        self.assertEqual(self.checker.extract_links_from_markdown(md_no_links), [])

        md_empty = ""
        self.assertEqual(self.checker.extract_links_from_markdown(md_empty), [])

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_success(self, mock_get, mock_head):
        mock_head.return_value = MagicMock(status_code=200, reason="OK")
        is_ok, status = self.checker.check_link("https://example.com/valid")
        self.assertTrue(is_ok)
        self.assertEqual(status, "200 OK")
        mock_head.assert_called_once_with("https://example.com/valid", timeout=1, allow_redirects=True)
        mock_get.assert_not_called() # HEAD should be sufficient

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_broken_404(self, mock_get, mock_head):
        mock_head.return_value = MagicMock(status_code=404, reason="Not Found")
        mock_get.return_value = MagicMock(status_code=404, reason="Not Found") # Fallback to GET
        is_ok, status = self.checker.check_link("https://example.com/broken")
        self.assertFalse(is_ok)
        self.assertEqual(status, "404 Not Found")
        mock_head.assert_called_once() # HEAD is called first
        mock_get.assert_called_once() # GET is called as fallback due to 404 from HEAD

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_server_error_500(self, mock_get, mock_head):
        mock_head.return_value = MagicMock(status_code=500, reason="Internal Server Error")
        mock_get.return_value = MagicMock(status_code=500, reason="Internal Server Error") # Fallback to GET
        is_ok, status = self.checker.check_link("https://example.com/server-error")
        self.assertFalse(is_ok)
        self.assertEqual(status, "500 Internal Server Error")
        mock_head.assert_called_once()
        mock_get.assert_called_once()

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_connection_error(self, mock_get, mock_head):
        mock_head.side_effect = requests.exceptions.ConnectionError("Failed to connect")
        mock_get.side_effect = requests.exceptions.ConnectionError("Failed to connect") # Fallback to GET
        is_ok, status = self.checker.check_link("https://nonexistent.com")
        self.assertFalse(is_ok)
        self.assertEqual(status, "Connection Error")
        mock_head.assert_called_once()
        mock_get.assert_called_once()

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_timeout(self, mock_get, mock_head):
        mock_head.side_effect = requests.exceptions.Timeout("Request timed out")
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out") # Fallback to GET
        is_ok, status = self.checker.check_link("https://slow-server.com")
        self.assertFalse(is_ok)
        self.assertEqual(status, "Timeout")
        mock_head.assert_called_once()
        mock_get.assert_called_once()

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_head_method_not_allowed_fallback_to_get(self, mock_get, mock_head):
        mock_head.return_value = MagicMock(status_code=405, reason="Method Not Allowed")
        mock_get.return_value = MagicMock(status_code=200, reason="OK")
        is_ok, status = self.checker.check_link("https://example.com/no-head")
        self.assertTrue(is_ok)
        self.assertEqual(status, "200 OK")
        mock_head.assert_called_once()
        mock_get.assert_called_once() # Should fall back to GET if HEAD returns 405

    @patch('os.walk')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('src.scavenger.LinkChecker.check_link')
    @patch('sys.stdout', new_callable=MagicMock) # Mock stdout to capture prints
    def test_scan_directory(self, mock_stdout, mock_check_link, mock_open, mock_os_walk):
        # Mock rationale: Simulate directory structure and file content
        mock_os_walk.return_value = [
            ('/test_dir', [], ['file1.md', 'file2.txt']),
            ('/test_dir/subdir', [], ['subfile.markdown'])
        ]

        # Mock rationale: Simulate file content for markdown files
        file_contents = {
            '/test_dir/file1.md': "[Link1](https://valid.com)\n[Link2](https://broken.com)",
            '/test_dir/subdir/subfile.markdown': "No links here."
        }
        mock_open.side_effect = lambda filename, *args, **kwargs: MagicMock(
            read_data=file_contents.get(filename, "")
        )

        # Mock rationale: Simulate network responses for check_link
        mock_check_link.side_effect = [
            (True, "200 OK"),    # https://valid.com
            (False, "404 Not Found") # https://broken.com
        ]

        broken_links = self.checker.scan_directory('/test_dir')

        self.assertEqual(len(broken_links), 1)
        self.assertEqual(broken_links[0], ("https://broken.com", "404 Not Found"))

        # Verify that check_link was called for the expected links
        mock_check_link.assert_any_call("https://valid.com")
        mock_check_link.assert_any_call("https://broken.com")
        self.assertEqual(mock_check_link.call_count, 2)

        # Verify file open calls
        mock_open.assert_any_call('/test_dir/file1.md', 'r', encoding='utf-8')
        mock_open.assert_any_call('/test_dir/subdir/subfile.markdown', 'r', encoding='utf-8')
        self.assertEqual(mock_open.call_count, 2) # Only markdown files

        # Verify output
        output = mock_stdout.write.call_args_list
        output_str = "".join([call.args[0] for call in output])
        self.assertIn("Scanning directory: /test_dir", output_str)
        self.assertIn("Processing file: /test_dir/file1.md", output_str)
        self.assertIn("Checking: https://valid.com (Status: 200 OK)", output_str)
        self.assertIn("Checking: https://broken.com (Status: 404 Not Found)", output_str)
        self.assertIn("Processing file: /test_dir/subdir/subfile.markdown", output_str)
        self.assertIn("No external links found.", output_str)
        self.assertIn("Total links checked: 2", output_str)
        self.assertIn("Broken links found: 1", output_str)
        self.assertIn("- https://broken.com (404 Not Found)", output_str)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.scavenger.LinkChecker.scan_directory')
    def test_main_function(self, mock_scan_directory, mock_parse_args):
        # Mock rationale: Simulate command-line arguments without actually running the CLI
        mock_parse_args.return_value = MagicMock(path="/some/path")

        main()

        mock_scan_directory.assert_called_once_with("/some/path")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.scavenger.LinkChecker.scan_directory')
    def test_main_function_default_path(self, mock_scan_directory, mock_parse_args):
        # Mock rationale: Simulate command-line arguments without actually running the CLI
        mock_parse_args.return_value = MagicMock(path=".") # Default path

        main()

        mock_scan_directory.assert_called_once_with(".")


if __name__ == '__main__':
    unittest.main()
