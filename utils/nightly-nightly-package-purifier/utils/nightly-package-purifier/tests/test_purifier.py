import unittest
from unittest.mock import patch, MagicMock, call
import os
import sys
from io import StringIO

# Assuming purifier.py is in src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from purifier import find_artifacts, clean_artifacts, main, COMMON_ARTIFACT_PATTERNS, get_path_size

class TestPurifier(unittest.TestCase):

    def setUp(self):
        # Capture stdout/stderr for testing CLI output
        self.held_stdout = sys.stdout
        self.held_stderr = sys.stderr
        self.new_stdout = StringIO()
        self.new_stderr = StringIO()
        sys.stdout = self.new_stdout
        sys.stderr = self.new_stderr

    def tearDown(self):
        # Restore stdout/stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    @patch('os.walk')
    def test_find_artifacts_basic(self, mock_os_walk):
        # Mock rationale: os.walk is a file system interaction. Mocking it allows
        # us to simulate different directory structures without actual disk I/O.
        mock_os_walk.return_value = [
            ('/project', ['src', 'node_modules', '__pycache__'], ['main.py', 'package.json']),
            ('/project/src', [], ['app.py']),
            ('/project/node_modules', ['some_lib'], ['index.js']),
            ('/project/__pycache__', [], ['app.cpython-39.pyc']),
        ]
        
        found = find_artifacts('/project')
        expected = [
            '/project/node_modules',
            '/project/__pycache__',
        ]
        self.assertCountEqual(found, expected)

    @patch('os.walk')
    def test_find_artifacts_nested(self, mock_os_walk):
        # Mock rationale: Simulating nested structures to ensure recursive scanning works.
        mock_os_walk.return_value = [
            ('/project', ['sub_project', 'build'], []),
            ('/project/sub_project', ['target', 'venv'], []),
            ('/project/sub_project/target', [], ['lib.so']),
            ('/project/sub_project/venv', ['bin'], []),
            ('/project/build', [], ['app.exe']),
        ]
        
        found = find_artifacts('/project')
        expected = [
            '/project/build',
            '/project/sub_project/target',
            '/project/sub_project/venv',
        ]
        self.assertCountEqual(found, expected)

    @patch('os.walk')
    def test_find_artifacts_no_match(self, mock_os_walk):
        # Mock rationale: Testing the scenario where no artifacts are found.
        mock_os_walk.return_value = [
            ('/project', ['src', 'docs'], ['main.py', 'README.md']),
            ('/project/src', [], ['app.py']),
        ]
        
        found = find_artifacts('/project')
        self.assertEqual(found, [])

    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('os.walk') # For directory size calculation
    def test_get_path_size_file(self, mock_os_walk, mock_os_getsize, mock_os_isfile, mock_os_path_exists):
        # Mock rationale: get_path_size interacts with the file system. Mocking allows
        # us to control reported sizes and file types without actual disk I/O.
        mock_os_path_exists.return_value = True
        mock_os_isfile.return_value = True
        mock_os_getsize.return_value = 1024
        mock_os_walk.return_value = [] # Should not be called for a file

        size = get_path_size('/path/to/file.txt')
        self.assertEqual(size, 1024)
        mock_os_getsize.assert_called_once_with('/path/to/file.txt')
        mock_os_walk.assert_not_called()

    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('os.walk') # For directory size calculation
    def test_get_path_size_directory(self, mock_os_walk, mock_os_getsize, mock_os_isfile, mock_os_path_exists):
        # Mock rationale: get_path_size interacts with the file system. Mocking allows
        # us to control reported sizes and file types without actual disk I/O.
        mock_os_path_exists.return_value = True
        mock_os_isfile.return_value = False # It's a directory
        mock_os_walk.return_value = [
            ('/path/to/dir', [], ['file1.txt', 'file2.log']),
            ('/path/to/dir/subdir', [], ['file3.dat']),
        ]
        mock_os_getsize.side_effect = {
            '/path/to/dir/file1.txt': 100,
            '/path/to/dir/file2.log': 200,
            '/path/to/dir/subdir/file3.dat': 300,
        }.get

        size = get_path_size('/path/to/dir')
        self.assertEqual(size, 600) # 100 + 200 + 300
        self.assertEqual(mock_os_getsize.call_count, 3)
        mock_os_walk.assert_called_once_with('/path/to/dir')

    @patch('purifier.get_path_size')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    @patch('shutil.rmtree')
    @patch('os.remove')
    def test_clean_artifacts_dry_run(self, mock_os_remove, mock_shutil_rmtree, mock_os_isfile, mock_os_isdir, mock_os_path_exists, mock_get_path_size):
        # Mock rationale: These are all file system operations. Mocking them prevents
        # actual file deletion and allows control over file/directory existence and size.
        mock_os_path_exists.side_effect = lambda p: p in ['/project/node_modules', '/project/__pycache__', '/project/file.txt']
        mock_os_isdir.side_effect = lambda p: p in ['/project/node_modules', '/project/__pycache__']
        mock_os_isfile.side_effect = lambda p: p in ['/project/file.txt']
        
        # Mock get_path_size to return specific sizes for paths
        mock_get_path_size.side_effect = {
            '/project/node_modules': 1750000, # 1.75 MB
            '/project/__pycache__': 250000,  # 0.25 MB
            '/project/file.txt': 100000,     # 0.10 MB
        }.get

        paths = ['/project/node_modules', '/project/__pycache__', '/project/file.txt']
        clean_artifacts(paths, dry_run=True)

        mock_shutil_rmtree.assert_not_called()
        mock_os_remove.assert_not_called()
        
        output = self.new_stdout.getvalue()
        self.assertIn("[DRY RUN] Would remove directory: /project/node_modules (1.75 MB)", output)
        self.assertIn("[DRY RUN] Would remove directory: /project/__pycache__ (0.25 MB)", output)
        self.assertIn("[DRY RUN] Would remove file: /project/file.txt (0.10 MB)", output)
        self.assertIn("[DRY RUN] Would clean 3 items, freeing up 2.10 MB.", output)

    @patch('purifier.get_path_size')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    @patch('shutil.rmtree')
    @patch('os.remove')
    def test_clean_artifacts_actual_clean(self, mock_os_remove, mock_shutil_rmtree, mock_os_isfile, mock_os_isdir, mock_os_path_exists, mock_get_path_size):
        # Mock rationale: Similar to dry_run, but verifying actual removal calls.
        mock_os_path_exists.side_effect = lambda p: p in ['/project/node_modules', '/project/__pycache__', '/project/file.txt']
        mock_os_isdir.side_effect = lambda p: p in ['/project/node_modules', '/project/__pycache__']
        mock_os_isfile.side_effect = lambda p: p in ['/project/file.txt']

        mock_get_path_size.side_effect = {
            '/project/node_modules': 1024, # 1KB
            '/project/__pycache__': 512,  # 0.5KB
            '/project/file.txt': 256,     # 0.25KB
        }.get

        paths = ['/project/node_modules', '/project/__pycache__', '/project/file.txt']
        clean_artifacts(paths, dry_run=False)

        mock_shutil_rmtree.assert_has_calls([
            call('/project/node_modules'),
            call('/project/__pycache__')
        ], any_order=True)
        mock_os_remove.assert_called_once_with('/project/file.txt')
        
        output = self.new_stdout.getvalue()
        self.assertIn("Removing directory: /project/node_modules (0.00 MB)", output) # Size will be small for mock
        self.assertIn("Removing directory: /project/__pycache__ (0.00 MB)", output)
        self.assertIn("Removing file: /project/file.txt (0.00 MB)", output)
        self.assertIn("Cleaned 3 items, freeing up 0.00 MB.", output) # Total size will be small

    @patch('purifier.get_path_size')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    @patch('shutil.rmtree')
    @patch('os.remove')
    def test_clean_artifacts_non_existent_path(self, mock_os_remove, mock_shutil_rmtree, mock_os_isfile, mock_os_isdir, mock_os_path_exists, mock_get_path_size):
        # Mock rationale: Ensure the utility handles paths that might disappear between finding and cleaning.
        mock_os_path_exists.side_effect = lambda p: p == '/project/existent'
        mock_os_isdir.return_value = True
        mock_get_path_size.return_value = 1000

        paths = ['/project/existent', '/project/non_existent']
        clean_artifacts(paths, dry_run=False)

        mock_shutil_rmtree.assert_called_once_with('/project/existent')
        self.assertIn("Skipping non-existent path: /project/non_existent", self.new_stdout.getvalue())
        self.assertIn("Cleaned 1 items, freeing up 0.00 MB.", self.new_stdout.getvalue())

    @patch('sys.argv', ['purifier.py', '.', '--list'])
    @patch('purifier.find_artifacts')
    @patch('purifier.clean_artifacts')
    def test_main_list_mode(self, mock_clean_artifacts, mock_find_artifacts):
        # Mock rationale: Testing the CLI entry point. Mocking internal functions
        # prevents actual file system access and allows verification of argument passing.
        mock_find_artifacts.return_value = ['/project/node_modules', '/project/__pycache__']
        
        main()
        
        mock_find_artifacts.assert_called_once_with('.', COMMON_ARTIFACT_PATTERNS)
        mock_clean_artifacts.assert_called_once_with(['/project/node_modules', '/project/__pycache__'], dry_run=True)
        output = self.new_stdout.getvalue()
        self.assertIn("Scanning", output)
        self.assertIn("/project/node_modules", output)
        self.assertIn("/project/__pycache__", output)
        self.assertIn("Dry run complete. Use --clean to remove these items.", output)

    @patch('sys.argv', ['purifier.py', '/my/path', '--clean'])
    @patch('purifier.find_artifacts')
    @patch('purifier.clean_artifacts')
    def test_main_clean_mode(self, mock_clean_artifacts, mock_find_artifacts):
        # Mock rationale: Testing the CLI entry point for clean mode.
        mock_find_artifacts.return_value = ['/my/path/target']
        
        main()
        
        mock_find_artifacts.assert_called_once_with('/my/path', COMMON_ARTIFACT_PATTERNS)
        mock_clean_artifacts.assert_called_once_with(['/my/path/target'], dry_run=False)
        output = self.new_stdout.getvalue()
        self.assertIn("Initiating cleanup...", output)

    @patch('sys.argv', ['purifier.py', '--patterns', 'custom_cache', 'temp_files', '--list'])
    @patch('purifier.find_artifacts')
    @patch('purifier.clean_artifacts')
    def test_main_custom_patterns(self, mock_clean_artifacts, mock_find_artifacts):
        # Mock rationale: Verifying that custom patterns are correctly passed.
        mock_find_artifacts.return_value = ['/project/custom_cache']
        
        main()
        
        mock_find_artifacts.assert_called_once_with('.', ['custom_cache', 'temp_files'])
        mock_clean_artifacts.assert_called_once_with(['/project/custom_cache'], dry_run=True)
        output = self.new_stdout.getvalue()
        self.assertIn("custom_cache, temp_files", output)

    @patch('sys.argv', ['purifier.py', '.'])
    def test_main_no_action_exits_with_error(self):
        # Mock rationale: Testing error handling for missing --list or --clean.
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Please specify either --list to see what would be cleaned, or --clean to actually remove items.", self.new_stderr.getvalue())

    @patch('sys.argv', ['purifier.py', '--list'])
    @patch('purifier.find_artifacts')
    @patch('purifier.clean_artifacts')
    def test_main_no_artifacts_found(self, mock_clean_artifacts, mock_find_artifacts):
        # Mock rationale: Testing the scenario where find_artifacts returns an empty list.
        mock_find_artifacts.return_value = []
        
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0) # Exit 0 for no-op
        self.assertIn("No artifacts found matching the patterns.", self.new_stdout.getvalue())
        mock_clean_artifacts.assert_not_called()
