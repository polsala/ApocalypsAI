import unittest
import os
import time
import datetime
from unittest.mock import patch, MagicMock
from src.dust_collector import find_cosmic_dust, main

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        # Define a base time for consistent age calculations
        self.base_time = datetime.datetime(2023, 10, 26, 10, 0, 0)
        self.base_timestamp = self.base_time.timestamp()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    def test_find_cosmic_dust_empty_files(self, mock_isfile, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with an empty file.
        # os.path.isdir: Ensure the target path is seen as a directory.
        # os.walk: Provide a predefined directory and file structure.
        # os.path.getsize: Return 0 for the empty file, non-zero for others.
        # os.path.getmtime: Return a recent time for all files (age not relevant for empty check).
        # os.path.isfile: Ensure all mocked paths are considered files.

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['empty_file.txt', 'normal_file.txt'])
        ]
        mock_getsize.side_effect = lambda p: 0 if 'empty_file.txt' in p else 100
        mock_getmtime.return_value = self.base_timestamp # Recent modification time
        mock_isfile.return_value = True

        dust = find_cosmic_dust('/test_dir', min_age_days=30)
        self.assertEqual(len(dust), 1)
        self.assertEqual(dust[0], ('/test_dir/empty_file.txt', 'Empty file'))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    def test_find_cosmic_dust_old_files(self, mock_isfile, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with an old file.
        # os.path.isdir: Ensure the target path is seen as a directory.
        # os.walk: Provide a predefined directory and file structure.
        # os.path.getsize: Return non-zero for all files.
        # os.path.getmtime: Return an old time for one file, recent for another.
        # os.path.isfile: Ensure all mocked paths are considered files.

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['old_file.log', 'recent_file.txt'])
        ]
        mock_getsize.return_value = 100 # Non-empty
        
        # old_file.log: modified 60 days ago (older than 30-day threshold)
        old_timestamp = (self.base_time - datetime.timedelta(days=60)).timestamp()
        # recent_file.txt: modified 10 days ago (not old enough)
        recent_timestamp = (self.base_time - datetime.timedelta(days=10)).timestamp()

        def mock_getmtime_side_effect(path):
            if 'old_file.log' in path:
                return old_timestamp
            return recent_timestamp
        mock_getmtime.side_effect = mock_getmtime_side_effect
        mock_isfile.return_value = True

        dust = find_cosmic_dust('/test_dir', min_age_days=30)
        self.assertEqual(len(dust), 1)
        expected_reason = f"Older than 30 days (last modified: {(self.base_time - datetime.timedelta(days=60)).strftime('%Y-%m-%d')})"
        self.assertEqual(dust[0], ('/test_dir/old_file.log', expected_reason))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    def test_find_cosmic_dust_mixed_files(self, mock_isfile, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with empty, old, and normal files.
        # Verify that both criteria are correctly applied and distinct.

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['empty.txt', 'old.log', 'recent.txt', 'another_empty.tmp'])
        ]
        
        old_timestamp = (self.base_time - datetime.timedelta(days=45)).timestamp() # Older than 30 days
        recent_timestamp = (self.base_time - datetime.timedelta(days=5)).timestamp() # Not old enough

        def mock_getsize_side_effect(path):
            if 'empty.txt' in path or 'another_empty.tmp' in path:
                return 0
            return 100 # Non-empty
        mock_getsize.side_effect = mock_getsize_side_effect

        def mock_getmtime_side_effect(path):
            if 'old.log' in path:
                return old_timestamp
            return recent_timestamp
        mock_getmtime.side_effect = mock_getmtime_side_effect
        mock_isfile.return_value = True

        dust = find_cosmic_dust('/test_dir', min_age_days=30)
        self.assertEqual(len(dust), 3) # empty.txt, old.log, another_empty.tmp

        # Sort for consistent assertion order
        dust.sort(key=lambda x: x[0])

        expected_reason_old = f"Older than 30 days (last modified: {(self.base_time - datetime.timedelta(days=45)).strftime('%Y-%m-%d')})"
        self.assertEqual(dust[0], ('/test_dir/another_empty.tmp', 'Empty file'))
        self.assertEqual(dust[1], ('/test_dir/empty.txt', 'Empty file'))
        self.assertEqual(dust[2], ('/test_dir/old.log', expected_reason_old))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    def test_find_cosmic_dust_no_dust(self, mock_isfile, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with only recent, non-empty files.
        # Verify that no dust is identified.

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log'])
        ]
        mock_getsize.return_value = 500 # Non-empty
        mock_getmtime.return_value = (self.base_time - datetime.timedelta(days=5)).timestamp() # Recent
        mock_isfile.return_value = True

        dust = find_cosmic_dust('/test_dir', min_age_days=30)
        self.assertEqual(len(dust), 0)

    @patch('os.path.isdir')
    def test_find_cosmic_dust_invalid_path(self, mock_isdir):
        # Mock rationale: Simulate an invalid target path.
        # os.path.isdir: Return False for the target path.

        mock_isdir.return_value = False
        dust = find_cosmic_dust('/non_existent_dir')
        self.assertEqual(len(dust), 0)

    @patch('src.dust_collector.find_cosmic_dust', return_value=[
        ('/test_dir/empty.txt', 'Empty file'),
        ('/test_dir/old.log', 'Older than 30 days')
    ])
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_list_action(self, mock_parse_args, mock_print, mock_find_dust):
        # Mock rationale: Test the main function's 'list' action.
        # find_cosmic_dust: Mock its return value to control test data.
        # builtins.print: Capture print output to verify messages.
        # argparse.ArgumentParser.parse_args: Simulate command-line arguments.

        mock_parse_args.return_value = MagicMock(
            path='/test_dir',
            age=30,
            action='list',
            dry_run=False
        )
        main()
        mock_print.assert_any_call("--- Identified Cosmic Dust (2 files) ---")
        mock_print.assert_any_call("- /test_dir/empty.txt (Empty file)")
        mock_print.assert_any_call("- /test_dir/old.log (Older than 30 days)")
        mock_print.assert_any_call("\n--- Listing Complete ---")

    @patch('src.dust_collector.find_cosmic_dust', return_value=[
        ('/test_dir/empty.txt', 'Empty file'),
        ('/test_dir/old.log', 'Older than 30 days')
    ])
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.remove')
    def test_main_delete_action_dry_run(self, mock_remove, mock_parse_args, mock_print, mock_find_dust):
        # Mock rationale: Test the main function's 'delete' action with dry-run.
        # os.remove: Ensure it's NOT called during a dry run.

        mock_parse_args.return_value = MagicMock(
            path='/test_dir',
            age=30,
            action='delete',
            dry_run=True
        )
        main()
        mock_print.assert_any_call("\n--- DRY RUN: Files listed above WOULD BE DELETED ---")
        mock_remove.assert_not_called()

    @patch('src.dust_collector.find_cosmic_dust', return_value=[
        ('/test_dir/empty.txt', 'Empty file'),
        ('/test_dir/old.log', 'Older than 30 days')
    ])
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.remove')
    def test_main_delete_action_actual_delete(self, mock_remove, mock_parse_args, mock_print, mock_find_dust):
        # Mock rationale: Test the main function's 'delete' action.
        # os.remove: Ensure it IS called for each identified file.

        mock_parse_args.return_value = MagicMock(
            path='/test_dir',
            age=30,
            action='delete',
            dry_run=False
        )
        main()
        mock_print.assert_any_call("\n--- Deleting Cosmic Dust ---")
        mock_remove.assert_any_call('/test_dir/empty.txt')
        mock_remove.assert_any_call('/test_dir/old.log')
        mock_print.assert_any_call("🗑️ Deleted: /test_dir/empty.txt")
        mock_print.assert_any_call("🗑️ Deleted: /test_dir/old.log")
        mock_print.assert_any_call("\nDeletion process complete.")
        self.assertEqual(mock_remove.call_count, 2)

    @patch('src.dust_collector.find_cosmic_dust', return_value=[])
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_dust_found(self, mock_parse_args, mock_print, mock_find_dust):
        # Mock rationale: Test the scenario where no dust is found.
        # find_cosmic_dust: Return an empty list.

        mock_parse_args.return_value = MagicMock(
            path='/test_dir',
            age=30,
            action='list',
            dry_run=False
        )
        main()
        # Check for specific messages, as other prints (like scanning message) will also occur.
        self.assertIn("🌌 Scanning '/test_dir' for cosmic dust (min age: 30 days)...", [call.args[0] for call in mock_print.call_args_list])
        self.assertIn("✨ No cosmic dust found. Your repository is sparkling clean!", [call.args[0] for call in mock_print.call_args_list])
        self.assertNotIn("--- Identified Cosmic Dust", [call.args[0] for call in mock_print.call_args_list])


    @patch('src.dust_collector.find_cosmic_dust', return_value=[
        ('/test_dir/unremovable.txt', 'Empty file')
    ])
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.remove', side_effect=OSError("Permission denied"))
    def test_main_delete_action_error(self, mock_remove, mock_parse_args, mock_print, mock_find_dust):
        # Mock rationale: Test error handling during deletion.
        # os.remove: Simulate an OSError (e.g., permission denied).

        mock_parse_args.return_value = MagicMock(
            path='/test_dir',
            age=30,
            action='delete',
            dry_run=False
        )
        main()
        mock_print.assert_any_call("❌ Error deleting '/test_dir/unremovable.txt': Permission denied")
        mock_remove.assert_called_once_with('/test_dir/unremovable.txt')
