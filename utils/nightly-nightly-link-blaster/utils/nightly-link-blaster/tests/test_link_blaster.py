import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import requests
from src.link_blaster import find_markdown_files, extract_links_from_markdown, check_link, main

class TestLinkBlaster(unittest.TestCase):

    @patch('os.walk')
    def test_find_markdown_files(self, mock_os_walk):
        # Mock rationale: Simulate a file system structure without actual disk I/O.
        mock_os_walk.return_value = [
            ('/repo', ('docs', 'src'), ('README.md', 'LICENSE')),
            ('/repo/docs', (), ('guide.md', 'faq.txt')),
            ('/repo/src', (), ('main.py',))
        ]
        files = find_markdown_files('/repo')
        expected_files = [
            os.path.join('/repo', 'README.md'),
            os.path.join('/repo/docs', 'guide.md')
        ]
        self.assertCountEqual(files, expected_files)

        # Test with no markdown files
        mock_os_walk.return_value = [
            ('/repo', ('src',), ('main.py',)),
            ('/repo/src', (), ('helper.txt',))
        ]
        self.assertEqual(find_markdown_files('/repo'), [])

    @patch('builtins.open', new_callable=mock_open)
    def test_extract_links_from_markdown(self, mock_file_open):
        # Mock rationale: Simulate reading file content without actual disk I/O.
        mock_file_open.return_value.read.return_value = (
            "# My Doc\n\n"
            "This is a [good link](https://example.com/page1).\n"
            "Another link: [ApocalypsAI](https://polsala.github.io/ApocalypsAI/).\n"
            "No link here.\n"
            "A broken link: [404](http://broken.link/404).\n"
            "Internal link [relative](/path/to/file) should be ignored.\n"
            "Link with query params: [params](https://example.com/search?q=test&id=123).\n"
            "Link with hash: [hash](https://example.com/page#section).\n"
        )
        filepath = 'test.md'
        links = extract_links_from_markdown(filepath)
        expected_links = [
            ('good link', 'https://example.com/page1', 3),
            ('ApocalypsAI', 'https://polsala.github.io/ApocalypsAI/', 4),
            ('404', 'http://broken.link/404', 6),
            ('params', 'https://example.com/search?q=test&id=123', 8),
            ('hash', 'https://example.com/page#section', 9)
        ]
        self.assertCountEqual(links, expected_links)

        # Test with no links
        mock_file_open.return_value.read.return_value = "# No Links\nJust plain text."
        self.assertEqual(extract_links_from_markdown('no_links.md'), [])

        # Test with file read error
        mock_file_open.side_effect = IOError("Permission denied")
        with patch('builtins.print') as mock_print:
            links = extract_links_from_markdown('error.md')
            self.assertEqual(links, [])
            mock_print.assert_called_with("Error reading file error.md: Permission denied")

    @patch('requests.head')
    def test_check_link_success(self, mock_requests_head):
        # Mock rationale: Simulate a successful HTTP response without actual network requests.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests_head.return_value = mock_response

        status = check_link('https://example.com')
        self.assertEqual(status, 200)
        mock_requests_head.assert_called_once_with('https://example.com', timeout=5, allow_redirects=True)

    @patch('requests.head')
    def test_check_link_broken(self, mock_requests_head):
        # Mock rationale: Simulate a broken HTTP response (404) without actual network requests.
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_head.return_value = mock_response

        status = check_link('http://broken.link/404')
        self.assertEqual(status, 404)

    @patch('requests.head')
    def test_check_link_server_error(self, mock_requests_head):
        # Mock rationale: Simulate a server error HTTP response (500) without actual network requests.
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_requests_head.return_value = mock_response

        status = check_link('http://server.error/500')
        self.assertEqual(status, 500)

    @patch('requests.head')
    def test_check_link_network_error(self, mock_requests_head):
        # Mock rationale: Simulate a network connection error without actual network requests.
        mock_requests_head.side_effect = requests.exceptions.ConnectionError("DNS lookup failed")

        status = check_link('http://nonexistent.domain')
        self.assertEqual(status, 0) # 0 indicates network error

    @patch('src.link_blaster.find_markdown_files')
    @patch('src.link_blaster.extract_links_from_markdown')
    @patch('src.link_blaster.check_link')
    @patch('builtins.print')
    def test_main_no_markdown_files(self, mock_print, mock_check_link, mock_extract_links, mock_find_md_files):
        # Mock rationale: Simulate no Markdown files being found to test the early exit condition.
        mock_find_md_files.return_value = []
        main()
        mock_print.assert_any_call("No Markdown files found to scan. All links are implicitly perfect! ✨")
        mock_extract_links.assert_not_called()
        mock_check_link.assert_not_called()

    @patch('src.link_blaster.find_markdown_files')
    @patch('src.link_blaster.extract_links_from_markdown')
    @patch('src.link_blaster.check_link')
    @patch('builtins.print')
    def test_main_no_links_in_markdown(self, mock_print, mock_check_link, mock_extract_links, mock_find_md_files):
        # Mock rationale: Simulate Markdown files existing but containing no external links.
        mock_find_md_files.return_value = ['doc1.md']
        mock_extract_links.return_value = []
        main()
        mock_print.assert_any_call("No external links found in Markdown files. Your documentation is a pristine, link-free paradise! 🏝️")
        mock_check_link.assert_not_called()

    @patch('src.link_blaster.find_markdown_files')
    @patch('src.link_blaster.extract_links_from_markdown')
    @patch('src.link_blaster.check_link')
    @patch('builtins.print')
    def test_main_all_links_good(self, mock_print, mock_check_link, mock_extract_links, mock_find_md_files):
        # Mock rationale: Simulate a scenario where all extracted links are valid (200 OK).
        mock_find_md_files.return_value = ['doc1.md', 'doc2.md']
        mock_extract_links.side_effect = [
            [('Link A', 'https://good.com/a', 1)],
            [('Link B', 'https://good.com/b', 5)]
        ]
        mock_check_link.side_effect = [200, 200] # For unique URLs 'https://good.com/a', 'https://good.com/b'

        main()
        mock_print.assert_any_call("✅ All external links are sparkling clean! No broken links found. Your docs are pristine! ✨")
        self.assertEqual(mock_check_link.call_count, 2)

    @patch('src.link_blaster.find_markdown_files')
    @patch('src.link_blaster.extract_links_from_markdown')
    @patch('src.link_blaster.check_link')
    @patch('builtins.print')
    def test_main_broken_links_found(self, mock_print, mock_check_link, mock_extract_links, mock_find_md_files):
        # Mock rationale: Simulate a mix of good and broken links to verify reporting.
        mock_find_md_files.return_value = ['doc1.md', 'doc2.md']
        mock_extract_links.side_effect = [
            [('Good Link', 'https://good.com', 1), ('Broken Link', 'https://broken.com/404', 2)],
            [('Another Good', 'https://good.com', 3), ('Network Error', 'http://no.domain', 4)]
        ]
        # Order of unique URLs: 'https://good.com', 'https://broken.com/404', 'http://no.domain'
        mock_check_link.side_effect = [200, 404, 0]

        main()
        mock_print.assert_any_call("🚨 BROKEN LINKS DETECTED! 🚨\n")
        mock_print.assert_any_call("  File: doc1.md (Line: 2)")
        mock_print.assert_any_call("    URL: https://broken.com/404")
        mock_print.assert_any_call("    Status: 404 (Non-2xx)\n")
        mock_print.assert_any_call("  File: doc2.md (Line: 4)")
        mock_print.assert_any_call("    URL: http://no.domain")
        mock_print.assert_any_call("    Status: Network Error (Could not connect)\n")
        mock_print.assert_any_call("\nFix these broken links to restore your documentation's glory! 🛠️")
        self.assertEqual(mock_check_link.call_count, 3)

    @patch('src.link_blaster.find_markdown_files')
    @patch('src.link_blaster.extract_links_from_markdown')
    @patch('src.link_blaster.check_link')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_custom_path(self, mock_parse_args, mock_print, mock_check_link, mock_extract_links, mock_find_md_files):
        # Mock rationale: Test that the --path argument is correctly handled.
        mock_parse_args.return_value = MagicMock(path='/custom/path')
        mock_find_md_files.return_value = [] # No files found in custom path for simplicity
        main()
        mock_find_md_files.assert_called_once_with('/custom/path')

if __name__ == '__main__':
    unittest.main()
