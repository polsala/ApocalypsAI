import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys

# Add the src directory to the path to allow importing scavenger
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from scavenger import (
    find_links_in_markdown,
    check_url_reachable,
    check_local_path_exists,
    scan_directory_for_broken_links,
    main
)

class TestScavenger(unittest.TestCase):

    def test_find_links_in_markdown(self):
        markdown_content = """
        # My Document

        This is a [link to Google](https://www.google.com).
        Here's another [link to example.org](http://example.org/path).
        A relative link: [local file](./docs/file.md).
        An absolute local link: [root file](/README.md).
        A link with query params: [search](https://www.google.com?q=test).
        An anchor link: [section](#section-1).
        A mailto link: [email me](mailto:test@example.com).

        Using reference links:
        [GitHub][github_ref]
        [Local Ref][local_ref]

        [github_ref]: https://github.com/polsala/ApocalypsAI
        [local_ref]: ./assets/image.png
        [unused_ref]: http://unused.com

        No link here.
        """
        
        direct_urls, reference_links = find_links_in_markdown(markdown_content)
        
        expected_direct_urls = [
            "https://www.google.com",
            "http://example.org/path",
            "./docs/file.md",
            "/README.md",
            "https://www.google.com?q=test",
            "mailto:test@example.com"
        ]
        self.assertCountEqual(direct_urls, expected_direct_urls)

        expected_reference_links = {
            "github_ref": "https://github.com/polsala/ApocalypsAI",
            "local_ref": "./assets/image.png",
            "unused_ref": "http://unused.com"
        }
        self.assertDictEqual(reference_links, expected_reference_links)

        # Test with resolved references
        all_urls, _ = find_links_in_markdown(markdown_content)
        expected_all_urls = [
            "https://www.google.com",
            "http://example.org/path",
            "./docs/file.md",
            "/README.md",
            "https://www.google.com?q=test",
            "mailto:test@example.com",
            "https://github.com/polsala/ApocalypsAI",
            "./assets/image.png"
        ]
        self.assertCountEqual(all_urls, expected_all_urls)


    @patch('requests.get')
    def test_check_url_reachable(self, mock_get):
        # Mock rationale: We need to simulate network responses without making actual HTTP requests.
        # This ensures tests are fast, deterministic, and don't rely on external services.

        # Test case 1: URL is reachable (200 OK)
        mock_response_ok = MagicMock()
        mock_response_ok.status_code = 200
        mock_get.return_value = mock_response_ok
        is_reachable, message = check_url_reachable("https://example.com")
        self.assertTrue(is_reachable)
        self.assertEqual(message, "OK")
        mock_get.assert_called_once_with("https://example.com", timeout=5, allow_redirects=True)
        mock_get.reset_mock()

        # Test case 2: URL returns 404 Not Found
        mock_response_404 = MagicMock()
        mock_response_404.status_code = 404
        mock_get.return_value = mock_response_404
        is_reachable, message = check_url_reachable("https://example.com/nonexistent")
        self.assertFalse(is_reachable)
        self.assertEqual(message, "HTTP Error: 404")
        mock_get.reset_mock()

        # Test case 3: Connection Error
        mock_get.side_effect = requests.exceptions.ConnectionError("Failed to connect")
        is_reachable, message = check_url_reachable("https://bad-domain.com")
        self.assertFalse(is_reachable)
        self.assertEqual(message, "Connection Error")
        mock_get.reset_mock()

        # Test case 4: Timeout
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        is_reachable, message = check_url_reachable("https://slow-site.com")
        self.assertFalse(is_reachable)
        self.assertEqual(message, "Timeout")
        mock_get.reset_mock()

        # Test case 5: Not an external URL (should be skipped by this function)
        is_reachable, message = check_url_reachable("./local/path.md")
        self.assertTrue(is_reachable)
        self.assertEqual(message, "Not an external URL (skipped)")
        mock_get.assert_not_called()


    @patch('os.path.exists')
    def test_check_local_path_exists(self, mock_exists):
        # Mock rationale: We need to simulate file system existence without actually creating files.
        # This ensures tests are fast, deterministic, and don't modify the actual file system.

        base_dir = "/repo"

        # Test case 1: Path exists
        mock_exists.return_value = True
        is_exists, message = check_local_path_exists(base_dir, "./docs/file.md")
        self.assertTrue(is_exists)
        self.assertEqual(message, "OK")
        mock_exists.assert_called_once_with(os.path.normpath("/repo/docs/file.md"))
        mock_exists.reset_mock()

        # Test case 2: Path does not exist
        mock_exists.return_value = False
        is_exists, message = check_local_path_exists(base_dir, "./docs/missing.md")
        self.assertFalse(is_exists)
        self.assertEqual(message, "File Not Found")
        mock_exists.assert_called_once_with(os.path.normpath("/repo/docs/missing.md"))
        mock_exists.reset_mock()

        # Test case 3: Path with query params or anchors
        mock_exists.return_value = True
        is_exists, message = check_local_path_exists(base_dir, "./docs/file.md?v=1#section")
        self.assertTrue(is_exists)
        self.assertEqual(message, "OK")
        mock_exists.assert_called_once_with(os.path.normpath("/repo/docs/file.md"))
        mock_exists.reset_mock()

        # Test case 4: Absolute path
        mock_exists.return_value = True
        is_exists, message = check_local_path_exists(base_dir, "/README.md")
        self.assertTrue(is_exists)
        self.assertEqual(message, "OK")
        mock_exists.assert_called_once_with(os.path.normpath("/repo/README.md")) # os.path.join handles absolute paths correctly
        mock_exists.reset_mock()

        # Test case 5: External URL (should be skipped by this function)
        is_exists, message = check_local_path_exists(base_dir, "https://example.com")
        self.assertTrue(is_exists)
        self.assertEqual(message, "Not a local path (skipped)")
        mock_exists.assert_not_called()


    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('scavenger.check_url_reachable')
    @patch('scavenger.check_local_path_exists')
    def test_scan_directory_for_broken_links(
        self, mock_check_local_path_exists, mock_check_url_reachable, mock_file_open, mock_os_walk
    ):
        # Mock rationale: We need to simulate the file system structure and content,
        # as well as the results of URL and local path checks, without actual I/O or network.
        # This allows for comprehensive, isolated, and deterministic testing of the scanning logic.

        # Setup mock file system
        mock_os_walk.return_value = [
            ('/repo', ('docs', 'src'), ('README.md',)),
            ('/repo/docs', (), ('guide.md',)),
        ]

        # Mock file contents
        file_contents = {
            '/repo/README.md': """
                # Repo README
                [Good External](https://good.com)
                [Bad External](https://bad.com)
                [Good Local](./docs/guide.md)
                [Bad Local](./docs/missing.md)
                [Good Ref][good_ref]
                [Bad Ref][bad_ref]

                [good_ref]: https://good-ref.com
                [bad_ref]: ./docs/missing-ref.md
            """,
            '/repo/docs/guide.md': """
                # Guide
                [Another Good External](https://another-good.com)
                [Another Bad External](https://another-bad.com)
            """
        }
        mock_file_open.side_effect = lambda f, *args, **kwargs: mock_open(read_data=file_contents.get(f)).return_value

        # Setup mock link checkers
        mock_check_url_reachable.side_effect = [
            (True, "OK"),   # https://good.com
            (False, "HTTP Error: 404"), # https://bad.com
            (True, "OK"),   # https://good-ref.com
            (True, "OK"),   # https://another-good.com
            (False, "Connection Error"), # https://another-bad.com
        ]
        mock_check_local_path_exists.side_effect = [
            (True, "OK"),   # ./docs/guide.md (from README)
            (False, "File Not Found"), # ./docs/missing.md (from README)
            (False, "File Not Found"), # ./docs/missing-ref.md (from README ref)
        ]

        broken_links = scan_directory_for_broken_links('/repo', ['md'])

        self.assertEqual(len(broken_links), 4)

        expected_broken_links = [
            {
                'file': '/repo/README.md',
                'type': 'External',
                'link': 'https://bad.com',
                'reason': 'HTTP Error: 404'
            },
            {
                'file': '/repo/README.md',
                'type': 'Internal',
                'link': './docs/missing.md',
                'reason': 'File Not Found'
            },
            {
                'file': '/repo/README.md',
                'type': 'Internal',
                'link': './docs/missing-ref.md',
                'reason': 'File Not Found'
            },
            {
                'file': '/repo/docs/guide.md',
                'type': 'External',
                'link': 'https://another-bad.com',
                'reason': 'Connection Error'
            }
        ]
        # Sort lists of dicts for consistent comparison
        self.assertCountEqual(broken_links, expected_broken_links)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('scavenger.scan_directory_for_broken_links')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_broken_links(self, mock_parse_args, mock_scan, mock_stdout, mock_exit):
        # Mock rationale: We need to control command-line arguments, the output of the scanner,
        # and prevent actual program exit to test the main function's logic and output.

        mock_parse_args.return_value = MagicMock(path='.', extensions='md')
        mock_scan.return_value = [] # No broken links
        
        main()
        
        mock_scan.assert_called_once_with('.', ['md'])
        mock_stdout.write.assert_any_call("\nScan complete. No broken links found. The digital wasteland is surprisingly intact!\n")
        mock_exit.assert_called_once_with(0)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('scavenger.scan_directory_for_broken_links')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_broken_links(self, mock_parse_args, mock_scan, mock_stdout, mock_exit):
        # Mock rationale: Same as above, but simulating the case where broken links are found.

        mock_parse_args.return_value = MagicMock(path='.', extensions='md')
        mock_scan.return_value = [
            {
                "file": "test.md",
                "type": "External",
                "link": "https://broken.com",
                "reason": "HTTP Error: 404"
            }
        ]
        
        main()
        
        mock_scan.assert_called_once_with('.', ['md'])
        mock_stdout.write.assert_any_call("\n--- Broken Links Found ---\n")
        mock_stdout.write.assert_any_call("File: test.md\n")
        mock_stdout.write.assert_any_call("  Type: External\n")
        mock_stdout.write.assert_any_call("  Link: https://broken.com\n")
        mock_stdout.write.assert_any_call("  Reason: HTTP Error: 404\n\n")
        mock_stdout.write.assert_any_call("Scan complete. Found 1 broken links.\n")
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
