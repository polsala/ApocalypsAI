import unittest
import os
import tempfile
import shutil
import hashlib
from unittest.mock import patch, MagicMock

# Import the functions from the main script
from src.deduplicator import calculate_file_hash, find_duplicates, main, CHUNK_SIZE

class TestDeduplicator(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir) # Change CWD to simplify paths in tests

    def tearDown(self):
        # Clean up the temporary directory
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def _create_file(self, filename, content):
        filepath = os.path.join(self.test_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath

    def test_calculate_file_hash_basic(self):
        filepath = self._create_file('test_file.txt', 'hello world')
        expected_hash = hashlib.sha256(b'hello world').hexdigest()
        self.assertEqual(calculate_file_hash(filepath), expected_hash)

    def test_calculate_file_hash_empty_file(self):
        filepath = self._create_file('empty.txt', '')
        expected_hash = hashlib.sha256(b'').hexdigest()
        self.assertEqual(calculate_file_hash(filepath), expected_hash)

    def test_calculate_file_hash_large_file(self):
        # Test with content larger than CHUNK_SIZE
        long_content = 'a' * (CHUNK_SIZE * 2 + 100)
        filepath = self._create_file('large_file.txt', long_content)
        expected_hash = hashlib.sha256(long_content.encode()).hexdigest()
        self.assertEqual(calculate_file_hash(filepath), expected_hash)

    def test_calculate_file_hash_non_existent_file(self):
        self.assertIsNone(calculate_file_hash('non_existent.txt'))

    def test_find_duplicates_no_duplicates(self):
        self._create_file('file1.txt', 'content A')
        self._create_file('file2.txt', 'content B')
        self._create_file('subdir/file3.txt', 'content C')
        duplicates = find_duplicates(self.test_dir)
        self.assertFalse(duplicates)

    def test_find_duplicates_with_duplicates(self):
        file_a1 = self._create_file('file_a1.txt', 'duplicate content')
        file_a2 = self._create_file('file_a2.txt', 'duplicate content')
        file_b1 = self._create_file('subdir/file_b1.txt', 'another duplicate')
        file_b2 = self._create_file('subdir2/file_b2.txt', 'another duplicate')
        self._create_file('unique.txt', 'unique content')

        duplicates = find_duplicates(self.test_dir)
        self.assertEqual(len(duplicates), 2)

        hash_a = hashlib.sha256(b'duplicate content').hexdigest()
        hash_b = hashlib.sha256(b'another duplicate').hexdigest()

        self.assertIn(hash_a, duplicates)
        self.assertIn(hash_b, duplicates)

        self.assertCountEqual(duplicates[hash_a], [file_a1, file_a2])
        self.assertCountEqual(duplicates[hash_b], [file_b1, file_b2])

    def test_find_duplicates_with_empty_files(self):
        file_e1 = self._create_file('empty1.txt', '')
        file_e2 = self._create_file('empty2.txt', '')
        self._create_file('empty_unique.txt', 'not empty')

        duplicates = find_duplicates(self.test_dir)
        self.assertEqual(len(duplicates), 1)

        hash_empty = hashlib.sha256(b'').hexdigest()
        self.assertIn(hash_empty, duplicates)
        self.assertCountEqual(duplicates[hash_empty], [file_e1, file_e2])

    @patch('builtins.print')
    @patch('os.remove')
    @patch('os.path.getsize', return_value=100) # Mock rationale: Avoid actual file system calls for size, ensure deterministic size for reporting.
    def test_main_dry_run(self, mock_getsize, mock_remove, mock_print):
        self._create_file('file_a1.txt', 'duplicate content')
        self._create_file('file_a2.txt', 'duplicate content')

        # Mock rationale: Simulate command line arguments for main function.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            directory=self.test_dir,
            dry_run=True,
            delete=False
        )):
            main()

        mock_remove.assert_not_called() # Mock rationale: Ensure no deletion occurs in dry-run mode.
        mock_print.assert_any_call(unittest.mock.ANY)
        mock_print.assert_any_call(f"If --delete were used, 1 files (totaling {100 / (1024*1024):.2f} MB) would be deleted.")
        mock_print.assert_any_call("No files were modified or deleted.")

    @patch('builtins.print')
    @patch('os.remove')
    @patch('builtins.input', return_value='y') # Mock rationale: Simulate user confirming deletion.
    @patch('os.path.getsize', return_value=100) # Mock rationale: Avoid actual file system calls for size, ensure deterministic size for reporting.
    def test_main_delete_confirmed(self, mock_getsize, mock_input, mock_remove, mock_print):
        file_a1 = self._create_file('file_a1.txt', 'duplicate content')
        file_a2 = self._create_file('file_a2.txt', 'duplicate content')

        # Mock rationale: Simulate command line arguments for main function.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            directory=self.test_dir,
            dry_run=False,
            delete=True
        )):
            main()

        # Mock rationale: Verify that os.remove was called for the duplicate file.
        mock_remove.assert_called_once_with(file_a2)
        mock_print.assert_any_call(f"Deleted: {file_a2}")
        mock_print.assert_any_call("\nSuccessfully deleted 1 duplicate files.")

    @patch('builtins.print')
    @patch('os.remove')
    @patch('builtins.input', return_value='n') # Mock rationale: Simulate user declining deletion.
    @patch('os.path.getsize', return_value=100) # Mock rationale: Avoid actual file system calls for size, ensure deterministic size for reporting.
    def test_main_delete_cancelled(self, mock_getsize, mock_input, mock_remove, mock_print):
        self._create_file('file_a1.txt', 'duplicate content')
        self._create_file('file_a2.txt', 'duplicate content')

        # Mock rationale: Simulate command line arguments for main function.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            directory=self.test_dir,
            dry_run=False,
            delete=True
        )):
            main()

        mock_remove.assert_not_called() # Mock rationale: Ensure no deletion occurs if cancelled.
        mock_print.assert_any_call("Deletion cancelled. No files were deleted.")

    @patch('builtins.print')
    @patch('sys.exit') # Mock rationale: Prevent actual program exit during test.
    def test_main_directory_not_found(self, mock_exit, mock_print):
        # Mock rationale: Simulate command line arguments for main function with a non-existent directory.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            directory='/non/existent/path',
            dry_run=False,
            delete=False
        )):
            main()

        mock_print.assert_any_call("Error: Directory not found: /non/existent/path")
        mock_exit.assert_called_once_with(1) # Mock rationale: Verify program exits with error code.

    @patch('builtins.print')
    @patch('sys.exit') # Mock rationale: Prevent actual program exit during test.
    def test_main_no_duplicates_found(self, mock_exit, mock_print):
        self._create_file('unique1.txt', 'content1')
        self._create_file('unique2.txt', 'content2')

        # Mock rationale: Simulate command line arguments for main function.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            directory=self.test_dir,
            dry_run=False,
            delete=False
        )):
            main()

        mock_print.assert_any_call("No duplicate files found. Your data hoard is pristine!")
        mock_exit.assert_called_once_with(0) # Mock rationale: Verify program exits with success code.

    def test_find_duplicates_with_symlinks(self):
        target_file = self._create_file('target.txt', 'symlink content')
        symlink_file = os.path.join(self.test_dir, 'symlink.txt')
        os.symlink(target_file, symlink_file)

        # Create a duplicate of the target file, but not the symlink itself
        duplicate_file = self._create_file('duplicate_target.txt', 'symlink content')

        duplicates = find_duplicates(self.test_dir)
        self.assertEqual(len(duplicates), 1)

        hash_content = hashlib.sha256(b'symlink content').hexdigest()
        self.assertIn(hash_content, duplicates)
        # The symlink itself should not be considered a duplicate or even processed for its content
        self.assertCountEqual(duplicates[hash_content], [target_file, duplicate_file])


if __name__ == '__main__':
    unittest.main()
