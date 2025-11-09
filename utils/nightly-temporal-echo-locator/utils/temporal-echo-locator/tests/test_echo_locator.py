import unittest
import os
import json
from unittest.mock import patch, mock_open
from src.echo_locator import find_echoes

class TestEchoLocator(unittest.TestCase):

    # Mock rationale: We need to simulate a file system structure and file contents
    # without actually touching the disk, ensuring deterministic and offline tests.
    # `os.walk` is mocked to control directory traversal, and `builtins.open`
    # is mocked to provide specific file content for given paths.

    def _setup_mock_open(self, mock_file_open, file_contents):
        """Helper to configure mock_open for iterating over file contents."""
        def mock_open_side_effect(file_path, *args, **kwargs):
            if file_path in file_contents:
                mock_handle = mock_open(read_data=file_contents[file_path]).return_value
                # Make the mock file handle iterable for `for line in f:`
                mock_handle.__iter__.return_value = iter(file_contents[file_path].splitlines(keepends=True))
                return mock_handle
            raise FileNotFoundError(f"No such file: {file_path}")
        mock_file_open.side_effect = mock_open_side_effect

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_echoes_basic(self, mock_file_open, mock_os_walk):
        # Setup mock file system structure
        mock_os_walk.return_value = [
            ('/mock_repo', ['src', 'docs'], ['README.md']),
            ('/mock_repo/src', [], ['main.py', 'helper.js']),
            ('/mock_repo/docs', [], ['guide.md'])
        ]

        # Setup mock file contents
        file_contents = {
            '/mock_repo/README.md': "This is a README.\nTODO: Update this section.",
            '/mock_repo/src/main.py': "def func():\n    # FIXME: This needs refactoring\n    pass",
            '/mock_repo/src/helper.js': "// No echoes here\nconsole.log('hello');",
            '/mock_repo/docs/guide.md': "## Guide\nThis is a guide.\nHACK: Temporary solution."
        }
        self._setup_mock_open(mock_file_open, file_contents)

        keywords = ['TODO', 'FIXME', 'HACK']
        extensions = ['.py', '.js', '.md']
        echoes = find_echoes('/mock_repo', keywords, extensions)

        self.assertEqual(len(echoes), 3)
        self.assertIn({
            'file_path': '/mock_repo/README.md',
            'line_number': 2,
            'line_content': 'TODO: Update this section.',
            'keyword': 'TODO'
        }, echoes)
        self.assertIn({
            'file_path': '/mock_repo/src/main.py',
            'line_number': 2,
            'line_content': '# FIXME: This needs refactoring',
            'keyword': 'FIXME'
        }, echoes)
        self.assertIn({
            'file_path': '/mock_repo/docs/guide.md',
            'line_number': 3,
            'line_content': 'HACK: Temporary solution.',
            'keyword': 'HACK'
        }, echoes)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_echoes_no_matches(self, mock_file_open, mock_os_walk):
        mock_os_walk.return_value = [
            ('/mock_repo', [], ['clean.py', 'another.txt'])
        ]
        file_contents = {
            '/mock_repo/clean.py': "print('hello')",
            '/mock_repo/another.txt': "Just some text."
        }
        self._setup_mock_open(mock_file_open, file_contents)

        keywords = ['TODO', 'FIXME']
        extensions = ['.py', '.txt']
        echoes = find_echoes('/mock_repo', keywords, extensions)
        self.assertEqual(len(echoes), 0)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_echoes_case_insensitivity(self, mock_file_open, mock_os_walk):
        mock_os_walk.return_value = [
            ('/mock_repo', [], ['case.py'])
        ]
        file_contents = {
            '/mock_repo/case.py': "def foo():\n    # todo: lowercase todo\n    # ToDo: mixed case\n    pass"
        }
        self._setup_mock_open(mock_file_open, file_contents)

        keywords = ['TODO'] # Pattern is compiled with IGNORECASE
        extensions = ['.py']
        echoes = find_echoes('/mock_repo', keywords, extensions)
        self.assertEqual(len(echoes), 2)
        self.assertIn({
            'file_path': '/mock_repo/case.py',
            'line_number': 2,
            'line_content': '# todo: lowercase todo',
            'keyword': 'todo'
        }, echoes)
        self.assertIn({
            'file_path': '/mock_repo/case.py',
            'line_number': 3,
            'line_content': '# ToDo: mixed case',
            'keyword': 'ToDo'
        }, echoes)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_echoes_unsupported_extension(self, mock_file_open, mock_os_walk):
        mock_os_walk.return_value = [
            ('/mock_repo', [], ['script.sh', 'config.yaml'])
        ]
        file_contents = {
            '/mock_repo/script.sh': "# TODO: Fix this script",
            '/mock_repo/config.yaml': "# FIXME: Update config"
        }
        self._setup_mock_open(mock_file_open, file_contents)

        keywords = ['TODO', 'FIXME']
        extensions = ['.sh'] # Only .sh is supported
        echoes = find_echoes('/mock_repo', keywords, extensions)
        self.assertEqual(len(echoes), 1)
        self.assertIn({
            'file_path': '/mock_repo/script.sh',
            'line_number': 1,
            'line_content': '# TODO: Fix this script',
            'keyword': 'TODO'
        }, echoes)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_echoes_empty_directory(self, mock_file_open, mock_os_walk):
        mock_os_walk.return_value = [] # Simulate an empty directory
        file_contents = {}
        self._setup_mock_open(mock_file_open, file_contents)

        keywords = ['TODO']
        extensions = ['.py']
        echoes = find_echoes('/mock_repo', keywords, extensions)
        self.assertEqual(len(echoes), 0)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_echoes_file_read_error(self, mock_file_open, mock_os_walk):
        mock_os_walk.return_value = [
            ('/mock_repo', [], ['bad_file.py', 'good_file.py'])
        ]
        file_contents = {
            '/mock_repo/good_file.py': "# TODO: This is fine"
        }

        def mock_open_side_effect(file_path, *args, **kwargs):
            if file_path == '/mock_repo/bad_file.py':
                raise IOError("Permission denied") # Simulate a file read error
            elif file_path in file_contents:
                mock_handle = mock_open(read_data=file_contents[file_path]).return_value
                mock_handle.__iter__.return_value = iter(file_contents[file_path].splitlines(keepends=True))
                return mock_handle
            raise FileNotFoundError(f"No such file: {file_path}")

        mock_file_open.side_effect = mock_open_side_effect

        keywords = ['TODO']
        extensions = ['.py']
        echoes = find_echoes('/mock_repo', keywords, extensions)
        self.assertEqual(len(echoes), 1)
        self.assertIn({
            'file_path': '/mock_repo/good_file.py',
            'line_number': 1,
            'line_content': '# TODO: This is fine',
            'keyword': 'TODO'
        }, echoes)
        # Ensure that the bad_file.py didn't cause a crash and was skipped.

if __name__ == '__main__':
    unittest.main()
