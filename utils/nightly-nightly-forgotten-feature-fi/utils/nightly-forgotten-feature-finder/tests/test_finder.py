import unittest
from unittest.mock import patch, mock_open
import os
import sys

# Mock rationale: We need to simulate a file system without actually creating files
# on disk. `os.walk` is patched to control directory traversal, and `builtins.open` is
# patched to provide specific file contents when a file is "read".
# This ensures tests are deterministic, fast, and don't leave artifacts.

# Adjust sys.path to allow importing `finder` from the `src` directory.
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_dir)
from finder import find_forgotten_features
sys.path.pop(0)


class TestForgottenFeatureFinder(unittest.TestCase):

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_no_forgotten_features(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a project with no relevant markers.
        mock_os_walk.return_value = [
            ('.', ('src', 'tests'), ('main.py', 'utils.py')),
            ('./src', (), ('helper.py',)),
        ]
        mock_file_open.side_effect = [
            mock_open(read_data="print('Hello')\ndef func(): pass").return_value,
            mock_open(read_data="class MyClass:\n    def __init__(self): pass").return_value,
            mock_open(read_data="def another_func():\n    return 1").return_value,
        ]

        report = find_forgotten_features('.')
        self.assertEqual(len(report), 0)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_single_file_multiple_markers(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a single file with multiple types of markers.
        mock_os_walk.return_value = [
            ('.', ('src',), ('app.py',)),
        ]
        mock_file_open.return_value.read.return_value = (
            "import os\n"
            "# TODO: Refactor this module\n"
            "def process_data():\n"
            "    # FIXME: This needs to handle edge cases better\n"
            "    data = [] # HACK: Temporary data structure\n"
            "    return data\n"
        )

        report = find_forgotten_features('.')
        self.assertEqual(len(report), 3)
        self.assertIn("./app.py:2: TODO: Refactor this module", report)
        self.assertIn("./app.py:4: FIXME: This needs to handle edge cases better", report)
        self.assertIn("./app.py:5: HACK: Temporary data structure", report)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_multiple_files_different_markers(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate multiple files across directories with various markers.
        mock_os_walk.return_value = [
            ('.', ('src', 'docs'), ('README.md',)),
            ('./src', (), ('api.py',)),
            ('./docs', (), ('guide.md',)),
        ]
        
        # Define mock file contents for each file
        mock_file_contents = {
            os.path.join('.', 'README.md'): "Project Info\n# BUG: Known issue with setup\n",
            os.path.join('./src', 'api.py'): "def get_user():\n    pass # XXX: Security review needed\n",
            os.path.join('./docs', 'guide.md'): "User Guide\n\n## Installation\n# TODO: Add more details on dependencies\n",
        }

        # Configure mock_open to return different content based on the file path
        def mock_open_side_effect(file_path, *args, **kwargs):
            if file_path in mock_file_contents:
                return mock_open(read_data=mock_file_contents[file_path]).return_value
            raise FileNotFoundError(f"File not found: {file_path}")

        mock_file_open.side_effect = mock_open_side_effect

        report = find_forgotten_features('.')
        self.assertEqual(len(report), 3)
        self.assertIn("./README.md:2: BUG: Known issue with setup", report)
        self.assertIn("./src/api.py:2: XXX: Security review needed", report)
        self.assertIn("./docs/guide.md:4: TODO: Add more details on dependencies", report)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_case_insensitivity(self, mock_file_open, mock_os_walk):
        # Mock rationale: Ensure markers are found regardless of case.
        mock_os_walk.return_value = [
            ('.', (), ('script.py',)),
        ]
        mock_file_open.return_value.read.return_value = (
            "def func():\n"
            "    # todo: lowercase marker\n"
            "    # FixMe: mixed case marker\n"
            "    pass\n"
        )

        report = find_forgotten_features('.')
        self.assertEqual(len(report), 2)
        self.assertIn("./script.py:2: TODO: lowercase marker", report)
        self.assertIn("./script.py:3: FIXME: mixed case marker", report)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_excluded_directories(self, mock_file_open, mock_os_walk):
        # Mock rationale: Verify that specified directories are skipped.
        mock_os_walk.return_value = [
            ('.', ('src', 'node_modules', '.git'), ('main.py',)),
            ('./src', (), ('helper.py',)),
            ('./node_modules', (), ('lib.js',)), # Should be excluded
            ('./.git', (), ('config',)), # Should be excluded
        ]
        
        mock_file_contents = {
            os.path.join('.', 'main.py'): "# TODO: Main task\n",
            os.path.join('./src', 'helper.py'): "# FIXME: Helper issue\n",
            os.path.join('./node_modules', 'lib.js'): "// TODO: Library task (should be ignored)\n",
            os.path.join('./.git', 'config'): "# TODO: Git config task (should be ignored)\n",
        }

        def mock_open_side_effect(file_path, *args, **kwargs):
            if file_path in mock_file_contents:
                return mock_open(read_data=mock_file_contents[file_path]).return_value
            raise FileNotFoundError(f"File not found: {file_path}")

        mock_file_open.side_effect = mock_open_side_effect

        report = find_forgotten_features('.')
        self.assertEqual(len(report), 2)
        self.assertIn("./main.py:1: TODO: Main task", report)
        self.assertIn("./src/helper.py:1: FIXME: Helper issue", report)
        self.assertNotIn("./node_modules/lib.js:1: TODO: Library task (should be ignored)", report)
        self.assertNotIn("./.git/config:1: TODO: Git config task (should be ignored)", report)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_unreadable_file_skipped(self, mock_file_open, mock_os_walk):
        # Mock rationale: Ensure the utility doesn't crash on unreadable files.
        mock_os_walk.return_value = [
            ('.', (), ('readable.py', 'unreadable.py')),
        ]
        
        # Simulate an IOError for 'unreadable.py'
        def mock_open_side_effect(file_path, *args, **kwargs):
            if 'unreadable.py' in file_path:
                raise IOError("Permission denied")
            return mock_open(read_data="# TODO: This is readable\n").return_value

        mock_file_open.side_effect = mock_open_side_effect

        report = find_forgotten_features('.')
        self.assertEqual(len(report), 1)
        self.assertIn("./readable.py:1: TODO: This is readable", report)
        # Ensure no error was raised and the unreadable file was skipped.

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_binary_file_skipped_or_ignored(self, mock_file_open, mock_os_walk):
        # Mock rationale: Ensure binary files don't cause encoding errors or false positives.
        # The `errors='ignore'` in open() should handle this, but good to test.
        mock_os_walk.return_value = [
            ('.', (), ('text.py', 'image.png')),
        ]
        
        mock_file_contents = {
            os.path.join('.', 'text.py'): "# TODO: Text file task\n",
            os.path.join('.', 'image.png'): b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82'
        }

        def mock_open_side_effect(file_path, *args, **kwargs):
            if file_path == os.path.join('.', 'text.py'):
                return mock_open(read_data=mock_file_contents[file_path]).return_value
            elif file_path == os.path.join('.', 'image.png'):
                # Simulate a binary file that might cause decoding issues if not handled
                # The `errors='ignore'` in `open` should prevent a crash.
                # We'll return a mock file object that, when read, would contain binary data
                # but the `find_forgotten_features` function uses `encoding='utf-8', errors='ignore'`
                # which should prevent an error.
                return mock_open(read_data=mock_file_contents[file_path].decode('latin-1', errors='ignore')).return_value
            raise FileNotFoundError(f"File not found: {file_path}")

        mock_file_open.side_effect = mock_open_side_effect

        report = find_forgotten_features('.')
        self.assertEqual(len(report), 1)
        self.assertIn("./text.py:1: TODO: Text file task", report)
        self.assertNotIn("image.png", report) # Ensure binary file is not processed or reported
