import unittest
from unittest.mock import patch, call
import os
import sys
from io import StringIO

# Add the parent directory of 'src' to sys.path to allow importing dust_collector
# This makes the test runnable directly from the 'tests' directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.dust_collector import collect_dust, DEFAULT_THRESHOLD, QUARANTINE_DIR_NAME

# Mock rationale: We need to simulate file system operations (listing directories, getting file sizes, moving files)
# without actually touching the disk. `os.walk`, `os.path.isdir`, `os.path.isfile`, `os.path.getsize`,
# `os.makedirs`, `os.rename`, and `os.path.exists` are all mocked to provide deterministic behavior and prevent side effects.
# `sys.stdout` and `sys.stderr` are mocked to capture printed output for assertion.

class TestCosmicDustCollector(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    def test_no_dust_found(self, mock_getsize, mock_isfile, mock_walk, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Simulate a directory with no files or only large files.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['large_file.txt'])
        ]
        mock_isfile.return_value = True
        mock_getsize.return_value = 2000 # Larger than default 1024 threshold

        collect_dust('/test_dir', DEFAULT_THRESHOLD, False)

        self.assertIn("No cosmic dust found", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    def test_dust_reported_no_quarantine(self, mock_getsize, mock_isfile, mock_walk, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Simulate a directory with small files to be reported.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', ['subdir'], ['small_file1.txt', 'large_file.log']),
            ('/test_dir/subdir', [], ['empty_file.txt', 'small_file2.json'])
        ]
        mock_isfile.side_effect = lambda x: x in [
            '/test_dir/small_file1.txt',
            '/test_dir/large_file.log',
            '/test_dir/subdir/empty_file.txt',
            '/test_dir/subdir/small_file2.json'
        ]
        mock_getsize.side_effect = lambda x: {
            '/test_dir/small_file1.txt': 100,
            '/test_dir/large_file.log': 1500,
            '/test_dir/subdir/empty_file.txt': 0,
            '/test_dir/subdir/small_file2.json': 500
        }.get(x, 0)

        collect_dust('/test_dir', DEFAULT_THRESHOLD, False)

        output = mock_stdout.getvalue()
        self.assertIn("--- Cosmic Dust Report", output)
        self.assertIn("[DUST] /test_dir/small_file1.txt (100 bytes)", output)
        self.assertIn("[DUST] /test_dir/subdir/empty_file.txt (0 bytes)", output)
        self.assertIn("[DUST] /test_dir/subdir/small_file2.json (500 bytes)", output)
        self.assertNotIn("large_file.log", output) # Should be ignored due to size
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('os.makedirs')
    @patch('os.rename')
    @patch('os.path.exists') # For collision handling
    def test_dust_quarantined(self, mock_exists, mock_rename, mock_makedirs, mock_getsize, mock_isfile, mock_walk, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Simulate a directory with small files to be quarantined.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['temp.tmp', 'log.txt'])
        ]
        mock_isfile.side_effect = lambda x: x in [
            '/test_dir/temp.tmp',
            '/test_dir/log.txt'
        ]
        mock_getsize.side_effect = lambda x: {
            '/test_dir/temp.tmp': 50,
            '/test_dir/log.txt': 200
        }.get(x, 0)
        mock_exists.return_value = False # No collision initially

        collect_dust('/test_dir', DEFAULT_THRESHOLD, True)

        output = mock_stdout.getvalue()
        self.assertIn("Initiating quarantine protocol...", output)
        self.assertIn("[QUARANTINED] /test_dir/temp.tmp (50 bytes) -> /test_dir/.quarantine/temp.tmp", output)
        self.assertIn("[QUARANTINED] /test_dir/log.txt (200 bytes) -> /test_dir/.quarantine/log.txt", output)
        self.assertEqual(mock_stderr.getvalue(), "")

        mock_makedirs.assert_called_with(os.path.join('/test_dir', QUARANTINE_DIR_NAME), exist_ok=True)
        mock_rename.assert_has_calls([
            call('/test_dir/temp.tmp', os.path.join('/test_dir', QUARANTINE_DIR_NAME, 'temp.tmp')),
            call('/test_dir/log.txt', os.path.join('/test_dir', QUARANTINE_DIR_NAME, 'log.txt'))
        ], any_order=True)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('os.makedirs')
    @patch('os.rename')
    @patch('os.path.exists') # For collision handling
    def test_quarantine_collision_handling(self, mock_exists, mock_rename, mock_makedirs, mock_getsize, mock_isfile, mock_walk, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Simulate a scenario where a file with the same name already exists in quarantine.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['duplicate.txt'])
        ]
        mock_isfile.side_effect = lambda x: x == '/test_dir/duplicate.txt'
        mock_getsize.return_value = 100

        # Simulate that /test_dir/.quarantine/duplicate.txt already exists
        def exists_side_effect(path):
            return path == os.path.join('/test_dir', '.quarantine', 'duplicate.txt')
        mock_exists.side_effect = exists_side_effect

        collect_dust('/test_dir', DEFAULT_THRESHOLD, True)

        output = mock_stdout.getvalue()
        expected_quarantine_path = os.path.join('/test_dir', QUARANTINE_DIR_NAME, 'duplicate_1.txt')
        self.assertIn(f"[QUARANTINED] /test_dir/duplicate.txt (100 bytes) -> {expected_quarantine_path}", output)
        mock_rename.assert_called_once_with('/test_dir/duplicate.txt', expected_quarantine_path)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    def test_invalid_path(self, mock_getsize, mock_isfile, mock_walk, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Test error handling for an invalid input path.
        mock_isdir.return_value = False

        with self.assertRaises(SystemExit) as cm:
            collect_dust('/non_existent_dir', DEFAULT_THRESHOLD, False)
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Path '/non_existent_dir' is not a valid directory.", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    def test_os_error_on_file_access(self, mock_getsize, mock_isfile, mock_walk, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Simulate an OSError when trying to access a file (e.g., permissions issue).
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['unreadable.txt', 'readable.txt'])
        ]
        mock_isfile.side_effect = lambda x: x in ['/test_dir/unreadable.txt', '/test_dir/readable.txt']

        def getsize_side_effect(path):
            if path == '/test_dir/unreadable.txt':
                raise OSError("Permission denied")
            elif path == '/test_dir/readable.txt':
                return 50 # Small enough to be dust
            return 0
        mock_getsize.side_effect = getsize_side_effect

        collect_dust('/test_dir', DEFAULT_THRESHOLD, False)

        output = mock_stdout.getvalue()
        error_output = mock_stderr.getvalue()

        self.assertIn("Warning: Could not access '/test_dir/unreadable.txt': Permission denied", error_output)
        self.assertIn("[DUST] /test_dir/readable.txt (50 bytes)", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('os.makedirs')
    @patch('os.rename')
    def test_os_error_on_quarantine(self, mock_rename, mock_makedirs, mock_getsize, mock_isfile, mock_walk, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Simulate an OSError during the rename operation for quarantine.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['problem_file.txt'])
        ]
        mock_isfile.return_value = True
        mock_getsize.return_value = 100
        mock_rename.side_effect = OSError("Disk full")

        collect_dust('/test_dir', DEFAULT_THRESHOLD, True)

        output = mock_stdout.getvalue()
        error_output = mock_stderr.getvalue()

        self.assertIn("Error quarantining '/test_dir/problem_file.txt': Disk full", error_output)
        self.assertNotIn("[QUARANTINED]", output) # Should not report successful quarantine

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    def test_quarantine_dir_exclusion(self, mock_getsize, mock_isfile, mock_walk, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Ensure that files within a .quarantine directory are not scanned.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', ['subdir', '.quarantine'], ['file_outside.txt']),
            ('/test_dir/subdir', [], ['file_in_subdir.txt']),
            ('/test_dir/.quarantine', [], ['quarantined_file.txt'])
        ]
        mock_isfile.side_effect = lambda x: x in [
            '/test_dir/file_outside.txt',
            '/test_dir/subdir/file_in_subdir.txt',
            '/test_dir/.quarantine/quarantined_file.txt'
        ]
        mock_getsize.return_value = 50 # All files are small

        collect_dust('/test_dir', DEFAULT_THRESHOLD, False)

        output = mock_stdout.getvalue()
        self.assertIn("[DUST] /test_dir/file_outside.txt (50 bytes)", output)
        self.assertIn("[DUST] /test_dir/subdir/file_in_subdir.txt (50 bytes)", output)
        self.assertNotIn("quarantined_file.txt", output) # Should not be reported
        self.assertEqual(mock_stderr.getvalue(), "")


if __name__ == '__main__':
    unittest.main()
