import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the src directory to the path to allow importing sweeper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from sweeper import find_dust_bunnies, generate_cleanup_command, DEFAULT_PATTERNS
sys.path.pop(0)

class TestSweeper(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_dust_bunnies_basic(self, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate a valid root directory.
        # os.walk is mocked to simulate a file system structure for testing.
        mock_isdir.return_value = True
        
        # Simulate a simple directory structure with some dust bunnies
        mock_walk.return_value = [
            ('/repo', ['src', 'node_modules', '__pycache__'], ['README.md', 'main.py', 'config.log']),
            ('/repo/src', [], ['app.py']),
            ('/repo/node_modules', ['some_lib'], ['package.json']),
            ('/repo/__pycache__', [], ['app.cpython-39.pyc'])
        ]

        patterns = ['node_modules', '__pycache__', '*.log', '*.pyc']
        found_bunnies = find_dust_bunnies('/repo', patterns)
        
        expected_bunnies = [
            '/repo/__pycache__',
            '/repo/config.log',
            '/repo/node_modules'
        ]
        self.assertCountEqual(found_bunnies, expected_bunnies)

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_dust_bunnies_no_bunnies(self, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate a valid root directory.
        # os.walk is mocked to simulate a file system structure with no matching patterns.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/repo', ['src'], ['README.md', 'main.py']),
            ('/repo/src', [], ['app.py'])
        ]

        patterns = ['node_modules', '__pycache__', '*.log']
        found_bunnies = find_dust_bunnies('/repo', patterns)
        self.assertEqual(found_bunnies, [])

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_dust_bunnies_nested_patterns(self, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate a valid root directory.
        # os.walk is mocked to simulate a nested file system structure.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/repo', ['src', 'build'], ['project.log']),
            ('/repo/src', ['__pycache__'], ['module.py']),
            ('/repo/src/__pycache__', [], ['module.cpython-39.pyc']),
            ('/repo/build', ['dist'], ['temp.tmp']),
            ('/repo/build/dist', [], ['bundle.js'])
        ]

        patterns = ['build', '__pycache__', '*.log', '*.tmp']
        found_bunnies = find_dust_bunnies('/repo', patterns)
        
        expected_bunnies = [
            '/repo/__pycache__',
            '/repo/build',
            '/repo/project.log',
            '/repo/build/temp.tmp'
        ]
        self.assertCountEqual(found_bunnies, expected_bunnies)

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_dust_bunnies_non_existent_path(self, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate an invalid root directory.
        # os.walk is not expected to be called if the path is invalid.
        mock_isdir.return_value = False
        
        with patch('sys.stderr', new_callable=MagicMock) as mock_stderr:
            found_bunnies = find_dust_bunnies('/nonexistent', DEFAULT_PATTERNS)
            self.assertEqual(found_bunnies, [])
            mock_stderr.write.assert_called_with("Error: Path '/nonexistent' is not a valid directory.\n")
        mock_walk.assert_not_called()

    def test_generate_cleanup_command_unix_file(self):
        # Mock rationale: sys.platform is mocked to simulate a Unix-like environment.
        # os.path.isdir is mocked to simulate a file.
        with patch('sys.platform', 'linux'), patch('os.path.isdir', return_value=False):
            self.assertEqual(generate_cleanup_command('/path/to/file.log'), 'rm -f "/path/to/file.log"')

    def test_generate_cleanup_command_unix_dir(self):
        # Mock rationale: sys.platform is mocked to simulate a Unix-like environment.
        # os.path.isdir is mocked to simulate a directory.
        with patch('sys.platform', 'linux'), patch('os.path.isdir', return_value=True):
            self.assertEqual(generate_cleanup_command('/path/to/dir'), 'rm -rf "/path/to/dir"')

    def test_generate_cleanup_command_windows_file(self):
        # Mock rationale: sys.platform is mocked to simulate a Windows environment.
        # os.path.isdir is mocked to simulate a file.
        with patch('sys.platform', 'win32'), patch('os.path.isdir', return_value=False):
            self.assertEqual(generate_cleanup_command('C:\\path\\to\\file.log'), 'del /f /q "C:\\path\\to\\file.log"')

    def test_generate_cleanup_command_windows_dir(self):
        # Mock rationale: sys.platform is mocked to simulate a Windows environment.
        # os.path.isdir is mocked to simulate a directory.
        with patch('sys.platform', 'win32'), patch('os.path.isdir', return_value=True):
            self.assertEqual(generate_cleanup_command('C:\\path\\to\\dir'), 'rd /s /q "C:\\path\\to\\dir"')

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_dust_bunnies_with_default_patterns(self, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate a valid root directory.
        # os.walk is mocked to simulate a file system structure that matches some default patterns.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/repo', ['venv', 'src'], ['README.md', '.DS_Store']),
            ('/repo/venv', ['bin'], ['python']),
            ('/repo/src', ['__pycache__'], ['app.py']),
            ('/repo/src/__pycache__', [], ['app.cpython-39.pyc'])
        ]

        found_bunnies = find_dust_bunnies('/repo', DEFAULT_PATTERNS)
        expected_bunnies = [
            '/repo/.DS_Store',
            '/repo/__pycache__',
            '/repo/venv'
        ]
        self.assertCountEqual(found_bunnies, expected_bunnies)

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_dust_bunnies_specific_file_pattern(self, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate a valid root directory.
        # os.walk is mocked to simulate a file system structure with a specific file pattern match.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/repo', [], ['npm-debug.log', 'app.js'])
        ]
        patterns = ['npm-debug.log']
        found_bunnies = find_dust_bunnies('/repo', patterns)
        self.assertCountEqual(found_bunnies, ['/repo/npm-debug.log'])

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_dust_bunnies_directory_exclusion(self, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate a valid root directory.
        # os.walk is mocked to simulate a file system structure where a matched directory
        # should prevent its contents from being walked.
        mock_isdir.return_value = True
        
        # Simulate a structure where 'node_modules' is a dust bunny, and it contains 'sub_dir'
        mock_walk.return_value = [
            ('/repo', ['src', 'node_modules'], ['index.js']),
            ('/repo/src', [], ['app.js']),
            ('/repo/node_modules', ['sub_dir'], ['package.json'])
            # Note: '/repo/node_modules/sub_dir' and its contents are intentionally omitted from mock_walk
            # to simulate os.walk not descending into 'node_modules' after it's identified.
        ]

        patterns = ['node_modules']
        found_bunnies = find_dust_bunnies('/repo', patterns)
        
        # Only node_modules itself should be found, not its contents, because the sweeper
        # logic prevents os.walk from descending into identified dust bunny directories.
        self.assertCountEqual(found_bunnies, ['/repo/node_modules'])


if __name__ == '__main__':
    unittest.main()
