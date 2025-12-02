import unittest
from unittest.mock import patch, mock_open, call
import os
import sys
from datetime import datetime, timedelta

# Add the src directory to the path to allow importing dust_collector
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import dust_collector

class TestDustCollector(unittest.TestCase):

    def setUp(self):
        self.root_dir = '/mock/root'
        self.config_content = """
rules:
  - name: "Temporary Files"
    patterns:
      - "*.tmp"
      - "temp_*"
    max_age_days: 7
  - name: "Old Logs"
    patterns:
      - "*.log"
    max_age_days: 30
  - name: "Build Artifacts"
    patterns:
      - "build/*"
    max_age_days: 14
"""
        self.mock_now = datetime(2023, 10, 26, 10, 0, 0) # Fixed current time for deterministic tests

    @patch('builtins.print')
    @patch('os.remove')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.join', side_effect=os.path.join) # Mock rationale: os.path.join is used to construct full paths. Using the real function ensures correct path construction logic for testing.
    @patch('os.path.relpath', side_effect=os.path.relpath) # Mock rationale: os.path.relpath is used to get paths relative to the root. Using the real function ensures correct relative path logic for pattern matching.
    def test_basic_cleanup(self, mock_relpath, mock_join, mock_walk, mock_isdir, mock_getmtime, mock_remove, mock_print):
        # Mock rationale: os.walk is mocked to simulate a file system structure without actual disk access.
        mock_walk.return_value = [
            (self.root_dir, ['subdir'], ['file1.tmp', 'recent.log']),
            (os.path.join(self.root_dir, 'subdir'), [], ['old.log', 'temp_file.tmp', 'keep.txt']),
            (os.path.join(self.root_dir, 'build'), [], ['artifact.zip'])
        ]
        # Mock rationale: os.path.isdir is mocked to confirm the root directory exists without actual disk access.
        mock_isdir.return_value = True

        # Mock rationale: os.path.getmtime is mocked to control file modification times, allowing deterministic age-based filtering.
        # Files older than 7 days for .tmp, 30 days for .log, 14 days for build/*
        file_mtimes = {
            os.path.join(self.root_dir, 'file1.tmp'): (self.mock_now - timedelta(days=10)).timestamp(), # Older than 7 days
            os.path.join(self.root_dir, 'recent.log'): (self.mock_now - timedelta(days=5)).timestamp(),  # Not older than 30 days
            os.path.join(self.root_dir, 'subdir', 'old.log'): (self.mock_now - timedelta(days=35)).timestamp(), # Older than 30 days
            os.path.join(self.root_dir, 'subdir', 'temp_file.tmp'): (self.mock_now - timedelta(days=8)).timestamp(), # Older than 7 days
            os.path.join(self.root_dir, 'subdir', 'keep.txt'): (self.mock_now - timedelta(days=100)).timestamp(), # Not matching pattern
            os.path.join(self.root_dir, 'build', 'artifact.zip'): (self.mock_now - timedelta(days=20)).timestamp() # Older than 14 days
        }
        mock_getmtime.side_effect = lambda p: file_mtimes.get(p, self.mock_now.timestamp())

        with patch('dust_collector.datetime') as mock_dt:
            # Mock rationale: datetime.now is mocked to provide a fixed 'current' time, ensuring age calculations are deterministic.
            mock_dt.now.return_value = self.mock_now
            mock_dt.fromtimestamp.side_effect = datetime.fromtimestamp # Mock rationale: fromtimestamp is a static method, using the real one ensures correct timestamp conversion.
            mock_dt.timedelta = timedelta # Mock rationale: timedelta is a class, using the real one ensures correct duration calculations.

            with mock_open(read_data=self.config_content) as m_open:
                # Mock rationale: builtins.open is mocked to simulate reading the configuration file without actual disk I/O.
                dust_collector.collect_dust(self.root_dir, dust_collector.load_config('mock_config.yaml'))

                # Assertions
                expected_removals = [
                    os.path.join(self.root_dir, 'file1.tmp'),
                    os.path.join(self.root_dir, 'subdir', 'old.log'),
                    os.path.join(self.root_dir, 'subdir', 'temp_file.tmp'),
                    os.path.join(self.root_dir, 'build', 'artifact.zip')
                ]
                mock_remove.assert_has_calls([call(p) for p in expected_removals], any_order=True)
                self.assertEqual(mock_remove.call_count, len(expected_removals))

                # Verify print calls for removed files
                for path in expected_removals:
                    self.assertIn(call(f"  Removing: {path} (Last modified: {datetime.fromtimestamp(file_mtimes[path]).strftime('%Y-%m-%d %H:%M:%S')})"), mock_print.call_args_list)

    @patch('builtins.print')
    @patch('os.remove')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.join', side_effect=os.path.join)
    @patch('os.path.relpath', side_effect=os.path.relpath)
    def test_dry_run(self, mock_relpath, mock_join, mock_walk, mock_isdir, mock_getmtime, mock_remove, mock_print):
        mock_walk.return_value = [
            (self.root_dir, [], ['file1.tmp'])
        ]
        mock_isdir.return_value = True
        file_mtimes = {
            os.path.join(self.root_dir, 'file1.tmp'): (self.mock_now - timedelta(days=10)).timestamp()
        }
        mock_getmtime.side_effect = lambda p: file_mtimes.get(p, self.mock_now.timestamp())

        with patch('dust_collector.datetime') as mock_dt:
            mock_dt.now.return_value = self.mock_now
            mock_dt.fromtimestamp.side_effect = datetime.fromtimestamp
            mock_dt.timedelta = timedelta

            with mock_open(read_data=self.config_content) as m_open:
                dust_collector.collect_dust(self.root_dir, dust_collector.load_config('mock_config.yaml'), dry_run=True)

                mock_remove.assert_not_called()
                self.assertIn(call(f"  Would remove: {os.path.join(self.root_dir, 'file1.tmp')} (Last modified: {datetime.fromtimestamp(file_mtimes[os.path.join(self.root_dir, 'file1.tmp')]).strftime('%Y-%m-%d %H:%M:%S')})"), mock_print.call_args_list)

    @patch('builtins.print')
    @patch('os.remove')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.join', side_effect=os.path.join)
    @patch('os.path.relpath', side_effect=os.path.relpath)
    def test_no_matching_files(self, mock_relpath, mock_join, mock_walk, mock_isdir, mock_getmtime, mock_remove, mock_print):
        mock_walk.return_value = [
            (self.root_dir, [], ['keep.txt', 'another.file'])
        ]
        mock_isdir.return_value = True
        file_mtimes = {
            os.path.join(self.root_dir, 'keep.txt'): (self.mock_now - timedelta(days=100)).timestamp(),
            os.path.join(self.root_dir, 'another.file'): (self.mock_now - timedelta(days=100)).timestamp()
        }
        mock_getmtime.side_effect = lambda p: file_mtimes.get(p, self.mock_now.timestamp())

        with patch('dust_collector.datetime') as mock_dt:
            mock_dt.now.return_value = self.mock_now
            mock_dt.fromtimestamp.side_effect = datetime.fromtimestamp
            mock_dt.timedelta = timedelta

            with mock_open(read_data=self.config_content) as m_open:
                dust_collector.collect_dust(self.root_dir, dust_collector.load_config('mock_config.yaml'))

                mock_remove.assert_not_called()
                self.assertIn(call("\nCosmic dust collection complete. 0 files removed."), mock_print.call_args_list)

    @patch('builtins.print')
    @patch('sys.exit')
    @patch('builtins.open', new_callable=mock_open, read_data='invalid yaml content')
    def test_load_config_invalid_yaml(self, mock_open, mock_exit, mock_print):
        # Mock rationale: builtins.open is mocked to simulate reading a malformed YAML file.
        # Mock rationale: sys.exit is mocked to prevent the test from terminating the runner, allowing assertion on its call.
        dust_collector.load_config('bad_config.yaml')
        mock_exit.assert_called_once_with(1)
        self.assertIn(call("Error parsing config file 'bad_config.yaml': ", unittest.mock.ANY), mock_print.call_args_list)

    @patch('builtins.print')
    @patch('sys.exit')
    @patch('builtins.open', new_callable=mock_open, read_data='rules: not_a_list')
    def test_load_config_invalid_format(self, mock_open, mock_exit, mock_print):
        # Mock rationale: builtins.open is mocked to simulate reading a YAML file with incorrect structure.
        # Mock rationale: sys.exit is mocked to prevent the test from terminating the runner.
        dust_collector.load_config('bad_format.yaml')
        mock_exit.assert_called_once_with(1)
        self.assertIn(call("Error in config file format: Config file must contain a 'rules' list."), mock_print.call_args_list)

    @patch('builtins.print')
    @patch('sys.exit')
    @patch('os.path.isdir', return_value=False) # Mock rationale: os.path.isdir is mocked to simulate a non-existent root directory.
    def test_collect_dust_invalid_root_dir(self, mock_isdir, mock_exit, mock_print):
        # We need a valid config dict for collect_dust, so we mock load_config to return a dummy one.
        with patch('dust_collector.load_config', return_value={'rules': []}):
            dust_collector.collect_dust('/nonexistent/path', {'rules': []})
        mock_exit.assert_called_once_with(1)
        self.assertIn(call("Error: Root directory '/nonexistent/path' not found or is not a directory.", file=sys.stderr), mock_print.call_args_list)

    @patch('builtins.print')
    @patch('os.remove')
    @patch('os.path.getmtime')
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.join', side_effect=os.path.join)
    @patch('os.path.relpath', side_effect=os.path.relpath)
    def test_rule_missing_patterns_or_age(self, mock_relpath, mock_join, mock_walk, mock_isdir, mock_getmtime, mock_remove, mock_print):
        mock_walk.return_value = []
        invalid_config_content = """
rules:
  - name: "Incomplete Rule 1"
    patterns:
      - "*.tmp"
    # max_age_days is missing
  - name: "Incomplete Rule 2"
    max_age_days: 5
    # patterns is missing
"""
        with patch('dust_collector.datetime') as mock_dt:
            mock_dt.now.return_value = self.mock_now
            mock_dt.fromtimestamp.side_effect = datetime.fromtimestamp
            mock_dt.timedelta = timedelta

            with mock_open(read_data=invalid_config_content) as m_open:
                dust_collector.collect_dust(self.root_dir, dust_collector.load_config('mock_config.yaml'))

                mock_remove.assert_not_called()
                self.assertIn(call("Warning: Rule 'Incomplete Rule 1' is missing 'patterns' or 'max_age_days'. Skipping.", file=sys.stderr), mock_print.call_args_list)
                self.assertIn(call("Warning: Rule 'Incomplete Rule 2' is missing 'patterns' or 'max_age_days'. Skipping.", file=sys.stderr), mock_print.call_args_list)

if __name__ == '__main__':
    unittest.main()
