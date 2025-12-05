import unittest
import os
import shutil
import time
import datetime
from unittest.mock import patch, MagicMock

# Import the functions to be tested
from src.reverser import clean_old_files, list_quarantined_batches, restore_batch, QUARANTINE_DIR_NAME

class TestChronoShiftReverser(unittest.TestCase):

    def setUp(self):
        # Mock rationale: Mock datetime.datetime.now() for deterministic timestamping.
        self.mock_now = datetime.datetime(2023, 10, 27, 14, 30, 0)
        self.patcher_datetime = patch('src.reverser.datetime.datetime')
        self.mock_datetime = self.patcher_datetime.start()
        self.mock_datetime.now.return_value = self.mock_now
        self.mock_datetime.strftime.side_effect = lambda fmt: self.mock_now.strftime(fmt)
        self.mock_datetime.side_effect = lambda *args, **kwargs: datetime.datetime(*args, **kwargs)
        
        # Mock rationale: Mock time.time() for deterministic file modification times.
        self.mock_time_now = time.mktime(self.mock_now.timetuple())
        self.patcher_time = patch('src.reverser.time.time', return_value=self.mock_time_now)
        self.mock_time = self.patcher_time.start()

    def tearDown(self):
        self.patcher_datetime.stop()
        self.patcher_time.stop()

    @patch('src.reverser.os.path.isdir')
    @patch('src.reverser.os.makedirs')
    @patch('src.reverser.os.walk')
    @patch('src.reverser.os.path.isfile')
    @patch('src.reverser.os.path.getmtime')
    @patch('src.reverser.shutil.move')
    @patch('src.reverser.os.rmdir')
    @patch('src.reverser.os.listdir')
    @patch('builtins.print') # Mock rationale: Mock print to capture output and prevent console spam during tests.
    def test_clean_old_files_no_files(self, mock_print, mock_listdir, mock_rmdir, mock_move, mock_getmtime, mock_isfile, mock_walk, mock_makedirs, mock_isdir):
        # Mock rationale: Simulate an empty directory for cleaning, ensuring no files are moved and empty quarantine directories are removed.
        mock_isdir.side_effect = lambda p: p == '/test_dir'
        mock_walk.return_value = [('/test_dir', [], [])]
        mock_isfile.return_value = False # No files exist
        mock_listdir.return_value = [] # Quarantine dir will be empty after batch dir removal

        clean_old_files('/test_dir', 7)

        mock_makedirs.assert_called_once_with('/test_dir/.quarantine/2023-10-27_14-30-00', exist_ok=True)
        mock_move.assert_not_called()
        mock_rmdir.assert_any_call('/test_dir/.quarantine/2023-10-27_14-30-00')
        mock_rmdir.assert_any_call('/test_dir/.quarantine') # Base quarantine dir should also be removed if empty
        mock_print.assert_any_call("No old files found to quarantine. Removing empty batch directory.")

    @patch('src.reverser.os.path.isdir')
    @patch('src.reverser.os.makedirs')
    @patch('src.reverser.os.walk')
    @patch('src.reverser.os.path.isfile')
    @patch('src.reverser.os.path.getmtime')
    @patch('src.reverser.shutil.move')
    @patch('src.reverser.os.rmdir')
    @patch('src.reverser.os.listdir')
    @patch('builtins.print')
    def test_clean_old_files_with_old_and_new_files(self, mock_print, mock_listdir, mock_rmdir, mock_move, mock_getmtime, mock_isfile, mock_walk, mock_makedirs, mock_isdir):
        # Mock rationale: Simulate a directory with both old and new files, verifying only old files are moved and correct paths are used.
        target_dir = '/test_dir'
        quarantine_base = os.path.join(target_dir, QUARANTINE_DIR_NAME)
        batch_dir = os.path.join(quarantine_base, '2023-10-27_14-30-00')

        mock_isdir.side_effect = lambda p: p == target_dir or p == quarantine_base
        mock_walk.return_value = [
            (target_dir, [], ['old_file.txt', 'new_file.log']),
            (os.path.join(target_dir, 'subdir'), [], ['another_old.txt'])
        ]
        mock_isfile.side_effect = lambda p: p in [
            os.path.join(target_dir, 'old_file.txt'),
            os.path.join(target_dir, 'new_file.log'),
            os.path.join(target_dir, 'subdir', 'another_old.txt')
        ]

        # old_file.txt and another_old.txt are older than 7 days
        # new_file.log is newer than 7 days
        seven_days_ago = self.mock_time_now - (7 * 24 * 60 * 60)
        mock_getmtime.side_effect = lambda p: {
            os.path.join(target_dir, 'old_file.txt'): seven_days_ago - 100, # Older
            os.path.join(target_dir, 'new_file.log'): self.mock_time_now - 100, # Newer
            os.path.join(target_dir, 'subdir', 'another_old.txt'): seven_days_ago - 200 # Older
        }.get(p, self.mock_time_now)
        mock_listdir.return_value = ['some_file_in_quarantine'] # To prevent rmdir of base quarantine

        clean_old_files(target_dir, 7)

        mock_makedirs.assert_any_call(batch_dir, exist_ok=True)
        mock_makedirs.assert_any_call(os.path.join(batch_dir, 'subdir'), exist_ok=True)

        mock_move.assert_any_call(os.path.join(target_dir, 'old_file.txt'), os.path.join(batch_dir, 'old_file.txt'))
        mock_move.assert_any_call(os.path.join(target_dir, 'subdir', 'another_old.txt'), os.path.join(batch_dir, 'subdir', 'another_old.txt'))
        self.assertEqual(mock_move.call_count, 2)
        mock_print.assert_any_call("Successfully quarantined 2 files.")
        mock_rmdir.assert_not_called() # Should not remove batch dir as files were moved

    @patch('src.reverser.os.path.isdir')
    @patch('src.reverser.os.listdir')
    @patch('builtins.print')
    def test_list_quarantined_batches_no_quarantine_dir(self, mock_print, mock_listdir, mock_isdir):
        # Mock rationale: Simulate a scenario where no .quarantine directory exists, ensuring appropriate message is printed.
        mock_isdir.return_value = False

        list_quarantined_batches('/test_dir')

        mock_print.assert_called_once_with(f"No quarantine directory found at '/test_dir/{QUARANTINE_DIR_NAME}'.")
        mock_listdir.assert_not_called()

    @patch('src.reverser.os.path.isdir')
    @patch('src.reverser.os.listdir')
    @patch('builtins.print')
    def test_list_quarantined_batches_with_batches(self, mock_print, mock_listdir, mock_isdir):
        # Mock rationale: Simulate a .quarantine directory with multiple timestamped batches, verifying they are listed correctly and sorted.
        target_dir = '/test_dir'
        quarantine_base = os.path.join(target_dir, QUARANTINE_DIR_NAME)
        mock_isdir.side_effect = lambda p: p == quarantine_base or p.startswith(os.path.join(quarantine_base, '20'))
        mock_listdir.return_value = ['2023-10-25_10-00-00', '2023-10-26_11-00-00', '2023-10-24_09-00-00']

        list_quarantined_batches(target_dir)

        mock_print.assert_any_call(f"Quarantined batches in '{target_dir}':")
        mock_print.assert_any_call("- 2023-10-24_09-00-00")
        mock_print.assert_any_call("- 2023-10-25_10-00-00")
        mock_print.assert_any_call("- 2023-10-26_11-00-00")
        self.assertEqual(mock_print.call_count, 4) # Header + 3 batches

    @patch('src.reverser.os.path.isdir')
    @patch('src.reverser.os.makedirs')
    @patch('src.reverser.os.walk')
    @patch('src.reverser.shutil.move')
    @patch('src.reverser.shutil.rmtree')
    @patch('src.reverser.os.listdir')
    @patch('src.reverser.os.rmdir')
    @patch('builtins.print')
    def test_restore_batch_success(self, mock_print, mock_rmdir, mock_listdir, mock_rmtree, mock_move, mock_walk, mock_makedirs, mock_isdir):
        # Mock rationale: Simulate restoring a batch with files, verifying files are moved back and quarantine directories are cleaned up.
        target_dir = '/test_dir'
        batch_name = '2023-10-27_14-30-00'
        quarantine_base = os.path.join(target_dir, QUARANTINE_DIR_NAME)
        batch_path = os.path.join(quarantine_base, batch_name)

        mock_isdir.side_effect = lambda p: p == batch_path or p == quarantine_base
        mock_walk.return_value = [
            (batch_path, [], ['file1.txt']),
            (os.path.join(batch_path, 'sub'), [], ['file2.log'])
        ]
        mock_listdir.return_value = [] # Quarantine base will be empty after this restore

        restore_batch(target_dir, batch_name)

        mock_makedirs.assert_any_call(target_dir, exist_ok=True)
        mock_makedirs.assert_any_call(os.path.join(target_dir, 'sub'), exist_ok=True)

        mock_move.assert_any_call(os.path.join(batch_path, 'file1.txt'), os.path.join(target_dir, 'file1.txt'))
        mock_move.assert_any_call(os.path.join(batch_path, 'sub', 'file2.log'), os.path.join(target_dir, 'sub', 'file2.log'))
        self.assertEqual(mock_move.call_count, 2)
        mock_rmtree.assert_called_once_with(batch_path)
        mock_rmdir.assert_called_once_with(quarantine_base)
        mock_print.assert_any_call(f"Successfully restored 2 files from batch '{batch_name}'.")

    @patch('src.reverser.os.path.isdir')
    @patch('builtins.print')
    def test_restore_batch_not_found(self, mock_print, mock_isdir):
        # Mock rationale: Simulate attempting to restore a non-existent batch, ensuring an error message is printed.
        mock_isdir.return_value = False

        restore_batch('/test_dir', 'non-existent-batch')

        mock_print.assert_called_once_with(f"Error: Quarantine batch 'non-existent-batch' not found at '/test_dir/{QUARANTINE_DIR_NAME}/non-existent-batch'.")

    @patch('src.reverser.os.path.isdir')
    @patch('builtins.print')
    def test_clean_old_files_target_dir_not_exist(self, mock_print, mock_isdir):
        # Mock rationale: Simulate cleaning a non-existent target directory, ensuring an error message is printed.
        mock_isdir.return_value = False

        clean_old_files('/non_existent_dir', 7)

        mock_print.assert_called_once_with("Error: Target directory '/non_existent_dir' does not exist.")


if __name__ == '__main__':
    unittest.main()
