import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys

# Add the src directory to the path to allow importing link_checker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from link_checker import find_markdown_files, extract_external_links, check_link_status, main

class TestLinkChecker(unittest.TestCase):

    @patch('os.walk')
    def test_find_markdown_files(self, mock_os_walk):
        # Mock rationale: Simulate file system traversal without actual disk access.
        mock_os_walk.return_value = [
            ('/repo', ('utils', 'docs'), ('README.md', 'LICENSE')),
            ('/repo/utils', ('nightly-util',), ('helper.py',)),
            ('/repo/utils/nightly-util', (), ('README.md', 'src.py')),
            ('/repo/docs', (), ('guide.md', 'index.html')),
        ]
        expected_files = [
            '/repo/README.md',
            '/repo/utils/nightly-util/README.md',
            '/repo/docs/guide.md',
        ]
        self.assertCountEqual(find_markdown_files('/repo'), expected_files)

    @patch('builtins.open', new_callable=mock_open)
    def test_extract_external_links(self, mock_file_open):
        # Mock rationale: Simulate reading file content without actual disk I/O.
        mock_file_open.return_value.read.return_value = """
# My Project

This is a project with some links.
- [Google](https://www.google.com)
- [Local File](./local.md)
- [Another External](http://example.com/path)
- [Internal Anchor](#section)
- [No Protocol Link](www.badlink.com)
- [Link with spaces](https://example.com/with spaces)
- [Link with query](https://example.com/query?param=value)
"""
        # The regex in link_checker.py extracts URLs as they appear in Markdown.
        # It does not perform URL encoding for spaces, so the test reflects this.
        expected_links_as_extracted = [
            "https://www.google.com",
            "http://example.com/path",
            "https://example.com/with spaces",
            "https://example.com/query?param=value"
        ]
        self.assertCountEqual(extract_external_links('dummy.md'), expected_links_as_extracted)

        # Test with no links
        mock_file_open.return_value.read.return_value = "No links here."
        self.assertEqual(extract_external_links('dummy.md'), [])

        # Test with only internal links
        mock_file_open.return_value.read.return_value = "[Local](./local.md) [Anchor](#section)"
        self.assertEqual(extract_external_links('dummy.md'), [])

    @patch('requests.head')
    def test_check_link_status_success(self, mock_head):
        # Mock rationale: Simulate network responses without making actual HTTP requests.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.reason = "OK"
        mock_head.return_value = mock_response

        is_broken, status_msg = check_link_status("https://example.com")
        self.assertFalse(is_broken)
        self.assertEqual(status_msg, "200 OK")
        mock_head.assert_called_once_with("https://example.com", timeout=5, allow_redirects=True)

    @patch('requests.head')
    def test_check_link_status_404(self, mock_head):
        # Mock rationale: Simulate a 'Not Found' HTTP response.
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_head.return_value = mock_response

        is_broken, status_msg = check_link_status("https://example.com/non-existent")
        self.assertTrue(is_broken)
        self.assertEqual(status_msg, "404 Not Found")

    @patch('requests.head')
    def test_check_link_status_connection_error(self, mock_head):
        # Mock rationale: Simulate a network connection failure.
        mock_head.side_effect = requests.exceptions.ConnectionError("Failed to connect")

        is_broken, status_msg = check_link_status("https://broken-domain.com")
        self.assertTrue(is_broken)
        self.assertEqual(status_msg, "Connection Error")

    @patch('requests.head')
    def test_check_link_status_timeout_error(self, mock_head):
        # Mock rationale: Simulate a request timeout.
        mock_head.side_effect = requests.exceptions.Timeout("Request timed out")

        is_broken, status_msg = check_link_status("https://slow-server.com")
        self.assertTrue(is_broken)
        self.assertEqual(status_msg, "Timeout Error")

    @patch('link_checker.find_markdown_files')
    @patch('link_checker.extract_external_links')
    @patch('link_checker.check_link_status')
    @patch('builtins.print') # Mock print to capture output
    @patch('os.getcwd', return_value='/repo') # Mock current working directory
    @patch('os.path.basename', side_effect=os.path.basename) # Keep basename functional
    @patch('os.path.relpath', side_effect=os.path.relpath) # Keep relpath functional
    def test_main_no_broken_links(self, mock_relpath, mock_basename, mock_getcwd, mock_print, mock_check_link_status, mock_extract_external_links, mock_find_markdown_files):
        # Mock rationale: Simulate a full run of the main function without actual file I/O or network requests.
        mock_find_markdown_files.return_value = ['/repo/README.md']
        mock_extract_external_links.return_value = ['https://good.com']
        mock_check_link_status.return_value = (False, '200 OK')

        main()

        mock_print.assert_any_call("Scanning for broken links...")
        mock_print.assert_any_call("Found 1 .md files.")
        mock_print.assert_any_call("Checking link: https://good.com (from README.md)")
        mock_print.assert_any_call("\nNo broken links found. All web weavers are in good repair!")
        self.assertEqual(mock_print.call_count, 4) # 3 prints + final message

    @patch('link_checker.find_markdown_files')
    @patch('link_checker.extract_external_links')
    @patch('link_checker.check_link_status')
    @patch('builtins.print')
    @patch('os.getcwd', return_value='/repo')
    @patch('os.path.basename', side_effect=os.path.basename)
    @patch('os.path.relpath', side_effect=os.path.relpath)
    def test_main_with_broken_links(self, mock_relpath, mock_basename, mock_getcwd, mock_print, mock_check_link_status, mock_extract_external_links, mock_find_markdown_files):
        # Mock rationale: Simulate a full run of the main function with some broken links.
        mock_find_markdown_files.return_value = ['/repo/README.md', '/repo/docs/AGENTS.md']
        mock_extract_external_links.side_effect = [
            ['https://broken1.com', 'https://good.com'], # For README.md
            ['https://broken2.com'] # For AGENTS.md
        ]
        mock_check_link_status.side_effect = [
            (True, '404 Not Found'), # broken1.com
            (False, '200 OK'),       # good.com
            (True, 'Connection Error') # broken2.com
        ]

        main()

        mock_print.assert_any_call("Scanning for broken links...")
        mock_print.assert_any_call("Found 2 .md files.")
        mock_print.assert_any_call("Checking link: https://broken1.com (from README.md)")
        mock_print.assert_any_call("Checking link: https://good.com (from README.md)")
        mock_print.assert_any_call("Checking link: https://broken2.com (from AGENTS.md)")
        mock_print.assert_any_call("\n--- Broken Links Found ---")
        mock_print.assert_any_call("- README.md: https://broken1.com (404 Not Found)")
        mock_print.assert_any_call("- docs/AGENTS.md: https://broken2.com (Connection Error)")

        # Verify the number of calls to print, accounting for the initial messages and then the broken links.
        # Initial: "Scanning...", "Found X files."
        # Per link: "Checking link..." (3 times)
        # Final: "--- Broken Links Found ---", then 2 broken link reports.
        # Total: 2 + 3 + 1 + 2 = 8 calls
        self.assertEqual(mock_print.call_count, 8)

if __name__ == '__main__':
    unittest.main()
