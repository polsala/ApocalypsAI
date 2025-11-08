import unittest
from unittest.mock import patch, Mock
import os
import sys
from io import StringIO
from src.link_necromancer import extract_links_from_markdown, check_url_status, main

class TestLinkNecromancer(unittest.TestCase):

    def test_extract_links_from_markdown(self):
        markdown_content = """
        # My Document

        This is a link to [Google](https://www.google.com).
        Another link: [GitHub](https://github.com/polsala/ApocalypsAI).
        A link with a query: [Example](http://example.com/path?query=1&param=2).
        No link here.
        [Local link](/path/to/local) - should not be extracted.
        [FTP link](ftp://ftp.example.com) - should not be extracted.
        """
        expected_links = [
            "https://www.google.com",
            "https://github.com/polsala/ApocalypsAI",
            "http://example.com/path?query=1&param=2"
        ]
        self.assertCountEqual(extract_links_from_markdown(markdown_content), expected_links)

        self.assertEqual(extract_links_from_markdown("No links at all."), [])
        self.assertEqual(extract_links_from_markdown("[text](http://)"), []) # Invalid URL after http://

    @patch('requests.head')
    def test_check_url_status_alive(self, mock_head):
        # Mock rationale: We don't want to make actual network requests during tests.
        # We simulate a successful HTTP HEAD response.
        mock_response = Mock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response

        is_alive, status_code, error_message = check_url_status("http://alive.com")
        self.assertTrue(is_alive)
        self.assertEqual(status_code, 200)
        self.assertIsNone(error_message)
        mock_head.assert_called_once_with("http://alive.com", timeout=5.0, allow_redirects=True)

    @patch('requests.head')
    def test_check_url_status_dead_404(self, mock_head):
        # Mock rationale: Simulate a 404 Not Found response without actual network calls.
        mock_response = Mock()
        mock_response.status_code = 404
        mock_head.return_value = mock_response

        is_alive, status_code, error_message = check_url_status("http://dead.com/404")
        self.assertFalse(is_alive)
        self.assertEqual(status_code, 404)
        self.assertIsNone(error_message)

    @patch('requests.head')
    def test_check_url_status_connection_error(self, mock_head):
        # Mock rationale: Simulate a network connection error (e.g., DNS failure, host down).
        mock_head.side_effect = requests.exceptions.ConnectionError("Failed to connect")

        is_alive, status_code, error_message = check_url_status("http://nonexistent.com")
        self.assertFalse(is_alive)
        self.assertIsNone(status_code)
        self.assertIn("Failed to connect", error_message)

    @patch('requests.head')
    def test_check_url_status_timeout(self, mock_head):
        # Mock rationale: Simulate a request timeout.
        mock_head.side_effect = requests.exceptions.Timeout("Request timed out")

        is_alive, status_code, error_message = check_url_status("http://slow.com")
        self.assertFalse(is_alive)
        self.assertIsNone(status_code)
        self.assertIn("Request timed out", error_message)

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('src.link_necromancer.check_url_status')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_dead_links(self, mock_stdout, mock_check_url_status, mock_open):
        # Mock rationale:
        # 1. `builtins.open`: Avoids actual file system access. We provide mock file content.
        # 2. `check_url_status`: Prevents actual network requests. All links are mocked as alive.
        # 3. `sys.stdout`: Captures print output for assertion.

        mock_open.return_value.read.return_value = """
        [Alive Link 1](https://alive1.com)
        [Alive Link 2](https://alive2.com)
        """
        mock_check_url_status.return_value = (True, 200, None) # All links are alive

        # Simulate command line arguments
        test_args = ['link_necromancer.py', 'test_file.md']
        with patch.object(sys, 'argv', test_args):
            main()

        output = mock_stdout.getvalue()
        self.assertIn("Scanning test_file.md...", output)
        self.assertIn("✅ All links alive.", output)
        self.assertIn("No dead links found across all scanned files. The documentation lives!", output)
        self.assertEqual(mock_check_url_status.call_count, 2) # Two links checked

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('src.link_necromancer.check_url_status')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_dead_links(self, mock_stdout, mock_check_url_status, mock_open):
        # Mock rationale:
        # 1. `builtins.open`: Avoids actual file system access.
        # 2. `check_url_status`: Prevents actual network requests. One link is mocked as dead.
        # 3. `sys.stdout`: Captures print output for assertion.

        mock_open.return_value.read.return_value = """
        [Alive Link](https://alive.com)
        [Dead Link](https://dead.com)
        """
        # Configure mock_check_url_status to return different values for different calls
        mock_check_url_status.side_effect = [
            (True, 200, None),  # First link is alive
            (False, 404, None)  # Second link is dead
        ]

        test_args = ['link_necromancer.py', 'test_file.md']
        with patch.object(sys, 'argv', test_args):
            main()

        output = mock_stdout.getvalue()
        self.assertIn("Scanning test_file.md...", output)
        self.assertIn("💀 Dead link found: https://dead.com (Status: 404)", output)
        self.assertIn("Some dead links were found. Time for some necromancy!", output)
        self.assertEqual(mock_check_url_status.call_count, 2)

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('src.link_necromancer.check_url_status')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_file_not_found(self, mock_stdout, mock_check_url_status, mock_open):
        # Mock rationale:
        # 1. `builtins.open`: Simulate FileNotFoundError.
        # 2. `check_url_status`: Not called in this scenario, but mocked for consistency.
        # 3. `sys.stdout`: Captures print output.

        mock_open.side_effect = FileNotFoundError
        
        test_args = ['link_necromancer.py', 'non_existent_file.md']
        with patch.object(sys, 'argv', test_args):
            main()

        output = mock_stdout.getvalue()
        self.assertIn("Scanning non_existent_file.md...", output)
        self.assertIn("❌ Error: File not found: non_existent_file.md", output)
        self.assertIn("No dead links found across all scanned files. The documentation lives!", output) # Because no *actual* dead links were found, only a file error.
        self.assertEqual(mock_check_url_status.call_count, 0) # No links to check

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('src.link_necromancer.check_url_status')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_links_in_file(self, mock_stdout, mock_check_url_status, mock_open):
        # Mock rationale:
        # 1. `builtins.open`: Provides content without links.
        # 2. `check_url_status`: Not called as no links are extracted.
        # 3. `sys.stdout`: Captures print output.

        mock_open.return_value.read.return_value = "This file has no links."
        
        test_args = ['link_necromancer.py', 'no_links.md']
        with patch.object(sys, 'argv', test_args):
            main()

        output = mock_stdout.getvalue()
        self.assertIn("Scanning no_links.md...", output)
        self.assertIn("ℹ️ No external links found.", output)
        self.assertIn("No dead links found across all scanned files. The documentation lives!", output)
        self.assertEqual(mock_check_url_status.call_count, 0)

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('src.link_necromancer.check_url_status')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_multiple_files(self, mock_stdout, mock_check_url_status, mock_open):
        # Mock rationale:
        # 1. `builtins.open`: Provides different content for different files.
        # 2. `check_url_status`: Mocks link status for multiple files.
        # 3. `sys.stdout`: Captures print output.

        # Configure mock_open to return different content based on file path
        def mock_open_side_effect(file_path, *args, **kwargs):
            if file_path == 'file1.md':
                mock_file = Mock()
                mock_file.read.return_value = "[Link1](https://link1.com)"
                return mock_file
            elif file_path == 'file2.md':
                mock_file = Mock()
                mock_file.read.return_value = "[Link2](https://link2.com)"
                return mock_file
            raise FileNotFoundError
        
        mock_open.side_effect = mock_open_side_effect

        # Configure check_url_status for the two links
        mock_check_url_status.side_effect = [
            (True, 200, None),  # link1.com is alive
            (False, None, "Connection refused") # link2.com is dead
        ]

        test_args = ['link_necromancer.py', 'file1.md', 'file2.md']
        with patch.object(sys, 'argv', test_args):
            main()

        output = mock_stdout.getvalue()
        self.assertIn("Scanning file1.md...", output)
        self.assertIn("✅ All links alive.", output)
        self.assertIn("Scanning file2.md...", output)
        self.assertIn("💀 Dead link found: https://link2.com (Error: Connection refused)", output)
        self.assertIn("Some dead links were found. Time for some necromancy!", output)
        self.assertEqual(mock_check_url_status.call_count, 2)


if __name__ == '__main__':
    unittest.main()
