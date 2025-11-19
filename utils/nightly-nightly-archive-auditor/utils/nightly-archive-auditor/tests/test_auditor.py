import unittest
from unittest.mock import patch, MagicMock
import datetime
import os
import sys
from io import StringIO

# Add the src directory to the path to import auditor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from auditor import find_stale_files, generate_report, main

class TestApocalypseArchiveAuditor(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print output
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('auditor.datetime')
    @patch('auditor.os.walk')
    @patch('auditor.os.path.getmtime')
    def test_find_stale_files_no_stale(self, mock_getmtime, mock_walk, mock_datetime):
        # Mock rationale: Simulate current time for deterministic age calculation.
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        # Mock rationale: Simulate datetime.datetime.fromtimestamp for deterministic conversion.
        mock_datetime.datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
        mock_datetime.timedelta.side_effect = datetime.timedelta

        # Mock rationale: Simulate a directory structure with files.
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log']),
            ('/test_dir/subdir', [], ['file3.md'])
        ]

        # Mock rationale: Simulate modification times for files.
        # All files are newer than the 30-day threshold (current_time - 30 days = 2023-09-26)
        mock_getmtime.side_effect = {
            '/test_dir/file1.txt': datetime.datetime(2023, 10, 1, 12, 0, 0).timestamp(), # 25 days old
            '/test_dir/file2.log': datetime.datetime(2023, 9, 27, 8, 0, 0).timestamp(), # 29 days old
            '/test_dir/subdir/file3.md': datetime.datetime(2023, 10, 15, 14, 0, 0).timestamp(), # 11 days old
        }.get

        stale_files = find_stale_files('/test_dir', 30)
        self.assertEqual(len(stale_files), 0)

    @patch('auditor.datetime')
    @patch('auditor.os.walk')
    @patch('auditor.os.path.getmtime')
    def test_find_stale_files_with_stale(self, mock_getmtime, mock_walk, mock_datetime):
        # Mock rationale: Simulate current time for deterministic age calculation.
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        # Mock rationale: Simulate datetime.datetime.fromtimestamp for deterministic conversion.
        mock_datetime.datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
        mock_datetime.timedelta.side_effect = datetime.timedelta

        # Mock rationale: Simulate a directory structure with files.
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log']),
            ('/test_dir/subdir', [], ['file3.md'])
        ]

        # Mock rationale: Simulate modification times for files.
        # Threshold: 30 days (2023-09-26)
        mock_getmtime.side_effect = {
            '/test_dir/file1.txt': datetime.datetime(2023, 9, 1, 12, 0, 0).timestamp(), # 55 days old (stale)
            '/test_dir/file2.log': datetime.datetime(2023, 10, 1, 8, 0, 0).timestamp(), # 25 days old (not stale)
            '/test_dir/subdir/file3.md': datetime.datetime(2023, 8, 15, 14, 0, 0).timestamp(), # 72 days old (stale)
        }.get

        stale_files = find_stale_files('/test_dir', 30)
        self.assertEqual(len(stale_files), 2)
        self.assertIn(('/test_dir/file1.txt', datetime.datetime(2023, 9, 1, 12, 0)), stale_files)
        self.assertIn(('/test_dir/subdir/file3.md', datetime.datetime(2023, 8, 15, 14, 0)), stale_files)

    @patch('auditor.datetime')
    def test_generate_report_no_stale(self, mock_datetime):
        # Mock rationale: Simulate current time for deterministic report generation.
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.timedelta.side_effect = datetime.timedelta # Ensure timedelta works

        report = generate_report([], '/test_dir', 365)
        self.assertIn("No stale files found. Your archives are surprisingly fresh!", report)
        self.assertIn("# Apocalypse Archive Auditor Report for '/test_dir'", report)

    @patch('auditor.datetime')
    def test_generate_report_with_stale(self, mock_datetime):
        # Mock rationale: Simulate current time for deterministic report generation.
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.timedelta.side_effect = datetime.timedelta # Ensure timedelta works

        stale_files = [
            ('/test_dir/old_file.txt', datetime.datetime(2022, 1, 1, 10, 0)),
            ('/test_dir/subdir/older_file.log', datetime.datetime(2021, 5, 15, 12, 0)),
        ]
        report = generate_report(stale_files, '/test_dir', 365)

        self.assertIn("Found 2 potentially stale files:", report)
        self.assertIn("| File Path | Last Modified | Age (days) |", report)
        self.assertIn("| :-------- | :------------ | :--------- |", report)
        self.assertIn("| `/test_dir/subdir/older_file.log` | 2021-05-15 | 894 |", report) # 2023-10-26 - 2021-05-15 = 894 days
        self.assertIn("| `/test_dir/old_file.txt` | 2022-01-01 | 663 |", report) # 2023-10-26 - 2022-01-01 = 663 days
        # Check sorting (older_file should come first)
        self.assertTrue(report.find('older_file.log') < report.find('old_file.txt'))


    @patch('auditor.os.path.isdir', return_value=True)
    @patch('auditor.find_stale_files', return_value=[])
    @patch('auditor.generate_report', return_value="Mock Report Content")
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_stale_files(self, mock_stdout, mock_generate_report, mock_find_stale_files, mock_isdir):
        # Mock rationale: Simulate command-line arguments.
        with patch('sys.argv', ['auditor.py', '/mock_dir', '--age', '100']):
            main()
            self.assertIn("Scanning '/mock_dir' for files older than 100 days...", mock_stdout.getvalue())
            self.assertIn("Mock Report Content", mock_stdout.getvalue())
            mock_find_stale_files.assert_called_once_with('/mock_dir', 100)
            mock_generate_report.assert_called_once_with([], '/mock_dir', 100)

    @patch('auditor.os.path.isdir', return_value=False)
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_invalid_directory(self, mock_stderr, mock_isdir):
        # Mock rationale: Simulate command-line arguments.
        with patch('sys.argv', ['auditor.py', '/non_existent_dir']):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: Directory '/non_existent_dir' not found or is not a directory.", mock_stderr.getvalue())

    @patch('auditor.datetime')
    @patch('auditor.os.walk')
    @patch('auditor.os.path.getmtime')
    def test_find_stale_files_os_error_handling(self, mock_getmtime, mock_walk, mock_datetime):
        # Mock rationale: Simulate current time for deterministic age calculation.
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        # Mock rationale: Simulate datetime.datetime.fromtimestamp for deterministic conversion.
        mock_datetime.datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
        mock_datetime.timedelta.side_effect = datetime.timedelta

        # Mock rationale: Simulate a directory structure with files, one causing an OSError.
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'inaccessible.txt']),
        ]

        # Mock rationale: Simulate modification times, with one raising OSError.
        def getmtime_side_effect(path):
            if path == '/test_dir/file1.txt':
                return datetime.datetime(2023, 9, 1, 12, 0, 0).timestamp() # Stale
            elif path == '/test_dir/inaccessible.txt':
                raise OSError("Permission denied")
            return 0 # Should not be reached

        mock_getmtime.side_effect = getmtime_side_effect

        stale_files = find_stale_files('/test_dir', 30)
        self.assertEqual(len(stale_files), 1)
        self.assertIn(('/test_dir/file1.txt', datetime.datetime(2023, 9, 1, 12, 0)), stale_files)
        # Ensure inaccessible.txt was skipped without crashing

if __name__ == '__main__':
    unittest.main()
