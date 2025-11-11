import unittest
import os
import datetime
from unittest.mock import patch, MagicMock
from src.collector import CosmicDustBunnyCollector

class TestCosmicDustBunnyCollector(unittest.TestCase):

    def setUp(self):
        # Mock current datetime for consistent age calculations
        self.mock_now = datetime.datetime(2023, 10, 26, 10, 0, 0)
        self.patcher_datetime_now = patch('datetime.datetime')
        self.mock_datetime = self.patcher_datetime_now.start()
        self.mock_datetime.now.return_value = self.mock_now
        self.mock_datetime.fromtimestamp = datetime.datetime.fromtimestamp # Keep original for conversion
        self.mock_datetime.timedelta = datetime.timedelta # Keep original for timedelta

        # Mock os.path.isdir to always return True for our target_dir
        self.patcher_isdir = patch('os.path.isdir', return_value=True)
        self.mock_isdir = self.patcher_isdir.start()

        # Mock os.makedirs to prevent actual directory creation
        self.patcher_makedirs = patch('os.makedirs')
        self.mock_makedirs = self.patcher_makedirs.start()

        # Mock os.path.exists for quarantine directory checks
        self.patcher_exists = patch('os.path.exists', return_value=False) # Default to not existing
        self.mock_exists = self.patcher_exists.start()


    def tearDown(self):
        self.patcher_datetime_now.stop()
        self.patcher_isdir.stop()
        self.patcher_makedirs.stop()
        self.patcher_exists.stop()

    def test_init_invalid_directory(self):
        # Mock rationale: Ensure that the collector correctly validates the target directory.
        # We temporarily set os.path.isdir to False for this specific test.
        with patch('os.path.isdir', return_value=False):
            with self.assertRaisesRegex(ValueError, "Target directory 'nonexistent' does not exist."):
                CosmicDustBunnyCollector("nonexistent", 90)

    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_non_recursive(self, mock_getmtime, mock_isfile, mock_listdir):
        # Mock rationale: Simulate a directory structure and file modification times
        # without touching the actual filesystem. This allows deterministic testing
        # of the file identification logic.
        mock_listdir.return_value = ['old_file.txt', 'new_file.txt', 'folder']
        mock_isfile.side_effect = lambda x: x in ['/test_dir/old_file.txt', '/test_dir/new_file.txt']

        # old_file.txt: modified 100 days ago (older than 90 days threshold)
        old_timestamp = (self.mock_now - datetime.timedelta(days=100)).timestamp()
        # new_file.txt: modified 50 days ago (newer than 90 days threshold)
        new_timestamp = (self.mock_now - datetime.timedelta(days=50)).timestamp()

        def getmtime_side_effect(path):
            if path == '/test_dir/old_file.txt':
                return old_timestamp
            elif path == '/test_dir/new_file.txt':
                return new_timestamp
            return 0 # Should not be called for other paths

        mock_getmtime.side_effect = getmtime_side_effect

        collector = CosmicDustBunnyCollector("/test_dir", 90, dry_run=True)
        bunnies = collector.find_dust_bunnies()
        self.assertEqual(len(bunnies), 1)
        self.assertIn('/test_dir/old_file.txt', bunnies)
        self.assertNotIn('/test_dir/new_file.txt', bunnies)
        self.assertNotIn('/test_dir/folder', bunnies)

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_recursive(self, mock_getmtime, mock_walk):
        # Mock rationale: Simulate a recursive directory structure and file modification times
        # without touching the actual filesystem. This allows deterministic testing
        # of the recursive file identification logic.
        
        # Structure:
        # /test_dir/
        #   old_file_root.txt (100 days old)
        #   subdir1/
        #     old_file_subdir1.txt (120 days old)
        #     new_file_subdir1.txt (30 days old)
        #   subdir2/
        #     another_old_file.txt (95 days old)

        old_timestamp_root = (self.mock_now - datetime.timedelta(days=100)).timestamp()
        old_timestamp_subdir1 = (self.mock_now - datetime.timedelta(days=120)).timestamp()
        new_timestamp_subdir1 = (self.mock_now - datetime.timedelta(days=30)).timestamp()
        old_timestamp_subdir2 = (self.mock_now - datetime.timedelta(days=95)).timestamp()

        mock_walk.return_value = [
            ('/test_dir', ['subdir1', 'subdir2'], ['old_file_root.txt']),
            ('/test_dir/subdir1', [], ['old_file_subdir1.txt', 'new_file_subdir1.txt']),
            ('/test_dir/subdir2', [], ['another_old_file.txt'])
        ]

        def getmtime_side_effect(path):
            if path == '/test_dir/old_file_root.txt': return old_timestamp_root
            if path == '/test_dir/subdir1/old_file_subdir1.txt': return old_timestamp_subdir1
            if path == '/test_dir/subdir1/new_file_subdir1.txt': return new_timestamp_subdir1
            if path == '/test_dir/subdir2/another_old_file.txt': return old_timestamp_subdir2
            return 0

        mock_getmtime.side_effect = getmtime_side_effect

        collector = CosmicDustBunnyCollector("/test_dir", 90, dry_run=True, recursive=True)
        bunnies = collector.find_dust_bunnies()
        self.assertEqual(len(bunnies), 3)
        self.assertIn('/test_dir/old_file_root.txt', bunnies)
        self.assertIn('/test_dir/subdir1/old_file_subdir1.txt', bunnies)
        self.assertIn('/test_dir/subdir2/another_old_file.txt', bunnies)
        self.assertNotIn('/test_dir/subdir1/new_file_subdir1.txt', bunnies)

    @patch('os.listdir', return_value=['old_file.txt'])
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print') # Mock print to capture output
    def test_collect_dust_bunnies_delete(self, mock_print, mock_remove, mock_getmtime, mock_isfile, mock_listdir):
        # Mock rationale: Test the deletion logic without actually deleting files.
        # We simulate a single old file and verify that os.remove is called correctly.
        old_timestamp = (self.mock_now - datetime.timedelta(days=100)).timestamp()
        mock_getmtime.return_value = old_timestamp

        collector = CosmicDustBunnyCollector("/test_dir", 90, dry_run=False)
        processed = collector.collect_dust_bunnies()

        mock_remove.assert_called_once_with('/test_dir/old_file.txt')
        self.assertEqual(len(processed), 1)
        self.assertIn('/test_dir/old_file.txt', processed)
        # Check print output for confirmation
        self.assertIn("Removed '/test_dir/old_file.txt'", [call.args[0] for call in mock_print.call_args_list])

    @patch('os.listdir', return_value=['old_file.txt'])
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getmtime')
    @patch('shutil.move')
    @patch('builtins.print')
    def test_collect_dust_bunnies_quarantine(self, mock_print, mock_move, mock_getmtime, mock_isfile, mock_listdir):
        # Mock rationale: Test the quarantine logic without actually moving files.
        # We simulate a single old file and verify that shutil.move is called correctly.
        old_timestamp = (self.mock_now - datetime.timedelta(days=100)).timestamp()
        mock_getmtime.return_value = old_timestamp
        self.mock_exists.side_effect = lambda x: x == '/quarantine_dir' # Quarantine dir exists after creation

        collector = CosmicDustBunnyCollector("/test_dir", 90, dry_run=False, quarantine_dir="/quarantine_dir")
        processed = collector.collect_dust_bunnies()

        self.mock_makedirs.assert_called_once_with('/quarantine_dir')
        mock_move.assert_called_once_with('/test_dir/old_file.txt', '/quarantine_dir/old_file.txt')
        self.assertEqual(len(processed), 1)
        self.assertIn('/test_dir/old_file.txt', processed)
        self.assertIn("Moved '/test_dir/old_file.txt' to quarantine: '/quarantine_dir/old_file.txt'", [call.args[0] for call in mock_print.call_args_list])

    @patch('os.listdir', return_value=['old_file.txt'])
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getmtime')
    @patch('shutil.move')
    @patch('builtins.print')
    def test_collect_dust_bunnies_quarantine_collision(self, mock_print, mock_move, mock_getmtime, mock_isfile, mock_listdir):
        # Mock rationale: Test the quarantine logic's ability to handle name collisions
        # by appending a counter, without actual file system operations.
        old_timestamp = (self.mock_now - datetime.timedelta(days=100)).timestamp()
        mock_getmtime.return_value = old_timestamp
        
        # Simulate that '/quarantine_dir/old_file.txt' already exists
        self.mock_exists.side_effect = lambda x: x in ['/quarantine_dir', '/quarantine_dir/old_file.txt']

        collector = CosmicDustBunnyCollector("/test_dir", 90, dry_run=False, quarantine_dir="/quarantine_dir")
        processed = collector.collect_dust_bunnies()

        mock_move.assert_called_once_with('/test_dir/old_file.txt', '/quarantine_dir/old_file_1.txt')
        self.assertEqual(len(processed), 1)
        self.assertIn('/test_dir/old_file.txt', processed)
        self.assertIn("Moved '/test_dir/old_file.txt' to quarantine: '/quarantine_dir/old_file_1.txt'", [call.args[0] for call in mock_print.call_args_list])

    @patch('os.listdir', return_value=['old_file.txt'])
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getmtime')
    @patch('os.remove', side_effect=OSError("Permission denied"))
    @patch('builtins.print')
    def test_collect_dust_bunnies_error_handling(self, mock_print, mock_remove, mock_getmtime, mock_isfile, mock_listdir):
        # Mock rationale: Verify that the collector gracefully handles errors during file operations
        # (e.g., permission denied) and prints an informative message, without crashing.
        old_timestamp = (self.mock_now - datetime.timedelta(days=100)).timestamp()
        mock_getmtime.return_value = old_timestamp

        collector = CosmicDustBunnyCollector("/test_dir", 90, dry_run=False)
        processed = collector.collect_dust_bunnies()

        mock_remove.assert_called_once_with('/test_dir/old_file.txt')
        self.assertEqual(len(processed), 0) # No files processed due to error
        self.assertIn("Error processing '/test_dir/old_file.txt': Permission denied", [call.args[0] for call in mock_print.call_args_list])

    @patch('os.listdir', return_value=[])
    @patch('builtins.print')
    def test_no_dust_bunnies_found(self, mock_print, mock_listdir):
        # Mock rationale: Ensure the collector behaves correctly when no old files are found.
        collector = CosmicDustBunnyCollector("/test_dir", 90, dry_run=True)
        bunnies = collector.collect_dust_bunnies()
        self.assertEqual(len(bunnies), 0)
        self.assertIn("No cosmic dust bunnies found. Your digital space is pristine... for now.", [call.args[0] for call in mock_print.call_args_list])

    @patch('os.listdir', return_value=['old_file.txt'])
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    def test_dry_run_no_operations(self, mock_print, mock_remove, mock_getmtime, mock_isfile, mock_listdir):
        # Mock rationale: Verify that in dry-run mode, no actual file operations (like removal) occur.
        old_timestamp = (self.mock_now - datetime.timedelta(days=100)).timestamp()
        mock_getmtime.return_value = old_timestamp

        collector = CosmicDustBunnyCollector("/test_dir", 90, dry_run=True)
        processed = collector.collect_dust_bunnies()

        mock_remove.assert_not_called()
        self.assertEqual(len(processed), 1)
        self.assertIn('/test_dir/old_file.txt', processed)
        self.assertIn("(Dry run: No files will be moved or deleted.)", [call.args[0] for call in mock_print.call_args_list])
