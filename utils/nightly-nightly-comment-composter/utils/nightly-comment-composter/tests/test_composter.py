import unittest
from unittest.mock import patch, mock_open
import os
from src.composter import find_stale_comments_in_file, scan_directory, STALE_COMMENT_PATTERN

class TestComposter(unittest.TestCase):

    def test_stale_comment_pattern(self):
        # Test various forms of stale comments
        self.assertIsNotNone(STALE_COMMENT_PATTERN.search("# TODO: finish this"))
        self.assertIsNotNone(STALE_COMMENT_PATTERN.search("# FIXME this is broken"))
        self.assertIsNotNone(STALE_COMMENT_PATTERN.search("# HACK - temporary fix"))
        self.assertIsNotNone(STALE_COMMENT_PATTERN.search("# NOTE: important detail"))
        self.assertIsNotNone(STALE_COMMENT_PATTERN.search("# todo: lowercase"))
        self.assertIsNotNone(STALE_COMMENT_PATTERN.search("#  FIXME   with extra spaces"))
        self.assertIsNotNone(STALE_COMMENT_PATTERN.search("    # TODO: indented"))

        # Test non-stale comments
        self.assertIsNone(STALE_COMMENT_PATTERN.search("# Regular comment"))
        self.assertIsNone(STALE_COMMENT_PATTERN.search("print('hello')"))
        self.assertIsNone(STALE_COMMENT_PATTERN.search("#TODOSomething (no space/colon)"))
        self.assertIsNone(STALE_COMMENT_PATTERN.search("# FIX ME (space in marker)"))

    @patch('builtins.open', new_callable=mock_open)
    def test_find_stale_comments_in_file_found(self, mock_file_open):
        # Mock rationale: Simulate reading a file from disk without actual I/O.
        # This ensures the test is deterministic and offline.
        mock_file_content = (
            "line 1\n"
            "# TODO: Do something important\n"
            "line 3\n"
            "# FIXME: This needs fixing\n"
            "line 5 # HACK: Temporary workaround\n"
            "line 6\n"
        )
        mock_file_open.return_value.__enter__.return_value = mock_file_content.splitlines(True)

        filepath = "/path/to/test_file.py"
        comments = find_stale_comments_in_file(filepath)

        self.assertEqual(len(comments), 3)
        self.assertEqual(comments[0]['file'], filepath)
        self.assertEqual(comments[0]['line'], 2)
        self.assertEqual(comments[0]['content'], "# TODO: Do something important")
        self.assertEqual(comments[1]['file'], filepath)
        self.assertEqual(comments[1]['line'], 4)
        self.assertEqual(comments[1]['content'], "# FIXME: This needs fixing")
        self.assertEqual(comments[2]['file'], filepath)
        self.assertEqual(comments[2]['line'], 5)
        self.assertEqual(comments[2]['content'], "line 5 # HACK: Temporary workaround") # Ensure full line is captured

    @patch('builtins.open', new_callable=mock_open)
    def test_find_stale_comments_in_file_not_found(self, mock_file_open):
        # Mock rationale: Simulate reading a file with no stale comments.
        mock_file_content = (
            "line 1\n"
            "# A regular comment\n"
            "line 3\n"
            "print('hello')\n"
        )
        mock_file_open.return_value.__enter__.return_value = mock_file_content.splitlines(True)

        filepath = "/path/to/clean_file.py"
        comments = find_stale_comments_in_file(filepath)

        self.assertEqual(len(comments), 0)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.walk')
    def test_scan_directory_basic(self, mock_os_walk, mock_file_open):
        # Mock rationale: Simulate file system traversal using os.walk.
        # This avoids actual disk access and makes the test deterministic.
        mock_os_walk.return_value = [
            ('/root', ['dir1'], ['file1.py', 'file2.txt']),
            ('/root/dir1', [], ['file3.py'])
        ]

        # Mock rationale: Simulate content for file1.py and file3.py.
        # This ensures the comment finding logic is tested without real files.
        def mock_open_side_effect(filepath, *args, **kwargs):
            if filepath == os.path.join('/root', 'file1.py'):
                return mock_open(read_data="# TODO: In file1\nline2").return_value
            elif filepath == os.path.join('/root/dir1', 'file3.py'):
                return mock_open(read_data="line1\n# FIXME: In file3").return_value
            else:
                # For file2.txt or any other unexpected file, return empty
                return mock_open(read_data="").return_value

        mock_file_open.side_effect = mock_open_side_effect

        root_path = "/root"
        comments = scan_directory(root_path)

        self.assertEqual(len(comments), 2)
        self.assertEqual(comments[0]['file'], os.path.join('/root', 'file1.py'))
        self.assertEqual(comments[0]['line'], 1)
        self.assertEqual(comments[0]['content'], "# TODO: In file1")
        self.assertEqual(comments[1]['file'], os.path.join('/root/dir1', 'file3.py'))
        self.assertEqual(comments[1]['line'], 2)
        self.assertEqual(comments[1]['content'], "# FIXME: In file3")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.walk')
    def test_scan_directory_exclude_dirs_and_files(self, mock_os_walk, mock_file_open):
        # Mock rationale: Simulate file system traversal with exclusions.
        mock_os_walk.return_value = [
            ('/root', ['venv', 'src', 'tests'], ['main.py', 'config.py']),
            ('/root/venv', [], ['activate']), # Should be excluded
            ('/root/src', [], ['module1.py', 'module2.py']),
            ('/root/tests', [], ['test_main.py']) # Should be excluded by file name
        ]

        # Mock rationale: Simulate content for relevant files.
        def mock_open_side_effect(filepath, *args, **kwargs):
            if filepath == os.path.join('/root', 'main.py'):
                return mock_open(read_data="# TODO: Main task").return_value
            elif filepath == os.path.join('/root/src', 'module1.py'):
                return mock_open(read_data="# FIXME: Module 1 bug").return_value
            else:
                return mock_open(read_data="").return_value

        mock_file_open.side_effect = mock_open_side_effect

        root_path = "/root"
        exclude_dirs = ['venv', 'tests']
        exclude_files = ['config.py', 'test_main.py'] # config.py is not .py, but still excluded if matched

        comments = scan_directory(root_path, exclude_dirs, exclude_files)

        self.assertEqual(len(comments), 2) # main.py and module1.py
        self.assertEqual(comments[0]['file'], os.path.join('/root', 'main.py'))
        self.assertEqual(comments[0]['content'], "# TODO: Main task")
        self.assertEqual(comments[1]['file'], os.path.join('/root/src', 'module1.py'))
        self.assertEqual(comments[1]['content'], "# FIXME: Module 1 bug")

        # Ensure os.walk was called with correct pruning logic
        # This is implicitly tested by the result, but we can also check mock_os_walk calls if needed.
        # For os.walk, the dirnames list is modified in-place, so we can't directly check the final list passed to it.
        # However, the side_effect of mock_open confirms which files were attempted to be opened.

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    @patch('os.walk')
    def test_find_stale_comments_in_file_io_error(self, mock_os_walk, mock_file_open):
        # Mock rationale: Simulate an IOError when trying to open a file.
        # This tests error handling without needing actual file system permissions issues.
        filepath = "/path/to/unreadable_file.py"
        # We don't need to mock os.walk for this specific test, as it's testing the file-level function.
        # The patch for os.walk is just to satisfy the decorator order, but it won't be used.

        # Capture print output to check warning message
        with patch('builtins.print') as mock_print:
            comments = find_stale_comments_in_file(filepath)
            self.assertEqual(len(comments), 0)
            mock_print.assert_called_with(f"Warning: Could not read file {filepath}: Permission denied")

if __name__ == '__main__':
    unittest.main()
