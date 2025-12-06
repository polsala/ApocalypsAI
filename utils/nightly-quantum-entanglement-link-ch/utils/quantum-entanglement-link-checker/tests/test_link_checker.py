import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys

# Add the src directory to the path to allow importing link_checker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from link_checker import extract_links_from_markdown, check_link, main

class TestLinkChecker(unittest.TestCase):

    def test_extract_links_from_markdown(self):
        # Test various Markdown link formats
        markdown_content = """
        This is a [GitHub link](https://github.com/polsala/ApocalypsAI).
        Another link: <https://example.com/path/to/resource>.
        A link with query params: [search](https://google.com?q=test&param=value).
        No link here.
        An internal link (should be ignored by regex): [local](/local/path).
        Another external link: <http://anothersite.org>.
        """
        expected_links = {
            "https://github.com/polsala/ApocalypsAI",
            "https://example.com/path/to/resource",
            "https://google.com?q=test&param=value",
            "http://anothersite.org"
        }
        self.assertEqual(extract_links_from_markdown(markdown_content), expected_links)

        # Test with no links
        self.assertEqual(extract_links_from_markdown("No links here."), set())

        # Test with only internal links
        self.assertEqual(extract_links_from_markdown("[local](/path)"), set())

    @patch('requests.head')
    def test_check_link_ok(self, mock_head):
        # Mock rationale: Simulate a successful HTTP HEAD request.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.url = "https://example.com/"
        mock_response.raise_for_status.return_value = None
        mock_head.return_value = mock_response

        status, message = check_link("https://example.com/")
        self.assertEqual(status, "OK")
        self.assertEqual(message, "https://example.com/")
        mock_head.assert_called_once_with("https://example.com/", timeout=5, allow_redirects=True)

    @patch('requests.head')
    def test_check_link_redirect(self, mock_head):
        # Mock rationale: Simulate an HTTP HEAD request that results in a redirect.
        mock_response = MagicMock()
        mock_response.status_code = 301
        mock_response.url = "https://new.example.com/"
        mock_response.raise_for_status.return_value = None
        mock_head.return_value = mock_response

        status, message = check_link("https://old.example.com/")
        self.assertEqual(status, "REDIRECT")
        self.assertEqual(message, "https://old.example.com/ (-> https://new.example.com/)")

    @patch('requests.head')
    def test_check_link_broken_404(self, mock_head):
        # Mock rationale: Simulate an HTTP HEAD request returning a 404 Not Found error.
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_head.return_value = mock_response

        status, message = check_link("https://broken.link/404")
        self.assertEqual(status, "BROKEN")
        self.assertEqual(message, "https://broken.link/404 (Status: 404 Not Found)")

    @patch('requests.head')
    def test_check_link_connection_error(self, mock_head):
        # Mock rationale: Simulate a network connection error during the request.
        mock_head.side_effect = requests.exceptions.ConnectionError("Max retries exceeded")

        status, message = check_link("https://unreachable.site/")
        self.assertEqual(status, "ERROR")
        self.assertIn("Connection Error", message)

    @patch('requests.head')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_functionality_directory_scan(self, mock_stdout, mock_file_open, mock_os_walk, mock_head):
        # Mock rationale: Simulate file system traversal and file content reading.
        # Mock rationale: Simulate network responses for link checking.
        # Mock rationale: Capture stdout to verify printed output.

        # Setup mock file system
        mock_os_walk.return_value = [
            ('/path/to/repo', [], ['file1.md', 'file2.txt']),
            ('/path/to/repo/docs', [], ['doc.markdown'])
        ]

        # Setup mock file content
        file_contents = {
            '/path/to/repo/file1.md': "[Link 1](https://good.com) and <https://bad.com>.",
            '/path/to/repo/docs/doc.markdown': "[Link 2](https://redirect.org) and [Ignored Link](https://ignore.me)."
        }
        mock_file_open.side_effect = lambda filename, *args, **kwargs: mock_open(read_data=file_contents.get(filename, '')).return_value

        # Setup mock requests responses
        def mock_head_side_effect(url, *args, **kwargs):
            mock_response = MagicMock()
            if url == "https://good.com":
                mock_response.status_code = 200
                mock_response.url = url
                mock_response.raise_for_status.return_value = None
            elif url == "https://bad.com":
                mock_response.status_code = 404
                mock_response.reason = "Not Found"
                mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
            elif url == "https://redirect.org":
                mock_response.status_code = 301
                mock_response.url = "https://new.redirect.org"
                mock_response.raise_for_status.return_value = None
            elif url == "https://ignore.me":
                # This link should be ignored by the main function's logic, so this branch should not be hit
                raise ValueError(f"Link {url} should have been ignored.")
            else:
                raise ValueError(f"Unexpected URL: {url}")
            return mock_response

        mock_head.side_effect = mock_head_side_effect

        # Simulate command-line arguments
        with patch('sys.argv', ['link_checker.py', '/path/to/repo', '--ignore-domain', 'ignore.me']):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1) # Expect exit code 1 due to broken link

        # Verify output
        output = mock_stdout.write.call_args_list
        output_str = "".join(call.args[0] for call in output)

        self.assertIn("[OK] https://good.com", output_str)
        self.assertIn("[BROKEN] https://bad.com (Status: 404 Not Found)", output_str)
        self.assertIn("[REDIRECT] https://redirect.org (-> https://new.redirect.org)", output_str)
        self.assertIn("[IGNORED] https://ignore.me", output_str)

        self.assertIn("Total links scanned: 4", output_str)
        self.assertIn("Total links checked: 3", output_str)
        self.assertIn("OK: 1", output_str)
        self.assertIn("Redirects: 1", output_str)
        self.assertIn("Broken: 1", output_str)
        self.assertIn("Errors: 0", output_str)
        self.assertIn("Ignored: 1", output_str)

    @patch('requests.head')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.isdir', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_functionality_single_file(self, mock_stdout, mock_file_open, mock_is_dir, mock_is_file, mock_head):
        # Mock rationale: Simulate scanning a single markdown file.
        # Mock rationale: Simulate network responses for link checking.
        # Mock rationale: Capture stdout to verify printed output.

        # Setup mock file content for a single file
        file_contents = {
            '/path/to/repo/single.md': "[Link A](https://single-good.com) and [Link B](https://single-bad.com)."
        }
        mock_file_open.side_effect = lambda filename, *args, **kwargs: mock_open(read_data=file_contents.get(filename, '')).return_value

        # Setup mock requests responses
        def mock_head_side_effect(url, *args, **kwargs):
            mock_response = MagicMock()
            if url == "https://single-good.com":
                mock_response.status_code = 200
                mock_response.url = url
                mock_response.raise_for_status.return_value = None
            elif url == "https://single-bad.com":
                mock_response.status_code = 404
                mock_response.reason = "Not Found"
                mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
            else:
                raise ValueError(f"Unexpected URL: {url}")
            return mock_response

        mock_head.side_effect = mock_head_side_effect

        # Simulate command-line arguments for a single file
        with patch('sys.argv', ['link_checker.py', '/path/to/repo/single.md']):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1) # Expect exit code 1 due to broken link

        # Verify output
        output = mock_stdout.write.call_args_list
        output_str = "".join(call.args[0] for call in output)

        self.assertIn("[OK] https://single-good.com", output_str)
        self.assertIn("[BROKEN] https://single-bad.com (Status: 404 Not Found)", output_str)

        self.assertIn("Total links scanned: 2", output_str)
        self.assertIn("Total links checked: 2", output_str)
        self.assertIn("OK: 1", output_str)
        self.assertIn("Broken: 1", output_str)

    @patch('requests.head')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_functionality_ignore_pattern(self, mock_stdout, mock_file_open, mock_os_walk, mock_head):
        # Mock rationale: Simulate scanning with an ignore pattern.
        # Mock rationale: Simulate network responses for link checking.
        # Mock rationale: Capture stdout to verify printed output.

        mock_os_walk.return_value = [
            ('/path/to/repo', [], ['file.md'])
        ]

        file_contents = {
            '/path/to/repo/file.md': "[Link 1](https://good.com) and [Localhost](http://localhost:8080/api)."
        }
        mock_file_open.side_effect = lambda filename, *args, **kwargs: mock_open(read_data=file_contents.get(filename, '')).return_value

        def mock_head_side_effect(url, *args, **kwargs):
            mock_response = MagicMock()
            if url == "https://good.com":
                mock_response.status_code = 200
                mock_response.url = url
                mock_response.raise_for_status.return_value = None
            else:
                # localhost should be ignored, so this shouldn't be called for it
                raise ValueError(f"Unexpected URL: {url}") 
            return mock_response

        mock_head.side_effect = mock_head_side_effect

        with patch('sys.argv', ['link_checker.py', '/path/to/repo', '--ignore-pattern', '^http://localhost']):
            main()

        output = mock_stdout.write.call_args_list
        output_str = "".join(call.args[0] for call in output)

        self.assertIn("[OK] https://good.com", output_str)
        self.assertIn("[IGNORED] http://localhost:8080/api", output_str)

        self.assertIn("Total links scanned: 2", output_str)
        self.assertIn("Total links checked: 1", output_str)
        self.assertIn("OK: 1", output_str)
        self.assertIn("Ignored: 1", output_str)

if __name__ == '__main__':
    unittest.main()
