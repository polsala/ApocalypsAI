import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from io import StringIO

# Add the src directory to the path to allow importing dust_buster
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import dust_buster

class TestDustBuster(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('os.walk')
    @patch('os.path.islink')
    @patch('os.path.exists')
    @patch('os.path.realpath')
    def test_find_broken_symlinks_no_links(self, mock_realpath, mock_exists, mock_islink, mock_walk):
        # Mock rationale: Simulate a directory structure with no symlinks.
        mock_walk.return_value = [
            ('/root', ['dir1'], ['file1.txt']),
            ('/root/dir1', [], ['file2.txt'])
        ]
        mock_islink.return_value = False # Mock rationale: No file/dir is a symlink.
        mock_exists.return_value = True # Mock rationale: All files/dirs exist.
        mock_realpath.side_effect = lambda x: x # Mock rationale: Realpath returns itself if not a symlink.

        broken_links = dust_buster.find_broken_symlinks('/root')
        self.assertEqual(broken_links, [])

    @patch('os.walk')
    @patch('os.path.islink')
    @patch('os.path.exists')
    @patch('os.path.realpath')
    def test_find_broken_symlinks_with_broken_file_link(self, mock_realpath, mock_exists, mock_islink, mock_walk):
        # Mock rationale: Simulate a directory with one broken file symlink.
        mock_walk.return_value = [
            ('/root', [], ['link_to_nonexistent.txt', 'file1.txt'])
        ]
        # Mock rationale: 'link_to_nonexistent.txt' is a symlink, 'file1.txt' is not.
        mock_islink.side_effect = lambda p: p == '/root/link_to_nonexistent.txt'
        # Mock rationale: Target of 'link_to_nonexistent.txt' does not exist.
        mock_exists.side_effect = lambda p: p != '/root/nonexistent_target.txt'
        mock_realpath.side_effect = lambda p: '/root/nonexistent_target.txt' if p == '/root/link_to_nonexistent.txt' else p

        broken_links = dust_buster.find_broken_symlinks('/root')
        self.assertEqual(broken_links, ['/root/link_to_nonexistent.txt'])

    @patch('os.walk')
    @patch('os.path.islink')
    @patch('os.path.exists')
    @patch('os.path.realpath')
    def test_find_broken_symlinks_with_broken_dir_link(self, mock_realpath, mock_exists, mock_islink, mock_walk):
        # Mock rationale: Simulate a directory with one broken directory symlink.
        mock_walk.return_value = [
            ('/root', ['link_to_nonexistent_dir', 'existing_dir'], ['file1.txt'])
        ]
        # Mock rationale: 'link_to_nonexistent_dir' is a symlink, 'existing_dir' is not.
        mock_islink.side_effect = lambda p: p == '/root/link_to_nonexistent_dir'
        # Mock rationale: Target of 'link_to_nonexistent_dir' does not exist.
        mock_exists.side_effect = lambda p: p != '/root/nonexistent_target_dir'
        mock_realpath.side_effect = lambda p: '/root/nonexistent_target_dir' if p == '/root/link_to_nonexistent_dir' else p

        broken_links = dust_buster.find_broken_symlinks('/root')
        self.assertEqual(broken_links, ['/root/link_to_nonexistent_dir'])

    @patch('os.walk')
    @patch('os.listdir')
    def test_find_empty_dirs_no_empty_dirs(self, mock_listdir, mock_walk):
        # Mock rationale: Simulate a directory structure with no empty directories.
        mock_walk.return_value = [
            ('/root', ['dir1'], ['file1.txt']),
            ('/root/dir1', [], ['file2.txt'])
        ]
        mock_listdir.return_value = ['file.txt'] # Mock rationale: Directories are not empty.

        empty_dirs = dust_buster.find_empty_dirs('/root')
        self.assertEqual(empty_dirs, [])

    @patch('os.walk')
    @patch('os.listdir') # Not strictly needed for os.walk(topdown=False) but good practice if logic changes
    def test_find_empty_dirs_with_empty_dir(self, mock_listdir, mock_walk):
        # Mock rationale: Simulate a directory structure with one empty directory.
        mock_walk.return_value = [
            ('/root/empty_dir', [], []), # This will be found first due to topdown=False
            ('/root', ['empty_dir', 'full_dir'], ['file1.txt']),
        ]
        # Mock rationale: os.walk(topdown=False) handles the empty check by providing empty dirnames/filenames.
        # mock_listdir is not directly used by find_empty_dirs due to os.walk(topdown=False)
        # but if it were, we'd mock it to return [].

        empty_dirs = dust_buster.find_empty_dirs('/root')
        self.assertEqual(empty_dirs, ['/root/empty_dir'])

    @patch('os.walk')
    @patch('os.listdir')
    def test_find_empty_dirs_nested_empty_dirs(self, mock_listdir, mock_walk):
        # Mock rationale: Simulate nested empty directories.
        mock_walk.return_value = [
            ('/root/dir1/empty_nested', [], []),
            ('/root/dir1', ['empty_nested'], []),
            ('/root', ['dir1'], ['file.txt']),
        ]
        empty_dirs = dust_buster.find_empty_dirs('/root')
        # os.walk(topdown=False) ensures child is found before parent if parent becomes empty
        self.assertEqual(empty_dirs, ['/root/dir1/empty_nested', '/root/dir1'])


    @patch('os.path.isdir')
    @patch('dust_buster.find_broken_symlinks', return_value=[])
    @patch('dust_buster.find_empty_dirs', return_value=[])
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_dust_found(self, mock_parse_args, mock_find_empty, mock_find_broken, mock_isdir):
        # Mock rationale: Simulate no broken links or empty directories.
        mock_parse_args.return_value = MagicMock(path='/test_path', delete=False)
        mock_isdir.return_value = True # Mock rationale: The path is a valid directory.

        dust_buster.main()
        output = self.mock_stdout.getvalue()
        self.assertIn("No digital dust found. Your system is sparkling clean!", output)
        mock_find_broken.assert_called_once_with('/test_path')
        mock_find_empty.assert_called_once_with('/test_path')

    @patch('os.path.isdir')
    @patch('dust_buster.find_broken_symlinks', return_value=['/test_path/broken_link'])
    @patch('dust_buster.find_empty_dirs', return_value=['/test_path/empty_dir'])
    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.unlink')
    @patch('os.rmdir')
    def test_main_list_only(self, mock_rmdir, mock_unlink, mock_parse_args, mock_find_empty, mock_find_broken, mock_isdir):
        # Mock rationale: Simulate finding broken links and empty directories, but only listing them.
        mock_parse_args.return_value = MagicMock(path='/test_path', delete=False)
        mock_isdir.return_value = True # Mock rationale: The path is a valid directory.

        dust_buster.main()
        output = self.mock_stdout.getvalue()
        self.assertIn("--- Broken Symbolic Links Found ---", output)
        self.assertIn("  - /test_path/broken_link", output)
        self.assertIn("--- Empty Directories Found ---", output)
        self.assertIn("  - /test_path/empty_dir", output)
        self.assertIn("Run with '--delete' to remove the identified items.", output)
        mock_unlink.assert_not_called() # Mock rationale: Deletion should not happen in list-only mode.
        mock_rmdir.assert_not_called() # Mock rationale: Deletion should not happen in list-only mode.

    @patch('os.path.isdir')
    @patch('dust_buster.find_broken_symlinks', return_value=['/test_path/broken_link'])
    @patch('dust_buster.find_empty_dirs', return_value=['/test_path/empty_dir'])
    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.unlink')
    @patch('os.rmdir')
    def test_main_delete_mode(self, mock_rmdir, mock_unlink, mock_parse_args, mock_find_empty, mock_find_broken, mock_isdir):
        # Mock rationale: Simulate finding broken links and empty directories, and deleting them.
        mock_parse_args.return_value = MagicMock(path='/test_path', delete=True)
        mock_isdir.return_value = True # Mock rationale: The path is a valid directory.

        dust_buster.main()
        output = self.mock_stdout.getvalue()
        self.assertIn("--- Deleting Digital Dust ---", output)
        self.assertIn("Deleted broken symlink: /test_path/broken_link", output)
        self.assertIn("Deleted empty directory: /test_path/empty_dir", output)
        self.assertIn("Digital dust cleanup complete!", output)
        mock_unlink.assert_called_once_with('/test_path/broken_link') # Mock rationale: Symlink should be deleted.
        mock_rmdir.assert_called_once_with('/test_path/empty_dir') # Mock rationale: Empty directory should be deleted.

    @patch('os.path.isdir')
    @patch('dust_buster.find_broken_symlinks', return_value=[])
    @patch('dust_buster.find_empty_dirs', return_value=[])
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_path(self, mock_parse_args, mock_find_empty, mock_find_broken, mock_isdir):
        # Mock rationale: Simulate an invalid path being provided.
        mock_parse_args.return_value = MagicMock(path='/nonexistent_path', delete=False)
        mock_isdir.return_value = False # Mock rationale: The path is not a valid directory.

        with self.assertRaises(SystemExit) as cm:
            dust_buster.main()
        self.assertEqual(cm.exception.code, 1) # Mock rationale: Expect exit code 1 for error.
        output = self.mock_stdout.getvalue()
        self.assertIn("Error: The specified path '/nonexistent_path' is not a valid directory.", output)

    @patch('os.path.isdir')
    @patch('dust_buster.find_broken_symlinks', return_value=['/test_path/broken_link'])
    @patch('dust_buster.find_empty_dirs', return_value=[])
    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.unlink', side_effect=OSError("Permission denied"))
    @patch('os.rmdir')
    def test_main_delete_error_symlink(self, mock_rmdir, mock_unlink, mock_parse_args, mock_find_empty, mock_find_broken, mock_isdir):
        # Mock rationale: Simulate an OSError during symlink deletion.
        mock_parse_args.return_value = MagicMock(path='/test_path', delete=True)
        mock_isdir.return_value = True

        dust_buster.main()
        output = self.mock_stdout.getvalue()
        self.assertIn("Error deleting symlink /test_path/broken_link: Permission denied", output)
        mock_unlink.assert_called_once_with('/test_path/broken_link')
        mock_rmdir.assert_not_called() # No empty dirs to delete

    @patch('os.path.isdir')
    @patch('dust_buster.find_broken_symlinks', return_value=[])
    @patch('dust_buster.find_empty_dirs', return_value=['/test_path/empty_dir'])
    @patch('os.unlink')
    @patch('os.rmdir', side_effect=OSError("Directory not empty"))
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_delete_error_empty_dir(self, mock_parse_args, mock_unlink, mock_rmdir, mock_find_empty, mock_find_broken, mock_isdir):
        # Mock rationale: Simulate an OSError during empty directory deletion.
        mock_parse_args.return_value = MagicMock(path='/test_path', delete=True)
        mock_isdir.return_value = True

        dust_buster.main()
        output = self.mock_stdout.getvalue()
        self.assertIn("Error deleting directory /test_path/empty_dir: Directory not empty", output)
        mock_rmdir.assert_called_once_with('/test_path/empty_dir')
        mock_unlink.assert_not_called() # No broken links to delete
