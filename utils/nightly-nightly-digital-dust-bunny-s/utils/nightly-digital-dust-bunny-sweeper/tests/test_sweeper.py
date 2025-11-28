import unittest
from unittest.mock import patch, call
import os
import sys

# Add the src directory to the Python path to import the module under test
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from sweeper import clean_empty_dirs

class TestDigitalDustBunnySweeper(unittest.TestCase):

    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_no_empty_dirs(self, mock_walk, mock_isdir, mock_listdir, mock_rmdir):
        # Mock rationale: Simulate a directory structure with no empty directories.
        # os.walk will return directories with content. os.listdir will confirm they are not empty.
        # os.rmdir should not be called.
        
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['file.txt']),
            ('/root/dir1', [], ['another.txt']),
            ('/root/dir2', ['subdir'], []),
            ('/root/dir2/subdir', [], ['data.bin']),
        ]
        # Mock rationale: Ensure os.listdir always returns content for these paths.
        mock_listdir.side_effect = lambda p: ['file.txt'] if p == '/root' else \
                                            ['another.txt'] if p == '/root/dir1' else \
                                            ['subdir'] if p == '/root/dir2' else \
                                            ['data.bin'] if p == '/root/dir2/subdir' else ['some_content']

        removed = clean_empty_dirs('/root')
        self.assertEqual(removed, [])
        mock_rmdir.assert_not_called()
        mock_isdir.assert_called_with('/root')

    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_single_empty_dir(self, mock_walk, mock_isdir, mock_listdir, mock_rmdir):
        # Mock rationale: Simulate a structure where '/root/empty_dir' is empty.
        # os.walk will traverse it. os.listdir will confirm it's empty.
        # os.rmdir should be called for '/root/empty_dir'.
        
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root/empty_dir', [], []), # This is processed first due to topdown=False
            ('/root', ['empty_dir'], ['file.txt']),
        ]
        # Mock rationale: '/root/empty_dir' is empty, '/root' has 'file.txt'.
        mock_listdir.side_effect = lambda p: [] if p == '/root/empty_dir' else \
                                            ['file.txt'] if p == '/root' else \
                                            ['some_content'] # Default for other paths if any

        removed = clean_empty_dirs('/root')
        self.assertEqual(removed, ['/root/empty_dir'])
        mock_rmdir.assert_called_once_with('/root/empty_dir')
        mock_isdir.assert_called_with('/root')

    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_nested_empty_dirs(self, mock_walk, mock_isdir, mock_listdir, mock_rmdir):
        # Mock rationale: Simulate nested empty directories '/root/a/b/c'.
        # os.walk will return them in bottom-up order. os.listdir will confirm each is empty.
        # os.rmdir should be called for 'c', then 'b', then 'a'.
        
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root/a/b/c', [], []),
            ('/root/a/b', ['c'], []),
            ('/root/a', ['b'], []),
            ('/root', ['a'], ['file.txt']),
        ]
        # Mock rationale: 'c', 'b', 'a' are empty. '/root' has 'file.txt'.
        mock_listdir.side_effect = lambda p: [] if p in ['/root/a/b/c', '/root/a/b', '/root/a'] else \
                                            ['file.txt'] if p == '/root' else \
                                            ['some_content']

        removed = clean_empty_dirs('/root')
        self.assertEqual(removed, ['/root/a/b/c', '/root/a/b', '/root/a'])
        mock_rmdir.assert_has_calls([
            call('/root/a/b/c'),
            call('/root/a/b'),
            call('/root/a'),
        ])
        self.assertEqual(mock_rmdir.call_count, 3)
        mock_isdir.assert_called_with('/root')

    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_mixed_content_and_empty_dirs(self, mock_walk, mock_isdir, mock_listdir, mock_rmdir):
        # Mock rationale: Simulate a complex structure with some empty and some non-empty.
        # Only the truly empty ones should be removed.
        
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root/empty1', [], []),
            ('/root/full1/sub_empty', [], []),
            ('/root/full1', ['sub_empty'], ['file.txt']),
            ('/root/empty2', [], []),
            ('/root', ['empty1', 'full1', 'empty2'], ['main.log']),
        ]
        # Mock rationale: empty1, sub_empty, empty2 are empty. full1 and root have content.
        mock_listdir.side_effect = lambda p: [] if p in ['/root/empty1', '/root/full1/sub_empty', '/root/empty2'] else \
                                            ['file.txt'] if p == '/root/full1' else \
                                            ['main.log'] if p == '/root' else \
                                            ['some_content']

        removed = clean_empty_dirs('/root')
        self.assertEqual(sorted(removed), sorted(['/root/empty1', '/root/full1/sub_empty', '/root/empty2']))
        mock_rmdir.assert_has_calls([
            call('/root/empty1'),
            call('/root/full1/sub_empty'),
            call('/root/empty2'),
        ], any_order=True)
        self.assertEqual(mock_rmdir.call_count, 3)
        mock_isdir.assert_called_with('/root')

    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_dry_run(self, mock_walk, mock_isdir, mock_listdir, mock_rmdir):
        # Mock rationale: Test dry-run mode. Directories should be identified but not removed.
        
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root/empty_dir', [], []),
            ('/root', ['empty_dir'], ['file.txt']),
        ]
        mock_listdir.side_effect = lambda p: [] if p == '/root/empty_dir' else \
                                            ['file.txt'] if p == '/root' else \
                                            ['some_content']

        removed = clean_empty_dirs('/root', dry_run=True)
        self.assertEqual(removed, ['/root/empty_dir'])
        mock_rmdir.assert_not_called() # Crucial for dry-run
        mock_isdir.assert_called_with('/root')

    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_root_dir_not_removed_if_empty(self, mock_walk, mock_isdir, mock_listdir, mock_rmdir):
        # Mock rationale: If the root directory itself becomes empty after children are removed,
        # it should not be removed by the utility. The comparison uses abspath for robustness.
        
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root/empty_child', [], []),
            ('/root', ['empty_child'], []), # Root initially has empty_child, but no files
        ]
        # Mock rationale: empty_child is empty. After empty_child is "removed", /root becomes empty.
        mock_listdir.side_effect = lambda p: [] if p == '/root/empty_child' else \
                                            [] if p == '/root' else \
                                            ['some_content']

        # Mock os.path.abspath to return consistent paths for comparison
        with patch('os.path.abspath', side_effect=lambda p: p) as mock_abspath:
            removed = clean_empty_dirs('/root')
            self.assertEqual(removed, ['/root/empty_child'])
            mock_rmdir.assert_called_once_with('/root/empty_child')
            mock_isdir.assert_called_with('/root')
            mock_abspath.assert_any_call('/root')

    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_non_existent_root_dir(self, mock_walk, mock_isdir, mock_listdir, mock_rmdir):
        # Mock rationale: If the root directory does not exist, the function should return empty.
        
        mock_isdir.return_value = False # Simulate non-existent root
        
        removed = clean_empty_dirs('/nonexistent')
        self.assertEqual(removed, [])
        mock_rmdir.assert_not_called()
        mock_walk.assert_not_called() # os.walk should not be called if root doesn't exist
        mock_isdir.assert_called_once_with('/nonexistent')

    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_os_error_on_rmdir(self, mock_walk, mock_isdir, mock_listdir, mock_rmdir):
        # Mock rationale: Simulate an OSError during rmdir (e.g., permissions).
        # The utility should log the error but continue processing other directories.
        
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root/empty1', [], []),
            ('/root/empty2', [], []),
            ('/root', ['empty1', 'empty2'], []),
        ]
        mock_listdir.side_effect = lambda p: [] # All are empty
        
        # Mock rationale: Make rmdir fail for '/root/empty1' but succeed for '/root/empty2'.
        mock_rmdir.side_effect = lambda p: os.error("Permission denied") if p == '/root/empty1' else None

        # Capture stderr to check error message
        with patch('sys.stderr', new_callable=unittest.mock.StringIO) as mock_stderr:
            removed = clean_empty_dirs('/root')
            self.assertEqual(removed, ['/root/empty2']) # Only empty2 should be successfully removed
            self.assertIn("Error removing directory '/root/empty1': Permission denied", mock_stderr.getvalue())
        
        mock_rmdir.assert_has_calls([
            call('/root/empty1'),
            call('/root/empty2'),
        ])
        self.assertEqual(mock_rmdir.call_count, 2)
        mock_isdir.assert_called_with('/root')

    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_os_error_on_listdir(self, mock_walk, mock_isdir, mock_listdir, mock_rmdir):
        # Mock rationale: Simulate an OSError during listdir (e.g., permissions).
        # The utility should log the warning and skip that directory, not attempting to remove it.
        
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root/unreadable', [], []),
            ('/root/empty', [], []),
            ('/root', ['unreadable', 'empty'], []),
        ]
        # Mock rationale: listdir fails for '/root/unreadable', succeeds for '/root/empty'.
        mock_listdir.side_effect = lambda p: os.error("Permission denied") if p == '/root/unreadable' else []

        with patch('sys.stderr', new_callable=unittest.mock.StringIO) as mock_stderr:
            removed = clean_empty_dirs('/root')
            self.assertEqual(removed, ['/root/empty']) # Only empty should be removed
            self.assertIn("Warning: Could not list contents of '/root/unreadable': Permission denied", mock_stderr.getvalue())
        
        mock_rmdir.assert_called_once_with('/root/empty')
        mock_isdir.assert_called_with('/root')


if __name__ == '__main__':
    unittest.main()
