import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
from io import StringIO

# Import the function to be tested
from src.dust_collector import collect_dust

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        self.mock_stdout = StringIO()
        sys.stdout = self.mock_stdout

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.exists')
    def test_list_mode_no_dust(self, mock_exists, mock_move, mock_makedirs, mock_getsize, mock_walk):
        # Mock rationale: Simulate an empty directory structure and file sizes.
        # Mock rationale: Ensure no files are moved or directories created in list mode.
        mock_walk.return_value = [
            ('root', [], ['file1.txt', 'large.log'])
        ]
        mock_getsize.side_effect = lambda p: {
            'root/file1.txt': 2000, # Larger than default 1024
            'root/large.log': 5000
        }.get(p, 0)
        mock_exists.return_value = True # Assume root path exists

        result = collect_dust(
            scan_path='root',
            max_size_bytes=1024,
            allowed_extensions=[],
            mode='list',
            quarantine_dir='quarantine_dust',
            output_stream=self.mock_stdout
        )

        self.assertEqual(result, [])
        self.assertIn("No cosmic dust found! Your repository is sparkling clean.", self.mock_stdout.getvalue())
        mock_move.assert_not_called()
        mock_makedirs.assert_not_called()

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.exists')
    def test_list_mode_with_dust_by_size(self, mock_exists, mock_move, mock_makedirs, mock_getsize, mock_walk):
        # Mock rationale: Simulate files with varying sizes, some below the threshold.
        # Mock rationale: Verify that only small files are listed and no actions are taken.
        mock_walk.return_value = [
            ('root', ['subdir'], ['small.txt', 'large.txt']),
            ('root/subdir', [], ['tiny.log', 'medium.json'])
        ]
        mock_getsize.side_effect = lambda p: {
            'root/small.txt': 500,
            'root/large.txt': 2000,
            'root/subdir/tiny.log': 100,
            'root/subdir/medium.json': 1500
        }.get(p, 0)
        mock_exists.return_value = True

        result = collect_dust(
            scan_path='root',
            max_size_bytes=1024,
            allowed_extensions=[],
            mode='list',
            quarantine_dir='quarantine_dust',
            output_stream=self.mock_stdout
        )

        self.assertEqual(set(result), {'root/small.txt', 'root/subdir/tiny.log'})
        output = self.mock_stdout.getvalue()
        self.assertIn("[DUST] root/small.txt (500 bytes)", output)
        self.assertIn("[DUST] root/subdir/tiny.log (100 bytes)", output)
        self.assertNotIn("large.txt", output)
        self.assertNotIn("medium.json", output)
        mock_move.assert_not_called()
        mock_makedirs.assert_not_called()

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.exists')
    def test_list_mode_with_dust_by_extension(self, mock_exists, mock_move, mock_makedirs, mock_getsize, mock_walk):
        # Mock rationale: Simulate files with specific extensions and sizes.
        # Mock rationale: Verify that only files matching both size and extension are listed.
        mock_walk.return_value = [
            ('root', [], ['file.log', 'file.tmp', 'file.txt', 'another.log'])
        ]
        mock_getsize.side_effect = lambda p: {
            'root/file.log': 100,
            'root/file.tmp': 200,
            'root/file.txt': 50,
            'root/another.log': 1500 # Too large
        }.get(p, 0)
        mock_exists.return_value = True

        result = collect_dust(
            scan_path='root',
            max_size_bytes=1024,
            allowed_extensions=['.log', '.tmp'],
            mode='list',
            quarantine_dir='quarantine_dust',
            output_stream=self.mock_stdout
        )

        self.assertEqual(set(result), {'root/file.log', 'root/file.tmp'})
        output = self.mock_stdout.getvalue()
        self.assertIn("[DUST] root/file.log (100 bytes)", output)
        self.assertIn("[DUST] root/file.tmp (200 bytes)", output)
        self.assertNotIn("file.txt", output)
        self.assertNotIn("another.log", output)
        mock_move.assert_not_called()
        mock_makedirs.assert_not_called()

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.exists')
    def test_quarantine_mode(self, mock_exists, mock_move, mock_makedirs, mock_getsize, mock_walk):
        # Mock rationale: Simulate a directory with dust files.
        # Mock rationale: Verify that files are moved to the correct quarantine path and directories are created.
        mock_walk.return_value = [
            ('root', ['subdir'], ['small.txt', 'large.txt']),
            ('root/subdir', [], ['tiny.log'])
        ]
        mock_getsize.side_effect = lambda p: {
            'root/small.txt': 500,
            'root/large.txt': 2000,
            'root/subdir/tiny.log': 100
        }.get(p, 0)
        mock_exists.side_effect = lambda p: p != 'quarantine_dust' # quarantine_dust does not exist initially

        result = collect_dust(
            scan_path='root',
            max_size_bytes=1024,
            allowed_extensions=[],
            mode='quarantine',
            quarantine_dir='quarantine_dust',
            output_stream=self.mock_stdout
        )

        self.assertEqual(set(result), {'root/small.txt', 'root/subdir/tiny.log'})
        output = self.mock_stdout.getvalue()
        self.assertIn("Created quarantine directory: quarantine_dust", output)
        self.assertIn("[QUARANTINED] root/small.txt -> quarantine_dust/small.txt", output)
        self.assertIn("[QUARANTINED] root/subdir/tiny.log -> quarantine_dust/subdir/tiny.log", output)

        mock_makedirs.assert_any_call('quarantine_dust', exist_ok=True)
        mock_makedirs.assert_any_call('quarantine_dust/subdir', exist_ok=True)
        mock_move.assert_any_call('root/small.txt', 'quarantine_dust/small.txt')
        mock_move.assert_any_call('root/subdir/tiny.log', 'quarantine_dust/subdir/tiny.log')
        self.assertEqual(mock_move.call_count, 2)

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.exists')
    def test_quarantine_mode_existing_dir(self, mock_exists, mock_move, mock_makedirs, mock_getsize, mock_walk):
        # Mock rationale: Simulate a directory with dust files and an existing quarantine directory.
        # Mock rationale: Verify that files are moved and no new quarantine directory is created.
        mock_walk.return_value = [
            ('root', [], ['small.txt'])
        ]
        mock_getsize.side_effect = lambda p: {
            'root/small.txt': 500
        }.get(p, 0)
        mock_exists.return_value = True # quarantine_dust already exists

        result = collect_dust(
            scan_path='root',
            max_size_bytes=1024,
            allowed_extensions=[],
            mode='quarantine',
            quarantine_dir='quarantine_dust',
            output_stream=self.mock_stdout
        )

        self.assertEqual(set(result), {'root/small.txt'})
        output = self.mock_stdout.getvalue()
        self.assertNotIn("Created quarantine directory", output)
        self.assertIn("[QUARANTINED] root/small.txt -> quarantine_dust/small.txt", output)
        mock_makedirs.assert_called_once_with('quarantine_dust', exist_ok=True) # Still called, but exist_ok=True prevents error
        mock_move.assert_called_once_with('root/small.txt', 'quarantine_dust/small.txt')

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.exists')
    def test_file_not_found_during_scan(self, mock_exists, mock_move, mock_makedirs, mock_getsize, mock_walk):
        # Mock rationale: Simulate a scenario where a file disappears between os.walk and os.path.getsize.
        # Mock rationale: Verify that the utility handles FileNotFoundError gracefully and logs a warning.
        mock_walk.return_value = [
            ('root', [], ['existing.txt', 'missing.txt'])
        ]
        mock_getsize.side_effect = lambda p: {
            'root/existing.txt': 100
        }.get(p, FileNotFoundError)
        mock_exists.return_value = True

        result = collect_dust(
            scan_path='root',
            max_size_bytes=1024,
            allowed_extensions=[],
            mode='list',
            quarantine_dir='quarantine_dust',
            output_stream=self.mock_stdout
        )

        self.assertEqual(set(result), {'root/existing.txt'})
        output = self.mock_stdout.getvalue()
        self.assertIn("[DUST] root/existing.txt (100 bytes)", output)
        self.assertIn("Warning: File not found during scan: root/missing.txt", output)
        mock_move.assert_not_called()
        mock_makedirs.assert_not_called()

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.exists')
    def test_quarantine_mode_with_subdirectories(self, mock_exists, mock_move, mock_makedirs, mock_getsize, mock_walk):
        # Mock rationale: Simulate a complex directory structure with dust files in subdirectories.
        # Mock rationale: Verify that the quarantine process preserves the relative path structure.
        mock_walk.return_value = [
            ('root', ['dir1', 'dir2'], ['file_root.tmp']),
            ('root/dir1', [], ['file_dir1.log']),
            ('root/dir2', ['sub_dir2'], ['file_dir2.txt']),
            ('root/dir2/sub_dir2', [], ['file_sub_dir2.bak'])
        ]
        mock_getsize.side_effect = lambda p: {
            'root/file_root.tmp': 50,
            'root/dir1/file_dir1.log': 150,
            'root/dir2/file_dir2.txt': 250,
            'root/dir2/sub_dir2/file_sub_dir2.bak': 350
        }.get(p, 0)
        mock_exists.side_effect = lambda p: p != 'quarantine_dust' # quarantine_dust does not exist initially

        result = collect_dust(
            scan_path='root',
            max_size_bytes=1024,
            allowed_extensions=['.tmp', '.log', '.txt', '.bak'],
            mode='quarantine',
            quarantine_dir='quarantine_dust',
            output_stream=self.mock_stdout
        )

        expected_files = {
            'root/file_root.tmp',
            'root/dir1/file_dir1.log',
            'root/dir2/file_dir2.txt',
            'root/dir2/sub_dir2/file_sub_dir2.bak'
        }
        self.assertEqual(set(result), expected_files)

        mock_makedirs.assert_any_call('quarantine_dust', exist_ok=True)
        mock_makedirs.assert_any_call('quarantine_dust/dir1', exist_ok=True)
        mock_makedirs.assert_any_call('quarantine_dust/dir2', exist_ok=True)
        mock_makedirs.assert_any_call('quarantine_dust/dir2/sub_dir2', exist_ok=True)

        mock_move.assert_any_call('root/file_root.tmp', 'quarantine_dust/file_root.tmp')
        mock_move.assert_any_call('root/dir1/file_dir1.log', 'quarantine_dust/dir1/file_dir1.log')
        mock_move.assert_any_call('root/dir2/file_dir2.txt', 'quarantine_dust/dir2/file_dir2.txt')
        mock_move.assert_any_call('root/dir2/sub_dir2/file_sub_dir2.bak', 'quarantine_dust/dir2/sub_dir2/file_sub_dir2.bak')
        self.assertEqual(mock_move.call_count, 4)
