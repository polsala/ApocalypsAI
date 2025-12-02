import unittest
from unittest.mock import patch, MagicMock, call
import os
import sys
import io

# Import the main script to be tested
from src import dust_collector

class TestDustCollector(unittest.TestCase):

    def setUp(self):
        # Reset mocks before each test
        self.mock_os_walk = patch('os.walk').start()
        self.mock_os_path_getsize = patch('os.path.getsize').start()
        self.mock_os_path_isdir = patch('os.path.isdir').start()
        self.mock_os_path_exists = patch('os.path.exists').start()
        self.mock_os_makedirs = patch('os.makedirs').start()
        self.mock_os_rename = patch('os.rename').start()
        self.mock_os_path_relpath = patch('os.path.relpath').start()
        self.mock_os_path_dirname = patch('os.path.dirname').start()
        self.mock_print = patch('builtins.print').start()

        # Capture stdout for testing print statements
        self.held_stdout = io.StringIO()
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stdout # Also capture stderr

    def tearDown(self):
        patch.stopall()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def _setup_mock_filesystem(self, root_dir, files_with_sizes, quarantine_dir=None):
        # Mock rationale: Simulate file system structure and file sizes for deterministic testing.
        # This avoids actual disk I/O.

        # Setup os.walk to return a predefined directory structure
        walk_data = []
        dirs = set()
        for f_path in files_with_sizes.keys():
            d = os.path.dirname(f_path)
            dirs.add(d)
        
        # Create a mock for os.walk that yields (dirpath, dirnames, filenames)
        # For simplicity, we'll just list all files under root_dir directly for walk_data
        # In a real scenario, you'd parse paths to build a proper walk structure.
        # Here, we assume all files are directly under root_dir or its immediate subdirs for walk.
        
        # Example: root_dir/file1, root_dir/subdir/file2
        # os.walk(root_dir) -> ('root_dir', ['subdir'], ['file1'])
        # os.walk(root_dir/subdir) -> ('root_dir/subdir', [], ['file2'])

        # Let's simplify os.walk for this test to just return the root and all files.
        # More complex walk mocking would involve parsing paths and grouping.
        all_files = [os.path.basename(f) for f in files_with_sizes.keys() if os.path.dirname(f) == root_dir]
        subdirs = [os.path.basename(d) for d in dirs if os.path.dirname(d) == root_dir]
        walk_data.append((root_dir, list(subdirs), all_files))

        for d in subdirs:
            subdir_path = os.path.join(root_dir, d)
            subdir_files = [os.path.basename(f) for f in files_with_sizes.keys() if os.path.dirname(f) == subdir_path]
            walk_data.append((subdir_path, [], subdir_files))

        self.mock_os_walk.return_value = walk_data

        # Setup os.path.getsize for each file
        def getsize_side_effect(path):
            return files_with_sizes.get(path, 0)
        self.mock_os_path_getsize.side_effect = getsize_side_effect

        # Setup os.path.isdir and os.path.exists
        all_paths = set(files_with_sizes.keys())
        all_paths.add(root_dir)
        for f_path in files_with_sizes.keys():
            d = os.path.dirname(f_path)
            while d and d != root_dir and d not in all_paths:
                all_paths.add(d)
                d = os.path.dirname(d)
        
        if quarantine_dir:
            all_paths.add(quarantine_dir)
            q_parent = os.path.dirname(quarantine_dir)
            while q_parent and q_parent not in all_paths:
                all_paths.add(q_parent)
                q_parent = os.path.dirname(q_parent)

        self.mock_os_path_isdir.side_effect = lambda p: p in all_paths and p != root_dir + '/file1.txt' # Example non-dir
        self.mock_os_path_exists.side_effect = lambda p: p in all_paths

        # Mock os.path.relpath to return predictable relative paths
        def relpath_side_effect(path, start):
            if path.startswith(start):
                return path[len(start):].lstrip(os.sep)
            return path # Fallback
        self.mock_os_path_relpath.side_effect = relpath_side_effect

        # Mock os.path.dirname for quarantine path construction
        self.mock_os_path_dirname.side_effect = os.path.dirname # Use real dirname for path construction


    def test_list_cosmic_dust(self):
        root = '/test_project'
        files = {
            os.path.join(root, 'small_file.txt'): 50,
            os.path.join(root, 'empty_file.log'): 0,
            os.path.join(root, 'large_file.py'): 2000,
            os.path.join(root, 'subdir', 'tiny.tmp'): 10,
            os.path.join(root, 'subdir', 'medium.md'): 500
        }
        self._setup_mock_filesystem(root, files)
        self.mock_os_path_isdir.return_value = True # Mock rationale: Ensure root_dir is seen as a directory.
        self.mock_os_path_exists.return_value = True # Mock rationale: Ensure root_dir is seen as existing.

        threshold = 100
        result = dust_collector.collect_dust(root, threshold, 'list')

        expected_dust = [
            os.path.join(root, 'small_file.txt'),
            os.path.join(root, 'empty_file.log'),
            os.path.join(root, 'subdir', 'tiny.tmp')
        ]
        self.assertCountEqual(result, expected_dust)
        output = self.held_stdout.getvalue()
        self.assertIn("Scanning '/test_project' for cosmic dust (files <= 100 bytes)...".replace("'", "'"), output)
        self.assertIn("Found 3 pieces of cosmic dust.", output)
        self.assertIn(f"- {os.path.join(root, 'small_file.txt')} (50 bytes)", output)
        self.assertIn(f"- {os.path.join(root, 'empty_file.log')} (0 bytes)", output)
        self.assertIn(f"- {os.path.join(root, 'subdir', 'tiny.tmp')} (10 bytes)", output)
        self.mock_os_rename.assert_not_called() # Mock rationale: 'list' action should not move files.

    def test_quarantine_cosmic_dust(self):
        root = '/test_project'
        quarantine_dir = '/quarantine_zone'
        files = {
            os.path.join(root, 'small_file.txt'): 50,
            os.path.join(root, 'empty_file.log'): 0,
            os.path.join(root, 'large_file.py'): 2000,
            os.path.join(root, 'subdir', 'tiny.tmp'): 10,
            os.path.join(root, 'subdir', 'medium.md'): 500
        }
        self._setup_mock_filesystem(root, files, quarantine_dir)
        self.mock_os_path_isdir.return_value = True # Mock rationale: Ensure root_dir is seen as a directory.
        self.mock_os_path_exists.side_effect = lambda p: p in files or p == root or p == quarantine_dir or p == os.path.join(root, 'subdir') # Mock rationale: Simulate existence of paths.

        threshold = 100
        result = dust_collector.collect_dust(root, threshold, 'quarantine', quarantine_dir)

        expected_dust = [
            os.path.join(root, 'small_file.txt'),
            os.path.join(root, 'empty_file.log'),
            os.path.join(root, 'subdir', 'tiny.tmp')
        ]
        self.assertCountEqual(result, expected_dust)

        # Check if quarantine directory was created if it didn't exist
        self.mock_os_makedirs.assert_any_call(quarantine_dir) # Mock rationale: Verify quarantine dir creation.

        # Check if files were moved correctly, preserving relative paths
        self.mock_os_rename.assert_has_calls([
            call(os.path.join(root, 'small_file.txt'), os.path.join(quarantine_dir, 'small_file.txt')),
            call(os.path.join(root, 'empty_file.log'), os.path.join(quarantine_dir, 'empty_file.log')),
            call(os.path.join(root, 'subdir', 'tiny.tmp'), os.path.join(quarantine_dir, 'subdir', 'tiny.tmp'))
        ], any_order=True)

        output = self.held_stdout.getvalue()
        self.assertIn("Moving cosmic dust to quarantine at '/quarantine_zone'...".replace("'", "'"), output)
        self.assertIn(f"Quarantined: '{os.path.join(root, 'small_file.txt')}' -> '{os.path.join(quarantine_dir, 'small_file.txt')}'", output)

    def test_no_dust_found(self):
        root = '/test_project'
        files = {
            os.path.join(root, 'large_file.py'): 2000,
            os.path.join(root, 'another_large.txt'): 1500
        }
        self._setup_mock_filesystem(root, files)
        self.mock_os_path_isdir.return_value = True # Mock rationale: Ensure root_dir is seen as a directory.
        self.mock_os_path_exists.return_value = True # Mock rationale: Ensure root_dir is seen as existing.

        threshold = 100
        result = dust_collector.collect_dust(root, threshold, 'list')

        self.assertEqual(result, [])
        output = self.held_stdout.getvalue()
        self.assertIn("No cosmic dust found. Your space is sparkling clean! ✨", output)
        self.mock_os_rename.assert_not_called() # Mock rationale: No dust, no move operations.

    def test_root_dir_does_not_exist(self):
        root = '/non_existent_project'
        self.mock_os_path_isdir.return_value = False # Mock rationale: Simulate non-existent directory.
        self.mock_os_path_exists.return_value = False # Mock rationale: Simulate non-existent directory.

        result = dust_collector.collect_dust(root, 100, 'list')

        self.assertEqual(result, [])
        output = self.held_stdout.getvalue()
        self.assertIn(f"Error: Root directory '{root}' does not exist or is not a directory.", output)
        self.mock_os_walk.assert_not_called() # Mock rationale: Should not attempt to walk a non-existent directory.

    def test_quarantine_action_without_quarantine_dir(self):
        root = '/test_project'
        files = {os.path.join(root, 'small.txt'): 10}
        self._setup_mock_filesystem(root, files)
        self.mock_os_path_isdir.return_value = True # Mock rationale: Ensure root_dir is seen as a directory.
        self.mock_os_path_exists.return_value = True # Mock rationale: Ensure root_dir is seen as existing.

        result = dust_collector.collect_dust(root, 100, 'quarantine') # Missing quarantine_dir

        self.assertEqual(result, [])
        output = self.held_stdout.getvalue()
        self.assertIn("Error: --quarantine-dir is required when action is 'quarantine'.", output)
        self.mock_os_rename.assert_not_called() # Mock rationale: Should not attempt to move files without a destination.

    def test_main_function_list_action(self):
        # Mock rationale: Test the CLI entry point with mocked argparse and core logic.
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args,
             patch('src.dust_collector.collect_dust') as mock_collect_dust:
            mock_parse_args.return_value = MagicMock(
                path='/mock_path',
                threshold=50,
                action='list',
                quarantine_dir=None
            )
            dust_collector.main()
            mock_collect_dust.assert_called_once_with('/mock_path', 50, 'list', None)

    def test_main_function_quarantine_action(self):
        # Mock rationale: Test the CLI entry point with mocked argparse and core logic.
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args,
             patch('src.dust_collector.collect_dust') as mock_collect_dust:
            mock_parse_args.return_value = MagicMock(
                path='/mock_path',
                threshold=50,
                action='quarantine',
                quarantine_dir='/mock_quarantine'
            )
            dust_collector.main()
            mock_collect_dust.assert_called_once_with('/mock_path', 50, 'quarantine', '/mock_quarantine')

    def test_main_function_quarantine_action_missing_dir_error(self):
        # Mock rationale: Test the CLI entry point's error handling for missing quarantine_dir.
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args,
             patch('argparse.ArgumentParser.error') as mock_error,
             patch('src.dust_collector.collect_dust') as mock_collect_dust:
            mock_parse_args.return_value = MagicMock(
                path='/mock_path',
                threshold=50,
                action='quarantine',
                quarantine_dir=None
            )
            dust_collector.main()
            mock_error.assert_called_once_with("argument --quarantine-dir is required when --action is 'quarantine'")
            mock_collect_dust.assert_not_called()

    def test_quarantine_dir_creation_failure(self):
        root = '/test_project'
        quarantine_dir = '/quarantine_zone'
        files = {os.path.join(root, 'small.txt'): 10}
        self._setup_mock_filesystem(root, files, quarantine_dir)
        self.mock_os_path_isdir.return_value = True # Mock rationale: Ensure root_dir is seen as a directory.
        self.mock_os_path_exists.side_effect = lambda p: p == root # Mock rationale: Simulate quarantine_dir not existing initially.
        self.mock_os_makedirs.side_effect = OSError("Permission denied") # Mock rationale: Simulate a failure to create the directory.

        result = dust_collector.collect_dust(root, 100, 'quarantine', quarantine_dir)

        self.assertEqual(result, [])
        output = self.held_stdout.getvalue()
        self.assertIn(f"Error: Could not create quarantine directory '{quarantine_dir}': Permission denied", output)
        self.mock_os_rename.assert_not_called() # Mock rationale: No files should be moved if quarantine dir cannot be created.

    def test_file_access_error(self):
        root = '/test_project'
        files = {
            os.path.join(root, 'accessible.txt'): 10,
            os.path.join(root, 'inaccessible.txt'): 5
        }
        self._setup_mock_filesystem(root, files)
        self.mock_os_path_isdir.return_value = True # Mock rationale: Ensure root_dir is seen as a directory.
        self.mock_os_path_exists.return_value = True # Mock rationale: Ensure root_dir is seen as existing.

        def getsize_side_effect(path):
            if path == os.path.join(root, 'inaccessible.txt'):
                raise OSError("Permission denied") # Mock rationale: Simulate a file that cannot be accessed.
            return files.get(path, 0)
        self.mock_os_path_getsize.side_effect = getsize_side_effect

        result = dust_collector.collect_dust(root, 100, 'list')

        expected_dust = [os.path.join(root, 'accessible.txt')]
        self.assertCountEqual(result, expected_dust)
        output = self.held_stdout.getvalue()
        self.assertIn(f"Warning: Could not access '{os.path.join(root, 'inaccessible.txt')}': Permission denied", output)
        self.assertIn("Found 1 pieces of cosmic dust.", output)

    def test_quarantine_subdir_creation(self):
        root = '/test_project'
        quarantine_dir = '/quarantine_zone'
        files = {
            os.path.join(root, 'subdir1', 'small.txt'): 10,
            os.path.join(root, 'subdir2', 'nested', 'tiny.log'): 5
        }
        self._setup_mock_filesystem(root, files, quarantine_dir)
        self.mock_os_path_isdir.return_value = True # Mock rationale: Ensure root_dir is seen as a directory.
        self.mock_os_path_exists.side_effect = lambda p: p in [root, quarantine_dir, os.path.join(root, 'subdir1'), os.path.join(root, 'subdir2'), os.path.join(root, 'subdir2', 'nested')] # Mock rationale: Simulate existence of paths.

        threshold = 100
        dust_collector.collect_dust(root, threshold, 'quarantine', quarantine_dir)

        # Check if subdirectories were created within quarantine_dir
        self.mock_os_makedirs.assert_any_call(os.path.join(quarantine_dir, 'subdir1')) # Mock rationale: Verify subdir creation.
        self.mock_os_makedirs.assert_any_call(os.path.join(quarantine_dir, 'subdir2', 'nested')) # Mock rationale: Verify nested subdir creation.

        # Check if files were moved correctly, preserving relative paths
        self.mock_os_rename.assert_has_calls([
            call(os.path.join(root, 'subdir1', 'small.txt'), os.path.join(quarantine_dir, 'subdir1', 'small.txt')),
            call(os.path.join(root, 'subdir2', 'nested', 'tiny.log'), os.path.join(quarantine_dir, 'subdir2', 'nested', 'tiny.log'))
        ], any_order=True)

if __name__ == '__main__':
    unittest.main()
