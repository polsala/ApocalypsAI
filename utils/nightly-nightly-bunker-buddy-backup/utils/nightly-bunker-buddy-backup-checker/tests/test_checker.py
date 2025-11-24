import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime

# Mock rationale: We need to simulate file system interactions (existence, modification times)
# without actually touching the disk. This ensures tests are fast, deterministic, and isolated.
# `os.path.exists`, `os.path.isdir`, `os.path.getmtime`, `os.path.basename`, `os.path.join`
# are all mocked to control the test environment precisely.

# Add the src directory to the path for importing the checker module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import checker
sys.path.pop(0)

class TestBunkerBuddyBackupChecker(unittest.TestCase):

    def setUp(self):
        # Define some mock paths and times
        self.mock_source_file = '/app/critical_data/plans.txt'
        self.mock_source_dir = '/app/critical_data/configs'
        self.mock_backup_bunker = '/mnt/bunker_backups'
        self.mock_backup_file = os.path.join(self.mock_backup_bunker, 'plans.txt')
        self.mock_backup_dir = os.path.join(self.mock_backup_bunker, 'configs')

        self.time_old = datetime(2023, 1, 1, 10, 0, 0).timestamp()
        self.time_new = datetime(2023, 1, 1, 11, 0, 0).timestamp()
        self.time_newer = datetime(2023, 1, 1, 12, 0, 0).timestamp()

    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.path.basename', side_effect=os.path.basename) # Mock rationale: Keep basename behavior as is
    @patch('os.path.join', side_effect=os.path.join) # Mock rationale: Keep join behavior as is
    def test_source_missing(self, mock_join, mock_basename, mock_isdir, mock_getmtime, mock_exists):
        # Mock rationale: Simulate the source file not existing on the filesystem.
        mock_exists.side_effect = lambda p: p != self.mock_source_file and p == self.mock_backup_bunker
        mock_isdir.return_value = True

        status, message = checker.check_backup_status(self.mock_source_file, self.mock_backup_bunker)
        self.assertEqual(status, "SOURCE MISSING")
        self.assertIn("does not exist", message)

    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.path.basename', side_effect=os.path.basename)
    @patch('os.path.join', side_effect=os.path.join)
    def test_backup_missing_file(self, mock_join, mock_basename, mock_isdir, mock_getmtime, mock_exists):
        # Mock rationale: Simulate the source file existing, but its backup counterpart not existing.
        mock_exists.side_effect = lambda p: p == self.mock_source_file or p == self.mock_backup_bunker
        mock_isdir.return_value = True

        status, message = checker.check_backup_status(self.mock_source_file, self.mock_backup_bunker)
        self.assertEqual(status, "MISSING IN BUNKER")
        self.assertIn("is missing in the bunker", message)

    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.path.basename', side_effect=os.path.basename)
    @patch('os.path.join', side_effect=os.path.join)
    def test_backup_missing_dir(self, mock_join, mock_basename, mock_isdir, mock_getmtime, mock_exists):
        # Mock rationale: Simulate the source directory existing, but its backup counterpart not existing.
        mock_exists.side_effect = lambda p: p == self.mock_source_dir or p == self.mock_backup_bunker
        mock_isdir.return_value = True

        status, message = checker.check_backup_status(self.mock_source_dir, self.mock_backup_bunker)
        self.assertEqual(status, "MISSING IN BUNKER")
        self.assertIn("is missing in the bunker", message)

    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.path.basename', side_effect=os.path.basename)
    @patch('os.path.join', side_effect=os.path.join)
    def test_backup_outdated_file(self, mock_join, mock_basename, mock_isdir, mock_getmtime, mock_exists):
        # Mock rationale: Simulate both source and backup existing, but the source being newer.
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_getmtime.side_effect = lambda p: {
            self.mock_source_file: self.time_newer,
            self.mock_backup_file: self.time_old,
        }.get(p, self.time_old) # Default to old time for other paths

        status, message = checker.check_backup_status(self.mock_source_file, self.mock_backup_bunker)
        self.assertEqual(status, "OUTDATED")
        self.assertIn("is older", message)

    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.path.basename', side_effect=os.path.basename)
    @patch('os.path.join', side_effect=os.path.join)
    def test_backup_up_to_date_file(self, mock_join, mock_basename, mock_isdir, mock_getmtime, mock_exists):
        # Mock rationale: Simulate both source and backup existing, and the backup being as new or newer.
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_getmtime.side_effect = lambda p: {
            self.mock_source_file: self.time_new,
            self.mock_backup_file: self.time_newer, # Backup is newer or same
        }.get(p, self.time_old)

        status, message = checker.check_backup_status(self.mock_source_file, self.mock_backup_bunker)
        self.assertEqual(status, "UP-TO-DATE")
        self.assertIn("is up-to-date", message)

    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.path.basename', side_effect=os.path.basename)
    @patch('os.path.join', side_effect=os.path.join)
    def test_backup_up_to_date_dir(self, mock_join, mock_basename, mock_isdir, mock_getmtime, mock_exists):
        # Mock rationale: Simulate both source and backup directories existing, and the backup being as new or newer.
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_getmtime.side_effect = lambda p: {
            self.mock_source_dir: self.time_new,
            self.mock_backup_dir: self.time_newer, # Backup is newer or same
        }.get(p, self.time_old)

        status, message = checker.check_backup_status(self.mock_source_dir, self.mock_backup_bunker)
        self.assertEqual(status, "UP-TO-DATE")
        self.assertIn("is up-to-date", message)

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_bunker_not_found(self, mock_parse_args, mock_exit, mock_stderr, mock_stdout, mock_isdir, mock_exists):
        # Mock rationale: Simulate the main function being called with a non-existent bunker directory.
        mock_parse_args.return_value = MagicMock(
            source=[self.mock_source_file],
            backup=self.mock_backup_bunker
        )
        mock_exists.return_value = True # Source exists
        mock_isdir.side_effect = lambda p: p != self.mock_backup_bunker # Bunker is not a dir

        checker.main()
        mock_exit.assert_called_with(1)
        mock_stderr.assert_called_once()
        self.assertIn("Error: The specified bunker directory", mock_stderr.call_args[0][0])

    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.path.basename', side_effect=os.path.basename)
    @patch('os.path.join', side_effect=os.path.join)
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_all_ok(self, mock_parse_args, mock_exit, mock_stderr, mock_stdout, mock_join, mock_basename, mock_isdir, mock_getmtime, mock_exists):
        # Mock rationale: Simulate a scenario where all sources are up-to-date.
        mock_parse_args.return_value = MagicMock(
            source=[self.mock_source_file, self.mock_source_dir],
            backup=self.mock_backup_bunker
        )
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_getmtime.side_effect = lambda p: {
            self.mock_source_file: self.time_new,
            self.mock_backup_file: self.time_newer,
            self.mock_source_dir: self.time_new,
            self.mock_backup_dir: self.time_newer,
        }.get(p, self.time_old)

        checker.main()
        mock_exit.assert_called_with(0)
        self.assertIn("All critical supplies are accounted for", mock_stdout.call_args_list[-1].args[0])

    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.path.basename', side_effect=os.path.basename)
    @patch('os.path.join', side_effect=os.path.join)
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_some_issues(self, mock_parse_args, mock_exit, mock_stderr, mock_stdout, mock_join, mock_basename, mock_isdir, mock_getmtime, mock_exists):
        # Mock rationale: Simulate a scenario with mixed results, including an outdated file.
        mock_parse_args.return_value = MagicMock(
            source=[self.mock_source_file, self.mock_source_dir],
            backup=self.mock_backup_bunker
        )
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_getmtime.side_effect = lambda p: {
            self.mock_source_file: self.time_newer, # This one is outdated
            self.mock_backup_file: self.time_old,
            self.mock_source_dir: self.time_new,
            self.mock_backup_dir: self.time_newer,
        }.get(p, self.time_old)

        checker.main()
        mock_exit.assert_called_with(1)
        self.assertIn("Some critical supplies need your immediate attention!", mock_stdout.call_args_list[-1].args[0])
        self.assertIn("[OUTDATED", mock_stdout.call_args_list[1].args[0]) # Check for outdated status in output

    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.path.basename', side_effect=os.path.basename)
    @patch('os.path.join', side_effect=os.path.join)
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_source_missing_leads_to_exit_1(self, mock_parse_args, mock_exit, mock_stderr, mock_stdout, mock_join, mock_basename, mock_isdir, mock_getmtime, mock_exists):
        # Mock rationale: Simulate a scenario where a source file is missing, which should lead to exit code 1.
        mock_parse_args.return_value = MagicMock(
            source=[self.mock_source_file],
            backup=self.mock_backup_bunker
        )
        # Only bunker exists, source file does not
        mock_exists.side_effect = lambda p: p == self.mock_backup_bunker
        mock_isdir.return_value = True # Bunker is a directory

        checker.main()
        mock_exit.assert_called_with(1)
        self.assertIn("Attention, survivor!", mock_stdout.call_args_list[-1].args[0])
        self.assertIn("[SOURCE MISSING", mock_stdout.call_args_list[1].args[0])

if __name__ == '__main__':
    unittest.main()
