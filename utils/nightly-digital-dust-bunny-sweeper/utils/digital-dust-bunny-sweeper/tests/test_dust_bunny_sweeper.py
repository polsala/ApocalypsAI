import unittest
from unittest.mock import patch, MagicMock
import datetime
import os
import sys

# Adjust sys.path to allow importing the module from 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import dust_bunny_sweeper
sys.path.pop(0) # Clean up sys.path after import

class TestDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Define a fixed current time for deterministic testing
        self.mock_now = datetime.datetime(2023, 10, 27, 10, 0, 0)

    @patch('dust_bunny_sweeper.os.walk')
    @patch('dust_bunny_sweeper.os.path.getmtime')
    @patch('dust_bunny_sweeper.os.path.isdir', return_value=True)
    @patch('dust_bunny_sweeper.get_current_time') # Mock the time function in the utility
    def test_find_dust_bunnies_empty_dirs(self, mock_get_current_time, mock_isdir, mock_getmtime, mock_walk):
        """Test finding only empty directories."""
        mock_get_current_time.return_value = self.mock_now
        mock_getmtime.return_value = (self.mock_now - datetime.timedelta(days=10)).timestamp() # Files are recent

        # Mock os.walk to simulate a directory structure with empty dirs
        mock_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['file.txt']),
            ('/root/dir1', [], []), # Empty dir
            ('/root/dir2', ['subdir'], []),
            ('/root/dir2/subdir', [], []), # Empty dir
        ]

        empty_dirs, old_files = dust_bunny_sweeper.find_dust_bunnies(
            root_path='/root', age_days=30, patterns=[], dry_run=True
        )

        self.assertIn('/root/dir1', empty_dirs)
        self.assertIn('/root/dir2/subdir', empty_dirs)
        self.assertEqual(len(empty_dirs), 2)
        self.assertEqual(len(old_files), 0)

    @patch('dust_bunny_sweeper.os.walk')
    @patch('dust_bunny_sweeper.os.path.getmtime')
    @patch('dust_bunny_sweeper.os.path.isdir', return_value=True)
    @patch('dust_bunny_sweeper.get_current_time')
    def test_find_dust_bunnies_old_files(self, mock_get_current_time, mock_isdir, mock_getmtime, mock_walk):
        """Test finding only old files matching patterns."""
        mock_get_current_time.return_value = self.mock_now

        # Mock modification times: one old, one recent, one old but wrong pattern
        def getmtime_side_effect(path):
            if 'old_log.log' in path:
                return (self.mock_now - datetime.timedelta(days=40)).timestamp() # Older than 30 days
            elif 'recent_log.log' in path:
                return (self.mock_now - datetime.timedelta(days=10)).timestamp() # Newer than 30 days
            elif 'old_txt.txt' in path:
                return (self.mock_now - datetime.timedelta(days=40)).timestamp() # Older but wrong pattern
            return self.mock_now.timestamp()

        mock_getmtime.side_effect = getmtime_side_effect

        mock_walk.return_value = [
            ('/root', [], ['old_log.log', 'recent_log.log', 'old_txt.txt']),
        ]

        empty_dirs, old_files = dust_bunny_sweeper.find_dust_bunnies(
            root_path='/root', age_days=30, patterns=['*.log'], dry_run=True
        )

        self.assertEqual(len(empty_dirs), 0)
        self.assertIn('/root/old_log.log', old_files)
        self.assertNotIn('/root/recent_log.log', old_files)
        self.assertNotIn('/root/old_txt.txt', old_files)
        self.assertEqual(len(old_files), 1)

    @patch('dust_bunny_sweeper.os.walk')
    @patch('dust_bunny_sweeper.os.path.getmtime')
    @patch('dust_bunny_sweeper.os.path.isdir', return_value=True)
    @patch('dust_bunny_sweeper.get_current_time')
    def test_find_dust_bunnies_no_patterns_all_old_files(self, mock_get_current_time, mock_isdir, mock_getmtime, mock_walk):
        """Test finding all old files when no patterns are specified."""
        mock_get_current_time.return_value = self.mock_now

        def getmtime_side_effect(path):
            if 'old_file1.txt' in path or 'old_file2.log' in path:
                return (self.mock_now - datetime.timedelta(days=40)).timestamp()
            return (self.mock_now - datetime.timedelta(days=10)).timestamp()

        mock_getmtime.side_effect = getmtime_side_effect

        mock_walk.return_value = [
            ('/root', [], ['old_file1.txt', 'old_file2.log', 'recent_file.tmp']),
        ]

        empty_dirs, old_files = dust_bunny_sweeper.find_dust_bunnies(
            root_path='/root', age_days=30, patterns=[], dry_run=True
        )

        self.assertEqual(len(empty_dirs), 0)
        self.assertIn('/root/old_file1.txt', old_files)
        self.assertIn('/root/old_file2.log', old_files)
        self.assertNotIn('/root/recent_file.tmp', old_files)
        self.assertEqual(len(old_files), 2)

    @patch('dust_bunny_sweeper.os.rmdir')
    @patch('dust_bunny_sweeper.os.remove')
    @patch('builtins.print')
    def test_report_and_clean_delete_mode(self, mock_print, mock_remove, mock_rmdir):
        """Test report_and_clean in actual deletion mode."""
        empty_dirs = ['/root/empty1', '/root/empty2']
        old_files = ['/root/old_file.log', '/root/another_old.tmp']

        dust_bunny_sweeper.report_and_clean(empty_dirs, old_files, dry_run=False)

        self.assertEqual(mock_rmdir.call_count, 2)
        mock_rmdir.assert_any_call('/root/empty1')
        mock_rmdir.assert_any_call('/root/empty2')

        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call('/root/old_file.log')
        mock_remove.assert_any_call('/root/another_old.tmp')

        # Check for specific output messages (optional, but good for whimsical tone)
        mock_print.assert_any_call('\n🧹 Sweeping away empty directories...')
        mock_print.assert_any_call('    ✅ Removed: /root/empty1')
        mock_print.assert_any_call('\n🔥 Incinerating ancient data fragments...')
        mock_print.assert_any_call('    ✅ Incinerated: /root/old_file.log')
        mock_print.assert_any_call('✅ Digital dust bunnies vanquished! Your system is ready for anything.')

    @patch('dust_bunny_sweeper.os.rmdir')
    @patch('dust_bunny_sweeper.os.remove')
    @patch('builtins.print')
    def test_report_and_clean_dry_run_mode(self, mock_print, mock_remove, mock_rmdir):
        """Test report_and_clean in dry run mode."""
        empty_dirs = ['/root/empty1']
        old_files = ['/root/old_file.log']

        dust_bunny_sweeper.report_and_clean(empty_dirs, old_files, dry_run=True)

        mock_rmdir.assert_not_called()
        mock_remove.assert_not_called()

        mock_print.assert_any_call('\n(Dry run: Empty directories would be swept away.)')
        mock_print.assert_any_call('\n(Dry run: Ancient data fragments would be incinerated.)')
        mock_print.assert_any_call('💡 Review the report above. Run again without --dry-run to perform actions.')

    @patch('dust_bunny_sweeper.os.rmdir')
    @patch('dust_bunny_sweeper.os.remove')
    @patch('builtins.print')
    def test_report_and_clean_no_findings(self, mock_print, mock_remove, mock_rmdir):
        """Test report_and_clean when no dust bunnies are found."""
        empty_dirs = []
        old_files = []

        dust_bunny_sweeper.report_and_clean(empty_dirs, old_files, dry_run=True)

        mock_rmdir.assert_not_called()
        mock_remove.assert_not_called()

        mock_print.assert_any_call('\n✨ No empty directories found. Your digital catacombs are pristine!')
        mock_print.assert_any_call('\n🌟 No ancient data fragments found. Your archives are spick and span!')
        mock_print.assert_any_call('🎉 Your file system is remarkably clean. The apocalypse can wait!')

    @patch('dust_bunny_sweeper.os.walk')
    @patch('dust_bunny_sweeper.os.path.getmtime')
    @patch('dust_bunny_sweeper.os.path.isdir', return_value=True)
    @patch('dust_bunny_sweeper.get_current_time')
    @patch('builtins.print') # Mock print to capture output
    def test_find_dust_bunnies_os_error(self, mock_print, mock_get_current_time, mock_isdir, mock_getmtime, mock_walk):
        """Test handling of OSError during file access."""
        mock_get_current_time.return_value = self.mock_now
        mock_getmtime.side_effect = OSError("Permission denied")

        mock_walk.return_value = [
            ('/root', [], ['unreadable_file.log']),
        ]

        empty_dirs, old_files = dust_bunny_sweeper.find_dust_bunnies(
            root_path='/root', age_days=30, patterns=['*.log'], dry_run=True
        )

        self.assertEqual(len(empty_dirs), 0)
        self.assertEqual(len(old_files), 0)
        mock_print.assert_any_call('⚠️  Warning: Could not access /root/unreadable_file.log: Permission denied', file=sys.stderr)

    @patch('dust_bunny_sweeper.os.rmdir')
    @patch('dust_bunny_sweeper.os.remove')
    @patch('builtins.print')
    def test_report_and_clean_deletion_os_error(self, mock_print, mock_remove, mock_rmdir):
        """Test handling of OSError during deletion."""
        mock_rmdir.side_effect = [None, OSError("Dir not empty")] # First success, second fail
        mock_remove.side_effect = [None, OSError("File locked")] # First success, second fail

        empty_dirs = ['/root/empty1', '/root/empty2']
        old_files = ['/root/old_file.log', '/root/another_old.tmp']

        dust_bunny_sweeper.report_and_clean(empty_dirs, old_files, dry_run=False)

        self.assertEqual(mock_rmdir.call_count, 2)
        self.assertEqual(mock_remove.call_count, 2)

        mock_print.assert_any_call('    ✅ Removed: /root/empty1')
        mock_print.assert_any_call('    ❌ Failed to remove /root/empty2: Dir not empty', file=sys.stderr)
        mock_print.assert_any_call('    ✅ Incinerated: /root/old_file.log')
        mock_print.assert_any_call('    ❌ Failed to incinerate /root/another_old.tmp: File locked', file=sys.stderr)


if __name__ == '__main__':
    unittest.main()
