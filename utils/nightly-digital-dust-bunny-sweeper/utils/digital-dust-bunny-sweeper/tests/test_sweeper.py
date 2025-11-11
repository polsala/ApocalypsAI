import unittest
import os
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

# Import the functions from the sweeper module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from sweeper import find_dust_bunnies, is_empty_dir, is_log_or_temp_file, is_build_artifact
sys.path.pop(0)

class TestDigitalDustBunnySweeper(unittest.TestCase):

    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_is_empty_dir(self, mock_isdir, mock_listdir):
        # Mock rationale: os.path.isdir and os.listdir are file system operations that need to be controlled for deterministic testing.
        mock_isdir.return_value = True
        mock_listdir.return_value = []
        self.assertTrue(is_empty_dir('/test/empty_dir'))

        mock_listdir.return_value = ['file.txt']
        self.assertFalse(is_empty_dir('/test/non_empty_dir'))

        mock_isdir.return_value = False
        self.assertFalse(is_empty_dir('/test/not_a_dir'))

    def test_is_log_or_temp_file(self):
        self.assertTrue(is_log_or_temp_file('app.log'))
        self.assertTrue(is_log_or_temp_file('temp_data.tmp'))
        self.assertTrue(is_log_or_temp_file('backup.bak'))
        self.assertTrue(is_log_or_temp_file('file.swp'))
        self.assertTrue(is_log_or_temp_file('another.temp'))
        self.assertFalse(is_log_or_temp_file('main.py'))
        self.assertFalse(is_log_or_temp_file('document.pdf'))

    @patch('os.path.isdir')
    def test_is_build_artifact(self, mock_isdir):
        # Mock rationale: os.path.isdir is a file system operation that needs to be controlled for deterministic testing.
        # Test OS junk files
        self.assertTrue(is_build_artifact('/path/to/.DS_Store', '.DS_Store'))
        self.assertTrue(is_build_artifact('/path/to/Thumbs.db', 'Thumbs.db'))

        # Test Python build artifacts
        self.assertTrue(is_build_artifact('/path/to/__pycache__', '__pycache__'))

        # Test common build directories
        mock_isdir.return_value = True # Simulate that these paths are directories
        self.assertTrue(is_build_artifact('/path/to/build', 'build'))
        self.assertTrue(is_build_artifact('/path/to/dist', 'dist'))
        self.assertTrue(is_build_artifact('/path/to/target', 'target'))
        self.assertTrue(is_build_artifact('/path/to/.venv', '.venv'))
        self.assertTrue(is_build_artifact('/path/to/env', 'env'))

        mock_isdir.return_value = False # Simulate that these paths are files
        self.assertFalse(is_build_artifact('/path/to/my_script.py', 'my_script.py'))
        self.assertFalse(is_build_artifact('/path/to/src', 'src'))

    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.listdir')
    def test_find_dust_bunnies(self, mock_listdir, mock_isdir, mock_walk):
        # Mock rationale: os.walk, os.path.isdir, and os.listdir are core file system operations.
        # Mocking them allows us to simulate various directory structures and file types without touching the actual file system.

        # Simulate a directory structure:
        # /root
        # ├── empty_dir (empty)
        # ├── logs
        # │   └── app.log
        # ├── temp
        # │   └── data.tmp
        # ├── src
        # │   └── main.py
        # ├── build (build artifact dir)
        # │   └── temp.log (also a log file, but parent is artifact)
        # ├── .DS_Store (OS junk file)
        # └── __pycache__ (build artifact dir)

        mock_walk.return_value = [
            ('/root', ['empty_dir', 'logs', 'temp', 'src', 'build', '__pycache__'], ['.DS_Store']),
            ('/root/empty_dir', [], []),
            ('/root/logs', [], ['app.log']),
            ('/root/temp', [], ['data.tmp']),
            ('/root/src', [], ['main.py']),
            ('/root/build', [], ['temp.log']),
            ('/root/__pycache__', [], []),
        ]

        # Configure mocks for is_empty_dir, is_log_or_temp_file, is_build_artifact helpers
        # These are called internally by find_dust_bunnies, so their underlying os calls need to be mocked too.

        # Mock os.listdir for is_empty_dir checks
        def mock_listdir_side_effect(path):
            if path == '/root/empty_dir':
                return []
            return ['some_file'] # Default for non-empty
        mock_listdir.side_effect = mock_listdir_side_effect

        # Mock os.path.isdir for is_build_artifact checks
        def mock_isdir_side_effect(path):
            if path in ['/root/empty_dir', '/root/logs', '/root/temp', '/root/src', '/root/build', '/root/__pycache__']:
                return True
            return False
        mock_isdir.side_effect = mock_isdir_side_effect

        bunnies = find_dust_bunnies('/root')

        expected_bunnies = [
            ('[EMPTY DIR]', '/root/empty_dir'),
            ('[LOG/TEMP FILE]', '/root/logs/app.log'),
            ('[LOG/TEMP FILE]', '/root/temp/data.tmp'),
            ('[BUILD ARTIFACT]', '/root/.DS_Store'),
            ('[BUILD ARTIFACT DIR]', '/root/build'),
            ('[BUILD ARTIFACT DIR]', '/root/__pycache__'),
            ('[LOG/TEMP FILE]', '/root/build/temp.log') # Listed as a log file, even if parent is build artifact
        ]

        # Sort both lists for consistent comparison
        sorted_bunnies = sorted(bunnies, key=lambda x: x[1])
        sorted_expected = sorted(expected_bunnies, key=lambda x: x[1])

        self.assertEqual(len(sorted_bunnies), len(sorted_expected))
        self.assertEqual(sorted_bunnies, sorted_expected)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('os.path.isdir', return_value=True)
    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('sweeper.find_dust_bunnies') # Mock the core logic to control output
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_bunnies(self, mock_parse_args, mock_find_bunnies, mock_abspath, mock_isdir, mock_stdout):
        # Mock rationale: sys.stdout is mocked to capture printed output. os.path.isdir and os.path.abspath are mocked
        # to control file system checks. argparse.ArgumentParser.parse_args is mocked to control CLI arguments.
        # sweeper.find_dust_bunnies is mocked to control the core logic's return value for specific test scenarios.
        mock_parse_args.return_value = MagicMock(path='/test/repo')
        mock_find_bunnies.return_value = []

        from sweeper import main
        main()

        output = mock_stdout.getvalue()
        self.assertIn('Scanning /test/repo for digital dust bunnies...', output)
        self.assertIn('No digital dust bunnies found. Your repository is sparkling clean!', output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('os.path.isdir', return_value=True)
    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('sweeper.find_dust_bunnies')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_bunnies(self, mock_parse_args, mock_find_bunnies, mock_abspath, mock_isdir, mock_stdout):
        # Mock rationale: Same as above, controlling stdout, file system checks, CLI args, and core logic return.
        mock_parse_args.return_value = MagicMock(path='/test/repo')
        mock_find_bunnies.return_value = [
            ('[EMPTY DIR]', '/test/repo/empty_folder'),
            ('[LOG/TEMP FILE]', '/test/repo/logs/app.log')
        ]

        from sweeper import main
        main()

        output = mock_stdout.getvalue()
        self.assertIn('Scanning /test/repo for digital dust bunnies...', output)
        self.assertIn('Found 2 digital dust bunnies:', output)
        self.assertIn('- [EMPTY DIR] /test/repo/empty_folder', output)
        self.assertIn('- [LOG/TEMP FILE] /test/repo/logs/app.log', output)
        self.assertIn('Review the list above.', output)

    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir', return_value=False)
    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_path(self, mock_parse_args, mock_abspath, mock_isdir, mock_stderr):
        # Mock rationale: sys.stderr is mocked to capture error output. os.path.isdir and os.path.abspath are mocked
        # to simulate an invalid path. argparse.ArgumentParser.parse_args is mocked to control CLI arguments.
        mock_parse_args.return_value = MagicMock(path='/nonexistent/path')

        from sweeper import main
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)

        output = mock_stderr.getvalue()
        self.assertIn("Error: The provided path '/nonexistent/path' is not a valid directory.", output)
