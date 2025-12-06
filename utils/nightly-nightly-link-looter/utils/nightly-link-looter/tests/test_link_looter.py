import unittest
from unittest.mock import patch, Mock
import os
import tempfile
from io import StringIO
import sys
import requests # Import requests to catch its exceptions

# Assuming link_looter.py is in src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import link_looter

class TestLinkLooter(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()

    def _create_markdown_file(self, filename, content):
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath

    @patch('requests.head')
    @patch('requests.get')
    def test_find_links_in_markdown(self, mock_get, mock_head):
        markdown_content = """
        # My Document

        This is a [good link](https://example.com/page1).
        Another link: [ApocalypsAI](https://polsala.github.io/ApocalypsAI).
        No link here.
        A link with some text [inside](https://another.org/path).
        """
        expected_links = [
            "https://example.com/page1",
            "https://polsala.github.io/ApocalypsAI",
            "https://another.org/path"
        ]
        found_links = link_looter.find_links_in_markdown(markdown_content)
        self.assertCountEqual(found_links, expected_links) # Use assertCountEqual for order-independent comparison

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_success(self, mock_get, mock_head):
        # Mock rationale: Simulate a successful HTTP HEAD request (status 200).
        mock_head.return_value = Mock(status_code=200, raise_for_status=Mock())
        is_valid, status_message = link_looter.check_link("https://example.com/good")
        self.assertTrue(is_valid)
        self.assertEqual(status_message, "200 OK")
        mock_head.assert_called_once_with("https://example.com/good", timeout=5, allow_redirects=True)
        mock_get.assert_not_called() # GET should not be called if HEAD succeeds

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_404(self, mock_get, mock_head):
        # Mock rationale: Simulate a 404 Not Found error from HTTP HEAD request.
        mock_response = Mock(status_code=404, reason="Not Found")
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_head.return_value = mock_response

        is_valid, status_message = link_looter.check_link("https://example.com/404")
        self.assertFalse(is_valid)
        self.assertEqual(status_message, "404 Not Found")
        mock_head.assert_called_once()
        mock_get.assert_not_called()

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_connection_error(self, mock_get, mock_head):
        # Mock rationale: Simulate a connection error during HTTP HEAD request.
        mock_head.side_effect = requests.exceptions.ConnectionError("Failed to connect")

        is_valid, status_message = link_looter.check_link("https://example.com/unreachable")
        self.assertFalse(is_valid)
        self.assertIn("Connection Error", status_message)
        mock_head.assert_called_once()
        mock_get.assert_not_called()

    @patch('requests.head')
    @patch('requests.get')
    def test_check_link_head_not_allowed_fallback_to_get(self, mock_get, mock_head):
        # Mock rationale: Simulate a 405 Method Not Allowed for HEAD, then a successful GET.
        mock_head_response = Mock(status_code=405, reason="Method Not Allowed")
        mock_head_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_head_response)
        mock_head.return_value = mock_head_response

        mock_get_response = Mock(status_code=200, raise_for_status=Mock())
        mock_get.return_value = mock_get_response

        is_valid, status_message = link_looter.check_link("https://example.com/head-forbidden")
        self.assertTrue(is_valid)
        self.assertEqual(status_message, "200 OK")
        mock_head.assert_called_once()
        mock_get.assert_called_once_with("https://example.com/head-forbidden", timeout=5, allow_redirects=True)

    @patch('requests.head')
    @patch('requests.get')
    def test_process_markdown_file_no_links(self, mock_get, mock_head):
        filepath = self._create_markdown_file("no_links.md", "Just some text.")
        broken_links = link_looter.process_markdown_file(filepath)
        self.assertEqual(len(broken_links), 0)
        mock_head.assert_not_called()
        mock_get.assert_not_called()

    @patch('requests.head')
    @patch('requests.get')
    def test_process_markdown_file_good_links(self, mock_get, mock_head):
        # Mock rationale: All links should return 200 OK.
        mock_head.return_value = Mock(status_code=200, raise_for_status=Mock())
        filepath = self._create_markdown_file("good_links.md", """
        [Link 1](https://good.com/page1)
        [Link 2](https://good.com/page2)
        """)
        broken_links = link_looter.process_markdown_file(filepath)
        self.assertEqual(len(broken_links), 0)
        self.assertEqual(mock_head.call_count, 2) # Two links checked

    @patch('requests.head')
    @patch('requests.get')
    def test_process_markdown_file_mixed_links(self, mock_get, mock_head):
        # Mock rationale: One link is good (200), one is broken (404).
        # Configure mock_head to return different responses based on URL.
        def mock_head_side_effect(url, *args, **kwargs):
            if "good.com" in url:
                return Mock(status_code=200, raise_for_status=Mock())
            elif "bad.com" in url:
                mock_response = Mock(status_code=404, reason="Not Found")
                mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
                return mock_response
            raise ValueError("Unexpected URL in test")

        mock_head.side_effect = mock_head_side_effect

        filepath = self._create_markdown_file("mixed_links.md", """
        [Good Link](https://good.com/page)
        [Bad Link](https://bad.com/page)
        """)
        broken_links = link_looter.process_markdown_file(filepath)
        self.assertEqual(len(broken_links), 1)
        self.assertEqual(broken_links[0]["link"], "https://bad.com/page")
        self.assertEqual(broken_links[0]["status"], "404 Not Found")
        self.assertEqual(mock_head.call_count, 2)

    @patch('requests.head')
    @patch('requests.get')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_single_file_success(self, mock_parse_args, mock_stdout, mock_get, mock_head):
        # Mock rationale: Simulate a single Markdown file with good links.
        mock_parse_args.return_value = Mock(path=os.path.join(self.test_dir, "test.md"), timeout=5)
        mock_head.return_value = Mock(status_code=200, raise_for_status=Mock())

        filepath = self._create_markdown_file("test.md", "[Link](https://example.com/good)")

        with self.assertRaises(SystemExit) as cm:
            link_looter.main()
        self.assertEqual(cm.exception.code, 0) # Expect success exit code
        self.assertIn("No broken links found", mock_stdout.getvalue())
        mock_head.assert_called_once()

    @patch('requests.head')
    @patch('requests.get')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_single_file_failure(self, mock_parse_args, mock_stdout, mock_get, mock_head):
        # Mock rationale: Simulate a single Markdown file with a broken link (404).
        mock_parse_args.return_value = Mock(path=os.path.join(self.test_dir, "test.md"), timeout=5)
        mock_response = Mock(status_code=404, reason="Not Found")
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_head.return_value = mock_response

        filepath = self._create_markdown_file("test.md", "[Link](https://example.com/bad)")

        with self.assertRaises(SystemExit) as cm:
            link_looter.main()
        self.assertEqual(cm.exception.code, 1) # Expect error exit code
        self.assertIn("Broken link found", mock_stdout.getvalue())
        self.assertIn("404 Not Found", mock_stdout.getvalue())
        mock_head.assert_called_once()

    @patch('requests.head')
    @patch('requests.get')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_directory_scan(self, mock_parse_args, mock_stdout, mock_get, mock_head):
        # Mock rationale: Simulate a directory with one good and one bad link across two files.
        mock_parse_args.return_value = Mock(path=self.test_dir, timeout=5)

        def mock_head_side_effect(url, *args, **kwargs):
            if "good.com" in url:
                return Mock(status_code=200, raise_for_status=Mock())
            elif "bad.com" in url:
                mock_response = Mock(status_code=404, reason="Not Found")
                mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
                return mock_response
            raise ValueError("Unexpected URL in test")

        mock_head.side_effect = mock_head_side_effect

        self._create_markdown_file("file1.md", "[Link A](https://good.com/page)")
        self._create_markdown_file("file2.markdown", "[Link B](https://bad.com/page)")
        self._create_markdown_file("not_markdown.txt", "This is not markdown.")

        with self.assertRaises(SystemExit) as cm:
            link_looter.main()
        self.assertEqual(cm.exception.code, 1) # Expect error exit code
        output = mock_stdout.getvalue()
        self.assertIn("Broken link found in", output)
        self.assertIn("https://bad.com/page", output)
        self.assertIn("404 Not Found", output)
        self.assertIn("Found 1 broken links.", output)
        self.assertEqual(mock_head.call_count, 2) # Both good.com and bad.com links should be checked

    def tearDown(self):
        # Clean up the temporary directory and its contents
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main()
