import unittest
import os
import json
import hashlib
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime, timezone

# Import the function to be tested
from src.manifest_generator import generate_manifest, get_file_checksum

class TestManifestGenerator(unittest.TestCase):

    def setUp(self):
        self.test_dir = '/mock/test/dir'
        self.output_file = 'test_manifest.json'
        self.mock_now = datetime(2023, 10, 27, 10, 0, 0, tzinfo=timezone.utc)

    # Helper to mock datetime.fromtimestamp consistently
    def _mock_fromtimestamp_side_effect(self, ts, tz):
        mock_dt = MagicMock()
        mock_dt.isoformat.return_value = datetime.fromtimestamp(ts, tz=tz).isoformat(timespec='seconds')
        return mock_dt

    @patch('os.path.isdir')
    @patch('os.path.abspath')
    @patch('os.walk')
    @patch('os.stat')
    @patch('src.manifest_generator.get_file_checksum') # Mock rationale: Avoid actual file I/O for checksum calculation, ensuring determinism and speed.
    @patch('builtins.open', new_callable=mock_open) # Mock rationale: Avoid actual file system write for output, capturing content in memory.
    @patch('src.manifest_generator.datetime') # Mock rationale: Ensure deterministic timestamps for manifest creation and file modification dates.
    @patch('builtins.print') # Mock rationale: Suppress print statements during tests to avoid polluting test output.
    def test_basic_manifest_generation(self, mock_print, mock_datetime, mock_open_func, mock_checksum, mock_stat, mock_walk, mock_abspath, mock_isdir):
        mock_isdir.return_value = True
        mock_abspath.return_value = self.test_dir
        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp.side_effect = self._mock_fromtimestamp_side_effect

        # Mock os.walk to simulate a simple directory structure
        mock_walk.return_value = [
            (self.test_dir, [], ['file1.txt', 'file2.md'])
        ]

        # Mock os.stat for each file
        mock_stat.side_effect = [
            MagicMock(st_size=100, st_mtime=datetime(2023, 1, 1, 12, 0, 0).timestamp()), # file1.txt
            MagicMock(st_size=200, st_mtime=datetime(2023, 1, 2, 13, 0, 0).timestamp())  # file2.md
        ]

        # Mock checksums
        mock_checksum.side_effect = ['checksum1', 'checksum2']

        generate_manifest(self.test_dir, output_filename=self.output_file)

        # Verify output file was opened for writing
        mock_open_func.assert_called_once_with(self.output_file, 'w', encoding='utf-8')
        written_content = mock_open_func().write.call_args[0][0]
        manifest_data = json.loads(written_content)

        self.assertEqual(manifest_data['manifest_version'], '1.0')
        self.assertEqual(manifest_data['scan_timestamp'], self.mock_now.isoformat(timespec='seconds'))
        self.assertEqual(manifest_data['scanned_directory'], self.test_dir)
        self.assertEqual(len(manifest_data['files']), 2)

        self.assertEqual(manifest_data['files'][0]['path'], 'file1.txt')
        self.assertEqual(manifest_data['files'][0]['name'], 'file1.txt')
        self.assertEqual(manifest_data['files'][0]['size_bytes'], 100)
        self.assertEqual(manifest_data['files'][0]['last_modified_utc'], '2023-01-01T12:00:00Z')
        self.assertEqual(manifest_data['files'][0]['sha256_checksum'], 'checksum1')

        self.assertEqual(manifest_data['files'][1]['path'], 'file2.md')
        self.assertEqual(manifest_data['files'][1]['name'], 'file2.md')
        self.assertEqual(manifest_data['files'][1]['size_bytes'], 200)
        self.assertEqual(manifest_data['files'][1]['last_modified_utc'], '2023-01-02T13:00:00Z')
        self.assertEqual(manifest_data['files'][1]['sha256_checksum'], 'checksum2')

    @patch('os.path.isdir')
    @patch('os.path.abspath')
    @patch('os.walk')
    @patch('os.stat')
    @patch('src.manifest_generator.get_file_checksum') # Mock rationale: Avoid actual file I/O for checksum calculation, ensuring determinism and speed.
    @patch('builtins.open', new_callable=mock_open) # Mock rationale: Avoid actual file system write for output, capturing content in memory.
    @patch('src.manifest_generator.datetime') # Mock rationale: Ensure deterministic timestamps for manifest creation and file modification dates.
    @patch('builtins.print') # Mock rationale: Suppress print statements during tests to avoid polluting test output.
    def test_recursive_manifest_generation(self, mock_print, mock_datetime, mock_open_func, mock_checksum, mock_stat, mock_walk, mock_abspath, mock_isdir):
        mock_isdir.return_value = True
        mock_abspath.return_value = self.test_dir
        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp.side_effect = self._mock_fromtimestamp_side_effect

        # Mock os.walk for recursive structure
        mock_walk.return_value = [
            (self.test_dir, ['subdir'], ['root_file.txt']),
            (os.path.join(self.test_dir, 'subdir'), [], ['sub_file.md'])
        ]

        mock_stat.side_effect = [
            MagicMock(st_size=50, st_mtime=datetime(2023, 2, 1, 10, 0, 0).timestamp()),  # root_file.txt
            MagicMock(st_size=150, st_mtime=datetime(2023, 2, 2, 11, 0, 0).timestamp()) # sub_file.md
        ]
        mock_checksum.side_effect = ['checksum_root', 'checksum_sub']

        generate_manifest(self.test_dir, output_filename=self.output_file, recursive=True)

        written_content = mock_open_func().write.call_args[0][0]
        manifest_data = json.loads(written_content)

        self.assertEqual(len(manifest_data['files']), 2)
        self.assertEqual(manifest_data['files'][0]['path'], 'root_file.txt')
        self.assertEqual(manifest_data['files'][1]['path'], os.path.join('subdir', 'sub_file.md'))

    @patch('os.path.isdir')
    @patch('os.path.abspath')
    @patch('os.walk')
    @patch('os.stat')
    @patch('src.manifest_generator.get_file_checksum') # Mock rationale: Avoid actual file I/O for checksum calculation, ensuring determinism and speed.
    @patch('builtins.open', new_callable=mock_open) # Mock rationale: Avoid actual file system write for output, capturing content in memory.
    @patch('src.manifest_generator.datetime') # Mock rationale: Ensure deterministic timestamps for manifest creation and file modification dates.
    @patch('builtins.print') # Mock rationale: Suppress print statements during tests to avoid polluting test output.
    def test_exclude_patterns(self, mock_print, mock_datetime, mock_open_func, mock_checksum, mock_stat, mock_walk, mock_abspath, mock_isdir):
        mock_isdir.return_value = True
        mock_abspath.return_value = self.test_dir
        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp.side_effect = self._mock_fromtimestamp_side_effect

        mock_walk.return_value = [
            (self.test_dir, ['temp_dir', 'data'], ['file.txt', 'log.log']),
            (os.path.join(self.test_dir, 'temp_dir'), [], ['temp_file.tmp']),
            (os.path.join(self.test_dir, 'data'), [], ['important.json'])
        ]

        mock_stat.side_effect = [
            MagicMock(st_size=10, st_mtime=datetime(2023, 3, 1, 9, 0, 0).timestamp()), # file.txt
            MagicMock(st_size=20, st_mtime=datetime(2023, 3, 2, 9, 0, 0).timestamp()), # important.json
        ]
        mock_checksum.side_effect = ['checksum_txt', 'checksum_json']

        # Exclude log files and the entire temp_dir
        generate_manifest(self.test_dir, output_filename=self.output_file, recursive=True, exclude_patterns=['*.log', 'temp_dir/*'])

        written_content = mock_open_func().write.call_args[0][0]
        manifest_data = json.loads(written_content)

        self.assertEqual(len(manifest_data['files']), 2)
        self.assertEqual(manifest_data['files'][0]['path'], 'file.txt')
        self.assertEqual(manifest_data['files'][1]['path'], os.path.join('data', 'important.json'))

    @patch('os.path.isdir')
    @patch('os.path.abspath')
    @patch('os.walk')
    @patch('os.stat')
    @patch('src.manifest_generator.get_file_checksum') # Mock rationale: Avoid actual file I/O for checksum calculation, ensuring determinism and speed.
    @patch('builtins.open', new_callable=mock_open) # Mock rationale: Avoid actual file system write for output, capturing content in memory.
    @patch('src.manifest_generator.datetime') # Mock rationale: Ensure deterministic timestamps for manifest creation and file modification dates.
    @patch('builtins.print') # Mock rationale: Suppress print statements during tests to avoid polluting test output.
    def test_directory_not_found(self, mock_print, mock_datetime, mock_open_func, mock_checksum, mock_stat, mock_walk, mock_abspath, mock_isdir):
        mock_isdir.return_value = False # Simulate directory not existing

        with self.assertRaises(FileNotFoundError):
            generate_manifest('/nonexistent/dir')

    @patch('builtins.open', new_callable=mock_open) # Mock rationale: Avoid actual file I/O for checksum calculation, ensuring determinism and speed.
    def test_get_file_checksum(self, mock_open_func):
        mock_file_content = b'test content for checksum'
        mock_open_func.return_value.__enter__.return_value.read.side_effect = [mock_file_content, b'']

        expected_checksum = hashlib.sha256(mock_file_content).hexdigest()
        actual_checksum = get_file_checksum('/mock/file.txt')

        self.assertEqual(actual_checksum, expected_checksum)
        mock_open_func.assert_called_once_with('/mock/file.txt', 'rb')

    @patch('os.path.isdir')
    @patch('os.path.abspath')
    @patch('os.walk')
    @patch('os.stat')
    @patch('src.manifest_generator.get_file_checksum') # Mock rationale: Avoid actual file I/O for checksum calculation, ensuring determinism and speed.
    @patch('builtins.open', new_callable=mock_open) # Mock rationale: Avoid actual file system write for output, capturing content in memory.
    @patch('src.manifest_generator.datetime') # Mock rationale: Ensure deterministic timestamps for manifest creation and file modification dates.
    @patch('builtins.print') # Mock rationale: Suppress print statements during tests to avoid polluting test output.
    def test_os_error_during_stat(self, mock_print, mock_datetime, mock_open_func, mock_checksum, mock_stat, mock_walk, mock_abspath, mock_isdir):
        mock_isdir.return_value = True
        mock_abspath.return_value = self.test_dir
        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp.side_effect = self._mock_fromtimestamp_side_effect

        mock_walk.return_value = [
            (self.test_dir, [], ['file1.txt', 'unreadable.txt'])
        ]

        # Simulate OSError for 'unreadable.txt'
        mock_stat.side_effect = [
            MagicMock(st_size=100, st_mtime=datetime(2023, 1, 1, 12, 0, 0).timestamp()), # file1.txt
            OSError("Permission denied") # unreadable.txt
        ]

        mock_checksum.side_effect = ['checksum1'] # Only for file1.txt

        generate_manifest(self.test_dir, output_filename=self.output_file)

        written_content = mock_open_func().write.call_args[0][0]
        manifest_data = json.loads(written_content)

        self.assertEqual(len(manifest_data['files']), 1) # Only file1.txt should be in the manifest
        self.assertEqual(manifest_data['files'][0]['path'], 'file1.txt')
        mock_print.assert_called_with(f"Warning: Could not process file {os.path.join(self.test_dir, 'unreadable.txt')}: Permission denied")

    @patch('os.path.isdir')
    @patch('os.path.abspath')
    @patch('os.walk')
    @patch('os.stat')
    @patch('src.manifest_generator.get_file_checksum') # Mock rationale: Avoid actual file I/O for checksum calculation, ensuring determinism and speed.
    @patch('builtins.open', new_callable=mock_open) # Mock rationale: Avoid actual file system write for output, capturing content in memory.
    @patch('src.manifest_generator.datetime') # Mock rationale: Ensure deterministic timestamps for manifest creation and file modification dates.
    @patch('builtins.print') # Mock rationale: Suppress print statements during tests to avoid polluting test output.
    def test_os_error_during_checksum(self, mock_print, mock_datetime, mock_open_func, mock_checksum, mock_stat, mock_walk, mock_abspath, mock_isdir):
        mock_isdir.return_value = True
        mock_abspath.return_value = self.test_dir
        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp.side_effect = self._mock_fromtimestamp_side_effect

        mock_walk.return_value = [
            (self.test_dir, [], ['file1.txt', 'checksum_fail.txt'])
        ]

        mock_stat.side_effect = [
            MagicMock(st_size=100, st_mtime=datetime(2023, 1, 1, 12, 0, 0).timestamp()), # file1.txt
            MagicMock(st_size=50, st_mtime=datetime(2023, 1, 2, 13, 0, 0).timestamp())  # checksum_fail.txt
        ]

        # Simulate OSError during checksum calculation for 'checksum_fail.txt'
        mock_checksum.side_effect = ['checksum1', OSError("Checksum read error")]

        generate_manifest(self.test_dir, output_filename=self.output_file)

        written_content = mock_open_func().write.call_args[0][0]
        manifest_data = json.loads(written_content)

        self.assertEqual(len(manifest_data['files']), 1) # Only file1.txt should be in the manifest
        self.assertEqual(manifest_data['files'][0]['path'], 'file1.txt')
        mock_print.assert_called_with(f"Warning: Could not process file {os.path.join(self.test_dir, 'checksum_fail.txt')}: Failed to read file for checksum: {os.path.join(self.test_dir, 'checksum_fail.txt')} - Checksum read error")


if __name__ == '__main__':
    unittest.main()
