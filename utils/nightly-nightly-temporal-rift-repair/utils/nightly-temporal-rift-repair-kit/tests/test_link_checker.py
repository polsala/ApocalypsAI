import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
import shutil
from pathlib import Path
import requests

# Import the functions to be tested
from src.link_checker import find_urls_in_markdown, check_url, scan_directory_for_broken_links

class TestLinkChecker(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing file operations
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        # Clean up the temporary directory after tests
        shutil.rmtree(self.test_dir)

    def _create_md_file(self, filename, content):
        file_path = self.test_dir / filename
        file_path.write_text(content, encoding='utf-8')
        return file_path

    def test_find_urls_in_markdown(self):
        # Test case 1: No links
        content_no_links = "This is some text without any links."
        self.assertEqual(find_urls_in_markdown(content_no_links), [])

        # Test case 2: Markdown links
        content_md_links = "[Google](https://www.google.com) and [GitHub](https://github.com/polsala/ApocalypsAI)"
        expected_md_links = [
            "https://github.com/polsala/ApocalypsAI",
            "https://www.google.com"
        ]
        self.assertEqual(find_urls_in_markdown(content_md_links), sorted(expected_md_links))

        # Test case 3: Bare URLs
        content_bare_urls = "Visit https://www.python.org or http://docs.python.org/3/"
        expected_bare_urls = [
            "http://docs.python.org/3/",
            "https://www.python.org"
        ]
        self.assertEqual(find_urls_in_markdown(content_bare_urls), sorted(expected_bare_urls))

        # Test case 4: Mixed links and duplicates
        content_mixed_links = (
            "[Python](https://www.python.org) is great. Also see https://www.python.org. "
            "Another link: [Example](https://example.com/path)."
        )
        expected_mixed_links = [
            "https://example.com/path",
            "https://www.python.org"
        ]
        self.assertEqual(find_urls_in_markdown(content_mixed_links), sorted(expected_mixed_links))

        # Test case 5: Links with query parameters and fragments
        content_complex_links = (
            "https://example.com/search?q=test&page=1#section "
            "[Docs](https://docs.example.com/api?version=2.0)"
        )
        expected_complex_links = [
            "https://docs.example.com/api?version=2.0",
            "https://example.com/search?q=test&page=1#section"
        ]
        self.assertEqual(find_urls_in_markdown(content_complex_links), sorted(expected_complex_links))

    @patch('requests.head')
    def test_check_url_success(self, mock_head):
        # Mock rationale: Simulates a successful HTTP request (200 OK) without actual network access.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response

        is_reachable, status = check_url("https://www.valid-site.com")
        self.assertTrue(is_reachable)
        self.assertEqual(status, 200)
        mock_head.assert_called_once_with("https://www.valid-site.com", timeout=5, allow_redirects=True)

    @patch('requests.head')
    def test_check_url_broken(self, mock_head):
        # Mock rationale: Simulates a broken link (404 Not Found) without actual network access.
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_head.return_value = mock_response

        is_reachable, status = check_url("https://www.broken-site.com/non-existent")
        self.assertFalse(is_reachable)
        self.assertEqual(status, 404)

    @patch('requests.head')
    def test_check_url_connection_error(self, mock_head):
        # Mock rationale: Simulates a network connection error without actual network access.
        mock_head.side_effect = requests.exceptions.ConnectionError("Failed to connect")

        is_reachable, status = check_url("https://unreachable-domain.com")
        self.assertFalse(is_reachable)
        self.assertEqual(status, 'Connection Error')

    @patch('requests.head')
    def test_check_url_timeout(self, mock_head):
        # Mock rationale: Simulates a network timeout without actual network access.
        mock_head.side_effect = requests.exceptions.Timeout("Request timed out")

        is_reachable, status = check_url("https://slow-site.com")
        self.assertFalse(is_reachable)
        self.assertEqual(status, 'Timeout')

    @patch('requests.head')
    def test_check_url_request_error(self, mock_head):
        # Mock rationale: Simulates a general request error (e.g., invalid URL scheme) without actual network access.
        mock_head.side_effect = requests.exceptions.RequestException("Invalid URL")

        is_reachable, status = check_url("invalid-scheme://bad.com")
        self.assertFalse(is_reachable)
        self.assertIn('Request Error', status)

    @patch('requests.head')
    def test_check_url_ignored_domain(self, mock_head):
        # Mock rationale: Ensures that whitelisted domains are correctly ignored and not checked via network.
        # The mock should *not* be called for ignored domains.
        is_reachable, status = check_url("https://example.com/some/path")
        self.assertTrue(is_reachable)
        self.assertEqual(status, 'IGNORED')
        mock_head.assert_not_called()

    @patch('src.link_checker.check_url')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_scan_directory_no_broken_links(self, mock_exit, mock_stdout, mock_check_url):
        # Mock rationale: Simulates all links being valid, ensuring the script reports success and exits 0.
        # Mocking check_url prevents actual network requests.
        mock_check_url.return_value = (True, 200)

        self._create_md_file("doc1.md", "[Valid Link](https://www.google.com)")
        self._create_md_file("doc2.md", "No links here.")

        scan_directory_for_broken_links(str(self.test_dir))

        mock_exit.assert_called_once_with(0) # Should exit with 0 for success
        output = mock_stdout.getvalue()
        self.assertIn("Scan complete. Found 0 broken/unreachable links.", output)

    @patch('src.link_checker.check_url')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_scan_directory_with_broken_links(self, mock_exit, mock_stdout, mock_check_url):
        # Mock rationale: Simulates some links being broken, ensuring the script reports them and exits 1.
        # Mocking check_url prevents actual network requests.
        # Configure check_url to return different results for different URLs
        def mock_check_url_side_effect(url):
            if "broken-link.com" in url:
                return False, 404
            elif "unreachable.com" in url:
                return False, 'Connection Error'
            else:
                return True, 200
        mock_check_url.side_effect = mock_check_url_side_effect

        self._create_md_file("doc1.md", "[Good Link](https://www.google.com)\n[Bad Link](https://broken-link.com)")
        self._create_md_file("doc2.md", "[Another Bad Link](https://unreachable.com)")

        scan_directory_for_broken_links(str(self.test_dir))

        mock_exit.assert_called_once_with(1) # Should exit with 1 for failure
        output = mock_stdout.getvalue()
        self.assertIn(f"File: {self.test_dir}/doc1.md", output)
        self.assertIn("  [BROKEN] https://broken-link.com (Status: 404)", output)
        self.assertIn(f"File: {self.test_dir}/doc2.md", output)
        self.assertIn("  [BROKEN] https://unreachable.com (Status: Connection Error)", output)
        self.assertIn("Scan complete. Found 2 broken/unreachable links.", output)

    @patch('src.link_checker.check_url')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_scan_directory_empty_file(self, mock_exit, mock_stdout, mock_check_url):
        # Mock rationale: Ensures the script handles empty files gracefully.
        self._create_md_file("empty.md", "")
        scan_directory_for_broken_links(str(self.test_dir))
        mock_exit.assert_called_once_with(0)
        output = mock_stdout.getvalue()
        self.assertIn("Scan complete. Found 0 broken/unreachable links.", output)

    @patch('src.link_checker.check_url')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_scan_directory_non_markdown_files(self, mock_exit, mock_stdout, mock_check_url):
        # Mock rationale: Ensures only Markdown files are processed.
        self._create_md_file("script.py", "print('hello')")
        self._create_md_file("image.jpg", "binary content")
        self._create_md_file("README.txt", "Just text, no links.")
        scan_directory_for_broken_links(str(self.test_dir))
        mock_exit.assert_called_once_with(0)
        output = mock_stdout.getvalue()
        self.assertIn("Scan complete. Found 0 broken/unreachable links.", output)

    @patch('src.link_checker.check_url')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_scan_directory_with_ignored_links(self, mock_exit, mock_stdout, mock_check_url):
        # Mock rationale: Ensures that links to IGNORED_DOMAINS are not reported as broken.
        # check_url will return (True, 'IGNORED') for these.
        def mock_check_url_side_effect(url):
            if "example.com" in url:
                return True, 'IGNORED'
            else:
                return True, 200
        mock_check_url.side_effect = mock_check_url_side_effect

        self._create_md_file("doc.md", "[Ignored](https://example.com/test)\n[Valid](https://good.com)")
        scan_directory_for_broken_links(str(self.test_dir))

        mock_exit.assert_called_once_with(0)
        output = mock_stdout.getvalue()
        self.assertIn("Scan complete. Found 0 broken/unreachable links.", output)
        self.assertNotIn("BROKEN", output)
