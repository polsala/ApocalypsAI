import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# Add the src directory to the path to allow importing scavenger.py
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from scavenger import extract_links, check_link, scan_file, main

class TestScavenger(unittest.TestCase):

    def test_extract_links(self):
        content = """
        This is a test with a link: https://example.com/page1
        Another link here: http://sub.domain.org/path/to/resource?id=123&param=test
        And a duplicate: https://example.com/page1
        No link here.
        A link with a hash: https://example.com/page2#section
        """
        expected_links = [
            "http://sub.domain.org/path/to/resource?id=123&param=test",
            "https://example.com/page1",
            "https://example.com/page2#section"
        ]
        self.assertEqual(extract_links(content), sorted(expected_links))

        self.assertEqual(extract_links("No links at all."), [])
        self.assertEqual(extract_links("Link with www: https://www.google.com"), ["https://www.google.com"])

    @patch('scavenger.requests.head')
    def test_check_link_ok(self, mock_head):
        # Mock rationale: Simulate a successful HTTP request (200 OK).
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response

        is_ok, status_code = check_link("https://example.com/ok")
        self.assertTrue(is_ok)
        self.assertEqual(status_code, 200)
        mock_head.assert_called_once_with("https://example.com/ok", timeout=5, allow_redirects=True, verify=False)

    @patch('scavenger.requests.head')
    def test_check_link_not_found(self, mock_head):
        # Mock rationale: Simulate a 'Not Found' HTTP response (404).
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_head.return_value = mock_response

        is_ok, status_code = check_link("https://example.com/404")
        self.assertFalse(is_ok)
        self.assertEqual(status_code, 404)

    @patch('scavenger.requests.head')
    def test_check_link_server_error(self, mock_head):
        # Mock rationale: Simulate a server error HTTP response (500).
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_head.return_value = mock_response

        is_ok, status_code = check_link("https://example.com/500")
        self.assertFalse(is_ok)
        self.assertEqual(status_code, 500)

    @patch('scavenger.requests.head')
    def test_check_link_network_error(self, mock_head):
        # Mock rationale: Simulate a network error or timeout during the request.
        mock_head.side_effect = requests.exceptions.RequestException("Network error")

        is_ok, status_code = check_link("https://example.com/network-error")
        self.assertFalse(is_ok)
        self.assertEqual(status_code, 0) # 0 for network errors/timeouts

    @patch('scavenger.Path.read_text')
    @patch('scavenger.Path.is_file')
    @patch('scavenger.check_link')
    def test_scan_file(self, mock_check_link, mock_is_file, mock_read_text):
        # Mock rationale: Simulate file existence, content, and link checking results.
        mock_is_file.return_value = True
        mock_read_text.return_value = """
        Link 1: https://good.link/page
        Link 2: https://bad.link/page
        Link 3: https://another.good.link
        """

        # Configure mock_check_link to return specific results for each URL
        def mock_check_link_side_effect(url):
            if "good.link" in url:
                return True, 200
            elif "bad.link" in url:
                return False, 404
            elif "another.good.link" in url:
                return True, 200
            return False, 0 # Default for unexpected links

        mock_check_link.side_effect = mock_check_link_side_effect

        filepath = Path("test_doc.md")
        results = scan_file(filepath)

        expected_results = {
            "https://good.link/page": (True, 200),
            "https://bad.link/page": (False, 404),
            "https://another.good.link": (True, 200)
        }
        self.assertEqual(results, expected_results)
        mock_is_file.assert_called_once_with()
        mock_read_text.assert_called_once_with(encoding='utf-8')
        self.assertEqual(mock_check_link.call_count, 3)

    @patch('scavenger.Path.is_file')
    def test_scan_file_not_found(self, mock_is_file):
        # Mock rationale: Simulate a file that does not exist.
        mock_is_file.return_value = False
        filepath = Path("non_existent.md")
        with patch('sys.stderr', new=MagicMock()) as mock_stderr:
            results = scan_file(filepath)
            self.assertEqual(results, {})
            mock_stderr.write.assert_called_once_with(f"Warning: File not found: {filepath}\n")

    @patch('scavenger.Path.read_text')
    @patch('scavenger.Path.is_file')
    def test_scan_file_decode_error(self, mock_is_file, mock_read_text):
        # Mock rationale: Simulate a file that cannot be decoded (e.g., binary).
        mock_is_file.return_value = True
        mock_read_text.side_effect = UnicodeDecodeError('utf-8', b'', 0, 1, 'invalid start byte')
        filepath = Path("binary_file.bin")
        with patch('sys.stderr', new=MagicMock()) as mock_stderr:
            results = scan_file(filepath)
            self.assertEqual(results, {})
            mock_stderr.write.assert_called_once_with(f"Warning: Could not decode file {filepath}. Skipping.\n")

    @patch('scavenger.scan_file')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_functionality(self, mock_parse_args, mock_scan_file):
        # Mock rationale: Simulate command-line arguments and the behavior of scan_file.
        mock_args = MagicMock()
        mock_args.files = ["file1.md", "file2.html"]
        mock_parse_args.return_value = mock_args

        # Configure mock_scan_file to return specific results for each file
        def scan_file_side_effect(filepath):
            if "file1.md" in str(filepath):
                return {
                    "https://link1.com": (True, 200),
                    "https://broken1.com": (False, 404)
                }
            elif "file2.html" in str(filepath):
                return {
                    "https://link2.com": (True, 200),
                    "https://broken2.com": (False, 500),
                    "https://link3.com": (True, 200)
                }
            return {}

        mock_scan_file.side_effect = scan_file_side_effect

        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            main()
            # Assertions for print statements
            output = mock_stdout.write.call_args_list
            output_str = "".join(call.args[0] for call in output)

            self.assertIn("Scanning files for broken links...", output_str)
            self.assertIn("File: file1.md", output_str)
            self.assertIn("✅ https://link1.com (200 OK)", output_str)
            self.assertIn("❌ https://broken1.com (404 Not Found)", output_str)
            self.assertIn("File: file2.html", output_str)
            self.assertIn("✅ https://link2.com (200 OK)", output_str)
            self.assertIn("❌ https://broken2.com (500 Error)", output_str)
            self.assertIn("✅ https://link3.com (200 OK)", output_str)
            self.assertIn("Scan complete. Found 2 broken links across 2 files.", output_str)

            self.assertEqual(mock_scan_file.call_count, 2)
            mock_scan_file.assert_any_call(Path("file1.md"))
            mock_scan_file.assert_any_call(Path("file2.html"))

    @patch('scavenger.scan_file')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_broken_links(self, mock_parse_args, mock_scan_file):
        # Mock rationale: Simulate command-line arguments and a scenario with no broken links.
        mock_args = MagicMock()
        mock_args.files = ["file.md"]
        mock_parse_args.return_value = mock_args

        mock_scan_file.return_value = {
            "https://link.com": (True, 200)
        }

        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            main()
            output_str = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
            self.assertIn("Scan complete. Found 0 broken links across 1 file.", output_str)

    @patch('scavenger.scan_file')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_links_in_files(self, mock_parse_args, mock_scan_file):
        # Mock rationale: Simulate command-line arguments and files with no links.
        mock_args = MagicMock()
        mock_args.files = ["empty.md"]
        mock_parse_args.return_value = mock_args

        mock_scan_file.return_value = {}

        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            main()
            output_str = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
            self.assertIn("No links found or file could not be processed.", output_str)
            self.assertIn("Scan complete. Found 0 broken links across 1 file.", output_str)

if __name__ == '__main__':
    unittest.main()
