import unittest
import os
import sys
import datetime
from unittest.mock import patch, mock_open

# Mock rationale: We need to simulate file system interactions (os.walk, os.path.getmtime, open)
# without actually touching the disk, ensuring tests are fast, deterministic, and isolated.
# This allows us to control directory structures, file contents, and modification times precisely.

# Add the src directory to the Python path for importing the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import chronicle_keeper
sys.path.pop(0)

class TestChronicleKeeper(unittest.TestCase):

    def setUp(self):
        # Capture stdout to inspect printed output
        self.held_stdout = sys.stdout
        self.mock_stdout = unittest.mock.StringIO()
        sys.stdout = self.mock_stdout

    def tearDown(self):
        sys.stdout = self.held_stdout

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open)
    def test_empty_directory(self, mock_file_open, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate an empty directory to ensure base case handling.
        mock_walk.return_value = [] 
        chronicle_keeper.analyze_directory('/mock/path')
        output = self.mock_stdout.getvalue()

        self.assertIn('Total Files Processed: 0', output)
        self.assertIn('Total Lines of Code/Text: 0', output)
        self.assertIn('Total Comment Lines: 0', output)
        self.assertIn('No ancient scrolls found', output)
        mock_file_open.assert_not_called()

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open)
    def test_single_python_file(self, mock_file_open, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a single Python file with code and comments.
        mock_walk.return_value = [
            ('/mock/path', [], ['script.py'])
        ]
        mock_getmtime.return_value = datetime.datetime.now().timestamp() # Not ancient
        mock_file_open.return_value.readlines.return_value = [
            '# This is a comment\n',
            'import os\n',
            '\n',
            'def main():\n',
            '    print("Hello") # Inline comment is not counted by simple heuristic\n'
        ]

        chronicle_keeper.analyze_directory('/mock/path')
        output = self.mock_stdout.getvalue()

        self.assertIn('Total Files Processed: 1', output)
        self.assertIn('Total Lines of Code/Text: 5', output)
        self.assertIn('Total Comment Lines: 1', output) # Only counts lines starting with #
        self.assertIn('.py  : 1 files, 5 lines, 1 comments', output)
        self.assertIn('No ancient scrolls found', output)
        mock_file_open.assert_called_once_with(os.path.join('/mock/path', 'script.py'), 'r', encoding='utf-8', errors='ignore')

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open)
    def test_multiple_files_and_ancient_detection(self, mock_file_open, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate multiple files with different types and modification dates,
        # including one that is 'ancient' to test the ancient file detection logic.
        mock_walk.return_value = [
            ('/mock/path', ['subdir'], ['app.js', 'README.md']),
            ('/mock/path/subdir', [], ['old_script.py'])
        ]

        # Mock getmtime to return different timestamps for different files
        ancient_timestamp = (datetime.datetime.now() - datetime.timedelta(days=730)).timestamp() # 2 years ago
        recent_timestamp = datetime.datetime.now().timestamp()

        def mock_getmtime_side_effect(file_path):
            if 'old_script.py' in file_path:
                return ancient_timestamp
            return recent_timestamp
        mock_getmtime.side_effect = mock_getmtime_side_effect

        # Mock file contents using a dictionary and a side_effect function for mock_open
        file_contents = {
            os.path.join('/mock/path', 'app.js'): ['// JavaScript comment\n', 'console.log("Hello");\n'],
            os.path.join('/mock/path', 'README.md'): ['# Project Readme\n', 'This is a test.\n'],
            os.path.join('/mock/path/subdir', 'old_script.py'): ['# Old Python script\n', 'print("Old code")\n']
        }

        def mock_open_side_effect(file_path, *args, **kwargs):
            if file_path in file_contents:
                m = mock_open()
                m.return_value.readlines.return_value = file_contents[file_path]
                return m.return_value # Return the file handle mock
            raise FileNotFoundError(f"Mocked file not found: {file_path}")

        mock_file_open.side_effect = mock_open_side_effect

        chronicle_keeper.analyze_directory('/mock/path', ancient_threshold_days=365)
        output = self.mock_stdout.getvalue()

        self.assertIn('Total Files Processed: 3', output)
        self.assertIn('Total Lines of Code/Text: 6', output)
        self.assertIn('Total Comment Lines: 2', output) # 1 from JS, 1 from Python
        self.assertIn('.js  : 1 files, 2 lines, 1 comments', output)
        self.assertIn('.md  : 1 files, 2 lines, 0 comments', output)
        self.assertIn('.py  : 1 files, 2 lines, 1 comments', output)
        self.assertIn('Ancient Scrolls (Files not modified in the last 365 days)', output)
        self.assertIn(os.path.join('/mock/path/subdir', 'old_script.py'), output)
        self.assertNotIn(os.path.join('/mock/path', 'app.js'), output)
        self.assertNotIn(os.path.join('/mock/path', 'README.md'), output)

    @patch('os.path.isdir', return_value=False)
    def test_invalid_directory(self, mock_isdir):
        # Mock rationale: Test the error handling for a non-existent directory.
        with self.assertRaises(SystemExit) as cm:
            chronicle_keeper.analyze_directory('/nonexistent/path')
        self.assertEqual(cm.exception.code, 1)
        output = self.mock_stdout.getvalue()
        self.assertIn("Error: Directory not found at '/nonexistent/path'", output)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open)
    def test_unsupported_file_type(self, mock_file_open, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Ensure unsupported file types are skipped and not counted.
        mock_walk.return_value = [
            ('/mock/path', [], ['image.jpg', 'document.docx', 'script.py'])
        ]
        mock_getmtime.return_value = datetime.datetime.now().timestamp()
        mock_file_open.return_value.readlines.return_value = [
            'print("Python code")\n'
        ]

        chronicle_keeper.analyze_directory('/mock/path')
        output = self.mock_stdout.getvalue()

        self.assertIn('Total Files Processed: 1', output)
        self.assertIn('Total Lines of Code/Text: 1', output)
        self.assertIn('.py  : 1 files, 1 lines, 0 comments', output)
        self.assertNotIn('image.jpg', output)
        self.assertNotIn('document.docx', output)
        mock_file_open.assert_called_once_with(os.path.join('/mock/path', 'script.py'), 'r', encoding='utf-8', errors='ignore')

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open)
    def test_file_read_error(self, mock_file_open, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a file that causes an IOError during reading to ensure error handling.
        mock_walk.return_value = [
            ('/mock/path', [], ['bad_file.py'])
        ]
        mock_getmtime.return_value = datetime.datetime.now().timestamp()
        mock_file_open.side_effect = IOError("Permission denied")

        chronicle_keeper.analyze_directory('/mock/path')
        output = self.mock_stdout.getvalue()

        self.assertIn("Warning: Could not process '/mock/path/bad_file.py': Permission denied", output)
        self.assertIn('Total Files Processed: 0', output) # File not processed due to error
        self.assertIn('Total Lines of Code/Text: 0', output)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open)
    def test_comment_detection_various_languages(self, mock_file_open, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Test comment detection for different file types using simple heuristics.
        mock_walk.return_value = [
            ('/mock/path', [], ['test.py', 'test.js', 'test.html', 'test.yml'])
        ]
        mock_getmtime.return_value = datetime.datetime.now().timestamp()

        file_contents = {
            os.path.join('/mock/path', 'test.py'): ['# Python comment\n', 'code\n'],
            os.path.join('/mock/path', 'test.js'): ['// JS comment\n', '/* Multi-line */\n', 'code\n'],
            os.path.join('/mock/path', 'test.html'): ['<!-- HTML comment -->\n', '<div>code</div>\n'],
            os.path.join('/mock/path', 'test.yml'): ['# YAML comment\n', 'key: value\n']
        }

        def mock_open_side_effect(file_path, *args, **kwargs):
            if file_path in file_contents:
                m = mock_open()
                m.return_value.readlines.return_value = file_contents[file_path]
                return m.return_value
            raise FileNotFoundError(f"Mocked file not found: {file_path}")

        mock_file_open.side_effect = mock_open_side_effect

        chronicle_keeper.analyze_directory('/mock/path')
        output = self.mock_stdout.getvalue()

        self.assertIn('Total Files Processed: 4', output)
        self.assertIn('Total Lines of Code/Text: 8', output)
        self.assertIn('Total Comment Lines: 4', output) # 1 py, 1 js (//), 1 html, 1 yml
        self.assertIn('.py  : 1 files, 2 lines, 1 comments', output)
        self.assertIn('.js  : 1 files, 3 lines, 1 comments', output) # Only // is counted by is_comment_line for JS, /* Multi-line */ is one line starting with /*
        self.assertIn('.html: 1 files, 2 lines, 1 comments', output)
        self.assertIn('.yml : 1 files, 2 lines, 1 comments', output)

if __name__ == '__main__':
    unittest.main()
