import unittest
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock
from io import StringIO
import requests

# Adjust path to import the module from src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import link_rot_detector

class TestLinkRotDetector(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing files
        self.test_dir = tempfile.mkdtemp()
        self.original_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        # Clean up the temporary directory
        for root, _, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            os.rmdir(root)
        sys.stdout = self.original_stdout # Restore stdout

    def _create_md_file(self, filename, content):
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath

    @patch('requests.head')
    def test_find_markdown_files(self, mock_head):
        # Mock rationale: This test specifically checks file system traversal,
        # not network requests, so requests.head is mocked to prevent actual calls.
        self._create_md_file("file1.md", "content")
        self._create_md_file("file2.txt", "content")
        os.makedirs(os.path.join(self.test_dir, "subdir"))
        self._create_md_file("subdir/file3.md", "content")

        files = link_rot_detector.find_markdown_files(self.test_dir)
        expected_files = [
            os.path.join(self.test_dir, "file1.md"),
            os.path.join(self.test_dir, "subdir", "file3.md")
        ]
        self.assertCountEqual(files, expected_files)

    @patch('requests.head')
    def test_extract_links_from_markdown(self, mock_head):
        # Mock rationale: This test specifically checks link extraction from Markdown,
        # not network requests, so requests.head is mocked to prevent actual calls.
        filepath = self._create_md_file("test.md",
            "This is a [valid link](https://example.com/page1).\n"
            "Another [link](http://anothersite.org/path).\n"
            "No link here.\n"
            "[Local link](/local/path).\n"
            "[Duplicate link](https://example.com/page1).\n"
            "Invalid format [no url].\n"
            "Link with query [query](https://example.com/search?q=test&id=123).\n"
        )
        links = link_rot_detector.extract_links_from_markdown(filepath)
        expected_links = [
            "https://example.com/page1",
            "http://anothersite.org/path",
            "https://example.com/search?q=test&id=123"
        ]
        self.assertCountEqual(links, expected_links)

    @patch('requests.head')
    def test_check_link_status_ok(self, mock_head):
        # Mock rationale: Simulating a successful HTTP HEAD request without making a real network call.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.reason = "OK"
        mock_head.return_value = mock_response

        is_ok, status = link_rot_detector.check_link_status("https://example.com/ok")
        self.assertTrue(is_ok)
        self.assertEqual(status, "OK")
        mock_head.assert_called_once_with("https://example.com/ok", timeout=5, allow_redirects=True)

    @patch('requests.head')
    def test_check_link_status_404(self, mock_head):
        # Mock rationale: Simulating a 404 Not Found HTTP HEAD request without making a real network call.
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_head.return_value = mock_response

        is_ok, status = link_rot_detector.check_link_status("https://example.com/404")
        self.assertFalse(is_ok)
        self.assertEqual(status, "404 Not Found")

    @patch('requests.head')
    def test_check_link_status_connection_error(self, mock_head):
        # Mock rationale: Simulating a network connection error without making a real network call.
        mock_head.side_effect = requests.exceptions.ConnectionError("Mocked connection error")

        is_ok, status = link_rot_detector.check_link_status("https://example.com/error")
        self.assertFalse(is_ok)
        self.assertIn("Connection Error", status)

    @patch('requests.head')
    def test_check_link_status_timeout_error(self, mock_head):
        # Mock rationale: Simulating a network timeout error without making a real network call.
        mock_head.side_effect = requests.exceptions.Timeout("Mocked timeout error")

        is_ok, status = link_rot_detector.check_link_status("https://example.com/timeout")
        self.assertFalse(is_ok)
        self.assertIn("Timeout Error", status)

    @patch('requests.head')
    def test_main_no_broken_links(self, mock_head):
        # Mock rationale: Simulating all links being valid to test the "no broken links" scenario.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.reason = "OK"
        mock_head.return_value = mock_response

        self._create_md_file("doc1.md", "[Link1](https://good.com/a) [Link2](https://good.com/b)")
        self._create_md_file("doc2.md", "No external links here.")

        with patch.object(sys, 'argv', ['link_rot_detector.py', self.test_dir]):
            with self.assertRaises(SystemExit) as cm:
                link_rot_detector.main()
            self.assertEqual(cm.exception.code, 0) # Expect exit code 0 for success

        output = sys.stdout.getvalue()
        self.assertIn("All external links checked. No link rot detected.", output)
        self.assertIn("The digital garden is thriving!", output)
        self.assertEqual(mock_head.call_count, 2) # Two unique links checked

    @patch('requests.head')
    def test_main_with_broken_links(self, mock_head):
        # Mock rationale: Simulating a mix of valid and broken links to test the reporting mechanism.
        # Configure mock_head to return different responses based on the URL.
        def mock_head_side_effect(url, *args, **kwargs):
            mock_response = MagicMock()
            if "good.com" in url:
                mock_response.status_code = 200
                mock_response.reason = "OK"
            elif "bad404.com" in url:
                mock_response.status_code = 404
                mock_response.reason = "Not Found"
            elif "bad500.com" in url:
                mock_response.status_code = 500
                mock_response.reason = "Internal Server Error"
            elif "error.com" in url:
                raise requests.exceptions.ConnectionError("Mocked connection error")
            else:
                mock_response.status_code = 200 # Default for unexpected
                mock_response.reason = "OK"
            return mock_response

        mock_head.side_effect = mock_head_side_effect

        self._create_md_file("doc_a.md",
            "[Good Link](https://good.com/page1)\n"
            "[Bad 404 Link](https://bad404.com/page2)\n"
            "[Another Good Link](https://good.com/page3)"
        )
        self._create_md_file("doc_b.md",
            "[Bad 500 Link](https://bad500.com/page4)\n"
            "[Connection Error Link](https://error.com/page5)"
        )

        with patch.object(sys, 'argv', ['link_rot_detector.py', self.test_dir]):
            with self.assertRaises(SystemExit) as cm:
                link_rot_detector.main()
            self.assertEqual(cm.exception.code, 1) # Expect exit code 1 for issues

        output = sys.stdout.getvalue()
        self.assertIn(f"File: {os.path.join(self.test_dir, 'doc_a.md')}", output)
        self.assertIn("Broken Link: https://bad404.com/page2 (Status: 404 Not Found)", output)
        self.assertIn(f"File: {os.path.join(self.test_dir, 'doc_b.md')}", output)
        self.assertIn("Broken Link: https://bad500.com/page4 (Status: 500 Internal Server Error)", output)
        self.assertIn("Broken Link: https://error.com/page5 (Status: Connection Error: Could not connect to host.)", output)
        self.assertIn("Summary: Found 3 broken links in 2 files.", output)
        self.assertEqual(mock_head.call_count, 5) # 5 unique links checked

    @patch('requests.head')
    def test_main_invalid_directory(self, mock_head):
        # Mock rationale: This test checks argument parsing and directory validation,
        # not network requests, so requests.head is mocked to prevent actual calls.
        with patch.object(sys, 'argv', ['link_rot_detector.py', '/non/existent/path']):
            with self.assertRaises(SystemExit) as cm:
                link_rot_detector.main()
            self.assertEqual(cm.exception.code, 1) # Expect exit code 1 for error

        output = sys.stdout.getvalue()
        self.assertIn("Error: Directory '/non/existent/path' not found.", output)

    @patch('requests.head')
    def test_main_no_args(self, mock_head):
        # Mock rationale: This test checks argument parsing, not network requests.
        with patch.object(sys, 'argv', ['link_rot_detector.py']):
            with self.assertRaises(SystemExit) as cm:
                link_rot_detector.main()
            self.assertEqual(cm.exception.code, 1) # Expect exit code 1 for error

        output = sys.stdout.getvalue()
        self.assertIn("Usage: python src/link_rot_detector.py <path_to_directory>", output)

if __name__ == '__main__':
    unittest.main()
