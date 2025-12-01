import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
from pathlib import Path

# Add the src directory to the path for importing quibbler
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
import quibbler

class TestQuibbler(unittest.TestCase):

    def setUp(self):
        self.canonical_files = ["README.md", "LICENSE", "AGENTS.md", ".gitignore"]
        self.text_file_extensions = [
            ".py", ".md", ".txt", ".yml", ".yaml", ".json", ".sh", ".css", ".html",
            ".js", ".ts", ".java", ".c", ".cpp", ".h", ".hpp", ".xml", ".toml"
        ]
        self.root_dir = Path("/mock/repo")

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.stat')
    def test_no_quirks(self, mock_stat, mock_is_file, mock_open_func, mock_os_walk):
        # Mock rationale: Simulate a clean repository with no quirks.
        # os.walk: Provides the directory structure.
        # open: Provides file content.
        # Path.is_file: Confirms paths are files.
        # Path.stat: Provides file size for empty file check.

        mock_os_walk.return_value = [
            (str(self.root_dir), [], ["README.md", "main.py"]),
            (str(self.root_dir / "docs"), [], ["guide.md"])
        ]
        
        # Mock file content for open
        def mock_open_side_effect(file_path, mode='r', encoding='utf-8'):
            if "README.md" in file_path:
                return mock_open(read_data="This is a README.\n").return_value
            elif "main.py" in file_path:
                return mock_open(read_data="print('Hello')\n").return_value
            elif "guide.md" in file_path:
                return mock_open(read_data="Guide content.\n").return_value
            raise FileNotFoundError
        mock_open_func.side_effect = mock_open_side_effect

        # Mock Path.is_file and Path.stat
        mock_is_file.return_value = True
        mock_stat.return_value = MagicMock(st_size=100) # Non-empty

        quirks = quibbler.scan_directory(self.root_dir, self.canonical_files, self.text_file_extensions)

        self.assertFalse(quirks["trailing_whitespace"])
        self.assertFalse(quirks["inconsistent_casing"])
        self.assertFalse(quirks["empty_files"])

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.stat')
    def test_trailing_whitespace_quirk(self, mock_stat, mock_is_file, mock_open_func, mock_os_walk):
        # Mock rationale: Simulate a file with trailing whitespace.
        mock_os_walk.return_value = [
            (str(self.root_dir), [], ["bad_file.py"])
        ]
        mock_open_func.return_value.read.return_value = "line 1 \nline 2\n"
        mock_is_file.return_value = True
        mock_stat.return_value = MagicMock(st_size=100)

        quirks = quibbler.scan_directory(self.root_dir, self.canonical_files, self.text_file_extensions)

        self.assertEqual(len(quirks["trailing_whitespace"]), 1)
        self.assertIn(f"{self.root_dir}/bad_file.py:1: Trailing whitespace: 'line 1 '", quirks["trailing_whitespace"][0])
        self.assertFalse(quirks["inconsistent_casing"])
        self.assertFalse(quirks["empty_files"])

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.stat')
    def test_inconsistent_casing_quirk(self, mock_stat, mock_is_file, mock_open_func, mock_os_walk):
        # Mock rationale: Simulate a file with inconsistent casing (e.g., 'readme.md' instead of 'README.md').
        mock_os_walk.return_value = [
            (str(self.root_dir), [], ["readme.md"])
        ]
        mock_open_func.return_value.read.return_value = "content"
        mock_is_file.return_value = True
        mock_stat.return_value = MagicMock(st_size=100)

        quirks = quibbler.scan_directory(self.root_dir, self.canonical_files, self.text_file_extensions)

        self.assertEqual(len(quirks["inconsistent_casing"]), 1)
        self.assertIn(f"{self.root_dir}/readme.md: Expected 'README.md', found 'readme.md'", quirks["inconsistent_casing"][0])
        self.assertFalse(quirks["trailing_whitespace"])
        self.assertFalse(quirks["empty_files"])

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.stat')
    def test_empty_file_quirk(self, mock_stat, mock_is_file, mock_open_func, mock_os_walk):
        # Mock rationale: Simulate an empty file.
        mock_os_walk.return_value = [
            (str(self.root_dir), [], ["empty.txt"])
        ]
        mock_open_func.return_value.read.return_value = "" # Empty content
        mock_is_file.return_value = True
        mock_stat.return_value = MagicMock(st_size=0) # Zero size

        quirks = quibbler.scan_directory(self.root_dir, self.canonical_files, self.text_file_extensions)

        self.assertEqual(len(quirks["empty_files"]), 1)
        self.assertIn(f"{self.root_dir}/empty.txt", quirks["empty_files"][0])
        self.assertFalse(quirks["trailing_whitespace"])
        self.assertFalse(quirks["inconsistent_casing"])

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.stat')
    def test_multiple_quirks(self, mock_stat, mock_is_file, mock_open_func, mock_os_walk):
        # Mock rationale: Simulate a scenario with multiple types of quirks.
        mock_os_walk.return_value = [
            (str(self.root_dir), [], ["readme.md", "bad_code.py", "empty.txt"])
        ]

        def mock_open_side_effect(file_path, mode='r', encoding='utf-8'):
            if "readme.md" in file_path:
                return mock_open(read_data="README content.\n").return_value
            elif "bad_code.py" in file_path:
                return mock_open(read_data="import os \nprint('hello')  \n").return_value
            elif "empty.txt" in file_path:
                return mock_open(read_data="").return_value
            raise FileNotFoundError
        mock_open_func.side_effect = mock_open_side_effect

        # Mock Path.is_file and Path.stat
        def mock_stat_side_effect(path):
            if "readme.md" in str(path):
                return MagicMock(st_size=20)
            elif "bad_code.py" in str(path):
                return MagicMock(st_size=30)
            elif "empty.txt" in str(path):
                return MagicMock(st_size=0)
            return MagicMock(st_size=100) # Default for others
        mock_stat.side_effect = mock_stat_side_effect
        mock_is_file.return_value = True

        quirks = quibbler.scan_directory(self.root_dir, self.canonical_files, self.text_file_extensions)

        self.assertEqual(len(quirks["trailing_whitespace"]), 1)
        self.assertIn(f"{self.root_dir}/bad_code.py:2: Trailing whitespace: 'print('hello')  '", quirks["trailing_whitespace"][0])

        self.assertEqual(len(quirks["inconsistent_casing"]), 1)
        self.assertIn(f"{self.root_dir}/readme.md: Expected 'README.md', found 'readme.md'", quirks["inconsistent_casing"][0])

        self.assertEqual(len(quirks["empty_files"]), 1)
        self.assertIn(f"{self.root_dir}/empty.txt", quirks["empty_files"][0])

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('quibbler.scan_directory')
    @patch('pathlib.Path.is_dir')
    def test_main_no_quirks_exit_0(self, mock_is_dir, mock_scan_directory, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Test the main function's behavior when no quirks are found.
        # argparse.ArgumentParser.parse_args: Simulate command-line arguments.
        # quibbler.scan_directory: Control the output of the scan.
        # Path.is_dir: Ensure the directory is considered valid.
        # sys.stdout/stderr: Capture print output.

        mock_parse_args.return_value = MagicMock(directory="/mock/repo")
        mock_is_dir.return_value = True
        mock_scan_directory.return_value = {
            "trailing_whitespace": [],
            "inconsistent_casing": [],
            "empty_files": []
        }

        with self.assertRaises(SystemExit) as cm:
            quibbler.main()
        self.assertEqual(cm.exception.code, 0)
        mock_stdout.assert_called()
        self.assertIn("No quantum quirks detected! Your repository is pristine.", mock_stdout.call_args[0][0])

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('quibbler.scan_directory')
    @patch('pathlib.Path.is_dir')
    def test_main_with_quirks_exit_1(self, mock_is_dir, mock_scan_directory, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Test the main function's behavior when quirks are found.
        mock_parse_args.return_value = MagicMock(directory="/mock/repo")
        mock_is_dir.return_value = True
        mock_scan_directory.return_value = {
            "trailing_whitespace": ["/mock/repo/file.py:1: Trailing whitespace: 'line '"],
            "inconsistent_casing": [],
            "empty_files": []
        }

        with self.assertRaises(SystemExit) as cm:
            quibbler.main()
        self.assertEqual(cm.exception.code, 1)
        mock_stdout.assert_called()
        self.assertIn("Quantum quirks detected!", mock_stdout.call_args[0][0])
        self.assertIn("Trailing Whitespace", mock_stdout.call_args[0][0])

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('pathlib.Path.is_dir')
    def test_main_invalid_directory_exit_1(self, mock_is_dir, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Test the main function's behavior when an invalid directory is provided.
        mock_parse_args.return_value = MagicMock(directory="/nonexistent/repo")
        mock_is_dir.return_value = False

        with self.assertRaises(SystemExit) as cm:
            quibbler.main()
        self.assertEqual(cm.exception.code, 1)
        mock_stdout.assert_called()
        self.assertIn("Error: Directory '/nonexistent/repo' not found.", mock_stdout.call_args[0][0])


if __name__ == '__main__':
    unittest.main()
