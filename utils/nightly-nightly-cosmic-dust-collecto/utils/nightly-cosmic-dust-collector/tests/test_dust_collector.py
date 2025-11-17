import unittest
from unittest import mock
import datetime
import os
import sys

# Add the src directory to the Python path to import dust_collector
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import dust_collector

class TestDustCollector(unittest.TestCase):

    def setUp(self):
        # Define a fixed current time for deterministic tests
        self.fixed_current_time = datetime.datetime(2024, 4, 23, 10, 0, 0)

    @mock.patch('os.path.getmtime')
    @mock.patch('os.walk')
    def test_no_dust_found(self, mock_os_walk, mock_getmtime):
        # Mock rationale: os.walk simulates file system traversal, os.path.getmtime simulates file modification times.
        # This allows deterministic testing without actual file system interaction.

        # Simulate a directory with all recent files
        mock_os_walk.return_value = [
            ('/repo', ['sub'], ['file1.txt', 'file2.log']),
            ('/repo/sub', [], ['sub_file.md'])
        ]

        # All files modified recently (e.g., 10 days ago)
        recent_timestamp = (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()
        mock_getmtime.side_effect = [recent_timestamp, recent_timestamp, recent_timestamp]

        dusty_files = dust_collector.collect_dust('/repo', age_days=30, exclude_patterns=[], current_time=self.fixed_current_time)
        self.assertEqual(len(dusty_files), 0)

    @mock.patch('os.path.getmtime')
    @mock.patch('os.walk')
    def test_dust_found(self, mock_os_walk, mock_getmtime):
        # Mock rationale: os.walk simulates file system traversal, os.path.getmtime simulates file modification times.
        # This allows deterministic testing without actual file system interaction.

        # Simulate a directory with some old files
        mock_os_walk.return_value = [
            ('/repo', [], ['recent.txt', 'old_log.txt', 'very_old.tmp'])
        ]

        # Define modification times: one recent, two old
        recent_timestamp = (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()
        old_timestamp = (self.fixed_current_time - datetime.timedelta(days=100)).timestamp()
        very_old_timestamp = (self.fixed_current_time - datetime.timedelta(days=200)).timestamp()

        mock_getmtime.side_effect = [
            recent_timestamp,      # /repo/recent.txt
            old_timestamp,         # /repo/old_log.txt
            very_old_timestamp     # /repo/very_old.tmp
        ]

        dusty_files = dust_collector.collect_dust('/repo', age_days=90, exclude_patterns=[], current_time=self.fixed_current_time)
        self.assertEqual(len(dusty_files), 2)
        self.assertIn({'path': '/repo/old_log.txt', 'last_modified': datetime.datetime.fromtimestamp(old_timestamp).isoformat()}, dusty_files)
        self.assertIn({'path': '/repo/very_old.tmp', 'last_modified': datetime.datetime.fromtimestamp(very_old_timestamp).isoformat()}, dusty_files)

    @mock.patch('os.path.getmtime')
    @mock.patch('os.walk')
    def test_age_threshold(self, mock_os_walk, mock_getmtime):
        # Mock rationale: os.walk simulates file system traversal, os.path.getmtime simulates file modification times.
        # This allows deterministic testing without actual file system interaction.

        mock_os_walk.return_value = [
            ('/repo', [], ['file_80_days_old.txt', 'file_120_days_old.txt'])
        ]

        # Define modification times
        mtime_80_days_old = (self.fixed_current_time - datetime.timedelta(days=80)).timestamp()
        mtime_120_days_old = (self.fixed_current_time - datetime.timedelta(days=120)).timestamp()

        mock_getmtime.side_effect = [mtime_80_days_old, mtime_120_days_old]

        # Test with age_days = 90
        dusty_files_90 = dust_collector.collect_dust('/repo', age_days=90, exclude_patterns=[], current_time=self.fixed_current_time)
        self.assertEqual(len(dusty_files_90), 1)
        self.assertIn({'path': '/repo/file_120_days_old.txt', 'last_modified': datetime.datetime.fromtimestamp(mtime_120_days_old).isoformat()}, dusty_files_90)

        # Test with age_days = 70
        mock_getmtime.side_effect = [mtime_80_days_old, mtime_120_days_old] # Reset side_effect for second call
        dusty_files_70 = dust_collector.collect_dust('/repo', age_days=70, exclude_patterns=[], current_time=self.fixed_current_time)
        self.assertEqual(len(dusty_files_70), 2)

    @mock.patch('os.path.getmtime')
    @mock.patch('os.walk')
    def test_exclude_patterns(self, mock_os_walk, mock_getmtime):
        # Mock rationale: os.walk simulates file system traversal, os.path.getmtime simulates file modification times.
        # This allows deterministic testing without actual file system interaction.

        mock_os_walk.return_value = [
            ('/repo', ['node_modules', 'logs'], ['main.py', 'temp.log']),
            ('/repo/node_modules', [], ['package.json', 'index.js']),
            ('/repo/logs', [], ['app.log', 'error.log.old'])
        ]

        # All files are old
        old_timestamp = (self.fixed_current_time - datetime.timedelta(days=100)).timestamp()
        mock_getmtime.side_effect = [old_timestamp] * 6 # For all files

        # Exclude .log files and node_modules directory
        exclude_patterns = ['*.log', '/repo/node_modules/*', '*/node_modules/*']
        dusty_files = dust_collector.collect_dust('/repo', age_days=90, exclude_patterns=exclude_patterns, current_time=self.fixed_current_time)

        self.assertEqual(len(dusty_files), 1)
        self.assertIn({'path': '/repo/logs/error.log.old', 'last_modified': datetime.datetime.fromtimestamp(old_timestamp).isoformat()}, dusty_files)
        self.assertNotIn({'path': '/repo/main.py', 'last_modified': datetime.datetime.fromtimestamp(old_timestamp).isoformat()}, dusty_files) # Not excluded, but not old enough
        self.assertNotIn({'path': '/repo/temp.log', 'last_modified': datetime.datetime.fromtimestamp(old_timestamp).isoformat()}, dusty_files) # Excluded by *.log
        self.assertNotIn({'path': '/repo/node_modules/package.json', 'last_modified': datetime.datetime.fromtimestamp(old_timestamp).isoformat()}, dusty_files) # Excluded by node_modules/*
        self.assertNotIn({'path': '/repo/node_modules/index.js', 'last_modified': datetime.datetime.fromtimestamp(old_timestamp).isoformat()}, dusty_files) # Excluded by node_modules/*
        self.assertNotIn({'path': '/repo/logs/app.log', 'last_modified': datetime.datetime.fromtimestamp(old_timestamp).isoformat()}, dusty_files) # Excluded by *.log

    @mock.patch('os.path.getmtime')
    @mock.patch('os.walk')
    def test_empty_directory(self, mock_os_walk, mock_getmtime):
        # Mock rationale: os.walk simulates file system traversal, os.path.getmtime simulates file modification times.
        # This allows deterministic testing without actual file system interaction.

        mock_os_walk.return_value = [
            ('/empty_repo', [], [])
        ]
        mock_getmtime.side_effect = [] # No files to get mtime for

        dusty_files = dust_collector.collect_dust('/empty_repo', age_days=30, exclude_patterns=[], current_time=self.fixed_current_time)
        self.assertEqual(len(dusty_files), 0)

    @mock.patch('os.path.getmtime')
    @mock.patch('os.walk')
    def test_nested_directories(self, mock_os_walk, mock_getmtime):
        # Mock rationale: os.walk simulates file system traversal, os.path.getmtime simulates file modification times.
        # This allows deterministic testing without actual file system interaction.

        mock_os_walk.return_value = [
            ('/repo', ['src', 'data'], ['root_file.txt']),
            ('/repo/src', [], ['code.py']),
            ('/repo/data', ['archive'], ['report.csv']),
            ('/repo/data/archive', [], ['old_backup.zip'])
        ]

        # Define modification times: root_file and old_backup are old
        recent_timestamp = (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()
        old_timestamp = (self.fixed_current_time - datetime.timedelta(days=100)).timestamp()

        mock_getmtime.side_effect = [
            old_timestamp,      # /repo/root_file.txt
            recent_timestamp,   # /repo/src/code.py
            recent_timestamp,   # /repo/data/report.csv
            old_timestamp       # /repo/data/archive/old_backup.zip
        ]

        dusty_files = dust_collector.collect_dust('/repo', age_days=90, exclude_patterns=[], current_time=self.fixed_current_time)
        self.assertEqual(len(dusty_files), 2)
        self.assertIn({'path': '/repo/root_file.txt', 'last_modified': datetime.datetime.fromtimestamp(old_timestamp).isoformat()}, dusty_files)
        self.assertIn({'path': '/repo/data/archive/old_backup.zip', 'last_modified': datetime.datetime.fromtimestamp(old_timestamp).isoformat()}, dusty_files)

    @mock.patch('os.path.getmtime')
    @mock.patch('os.walk')
    def test_is_excluded_function(self, mock_os_walk, mock_getmtime):
        # Mock rationale: os.walk and os.path.getmtime are not directly used by is_excluded, but are part of the overall mock setup.
        # This test focuses on the helper function's logic.

        self.assertTrue(dust_collector.is_excluded('/repo/temp/file.tmp', ['*/temp/*']))
        self.assertTrue(dust_collector.is_excluded('/repo/logs/app.log', ['*.log']))
        self.assertFalse(dust_collector.is_excluded('/repo/src/main.py', ['*.log']))
        self.assertTrue(dust_collector.is_excluded('/repo/.git/HEAD', ['.git/*']))
        self.assertFalse(dust_collector.is_excluded('/repo/docs/README.md', ['.git/*']))
        self.assertTrue(dust_collector.is_excluded('/repo/build/output/temp.txt', ['/repo/build/**/*']))

    @mock.patch('sys.stdout', new_callable=mock.StringIO)
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('os.path.getmtime')
    @mock.patch('os.walk')
    def test_main_text_output(self, mock_os_walk, mock_getmtime, mock_isdir, mock_stdout):
        # Mock rationale: sys.stdout captures print output, os.path.isdir ensures the path is valid.
        # os.walk and os.path.getmtime simulate file system content and modification times.

        mock_os_walk.return_value = [
            ('/test_path', [], ['old_file.txt', 'recent_file.txt'])
        ]
        old_timestamp = (self.fixed_current_time - datetime.timedelta(days=100)).timestamp()
        recent_timestamp = (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()
        mock_getmtime.side_effect = [old_timestamp, recent_timestamp]

        with mock.patch('argparse.ArgumentParser.parse_args', return_value=mock.Mock(
            path='/test_path',
            age_days=90,
            exclude=[],
            output_format='text'
        )):
            with mock.patch('datetime.datetime') as mock_dt:
                mock_dt.now.return_value = self.fixed_current_time
                mock_dt.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
                mock_dt.timedelta = datetime.timedelta
                dust_collector.main()
                output = mock_stdout.getvalue()
                self.assertIn("Cosmic Dust Report for: /test_path (older than 90 days)", output)
                self.assertIn("Found 1 dusty files:", output)
                self.assertIn("  - /test_path/old_file.txt (Last modified: 2024-01-14)", output)
                self.assertNotIn("recent_file.txt", output)

    @mock.patch('sys.stdout', new_callable=mock.StringIO)
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('os.path.getmtime')
    @mock.patch('os.walk')
    def test_main_json_output(self, mock_os_walk, mock_getmtime, mock_isdir, mock_stdout):
        # Mock rationale: sys.stdout captures print output, os.path.isdir ensures the path is valid.
        # os.walk and os.path.getmtime simulate file system content and modification times.

        mock_os_walk.return_value = [
            ('/test_path', [], ['old_file.txt'])
        ]
        old_timestamp = (self.fixed_current_time - datetime.timedelta(days=100)).timestamp()
        mock_getmtime.side_effect = [old_timestamp]

        with mock.patch('argparse.ArgumentParser.parse_args', return_value=mock.Mock(
            path='/test_path',
            age_days=90,
            exclude=[],
            output_format='json'
        )):
            with mock.patch('datetime.datetime') as mock_dt:
                mock_dt.now.return_value = self.fixed_current_time
                mock_dt.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
                mock_dt.timedelta = datetime.timedelta
                dust_collector.main()
                output = mock_stdout.getvalue()
                output_json = json.loads(output)
                self.assertEqual(output_json['scan_path'], '/test_path')
                self.assertEqual(output_json['age_threshold_days'], 90)
                self.assertEqual(len(output_json['dusty_files']), 1)
                self.assertEqual(output_json['dusty_files'][0]['path'], '/test_path/old_file.txt')
                self.assertEqual(output_json['dusty_files'][0]['last_modified'], datetime.datetime.fromtimestamp(old_timestamp).isoformat())

if __name__ == '__main__':
    unittest.main()
