import unittest
import os
import sys
import tempfile
import shutil
from unittest.mock import patch, MagicMock
import requests

# Add the src directory to the Python path to import link_checker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import link_checker

class TestLinkChecker(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing file operations
        self.test_dir = tempfile.mkdtemp()
        self.root_dir = os.path.join(self.test_dir, 'docs')
        os.makedirs(self.root_dir)

        # Create some dummy files for testing
        self.file1_path = os.path.join(self.root_dir, 'file1.md')
        with open(self.file1_path, 'w') as f:
            f.write("Content of file1.")

        self.subdir_path = os.path.join(self.root_dir, 'subdir')
        os.makedirs(self.subdir_path)
        self.file2_path = os.path.join(self.subdir_path, 'file2.md')
        with open(self.file2_path, 'w') as f:
            f.write("Content of file2.")

        self.ignored_file_path = os.path.join(self.root_dir, 'ignored.bak')
        with open(self.ignored_file_path, 'w') as f:
            f.write("This file should be ignored.")

        self.ignored_dir_path = os.path.join(self.root_dir, 'node_modules')
        os.makedirs(self.ignored_dir_path)
        with open(os.path.join(self.ignored_dir_path, 'package.md'), 'w') as f:
            f.write("Should not be scanned.")


    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def test_find_markdown_files(self):
        # Mock rationale: os.walk is a file system operation, mocking it allows deterministic testing
        # without actual file system interaction, making tests faster and isolated.
        with patch('os.walk') as mock_walk:
            mock_walk.return_value = [
                (self.root_dir, ['subdir', 'node_modules'], ['file1.md', 'ignored.bak']),
                (os.path.join(self.root_dir, 'subdir'), [], ['file2.md']),
                (os.path.join(self.root_dir, 'node_modules'), [], ['package.md'])
            ]
            files = link_checker.find_markdown_files(self.root_dir, ['node_modules/*', '*.bak'])
            expected_files = [
                os.path.join(self.root_dir, 'file1.md'),
                os.path.join(self.root_dir, 'subdir', 'file2.md')
            ]
            self.assertCountEqual(files, expected_files)

        # Test with no ignore patterns
        with patch('os.walk') as mock_walk:
            mock_walk.return_value = [
                (self.root_dir, ['subdir'], ['file1.md', 'another.md']),
                (os.path.join(self.root_dir, 'subdir'), [], ['file2.md'])
            ]
            files = link_checker.find_markdown_files(self.root_dir, [])
            expected_files = [
                os.path.join(self.root_dir, 'file1.md'),
                os.path.join(self.root_dir, 'another.md'),
                os.path.join(self.root_dir, 'subdir', 'file2.md')
            ]
            self.assertCountEqual(files, expected_files)

    def test_extract_links(self):
        content = """
        This is a [local link](path/to/file.md).
        And an [external link](https://example.com/page).
        Another [relative link](../another/file.md).
        No link here.
        [Link with spaces](path to file.md)
        [Link with query](https://example.com/search?q=test)
        """
        links = link_checker.extract_links(content)
        expected_links = [
            "path/to/file.md",
            "https://example.com/page",
            "../another/file.md",
            "path to file.md",
            "https://example.com/search?q=test"
        ]
        self.assertCountEqual(links, expected_links)

    def test_is_external_link(self):
        self.assertTrue(link_checker.is_external_link("http://example.com"))
        self.assertTrue(link_checker.is_external_link("https://example.com/path"))
        self.assertFalse(link_checker.is_external_link("path/to/file.md"))
        self.assertFalse(link_checker.is_external_link("/absolute/path/to/file.md"))
        self.assertFalse(link_checker.is_external_link("ftp://example.com")) # Not http/https

    @patch('os.path.exists')
    def test_check_local_link(self, mock_exists):
        # Mock rationale: os.path.exists is a file system operation, mocking it allows deterministic testing
        # without actual file system interaction.
        scan_root = self.root_dir # e.g., /tmp/test_dir/docs
        current_file = os.path.join(self.root_dir, 'main.md') # e.g., /tmp/test_dir/docs/main.md

        # Test existing link
        mock_exists.return_value = True
        status, reason = link_checker.check_local_link(scan_root, current_file, 'file1.md')
        self.assertTrue(status)
        self.assertEqual(reason, "OK")
        mock_exists.assert_called_with(os.path.join(self.root_dir, 'file1.md'))

        # Test non-existing link
        mock_exists.return_value = False
        status, reason = link_checker.check_local_link(scan_root, current_file, 'non-existent.md')
        self.assertFalse(status)
        self.assertEqual(reason, "File not found")

        # Test relative link that exists
        mock_exists.return_value = True
        status, reason = link_checker.check_local_link(scan_root, os.path.join(self.subdir_path, 'file2.md'), '../file1.md')
        self.assertTrue(status)
        self.assertEqual(reason, "OK")
        mock_exists.assert_called_with(os.path.join(self.root_dir, 'file1.md'))

        # Test link escaping scan root
        mock_exists.return_value = True # Even if it exists, it should be flagged as escaping
        status, reason = link_checker.check_local_link(scan_root, current_file, '../../evil.md')
        self.assertFalse(status)
        self.assertEqual(reason, "Link path attempts to escape scan root")

        # Test absolute path within scan root (should be treated as valid if exists)
        mock_exists.return_value = True
        status, reason = link_checker.check_local_link(scan_root, current_file, os.path.join(self.root_dir, 'file1.md'))
        self.assertTrue(status)
        self.assertEqual(reason, "OK")
        mock_exists.assert_called_with(os.path.join(self.root_dir, 'file1.md'))

        # Test absolute path outside scan root
        mock_exists.return_value = True
        status, reason = link_checker.check_local_link(scan_root, current_file, '/etc/passwd')
        self.assertFalse(status)
        self.assertEqual(reason, "Link path attempts to escape scan root")


    @patch('requests.head')
    def test_check_external_link(self, mock_head):
        # Mock rationale: requests.head performs network requests, mocking it allows deterministic testing
        # without actual network interaction, making tests faster and isolated.

        # Test successful link
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_head.return_value = mock_response
        status, reason = link_checker.check_external_link("https://example.com")
        self.assertTrue(status)
        self.assertEqual(reason, "OK")
        mock_head.assert_called_with("https://example.com", timeout=5, allow_redirects=True)

        # Test 404 Not Found
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_head.return_value = mock_response
        status, reason = link_checker.check_external_link("https://example.com/404")
        self.assertFalse(status)
        self.assertEqual(reason, "HTTP Error: 404")

        # Test connection error
        mock_head.side_effect = requests.exceptions.ConnectionError
        status, reason = link_checker.check_external_link("https://bad-host.com")
        self.assertFalse(status)
        self.assertEqual(reason, "Connection Error")

        # Test timeout error
        mock_head.side_effect = requests.exceptions.Timeout
        status, reason = link_checker.check_external_link("https://slow-host.com")
        self.assertFalse(status)
        self.assertEqual(reason, "Timeout Error")

        # Test generic request exception
        mock_head.side_effect = requests.exceptions.RequestException("Generic error")
        status, reason = link_checker.check_external_link("https://error.com")
        self.assertFalse(status)
        self.assertEqual(reason, "Request Error: Generic error")

    @patch('link_checker.check_external_link')
    @patch('link_checker.check_local_link')
    @patch('link_checker.find_markdown_files')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('os.path.isdir')
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_functionality(self, mock_print, mock_exit, mock_isdir, mock_open, mock_find_md_files, mock_check_local, mock_check_external):
        # Mock rationale: The main function orchestrates file system access, network requests, and program exit.
        # Mocking these allows testing the logic flow without actual side effects.

        mock_isdir.return_value = True
        mock_find_md_files.return_value = [
            os.path.join(self.root_dir, 'doc1.md'),
            os.path.join(self.root_dir, 'doc2.md')
        ]

        # Mock file content for doc1.md
        mock_open.side_effect = [
            unittest.mock.mock_open(read_data="[Internal Link](file1.md)\n[External Link](https://good.com)").return_value,
            unittest.mock.mock_open(read_data="[Broken Internal Link](nonexistent.md)\n[Broken External Link](https://bad.com)").return_value
        ]

        # Configure check_local_link mocks
        mock_check_local.side_effect = [
            (True, "OK"), # For file1.md
            (False, "File not found") # For nonexistent.md
        ]

        # Configure check_external_link mocks
        mock_check_external.side_effect = [
            (True, "OK"), # For https://good.com
            (False, "HTTP Error: 404") # For https://bad.com
        ]

        # Simulate command line arguments
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path=self.root_dir,
            ignore_patterns=[],
            timeout=5
        )):
            link_checker.main()

            # Assertions
            mock_find_md_files.assert_called_once_with(os.path.abspath(self.root_dir), [])
            self.assertEqual(mock_open.call_count, 2) # Called for doc1.md and doc2.md

            # Check local link calls
            mock_check_local.assert_any_call(os.path.abspath(self.root_dir), os.path.join(self.root_dir, 'doc1.md'), 'file1.md')
            mock_check_local.assert_any_call(os.path.abspath(self.root_dir), os.path.join(self.root_dir, 'doc2.md'), 'nonexistent.md')

            # Check external link calls
            mock_check_external.assert_any_call('https://good.com', 5)
            mock_check_external.assert_any_call('https://bad.com', 5)

            # Expect exit with code 1 due to broken links
            mock_exit.assert_called_once_with(1)

            # Check print calls for expected output (simplified check)
            output_calls = [call_args[0][0] for call_args in mock_print.call_args_list]
            self.assertIn("--- Checking file:", output_calls[1])
            self.assertIn("[OK] Internal link: file1.md (OK)", output_calls[2])
            self.assertIn("[OK] External link: https://good.com (OK)", output_calls[3])
            self.assertIn("[BROKEN] Internal link: nonexistent.md (File not found)", output_calls[5])
            self.assertIn("[BROKEN] External link: https://bad.com (HTTP Error: 404)", output_calls[6])
            self.assertIn("Scan complete. Found 2 broken links in 2 files.", output_calls[-1])

        # Test case with no broken links
        mock_exit.reset_mock() # Reset exit mock for the next test
        mock_check_local.side_effect = [(True, "OK")] * 2 # All local links good
        mock_check_external.side_effect = [(True, "OK")] * 2 # All external links good
        mock_open.side_effect = [
            unittest.mock.mock_open(read_data="[Internal Link](file1.md)\n[External Link](https://good.com)").return_value,
            unittest.mock.mock_open(read_data="[Another Internal Link](file2.md)\n[Another External Link](https://another-good.com)").return_value
        ]

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path=self.root_dir,
            ignore_patterns=[],
            timeout=5
        )):
            link_checker.main()
            mock_exit.assert_called_once_with(0) # Expect exit with code 0 for no broken links


if __name__ == '__main__':
    unittest.main()
