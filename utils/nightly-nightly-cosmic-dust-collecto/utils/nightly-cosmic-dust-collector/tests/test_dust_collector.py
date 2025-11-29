import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add the src directory to the path to allow importing dust_collector
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
import dust_collector

class TestCosmicDustCollector(unittest.TestCase):

    @patch('os.walk')
    @patch('pathlib.Path.stat')
    @patch('pathlib.Path.is_dir')
    def test_list_action_dry_run(self, mock_is_dir, mock_stat, mock_walk):
        # Mock rationale: Simulate a directory structure and file sizes without touching the filesystem.
        # os.walk: Provides the directory and file structure.
        # pathlib.Path.stat: Returns file size for specific paths.
        # pathlib.Path.is_dir: Confirms the root path is a directory.
        mock_is_dir.return_value = True
        mock_walk.return_value = [
            ('/test_root', [], ['small_file.txt', 'large_file.log']),
            ('/test_root/subdir', [], ['empty.dat', 'medium.tmp'])
        ]
        
        # Mock stat for specific files
        mock_stat.side_effect = lambda: MagicMock(st_size=100) if 'small_file.txt' in str(mock_stat.mock_calls[-1].args[0]) else \
                                      MagicMock(st_size=5000) if 'large_file.log' in str(mock_stat.mock_calls[-1].args[0]) else \
                                      MagicMock(st_size=0) if 'empty.dat' in str(mock_stat.mock_calls[-1].args[0]) else \
                                      MagicMock(st_size=1500)

        root_path = Path('/test_root')
        threshold = 1024 # 1KB
        action = 'list'
        archive_dir = None
        dry_run = True

        results = dust_collector.collect_cosmic_dust(root_path, threshold, action, archive_dir, dry_run)

        self.assertIn("Found dust: /test_root/small_file.txt (100 bytes)", results)
        self.assertIn("Found dust: /test_root/subdir/empty.dat (0 bytes)", results)
        self.assertNotIn("large_file.log", results)
        self.assertNotIn("medium.tmp", results)
        self.assertEqual(len(results), 2)

    @patch('os.walk')
    @patch('pathlib.Path.stat')
    @patch('pathlib.Path.is_dir')
    @patch('pathlib.Path.unlink')
    def test_delete_action(self, mock_unlink, mock_is_dir, mock_stat, mock_walk):
        # Mock rationale: Simulate file deletion without actually deleting files.
        # pathlib.Path.unlink: Checks if delete was called.
        mock_is_dir.return_value = True
        mock_walk.return_value = [
            ('/test_root', [], ['dust_to_delete.txt', 'keep_me.txt'])
        ]
        mock_stat.side_effect = lambda: MagicMock(st_size=50) if 'dust_to_delete.txt' in str(mock_stat.mock_calls[-1].args[0]) else \
                                      MagicMock(st_size=2000)

        root_path = Path('/test_root')
        threshold = 100 # bytes
        action = 'delete'
        archive_dir = None
        dry_run = False

        results = dust_collector.collect_cosmic_dust(root_path, threshold, action, archive_dir, dry_run)

        self.assertIn("Deleted: /test_root/dust_to_delete.txt", results)
        self.assertNotIn("keep_me.txt", results)
        mock_unlink.assert_called_once_with()
        self.assertEqual(mock_unlink.call_args[0][0], Path('/test_root/dust_to_delete.txt'))

    @patch('os.walk')
    @patch('pathlib.Path.stat')
    @patch('pathlib.Path.is_dir')
    @patch('shutil.move')
    @patch('pathlib.Path.mkdir')
    def test_archive_action(self, mock_mkdir, mock_move, mock_is_dir, mock_stat, mock_walk):
        # Mock rationale: Simulate archiving files without actual file movement or directory creation.
        # shutil.move: Checks if move was called with correct source/destination.
        # pathlib.Path.mkdir: Prevents actual directory creation.
        mock_is_dir.return_value = True
        mock_walk.return_value = [
            ('/test_root', [], ['archive_me.log', 'big_file.zip'])
        ]
        mock_stat.side_effect = lambda: MagicMock(st_size=200) if 'archive_me.log' in str(mock_stat.mock_calls[-1].args[0]) else \
                                      MagicMock(st_size=5000)

        root_path = Path('/test_root')
        threshold = 1024 # bytes
        action = 'archive'
        archive_dir = Path('/archive_dest')
        dry_run = False

        results = dust_collector.collect_cosmic_dust(root_path, threshold, action, archive_dir, dry_run)

        self.assertIn("Archived: /test_root/archive_me.log -> /archive_dest/archive_me.log", results)
        self.assertNotIn("big_file.zip", results)
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_move.assert_called_once_with(Path('/test_root/archive_me.log'), Path('/archive_dest/archive_me.log'))

    @patch('os.walk')
    @patch('pathlib.Path.stat')
    @patch('pathlib.Path.is_dir')
    def test_no_dust_found(self, mock_is_dir, mock_stat, mock_walk):
        # Mock rationale: Simulate a directory with no files matching the criteria.
        mock_is_dir.return_value = True
        mock_walk.return_value = [
            ('/test_root', [], ['large_file.txt', 'another_large.log'])
        ]
        mock_stat.side_effect = lambda: MagicMock(st_size=2000) # All files are large

        root_path = Path('/test_root')
        threshold = 1000
        action = 'list'
        archive_dir = None
        dry_run = True

        results = dust_collector.collect_cosmic_dust(root_path, threshold, action, archive_dir, dry_run)

        self.assertEqual(len(results), 1)
        self.assertIn("No cosmic dust found in '/test_root' below 1000 bytes.", results)

    @patch('pathlib.Path.is_dir')
    def test_invalid_root_path(self, mock_is_dir):
        # Mock rationale: Test error handling for non-existent root paths.
        mock_is_dir.return_value = False

        root_path = Path('/non_existent_dir')
        threshold = 100
        action = 'list'
        archive_dir = None
        dry_run = True

        results = dust_collector.collect_cosmic_dust(root_path, threshold, action, archive_dir, dry_run)

        self.assertIn("Error: Path '/non_existent_dir' is not a valid directory.", results)

    @patch('os.walk')
    @patch('pathlib.Path.stat')
    @patch('pathlib.Path.is_dir')
    def test_os_error_handling(self, mock_is_dir, mock_stat, mock_walk):
        # Mock rationale: Simulate an OSError (e.g., permission denied) during file stat.
        mock_is_dir.return_value = True
        mock_walk.return_value = [
            ('/test_root', [], ['unreadable_file.txt'])
        ]
        mock_stat.side_effect = OSError("Permission denied")

        root_path = Path('/test_root')
        threshold = 1000
        action = 'list'
        archive_dir = None
        dry_run = True

        results = dust_collector.collect_cosmic_dust(root_path, threshold, action, archive_dir, dry_run)

        self.assertIn("Warning: Could not process /test_root/unreadable_file.txt: Permission denied", results)

    @patch('sys.exit')
    @patch('builtins.print')
    @patch('dust_collector.collect_cosmic_dust')
    def test_main_exit_codes(self, mock_collect_cosmic_dust, mock_print, mock_exit):
        # Mock rationale: Test the main function's exit codes based on collect_cosmic_dust results.
        # sys.exit: Prevents actual program exit during testing.
        # builtins.print: Captures output to stdout.
        # dust_collector.collect_cosmic_dust: Provides predefined results.

        # Test case 1: Success (dust found and action taken)
        mock_collect_cosmic_dust.return_value = ["Deleted: /path/to/dust.txt"]
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path=Path('/test'), threshold=100, action='delete', archive_dir=None, dry_run=False
        )):
            dust_collector.main()
            mock_exit.assert_called_with(0)
            mock_exit.reset_mock()

        # Test case 2: No-op (no dust found)
        mock_collect_cosmic_dust.return_value = ["No cosmic dust found in '/test' below 100 bytes."]
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path=Path('/test'), threshold=100, action='list', archive_dir=None, dry_run=True
        )):
            dust_collector.main()
            mock_exit.assert_called_with(2)
            mock_exit.reset_mock()

        # Test case 3: Failure (error message)
        mock_collect_cosmic_dust.return_value = ["Error: Path '/invalid' is not a valid directory."]
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path=Path('/invalid'), threshold=100, action='list', archive_dir=None, dry_run=True
        )):
            dust_collector.main()
            mock_exit.assert_called_with(1)
            mock_exit.reset_mock()

        # Test case 4: Warning (not a critical failure)
        mock_collect_cosmic_dust.return_value = ["Warning: Could not process /path/to/file: Permission denied"]
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path=Path('/test'), threshold=100, action='list', archive_dir=None, dry_run=True
        )):
            dust_collector.main()
            mock_exit.assert_called_with(0)
            mock_exit.reset_mock()

        # Test case 5: Archive action without archive_dir
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path=Path('/test'), threshold=100, action='archive', archive_dir=None, dry_run=False
        )):
            dust_collector.main()
            mock_exit.assert_called_with(1)
            mock_exit.reset_mock()

if __name__ == '__main__':
    unittest.main()
