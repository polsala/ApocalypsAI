import unittest
import os
import sys
from unittest.mock import patch, mock_open, MagicMock
from io import StringIO

# Add the src directory to the path to allow importing detector
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from detector import find_urls_in_file, check_url, detect_dead_links, main

class TestDetector(unittest.TestCase):

    def test_find_urls_in_file_basic(self):
        # Mock rationale: We need to simulate reading a file without actually creating one.
        # `mock_open` allows us to provide a string as the file content.
        mock_file_content = "This is a test file with a link: https://example.com/page and another http://test.org"
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            urls = find_urls_in_file("dummy.txt")
            self.assertIn("https://example.com/page", urls)
            self.assertIn("http://test.org", urls)
            self.assertEqual(len(urls), 2)

    def test_find_urls_in_file_no_urls(self):
        # Mock rationale: Simulate a file with no URLs.
        mock_file_content = "No links here, just plain text."
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            urls = find_urls_in_file("dummy.txt")
            self.assertEqual(len(urls), 0)

    def test_find_urls_in_file_duplicates(self):
        # Mock rationale: Ensure duplicate URLs are only returned once.
        mock_file_content = "Link: https://example.com/page. Another: https://example.com/page"
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            urls = find_urls_in_file("dummy.txt")
            self.assertEqual(len(urls), 1)
            self.assertIn("https://example.com/page", urls)

    def test_find_urls_in_file_not_found(self):
        # Mock rationale: Simulate a FileNotFoundError.
        with patch("builtins.open", side_effect=FileNotFoundError):
            urls = find_urls_in_file("non_existent.txt")
            self.assertEqual(urls, [])

    @patch('requests.head')
    def test_check_url_ok(self, mock_head):
        # Mock rationale: Simulate a successful HTTP HEAD request.
        # We create a mock response object with a 200 status code.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response

        url = "https://good.com"
        result_url, status = check_url(url)
        self.assertEqual(result_url, url)
        self.assertEqual(status, "OK")
        mock_head.assert_called_once_with(url, timeout=5, allow_redirects=True)

    @patch('requests.head')
    def test_check_url_broken(self, mock_head):
        # Mock rationale: Simulate a broken link (e.g., 404 Not Found).
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_head.return_value = mock_response

        url = "https://broken.com"
        result_url, status = check_url(url)
        self.assertEqual(result_url, url)
        self.assertEqual(status, "BROKEN (Status: 404)")

    @patch('requests.head')
    def test_check_url_connection_error(self, mock_head):
        # Mock rationale: Simulate a network connection error.
        mock_head.side_effect = requests.exceptions.ConnectionError

        url = "https://unreachable.com"
        result_url, status = check_url(url)
        self.assertEqual(result_url, url)
        self.assertEqual(status, "UNREACHABLE (Connection Error)")

    @patch('requests.head')
    def test_check_url_timeout(self, mock_head):
        # Mock rationale: Simulate a request timeout.
        mock_head.side_effect = requests.exceptions.Timeout

        url = "https://slow.com"
        result_url, status = check_url(url)
        self.assertEqual(result_url, url)
        self.assertEqual(status, "UNREACHABLE (Timeout)")

    @patch('detector.find_urls_in_file')
    @patch('detector.check_url')
    def test_detect_dead_links_all_ok(self, mock_check_url, mock_find_urls):
        # Mock rationale: Simulate a file with URLs and all of them being healthy.
        mock_find_urls.return_value = ["https://ok1.com", "https://ok2.com"]
        mock_check_url.side_effect = [
            ("https://ok1.com", "OK"),
            ("https://ok2.com", "OK")
        ]

        results = detect_dead_links("dummy.txt")
        self.assertEqual(len(results["ok"]), 2)
        self.assertEqual(len(results["broken"]), 0)
        self.assertEqual(len(results["unreachable"]), 0)
        self.assertIn("https://ok1.com", results["ok"])
        self.assertIn("https://ok2.com", results["ok"])

    @patch('detector.find_urls_in_file')
    @patch('detector.check_url')
    def test_detect_dead_links_mixed(self, mock_check_url, mock_find_urls):
        # Mock rationale: Simulate a file with a mix of healthy, broken, and unreachable links.
        mock_find_urls.return_value = ["https://ok.com", "https://broken.com", "https://timeout.com"]
        mock_check_url.side_effect = [
            ("https://ok.com", "OK"),
            ("https://broken.com", "BROKEN (Status: 404)"),
            ("https://timeout.com", "UNREACHABLE (Timeout)")
        ]

        results = detect_dead_links("dummy.txt")
        self.assertEqual(len(results["ok"]), 1)
        self.assertEqual(len(results["broken"]), 1)
        self.assertEqual(len(results["unreachable"]), 1)
        self.assertIn("https://ok.com", results["ok"])
        self.assertIn("https://broken.com (404)", results["broken"])
        self.assertIn("https://timeout.com (Timeout)", results["unreachable"])

    @patch('detector.find_urls_in_file')
    @patch('detector.check_url')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_success(self, mock_exit, mock_stdout, mock_check_url, mock_find_urls):
        # Mock rationale: Simulate a successful run of the main function (all links OK).
        # `sys.stdout` is mocked to capture print output. `sys.exit` is mocked to prevent actual exit.
        mock_find_urls.return_value = ["https://ok.com"]
        mock_check_url.return_value = ("https://ok.com", "OK")

        # Mock argparse to provide the --file argument
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(file="dummy.txt")):
            main()
            self.assertIn("No Broken Links Found!", mock_stdout.getvalue())
            self.assertIn("Healthy Links Found.", mock_stdout.getvalue())
            mock_exit.assert_called_once_with(0)

    @patch('detector.find_urls_in_file')
    @patch('detector.check_url')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_failure_broken_links(self, mock_exit, mock_stdout, mock_check_url, mock_find_urls):
        # Mock rationale: Simulate a run where broken links are found, expecting exit code 1.
        mock_find_urls.return_value = ["https://broken.com"]
        mock_check_url.return_value = ("https://broken.com", "BROKEN (Status: 404)")

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(file="dummy.txt")):
            main()
            self.assertIn("Broken Links Found:", mock_stdout.getvalue())
            mock_exit.assert_called_once_with(1)

    @patch('detector.find_urls_in_file')
    @patch('detector.check_url')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_failure_unreachable_links(self, mock_exit, mock_stdout, mock_check_url, mock_find_urls):
        # Mock rationale: Simulate a run where unreachable links are found, expecting exit code 1.
        mock_find_urls.return_value = ["https://unreachable.com"]
        mock_check_url.return_value = ("https://unreachable.com", "UNREACHABLE (Timeout)")

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(file="dummy.txt")):
            main()
            self.assertIn("Unreachable Links (Connection/Timeout/Other Errors):", mock_stdout.getvalue())
            mock_exit.assert_called_once_with(1)

    @patch('detector.find_urls_in_file')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_no_urls_found(self, mock_exit, mock_stdout, mock_find_urls):
        # Mock rationale: Simulate a file with no URLs, expecting exit code 0.
        mock_find_urls.return_value = []

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(file="dummy.txt")):
            main()
            self.assertIn("No URLs found to check.", mock_stdout.getvalue())
            mock_exit.assert_called_once_with(0)


if __name__ == '__main__':
    unittest.main()
