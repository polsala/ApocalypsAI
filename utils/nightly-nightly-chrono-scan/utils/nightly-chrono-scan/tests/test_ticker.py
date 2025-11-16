import unittest
import os
import json
import tempfile
import shutil
from unittest.mock import patch, mock_open, MagicMock

# Import the functions to be tested
from src.ticker import scan_directory, load_state, save_state, compare_snapshots, main

class TestChronoScan(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing file operations
        self.test_dir = tempfile.mkdtemp()
        self.state_file = os.path.join(self.test_dir, 'test_state.json')

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    @patch('os.walk')
    @patch('os.stat')
    def test_scan_directory(self, mock_stat, mock_walk):
        # Mock rationale: os.walk is a generator that traverses the filesystem.
        # We mock it to provide a controlled set of files and directories without
        # actually touching the disk, ensuring deterministic tests.
        # os.stat is mocked to return a consistent modification time for files.
        
        # Setup mock_walk to simulate a directory structure
        mock_walk.return_value = [
            ('/mock/path', ('subdir',), ('file1.txt', 'file2.log')),
            ('/mock/path/subdir', (), ('subfile.py',))
        ]

        # Setup mock_stat to return a consistent mtime for all files
        mock_stat_result = MagicMock()
        mock_stat_result.st_mtime = 1678886400.0 # A fixed timestamp
        mock_stat.return_value = mock_stat_result

        expected_snapshot = {
            '/mock/path/file1.txt': 1678886400.0,
            '/mock/path/file2.log': 1678886400.0,
            '/mock/path/subdir/subfile.py': 1678886400.0,
        }

        snapshot = scan_directory('/mock/path')
        self.assertEqual(snapshot, expected_snapshot)
        mock_walk.assert_called_once_with('/mock/path')
        self.assertEqual(mock_stat.call_count, 3)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('json.load')
    def test_load_state_success(self, mock_json_load, mock_exists, mock_open_file):
        # Mock rationale: builtins.open is mocked to prevent actual file I/O.
        # os.path.exists is mocked to control whether the state file is considered present.
        # json.load is mocked to provide a predefined dictionary as if read from a file.
        
        mock_json_load.return_value = {'file1.txt': 123.45}
        state = load_state('/mock/state.json')
        self.assertEqual(state, {'file1.txt': 123.45})
        mock_exists.assert_called_once_with('/mock/state.json')
        mock_open_file.assert_called_once_with('/mock/state.json', 'r')
        mock_json_load.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_load_state_file_not_found(self, mock_exists, mock_open_file):
        # Mock rationale: os.path.exists is mocked to simulate the absence of the state file.
        # builtins.open is mocked to ensure it's not called if the file doesn't exist.
        
        state = load_state('/mock/state.json')
        self.assertIsNone(state)
        mock_exists.assert_called_once_with('/mock/state.json')
        mock_open_file.assert_not_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('json.load', side_effect=json.JSONDecodeError('bad json', 'doc', 0))
    @patch('builtins.print') # To capture the warning message
    def test_load_state_invalid_json(self, mock_print, mock_json_load, mock_exists, mock_open_file):
        # Mock rationale: json.load is mocked to simulate a corrupted or invalid JSON file.
        # builtins.print is mocked to verify that a warning message is printed.
        
        state = load_state('/mock/state.json')
        self.assertIsNone(state)
        mock_print.assert_called_once()
        self.assertIn('Warning: Could not load state', mock_print.call_args[0][0])

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    @patch('json.dump')
    def test_save_state(self, mock_json_dump, mock_makedirs, mock_open_file):
        # Mock rationale: builtins.open is mocked to prevent actual file I/O.
        # os.makedirs is mocked to prevent actual directory creation.
        # json.dump is mocked to verify that the snapshot is correctly serialized.
        
        snapshot = {'file1.txt': 123.45}
        save_state('/mock/path/state.json', snapshot)
        mock_makedirs.assert_called_once_with('/mock/path', exist_ok=True)
        mock_open_file.assert_called_once_with('/mock/path/state.json', 'w')
        mock_json_dump.assert_called_once_with(snapshot, mock_open_file(), indent=4)

    def test_compare_snapshots_no_old_state(self):
        # Mock rationale: This function is pure, no mocks needed for its core logic.
        
        new_snapshot = {'file1.txt': 100.0}
        new, modified, deleted = compare_snapshots(None, new_snapshot)
        self.assertEqual(new, [])
        self.assertEqual(modified, [])
        self.assertEqual(deleted, [])

    def test_compare_snapshots_no_changes(self):
        # Mock rationale: This function is pure, no mocks needed for its core logic.
        
        old_snapshot = {'file1.txt': 100.0, 'file2.txt': 200.0}
        new_snapshot = {'file1.txt': 100.0, 'file2.txt': 200.0}
        new, modified, deleted = compare_snapshots(old_snapshot, new_snapshot)
        self.assertEqual(new, [])
        self.assertEqual(modified, [])
        self.assertEqual(deleted, [])

    def test_compare_snapshots_new_file(self):
        # Mock rationale: This function is pure, no mocks needed for its core logic.
        
        old_snapshot = {'file1.txt': 100.0}
        new_snapshot = {'file1.txt': 100.0, 'file2.txt': 200.0}
        new, modified, deleted = compare_snapshots(old_snapshot, new_snapshot)
        self.assertEqual(new, ['file2.txt'])
        self.assertEqual(modified, [])
        self.assertEqual(deleted, [])

    def test_compare_snapshots_modified_file(self):
        # Mock rationale: This function is pure, no mocks needed for its core logic.
        
        old_snapshot = {'file1.txt': 100.0, 'file2.txt': 200.0}
        new_snapshot = {'file1.txt': 100.0, 'file2.txt': 201.0} # Modified mtime
        new, modified, deleted = compare_snapshots(old_snapshot, new_snapshot)
        self.assertEqual(new, [])
        self.assertEqual(modified, ['file2.txt'])
        self.assertEqual(deleted, [])

    def test_compare_snapshots_deleted_file(self):
        # Mock rationale: This function is pure, no mocks needed for its core logic.
        
        old_snapshot = {'file1.txt': 100.0, 'file2.txt': 200.0}
        new_snapshot = {'file1.txt': 100.0}
        new, modified, deleted = compare_snapshots(old_snapshot, new_snapshot)
        self.assertEqual(new, [])
        self.assertEqual(modified, [])
        self.assertEqual(deleted, ['file2.txt'])

    def test_compare_snapshots_all_changes(self):
        # Mock rationale: This function is pure, no mocks needed for its core logic.
        
        old_snapshot = {'file1.txt': 100.0, 'file2.txt': 200.0, 'file3.txt': 300.0}
        new_snapshot = {'file1.txt': 100.0, 'file2.txt': 201.0, 'file4.txt': 400.0}
        new, modified, deleted = compare_snapshots(old_snapshot, new_snapshot)
        self.assertEqual(new, ['file4.txt'])
        self.assertEqual(modified, ['file2.txt'])
        self.assertEqual(deleted, ['file3.txt'])

    @patch('src.ticker.load_state', return_value=None)
    @patch('src.ticker.scan_directory', return_value={'/test/path/fileA.txt': 100.0})
    @patch('src.ticker.save_state')
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    def test_main_first_run(self, mock_print, mock_isdir, mock_save_state, mock_scan_directory, mock_load_state):
        # Mock rationale: We mock the core functions (load_state, scan_directory, save_state)
        # to control their behavior and isolate the 'main' function's logic.
        # os.path.isdir is mocked to confirm the path exists without actual filesystem checks.
        # builtins.print is mocked to capture stdout and verify output messages.
        
        with patch('sys.argv', ['ticker.py', '--path', '/test/path', '--state-file', self.state_file]):
            main()
            mock_load_state.assert_called_once_with(self.state_file)
            mock_scan_directory.assert_called_once_with('/test/path')
            mock_save_state.assert_called_once_with(self.state_file, {'/test/path/fileA.txt': 100.0})
            mock_print.assert_any_call(f"Chrono-scan initialized for '/test/path'. State saved to '{self.state_file}'.")
            mock_print.assert_any_call("Found 1 files to track.")

    @patch('src.ticker.load_state', return_value={'/test/path/fileA.txt': 100.0})
    @patch('src.ticker.scan_directory', return_value={'/test/path/fileA.txt': 100.0})
    @patch('src.ticker.save_state')
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    def test_main_no_changes(self, mock_print, mock_isdir, mock_save_state, mock_scan_directory, mock_load_state):
        # Mock rationale: Similar to above, mocking dependencies to test 'main' in isolation.
        
        with patch('sys.argv', ['ticker.py', '--path', '/test/path', '--state-file', self.state_file]):
            main()
            mock_load_state.assert_called_once_with(self.state_file)
            mock_scan_directory.assert_called_once_with('/test/path')
            mock_save_state.assert_called_once_with(self.state_file, {'/test/path/fileA.txt': 100.0})
            mock_print.assert_called_once_with("No significant temporal tears detected.")

    @patch('src.ticker.load_state', return_value={'/test/path/fileA.txt': 100.0})
    @patch('src.ticker.scan_directory', return_value={'/test/path/fileA.txt': 101.0, '/test/path/fileB.txt': 200.0})
    @patch('src.ticker.save_state')
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    def test_main_with_changes(self, mock_print, mock_isdir, mock_save_state, mock_scan_directory, mock_load_state):
        # Mock rationale: Similar to above, mocking dependencies to test 'main' in isolation.
        
        with patch('sys.argv', ['ticker.py', '--path', '/test/path', '--state-file', self.state_file]):
            main()
            mock_load_state.assert_called_once_with(self.state_file)
            mock_scan_directory.assert_called_once_with('/test/path')
            mock_save_state.assert_called_once_with(self.state_file, {'/test/path/fileA.txt': 101.0, '/test/path/fileB.txt': 200.0})
            
            # Check for specific output messages
            mock_print.assert_any_call("Temporal tears detected in '/test/path':")
            mock_print.assert_any_call("  New Files:")
            mock_print.assert_any_call("    - /test/path/fileB.txt")
            mock_print.assert_any_call("  Modified Files:")
            mock_print.assert_any_call("    - /test/path/fileA.txt")

    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_exit, mock_print, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate an invalid directory path.
        # builtins.print is mocked to capture the error message.
        # sys.exit is mocked to prevent the test runner from exiting prematurely.
        
        with patch('sys.argv', ['ticker.py', '--path', '/nonexistent/path', '--state-file', self.state_file]):
            main()
            mock_isdir.assert_called_once_with('/nonexistent/path')
            mock_print.assert_called_once_with("Error: Directory not found at '/nonexistent/path'")
            mock_exit.assert_called_once_with(1)
