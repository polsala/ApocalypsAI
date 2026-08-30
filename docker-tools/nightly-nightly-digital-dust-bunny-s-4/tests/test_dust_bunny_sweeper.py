import unittest
from unittest.mock import patch, MagicMock
import datetime
import os
from pathlib import Path
from io import StringIO
from rich.console import Console

# Import functions from the main script
from dust_bunny_sweeper import find_old_files, find_empty_dirs, generate_report, main

class TestDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        self.test_path = Path("/mock/scan_target")
        self.now = datetime.datetime.now()

    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_find_old_files(self, mock_os_walk, mock_getmtime):
        # Mock rationale: os.walk is mocked to simulate a file system structure
        # without creating actual files, ensuring deterministic and fast tests.
        # Mock rationale: os.path.getmtime is mocked to control file modification times,
        # allowing precise testing of the 'days_old' logic without relying on system time.

        # Simulate a directory structure
        mock_os_walk.return_value = [
            (str(self.test_path), [], ["file1.txt", "file2.log"]),
            (str(self.test_path / "subdir"), [], ["file3.doc"])
        ]

        # Simulate modification times
        # file1.txt: 100 days old (should be found)
        # file2.log: 50 days old (should not be found)
        # file3.doc: 120 days old (should be found)
        mock_getmtime.side_effect = [
            (self.now - datetime.timedelta(days=100)).timestamp(), # file1.txt
            (self.now - datetime.timedelta(days=50)).timestamp(),  # file2.log
            (self.now - datetime.timedelta(days=120)).timestamp()  # file3.doc
        ]

        old_files = find_old_files(self.test_path, 90)

        self.assertEqual(len(old_files), 2)
        self.assertIn(self.test_path / "file1.txt", [f[0] for f in old_files])
        self.assertIn(self.test_path / "subdir" / "file3.doc", [f[0] for f in old_files])
        self.assertNotIn(self.test_path / "file2.log", [f[0] for f in old_files])

        # Test with no old files
        mock_getmtime.side_effect = [
            (self.now - datetime.timedelta(days=10)).timestamp(),
            (self.now - datetime.timedelta(days=20)).timestamp(),
            (self.now - datetime.timedelta(days=30)).timestamp()
        ]
        old_files = find_old_files(self.test_path, 90)
        self.assertEqual(len(old_files), 0)

    @patch('os.walk')
    def test_find_empty_dirs(self, mock_os_walk):
        # Mock rationale: os.walk is mocked to simulate various directory structures,
        # including empty and non-empty ones, without actual file system interaction.

        # Scenario 1: Root is not empty, but contains empty subdirs
        mock_os_walk.return_value = [
            (str(self.test_path), ["dir1", "dir2", "dir3"], ["file.txt"]),
            (str(self.test_path / "dir1"), [], []), # Empty
            (str(self.test_path / "dir2"), ["subdir"], []), # Not empty (has subdir)
            (str(self.test_path / "dir2" / "subdir"), [], ["subfile.txt"]), # Not empty (has file)
            (str(self.test_path / "dir3"), [], []), # Empty
        ]
        empty_dirs = find_empty_dirs(self.test_path)
        self.assertEqual(len(empty_dirs), 2)
        self.assertIn(self.test_path / "dir1", empty_dirs)
        self.assertIn(self.test_path / "dir3", empty_dirs)
        self.assertNotIn(self.test_path, empty_dirs) # Root itself is not considered empty if it has files/subdirs

        # Scenario 2: Only root, which is empty
        mock_os_walk.return_value = [
            (str(self.test_path), [], []), # Empty root
        ]
        empty_dirs = find_empty_dirs(self.test_path)
        self.assertEqual(len(empty_dirs), 0) # Root itself is excluded by the check `if Path(root) != path:`

        # Scenario 3: No empty directories
        mock_os_walk.return_value = [
            (str(self.test_path), ["dir1"], ["file.txt"]),
            (str(self.test_path / "dir1"), [], ["file2.txt"]),
        ]
        empty_dirs = find_empty_dirs(self.test_path)
        self.assertEqual(len(empty_dirs), 0)

    @patch('rich.console.Console.print')
    def test_generate_report(self, mock_console_print):
        # Mock rationale: rich.console.Console.print is mocked to capture the output
        # and verify its content without printing to the actual console during tests.
        console = Console()
        days_old = 90

        # Test case 1: Both old files and empty directories
        old_files = [
            (self.test_path / "old_file.txt", self.now - datetime.timedelta(days=100)),
            (self.test_path / "another_old.log", self.now - datetime.timedelta(days=120))
        ]
        empty_dirs = [
            self.test_path / "empty_folder_a",
            self.test_path / "empty_folder_b"
        ]

        generate_report(console, self.test_path, days_old, old_files, empty_dirs)

        # Check that print was called with expected messages
        calls = [str(call.args[0]) for call in mock_console_print.call_args_list]
        self.assertIn("✨ Digital Dust Bunny Report ✨", calls[0])
        self.assertIn(f"Found {len(old_files)} ancient scrolls (files older than {days_old} days):", calls[1])
        self.assertIn(str(self.test_path / "old_file.txt"), calls[2])
        self.assertIn(str(self.test_path / "another_old.log"), calls[3])
        self.assertIn(f"Found {len(empty_dirs)} desolate caverns (empty directories):", calls[4])
        self.assertIn(str(self.test_path / "empty_folder_a"), calls[5])
        self.assertIn(str(self.test_path / "empty_folder_b"), calls[6])
        self.assertIn(f"Total Digital Dust Bunnies: {len(old_files) + len(empty_dirs)}", calls[7])
        self.assertIn("Consider tidying up to prevent a data-apocalypse!", calls[8])

        mock_console_print.reset_mock()

        # Test case 2: No old files, no empty directories
        old_files = []
        empty_dirs = []
        generate_report(console, self.test_path, days_old, old_files, empty_dirs)
        calls = [str(call.args[0]) for call in mock_console_print.call_args_list]
        self.assertIn("No ancient scrolls", calls[1])
        self.assertIn("No desolate caverns", calls[2])
        self.assertIn("Your digital realm is impeccably clean!", calls[4])

    @patch('argparse.ArgumentParser.parse_args')
    @patch('dust_bunny_sweeper.find_old_files')
    @patch('dust_bunny_sweeper.find_empty_dirs')
    @patch('dust_bunny_sweeper.generate_report')
    @patch('rich.console.Console.print')
    def test_main_function(self, mock_console_print, mock_generate_report, mock_find_empty_dirs, mock_find_old_files, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to control CLI arguments
        # without actual command-line parsing, ensuring consistent test input.
        # Mock rationale: find_old_files, find_empty_dirs, and generate_report are mocked
        # to isolate the main function's logic and prevent side effects or complex setup.

        # Configure mock arguments
        mock_args = MagicMock()
        mock_args.path = self.test_path
        mock_args.days_old = 60
        mock_args.no_empty_dirs = False
        mock_parse_args.return_value = mock_args

        # Configure mock return values for functions
        mock_find_old_files.return_value = [
            (self.test_path / "old.txt", self.now - datetime.timedelta(days=70))
        ]
        mock_find_empty_dirs.return_value = [
            self.test_path / "empty_dir"
        ]

        main()

        mock_console_print.assert_any_call(Text(f"⚠️ Initiating Digital Dust Bunny Sweep in {self.test_path}... ⚠️", style="bold blue"))
        mock_find_old_files.assert_called_once_with(self.test_path, 60)
        mock_find_empty_dirs.assert_called_once_with(self.test_path)
        mock_generate_report.assert_called_once()
        self.assertEqual(mock_generate_report.call_args[0][2], 60) # Check days_old passed

        # Test with --no_empty_dirs
        mock_find_old_files.reset_mock()
        mock_find_empty_dirs.reset_mock()
        mock_generate_report.reset_mock()
        mock_args.no_empty_dirs = True
        main()
        mock_find_old_files.assert_called_once()
        mock_find_empty_dirs.assert_not_called()
        mock_generate_report.assert_called_once()

        # Test with days_old = 0 (should skip old files scan)
        mock_find_old_files.reset_mock()
        mock_find_empty_dirs.reset_mock()
        mock_generate_report.reset_mock()
        mock_args.days_old = 0
        mock_args.no_empty_dirs = False
        main()
        mock_find_old_files.assert_not_called()
        mock_find_empty_dirs.assert_called_once()
        mock_generate_report.assert_called_once()


if __name__ == '__main__':
    unittest.main()
