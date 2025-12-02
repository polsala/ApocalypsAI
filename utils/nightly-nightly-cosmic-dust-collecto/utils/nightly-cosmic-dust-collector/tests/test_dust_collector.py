import unittest
from unittest.mock import patch, MagicMock, call
import os
import shutil
from src.dust_collector import collect_dust

class TestCosmicDustCollector(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('shutil.move')
    def test_no_dust_found(self, mock_shutil_move, mock_os_makedirs, mock_os_isfile, mock_os_getsize, mock_os_walk, mock_os_isdir):
        # Mock rationale: Simulate a directory with files, none of which are 'dust' based on size threshold.
        mock_os_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/test_repo', [], ['file_large.txt', 'another_large.log'])
        ]
        mock_os_isfile.side_effect = lambda p: p in ['/test_repo/file_large.txt', '/test_repo/another_large.log']
        mock_os_getsize.side_effect = lambda p: {
            '/test_repo/file_large.txt': 2000,
            '/test_repo/another_large.log': 1500
        }.get(p, 0)

        dust_files = collect_dust('/test_repo', max_size_bytes=1000)

        self.assertEqual(len(dust_files), 0)
        mock_shutil_move.assert_not_called()
        mock_os_makedirs.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('shutil.move')
    def test_dust_found_no_quarantine(self, mock_shutil_move, mock_os_makedirs, mock_os_isfile, mock_os_getsize, mock_os_walk, mock_os_isdir):
        # Mock rationale: Simulate a directory with some 'dust' files, but no quarantine directory is specified.
        # Files should be reported but not moved.
        mock_os_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/test_repo', ['sub_dir'], ['small.txt', 'empty.log', 'large.bin']),
            ('/test_repo/sub_dir', [], ['tiny.cfg'])
        ]
        mock_os_isfile.side_effect = lambda p: p in [
            '/test_repo/small.txt',
            '/test_repo/empty.log',
            '/test_repo/large.bin',
            '/test_repo/sub_dir/tiny.cfg'
        ]
        mock_os_getsize.side_effect = lambda p: {
            '/test_repo/small.txt': 500,
            '/test_repo/empty.log': 0,
            '/test_repo/large.bin': 2000,
            '/test_repo/sub_dir/tiny.cfg': 100
        }.get(p, 0)

        dust_files = collect_dust('/test_repo', max_size_bytes=1000)

        self.assertEqual(len(dust_files), 3)
        self.assertIn(('/test_repo/small.txt', 500), dust_files)
        self.assertIn(('/test_repo/empty.log', 0), dust_files)
        self.assertIn(('/test_repo/sub_dir/tiny.cfg', 100), dust_files)
        mock_shutil_move.assert_not_called()
        mock_os_makedirs.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('shutil.move')
    def test_dust_found_with_quarantine(self, mock_shutil_move, mock_os_makedirs, mock_os_isfile, mock_os_getsize, mock_os_walk, mock_os_isdir):
        # Mock rationale: Simulate a directory with 'dust' files and verify they are moved to the quarantine directory,
        # preserving their relative path structure.
        mock_os_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/test_repo', ['sub_dir'], ['small.txt', 'empty.log']),
            ('/test_repo/sub_dir', [], ['tiny.cfg'])
        ]
        mock_os_isfile.side_effect = lambda p: p in [
            '/test_repo/small.txt',
            '/test_repo/empty.log',
            '/test_repo/sub_dir/tiny.cfg'
        ]
        mock_os_getsize.side_effect = lambda p: {
            '/test_repo/small.txt': 500,
            '/test_repo/empty.log': 0,
            '/test_repo/sub_dir/tiny.cfg': 100
        }.get(p, 0)

        quarantine_path = '/quarantine_zone'
        dust_files = collect_dust('/test_repo', max_size_bytes=1000, quarantine_dir=quarantine_path)

        self.assertEqual(len(dust_files), 3)
        self.assertIn(('/test_repo/small.txt', 500), dust_files)
        self.assertIn(('/test_repo/empty.log', 0), dust_files)
        self.assertIn(('/test_repo/sub_dir/tiny.cfg', 100), dust_files)

        mock_os_makedirs.assert_has_calls([
            call(quarantine_path, exist_ok=True),
            call(os.path.join(quarantine_path, 'sub_dir'), exist_ok=True) # For tiny.cfg
        ], any_order=True)

        mock_shutil_move.assert_has_calls([
            call('/test_repo/small.txt', os.path.join(quarantine_path, 'small.txt')),
            call('/test_repo/empty.log', os.path.join(quarantine_path, 'empty.log')),
            call('/test_repo/sub_dir/tiny.cfg', os.path.join(quarantine_path, 'sub_dir', 'tiny.cfg'))
        ], any_order=True)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('shutil.move')
    def test_target_dir_not_found(self, mock_shutil_move, mock_os_makedirs, mock_os_isfile, mock_os_getsize, mock_os_walk, mock_os_isdir):
        # Mock rationale: Test the error handling when the target directory does not exist.
        mock_os_isdir.return_value = False

        with patch('builtins.print') as mock_print:
            dust_files = collect_dust('/non_existent_repo')
            self.assertEqual(len(dust_files), 0)
            mock_print.assert_called_with("Error: Target directory '/non_existent_repo' does not exist or is not a directory.")
        mock_os_walk.assert_not_called()
        mock_shutil_move.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('shutil.move')
    def test_os_error_during_file_processing(self, mock_shutil_move, mock_os_makedirs, mock_os_isfile, mock_os_getsize, mock_os_walk, mock_os_isdir):
        # Mock rationale: Simulate an OSError during file processing (e.g., permission denied when getting size).
        # The utility should log a warning and continue processing other files.
        mock_os_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/test_repo', [], ['problem_file.txt', 'good_file.txt'])
        ]
        mock_os_isfile.side_effect = lambda p: p in ['/test_repo/problem_file.txt', '/test_repo/good_file.txt']
        
        # Simulate OSError for 'problem_file.txt' when getting size
        def getsize_side_effect(path):
            if path == '/test_repo/problem_file.txt':
                raise OSError("Permission denied")
            return 100 # For good_file.txt

        mock_os_getsize.side_effect = getsize_side_effect

        with patch('builtins.print') as mock_print:
            dust_files = collect_dust('/test_repo', max_size_bytes=1000)
            self.assertEqual(len(dust_files), 1) # Only good_file.txt should be collected
            self.assertIn(('/test_repo/good_file.txt', 100), dust_files)
            mock_print.assert_called_with("Warning: Could not process file '/test_repo/problem_file.txt': Permission denied")
        mock_shutil_move.assert_not_called() # No quarantine in this test

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('shutil.move')
    def test_quarantine_dir_creation(self, mock_shutil_move, mock_os_makedirs, mock_os_isfile, mock_os_getsize, mock_os_walk, mock_os_isdir):
        # Mock rationale: Ensure the top-level quarantine directory is created if it doesn't exist.
        mock_os_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/test_repo', [], ['small.txt'])
        ]
        mock_os_isfile.return_value = True
        mock_os_getsize.return_value = 100

        quarantine_path = '/new_quarantine'
        collect_dust('/test_repo', max_size_bytes=1000, quarantine_dir=quarantine_path)

        mock_os_makedirs.assert_called_with(quarantine_path, exist_ok=True)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('shutil.move')
    def test_quarantine_subdirectories_created(self, mock_shutil_move, mock_os_makedirs, mock_os_isfile, mock_os_getsize, mock_os_walk, mock_os_isdir):
        # Mock rationale: Ensure subdirectories within the quarantine are created to preserve the original file structure.
        mock_os_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/test_repo', ['sub'], []),
            ('/test_repo/sub', [], ['nested_small.txt'])
        ]
        mock_os_isfile.side_effect = lambda p: p == '/test_repo/sub/nested_small.txt'
        mock_os_getsize.return_value = 50

        quarantine_path = '/q_zone'
        collect_dust('/test_repo', max_size_bytes=100, quarantine_dir=quarantine_path)

        mock_os_makedirs.assert_has_calls([
            call(quarantine_path, exist_ok=True),
            call(os.path.join(quarantine_path, 'sub'), exist_ok=True)
        ], any_order=True)
        mock_shutil_move.assert_called_once_with(
            '/test_repo/sub/nested_small.txt',
            os.path.join(quarantine_path, 'sub', 'nested_small.txt')
        )

if __name__ == '__main__':
    unittest.main()
