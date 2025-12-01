import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys

# Add the src directory to the path to allow importing linker.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from linker import find_and_link_duplicates, calculate_file_hash

class TestLinker(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.path.getsize')
    @patch('os.remove')
    @patch('os.link')
    def test_find_and_link_duplicates_basic(self, mock_link, mock_remove, mock_getsize, mock_isdir, mock_walk, mock_open_func):
        # Mock rationale: Simulate a directory structure with files and their contents.
        # This allows testing the core logic without actual file system interaction.

        target_dir = "/test/repo"
        mock_isdir.return_value = True
        mock_getsize.side_effect = lambda p: 100 if "fileA" in p or "fileB" in p or "fileC" in p else 50 # All test files are 100 bytes

        # Mock os.walk to return a specific directory structure
        mock_walk.return_value = [
            (target_dir, [], ["fileA.txt", "fileB.txt"]),
            (os.path.join(target_dir, "subdir"), [], ["fileC.txt", "unique.txt"])
        ]

        # Mock file contents for hashing
        # fileA.txt and fileC.txt will have the same content (and thus hash)
        # fileB.txt will have different content
        # unique.txt will have different content
        file_contents = {
            os.path.join(target_dir, "fileA.txt"): b"content_A",
            os.path.join(target_dir, "fileB.txt"): b"content_B",
            os.path.join(target_dir, "subdir", "fileC.txt"): b"content_A", # Duplicate of fileA.txt
            os.path.join(target_dir, "subdir", "unique.txt"): b"content_unique"
        }

        def mock_open_side_effect(filepath, mode='r', **kwargs):
            if 'b' in mode:
                mock_file = MagicMock()
                mock_file.__enter__.return_value.read.side_effect = [file_contents.get(filepath, b''), b'']
                return mock_file
            return mock_open_func(filepath, mode, **kwargs)

        mock_open_func.side_effect = mock_open_side_effect

        linked_files, bytes_saved = find_and_link_duplicates(target_dir)

        # Assertions
        self.assertEqual(len(linked_files), 1)
        self.assertEqual(linked_files[0][0], os.path.join(target_dir, "subdir", "fileC.txt"))
        self.assertEqual(linked_files[0][1], os.path.join(target_dir, "fileA.txt"))

        # Verify os.remove was called for the duplicate
        mock_remove.assert_called_once_with(os.path.join(target_dir, "subdir", "fileC.txt"))

        # Verify os.link was called to link the duplicate to the master
        mock_link.assert_called_once_with(
            os.path.join(target_dir, "fileA.txt"),
            os.path.join(target_dir, "subdir", "fileC.txt")
        )

        # Verify bytes saved (one file of 100 bytes was replaced)
        self.assertEqual(bytes_saved, 100)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.path.getsize')
    @patch('os.remove')
    @patch('os.link')
    def test_find_and_link_duplicates_no_duplicates(self, mock_link, mock_remove, mock_getsize, mock_isdir, mock_walk, mock_open_func):
        # Mock rationale: Simulate a directory with no duplicate files.
        # This ensures the utility correctly identifies the absence of duplicates and performs no linking.

        target_dir = "/test/repo"
        mock_isdir.return_value = True
        mock_getsize.return_value = 100

        mock_walk.return_value = [
            (target_dir, [], ["fileA.txt", "fileB.txt"])
        ]

        file_contents = {
            os.path.join(target_dir, "fileA.txt"): b"content_A",
            os.path.join(target_dir, "fileB.txt"): b"content_B"
        }

        def mock_open_side_effect(filepath, mode='r', **kwargs):
            if 'b' in mode:
                mock_file = MagicMock()
                mock_file.__enter__.return_value.read.side_effect = [file_contents.get(filepath, b''), b'']
                return mock_file
            return mock_open_func(filepath, mode, **kwargs)

        mock_open_func.side_effect = mock_open_side_effect

        linked_files, bytes_saved = find_and_link_duplicates(target_dir)

        self.assertEqual(len(linked_files), 0)
        self.assertEqual(bytes_saved, 0)
        mock_remove.assert_not_called()
        mock_link.assert_not_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.path.getsize')
    @patch('os.remove')
    @patch('os.link')
    def test_find_and_link_duplicates_multiple_duplicates(self, mock_link, mock_remove, mock_getsize, mock_isdir, mock_walk, mock_open_func):
        # Mock rationale: Simulate a scenario with multiple duplicate files for the same content.
        # This tests the utility's ability to handle more complex duplication patterns.

        target_dir = "/test/repo"
        mock_isdir.return_value = True
        mock_getsize.return_value = 100 # All files are 100 bytes

        mock_walk.return_value = [
            (target_dir, [], ["file1.txt", "file2.txt"]),
            (os.path.join(target_dir, "sub1"), [], ["file3.txt"]),
            (os.path.join(target_dir, "sub2"), [], ["file4.txt"])
        ]

        file_contents = {
            os.path.join(target_dir, "file1.txt"): b"content_X",
            os.path.join(target_dir, "file2.txt"): b"content_Y",
            os.path.join(target_dir, "sub1", "file3.txt"): b"content_X", # Duplicate of file1.txt
            os.path.join(target_dir, "sub2", "file4.txt"): b"content_X"  # Duplicate of file1.txt
        }

        def mock_open_side_effect(filepath, mode='r', **kwargs):
            if 'b' in mode:
                mock_file = MagicMock()
                mock_file.__enter__.return_value.read.side_effect = [file_contents.get(filepath, b''), b'']
                return mock_file
            return mock_open_func(filepath, mode, **kwargs)

        mock_open_func.side_effect = mock_open_side_effect

        linked_files, bytes_saved = find_and_link_duplicates(target_dir)

        self.assertEqual(len(linked_files), 2)
        # Ensure deterministic order for assertions
        linked_files.sort(key=lambda x: x[0])

        self.assertEqual(linked_files[0][0], os.path.join(target_dir, "sub1", "file3.txt"))
        self.assertEqual(linked_files[0][1], os.path.join(target_dir, "file1.txt"))
        self.assertEqual(linked_files[1][0], os.path.join(target_dir, "sub2", "file4.txt"))
        self.assertEqual(linked_files[1][1], os.path.join(target_dir, "file1.txt"))

        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call(os.path.join(target_dir, "sub1", "file3.txt"))
        mock_remove.assert_any_call(os.path.join(target_dir, "sub2", "file4.txt"))

        self.assertEqual(mock_link.call_count, 2)
        mock_link.assert_any_call(os.path.join(target_dir, "file1.txt"), os.path.join(target_dir, "sub1", "file3.txt"))
        mock_link.assert_any_call(os.path.join(target_dir, "file1.txt"), os.path.join(target_dir, "sub2", "file4.txt"))

        self.assertEqual(bytes_saved, 200) # Two files of 100 bytes each were replaced

    @patch('os.path.isdir')
    def test_find_and_link_duplicates_invalid_directory(self, mock_isdir):
        # Mock rationale: Test error handling for non-existent directories.
        # This ensures the utility fails gracefully when provided invalid input.

        mock_isdir.return_value = False
        with self.assertRaisesRegex(ValueError, "Directory not found"):
            find_and_link_duplicates("/non/existent/dir")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.path.getsize')
    @patch('os.remove')
    @patch('os.link')
    def test_find_and_link_duplicates_io_error_on_read(self, mock_link, mock_remove, mock_getsize, mock_isdir, mock_walk, mock_open_func):
        # Mock rationale: Simulate an IOError during file reading (e.g., permissions).
        # This ensures the utility can handle unreadable files without crashing and continues processing others.

        target_dir = "/test/repo"
        mock_isdir.return_value = True
        mock_getsize.return_value = 100

        mock_walk.return_value = [
            (target_dir, [], ["readable.txt", "unreadable.txt"])
        ]

        file_contents = {
            os.path.join(target_dir, "readable.txt"): b"content_readable",
        }

        def mock_open_side_effect(filepath, mode='r', **kwargs):
            if filepath == os.path.join(target_dir, "unreadable.txt"):
                raise IOError("Permission denied")
            if 'b' in mode:
                mock_file = MagicMock()
                mock_file.__enter__.return_value.read.side_effect = [file_contents.get(filepath, b''), b'']
                return mock_file
            return mock_open_func(filepath, mode, **kwargs)

        mock_open_func.side_effect = mock_open_side_effect

        # Expect no duplicates, as unreadable.txt won't be hashed
        linked_files, bytes_saved = find_and_link_duplicates(target_dir)

        self.assertEqual(len(linked_files), 0)
        self.assertEqual(bytes_saved, 0)
        mock_remove.assert_not_called()
        mock_link.assert_not_called()

    def test_calculate_file_hash(self):
        # Mock rationale: Test the hashing function in isolation with known inputs.
        # This ensures the core hashing logic is correct and deterministic.

        # Create a mock file object for testing
        mock_file_content = b"This is a test file content."
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.side_effect = [mock_file_content, b'']

        with patch('builtins.open', return_value=mock_file):
            # Calculate hash using the mocked file
            test_hash = calculate_file_hash("dummy_path.txt")
            # Expected SHA256 hash for "This is a test file content."
            expected_hash = hashlib.sha256(mock_file_content).hexdigest()
            self.assertEqual(test_hash, expected_hash)

if __name__ == '__main__':
    unittest.main()
