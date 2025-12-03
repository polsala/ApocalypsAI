import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
import shutil

# Import the functions to be tested
from src.link_stabilizer import (
    find_markdown_files,
    extract_links,
    check_external_link,
    check_internal_link
)

class TestLinkStabilizer(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.base_dir = self.test_dir # For check_internal_link's base_dir argument

        # Create some dummy Markdown files and directories
        os.makedirs(os.path.join(self.test_dir, 'docs'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'src'), exist_ok=True)

        self.file1_path = os.path.join(self.test_dir, 'docs', 'doc1.md')
        with open(self.file1_path, 'w') as f:
            f.write("# Doc 1\n")
            f.write("[Google](https://www.google.com)\n")
            f.write("[Broken External](http://broken.example.com/404)\n")
            f.write("[Local File](../src/code.md)\n")
            f.write("[Non Existent Local File](./non_existent.md)\n")
            f.write("[Anchor Link](#section)\n") # Should be ignored

        self.file2_path = os.path.join(self.test_dir, 'src', 'code.md')
        with open(self.file2_path, 'w') as f:
            f.write("# Code Doc\n")
            f.write("[Python Docs](https://docs.python.org/3/)\n")

        self.non_md_file_path = os.path.join(self.test_dir, 'src', 'script.py')
        with open(self.non_md_file_path, 'w') as f:
            f.write("print('hello')")

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    @patch('os.walk')
    def test_find_markdown_files(self, mock_os_walk):
        # Mock rationale: Simulate file system structure without creating actual files
        # to ensure deterministic and fast tests.
        mock_os_walk.return_value = [
            (self.test_dir, ['docs', 'src'], ['README.md']),
            (os.path.join(self.test_dir, 'docs'), [], ['doc1.md', 'image.png']),
            (os.path.join(self.test_dir, 'src'), [], ['code.md', 'script.py'])
        ]
        
        expected_files = sorted([
            os.path.join(self.test_dir, 'README.md'),
            os.path.join(self.test_dir, 'docs', 'doc1.md'),
            os.path.join(self.test_dir, 'src', 'code.md')
        ])
        found_files = sorted(find_markdown_files(self.test_dir))
        self.assertEqual(found_files, expected_files)

    def test_extract_links(self):
        external, internal = extract_links(self.file1_path)
        self.assertIn('https://www.google.com', external)
        self.assertIn('http://broken.example.com/404', external)
        self.assertIn('../src/code.md', internal)
        self.assertIn('./non_existent.md', internal)
        self.assertNotIn('#section', internal) # Anchor links should be ignored
        self.assertEqual(len(external), 2)
        self.assertEqual(len(internal), 2)

    @patch('requests.head')
    def test_check_external_link_success(self, mock_head):
        # Mock rationale: Simulate a successful HTTP response without making
        # an actual network call, ensuring tests are fast and deterministic.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.reason = 'OK'
        mock_head.return_value = mock_response

        is_valid, reason = check_external_link('https://www.google.com')
        self.assertTrue(is_valid)
        self.assertIn('Status: 200', reason)

    @patch('requests.head')
    def test_check_external_link_failure_404(self, mock_head):
        # Mock rationale: Simulate a 404 HTTP response without making
        # an actual network call, ensuring tests are fast and deterministic.
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.reason = 'Not Found'
        mock_head.return_value = mock_response

        is_valid, reason = check_external_link('http://broken.example.com/404')
        self.assertFalse(is_valid)
        self.assertIn('Status: 404 Not Found', reason)

    @patch('requests.head')
    def test_check_external_link_failure_connection_error(self, mock_head):
        # Mock rationale: Simulate a network connection error without making
        # an actual network call, ensuring tests are fast and deterministic.
        mock_head.side_effect = requests.exceptions.ConnectionError

        is_valid, reason = check_external_link('http://unreachable.com')
        self.assertFalse(is_valid)
        self.assertEqual('Connection Error', reason)

    @patch('os.path.exists')
    @patch('os.path.abspath')
    @patch('os.path.commonpath')
    def test_check_internal_link_exists(self, mock_commonpath, mock_abspath, mock_exists):
        # Mock rationale: Simulate file existence and path resolution without
        # relying on actual files or system paths, ensuring tests are isolated and deterministic.
        mock_exists.return_value = True
        mock_abspath.side_effect = lambda x: x # Mock abspath to return input for simplicity in this test
        mock_commonpath.return_value = self.base_dir # Assume path is within base_dir

        current_file = os.path.join(self.test_dir, 'docs', 'doc1.md')
        target_path = '../src/code.md'
        is_valid, reason = check_internal_link(self.base_dir, current_file, target_path)
        self.assertTrue(is_valid)
        self.assertEqual('File exists', reason)
        # Verify that os.path.exists was called with the resolved path
        expected_resolved_path = os.path.normpath(os.path.join(os.path.dirname(current_file), target_path))
        mock_exists.assert_called_with(expected_resolved_path)

    @patch('os.path.exists')
    @patch('os.path.abspath')
    @patch('os.path.commonpath')
    def test_check_internal_link_not_exists(self, mock_commonpath, mock_abspath, mock_exists):
        # Mock rationale: Simulate file non-existence and path resolution without
        # relying on actual files or system paths, ensuring tests are isolated and deterministic.
        mock_exists.return_value = False
        mock_abspath.side_effect = lambda x: x # Mock abspath to return input for simplicity in this test
        mock_commonpath.return_value = self.base_dir # Assume path is within base_dir

        current_file = os.path.join(self.test_dir, 'docs', 'doc1.md')
        target_path = './non_existent.md'
        is_valid, reason = check_internal_link(self.base_dir, current_file, target_path)
        self.assertFalse(is_valid)
        self.assertEqual('File not found', reason)
        expected_resolved_path = os.path.normpath(os.path.join(os.path.dirname(current_file), target_path))
        mock_exists.assert_called_with(expected_resolved_path)

    @patch('os.path.exists')
    @patch('os.path.abspath')
    @patch('os.path.commonpath')
    def test_check_internal_link_outside_base_dir(self, mock_commonpath, mock_abspath, mock_exists):
        # Mock rationale: Simulate a path pointing outside the allowed base directory
        # without relying on actual file system, ensuring security and scope checks are deterministic.
        mock_abspath.side_effect = lambda x: x # Mock abspath to return input for simplicity
        # Simulate commonpath indicating the target is NOT within the base_dir
        mock_commonpath.return_value = '/some/other/path'

        current_file = os.path.join(self.test_dir, 'docs', 'doc1.md')
        target_path = '/etc/passwd' # An absolute path outside the test_dir
        is_valid, reason = check_internal_link(self.base_dir, current_file, target_path)
        self.assertFalse(is_valid)
        self.assertIn("points outside the scanned directory", reason)
        mock_exists.assert_not_called() # Should not call exists if path is outside scope

if __name__ == '__main__':
    unittest.main()
