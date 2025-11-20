import unittest
import os
import requests
from unittest.mock import patch, mock_open
from src.scavenger import find_markdown_files, extract_urls_from_markdown, check_url, main

class TestScavenger(unittest.TestCase):

    @patch('os.walk')
    def test_find_markdown_files(self, mock_os_walk):
        # Mock rationale: Simulate file system traversal without actual disk access.
        mock_os_walk.return_value = [
            ('/repo', ('subdir1', 'subdir2'), ('README.md', 'LICENSE')),
            ('/repo/subdir1', (), ('file1.md', 'file2.txt')),
            ('/repo/subdir2', (), ('another.md',))
        ]
        expected_files = [
            os.path.join('/repo', 'README.md'),
            os.path.join('/repo/subdir1', 'file1.md'),
            os.path.join('/repo/subdir2', 'another.md')
        ]
        self.assertCountEqual(find_markdown_files('/repo'), expected_files)

        mock_os_walk.return_value = [] # No files
        self.assertEqual(find_markdown_files('/empty'), [])

    @patch('builtins.open', new_callable=mock_open)
    def test_extract_urls_from_markdown(self, mock_file_open):
        # Mock rationale: Simulate reading file content without actual disk access.

        # Test with various link types
        mock_file_open.return_value.read.return_value = """
# My Project

This is a link to [Google](https://www.google.com).
Another link: <https://example.com/path/to/resource?q=test>
And a broken one: [Broken](http://broken.link/page.html)
A relative link: [Local File](./local.md) - should be ignored
An anchor link: [Section](#section) - should be ignored
A link with query params: [API](https://api.example.com/data?id=123&param=value)
"""
        expected_urls = {
            "https://www.google.com",
            "https://example.com/path/to/resource?q=test",
            "http://broken.link/page.html",
            "https://api.example.com/data?id=123&param=value"
        }
        self.assertCountEqual(extract_urls_from_markdown('dummy.md'), list(expected_urls))

        # Test with no links
        mock_file_open.return_value.read.return_value = "No links here."
        self.assertEqual(extract_urls_from_markdown('no_links.md'), [])

        # Test with only relative/anchor links
        mock_file_open.return_value.read.return_value = "[Local](./file.md) and [Anchor](#section)"
        self.assertEqual(extract_urls_from_markdown('only_local.md'), [])

    @patch('requests.head')
    @patch('requests.get')
    def test_check_url(self, mock_requests_get, mock_requests_head):
        # Mock rationale: Simulate network requests and their responses without actual network access.

        # Test 200 OK
        mock_requests_head.return_value.status_code = 200
        self.assertEqual(check_url("http://good.com"), 200)

        # Test 404 Not Found
        mock_requests_head.return_value.status_code = 404
        self.assertEqual(check_url("http://bad.com"), 404)

        # Test 500 Internal Server Error
        mock_requests_head.return_value.status_code = 500
        self.assertEqual(check_url("http://server-error.com"), 500)

        # Test Connection Error
        mock_requests_head.side_effect = requests.exceptions.ConnectionError
        self.assertEqual(check_url("http://unreachable.com"), "Connection Error")
        mock_requests_head.side_effect = None # Reset side effect

        # Test Timeout
        mock_requests_head.side_effect = requests.exceptions.Timeout
        self.assertEqual(check_url("http://slow.com"), "Timeout")
        mock_requests_head.side_effect = None # Reset side effect

        # Test HEAD forbidden (405) -> fallback to GET
        mock_requests_head.return_value.status_code = 405
        mock_requests_get.return_value.status_code = 200
        self.assertEqual(check_url("http://head-forbidden.com"), 200)
        mock_requests_get.assert_called_once_with("http://head-forbidden.com", timeout=5, allow_redirects=True)
        mock_requests_get.reset_mock() # Reset for next test

        # Test HEAD forbidden (405) -> GET also fails (404)
        mock_requests_head.return_value.status_code = 405
        mock_requests_get.return_value.status_code = 404
        self.assertEqual(check_url("http://head-forbidden-get-fail.com"), 404)
        mock_requests_get.assert_called_once()
        mock_requests_get.reset_mock()

    @patch('src.scavenger.find_markdown_files')
    @patch('src.scavenger.extract_urls_from_markdown')
    @patch('src.scavenger.check_url')
    @patch('builtins.print') # Mock print to capture output
    def test_main_function(self, mock_print, mock_check_url, mock_extract_urls, mock_find_md_files):
        # Mock rationale: Isolate the main function logic from file system and network operations.
        # Mock print to verify output without polluting stdout during tests.

        # Scenario 1: No markdown files
        mock_find_md_files.return_value = []
        main()
        mock_print.assert_any_call("✅ No markdown files found to scavenge.")
        mock_print.reset_mock()

        # Scenario 2: Markdown file with all good links
        mock_find_md_files.return_value = ['/repo/README.md']
        mock_extract_urls.return_value = ['http://good.com', 'https://another.good.com']
        mock_check_url.side_effect = [200, 200]
        main()
        mock_print.assert_any_call("\n✅ Scavenging complete: All external links appear healthy!")
        mock_print.reset_mock()
        mock_extract_urls.reset_mock()
        mock_check_url.reset_mock()

        # Scenario 3: Markdown file with some broken links
        mock_find_md_files.return_value = ['/repo/README.md']
        mock_extract_urls.return_value = ['http://good.com', 'http://bad.com', 'http://unreachable.com']
        mock_check_url.side_effect = [200, 404, "Connection Error"]
        main()
        mock_print.assert_any_call("  [OK] http://good.com (Status: 200)")
        mock_print.assert_any_call("  [BROKEN] http://bad.com (Status: 404)")
        mock_print.assert_any_call("  [BROKEN] http://unreachable.com (Status: Connection Error)")
        mock_print.assert_any_call("\n🚨 Scavenging complete: Some broken links were found!")
        mock_print.reset_mock()
        mock_extract_urls.reset_mock()
        mock_check_url.reset_mock()

        # Scenario 4: Markdown file with no external links
        mock_find_md_files.return_value = ['/repo/docs/internal.md']
        mock_extract_urls.return_value = []
        main()
        mock_print.assert_any_call("  No external links found.")
        mock_print.assert_any_call("\n✅ Scavenging complete: All external links appear healthy!")
        mock_print.reset_mock()
        mock_extract_urls.reset_mock()
        mock_check_url.reset_mock()

if __name__ == '__main__':
    unittest.main()
