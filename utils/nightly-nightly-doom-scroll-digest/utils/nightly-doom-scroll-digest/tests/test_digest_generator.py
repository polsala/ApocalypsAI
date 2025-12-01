import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
from datetime import datetime

# Import the functions to be tested
from src.digest_generator import (
    get_file_state,
    load_previous_state,
    save_current_state,
    generate_digest_report,
    main
)

class TestDigestGenerator(unittest.TestCase):

    def setUp(self):
        self.root_dir = '/mock/project'
        self.state_file = os.path.join(self.root_dir, '.doom_scroll_state.json')
        self.output_file = '/mock/reports/digest.md'

    @patch('os.walk')
    @patch('os.stat')
    @patch('os.path.relpath', side_effect=lambda path, start: path.replace(start + '/', '')) # Mock relpath for testing
    def test_get_file_state(self, mock_relpath, mock_stat, mock_walk):
        # Mock rationale: os.walk is used to traverse the directory structure.
        # os.stat is used to get file metadata (mtime, size).
        # os.path.relpath is used to normalize file paths relative to the root.
        mock_walk.return_value = [
            (self.root_dir, [], ['file1.txt', 'file2.py']),
            (os.path.join(self.root_dir, 'subdir'), [], ['subfile.md'])
        ]

        # Mock stat results for each file
        mock_stat.side_effect = [
            MagicMock(st_mtime=1678886400.0, st_size=100), # file1.txt
            MagicMock(st_mtime=1678886401.0, st_size=200), # file2.py
            MagicMock(st_mtime=1678886402.0, st_size=300)  # subfile.md
        ]

        expected_state = {
            'file1.txt': {'mtime': 1678886400.0, 'size': 100},
            'file2.py': {'mtime': 1678886401.0, 'size': 200},
            'subdir/subfile.md': {'mtime': 1678886402.0, 'size': 300}
        }

        state = get_file_state(self.root_dir)
        self.assertEqual(state, expected_state)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_previous_state_exists(self, mock_json_load, mock_file_open, mock_exists):
        # Mock rationale: os.path.exists checks if the state file exists.
        # builtins.open is used to open the file.
        # json.load is used to parse the JSON content.
        mock_json_load.return_value = {'file.txt': {'mtime': 123, 'size': 456}}
        state = load_previous_state(self.state_file)
        self.assertEqual(state, {'file.txt': {'mtime': 123, 'size': 456}})
        mock_exists.assert_called_once_with(self.state_file)
        mock_file_open.assert_called_once_with(self.state_file, 'r')

    @patch('os.path.exists', return_value=False)
    def test_load_previous_state_not_exists(self, mock_exists):
        # Mock rationale: os.path.exists checks if the state file exists.
        state = load_previous_state(self.state_file)
        self.assertEqual(state, {})
        mock_exists.assert_called_once_with(self.state_file)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_current_state(self, mock_json_dump, mock_file_open):
        # Mock rationale: builtins.open is used to open the file.
        # json.dump is used to serialize and write the JSON content.
        current_state = {'file.txt': {'mtime': 123, 'size': 456}}
        save_current_state(self.state_file, current_state)
        mock_file_open.assert_called_once_with(self.state_file, 'w')
        mock_json_dump.assert_called_once_with(current_state, mock_file_open(), indent=2)

    @patch('datetime.now')
    def test_generate_digest_report_no_changes(self, mock_datetime_now):
        # Mock rationale: datetime.now is used to get the current date for the report header.
        mock_datetime_now.return_value = datetime(2023, 10, 27)
        previous_state = {
            'file1.txt': {'mtime': 1678886400.0, 'size': 100}
        }
        current_state = {
            'file1.txt': {'mtime': 1678886400.0, 'size': 100}
        }
        report = generate_digest_report(self.root_dir, previous_state, current_state)
        self.assertIn("# Doom Scroll Digest - 2023-10-27", report)
        self.assertIn("*No significant changes detected.*", report)
        self.assertNotIn("New Files", report)
        self.assertNotIn("Modified Files", report)
        self.assertNotIn("Deleted Files", report)

    @patch('datetime.now')
    def test_generate_digest_report_with_changes(self, mock_datetime_now):
        # Mock rationale: datetime.now is used to get the current date for the report header.
        mock_datetime_now.return_value = datetime(2023, 10, 27)
        previous_state = {
            'file1.txt': {'mtime': 1678886400.0, 'size': 100},
            'old_file.txt': {'mtime': 1678886300.0, 'size': 50}
        }
        current_state = {
            'file1.txt': {'mtime': 1678886500.0, 'size': 101}, # Modified
            'new_file.txt': {'mtime': 1678886600.0, 'size': 200} # New
        }
        report = generate_digest_report(self.root_dir, previous_state, current_state)

        self.assertIn("# Doom Scroll Digest - 2023-10-27", report)
        self.assertIn("## Changes Detected in /mock/project", report)
        self.assertIn("### New Files:", report)
        self.assertIn("- `new_file.txt`", report)
        self.assertIn("### Modified Files:", report)
        self.assertIn("- `file1.txt` (Modified on 2023-10-27 00:01:40)", report)
        self.assertIn("### Deleted Files:", report)
        self.assertIn("- `old_file.txt`", report)
        self.assertNotIn("*No significant changes detected.*", report)

    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('os.path.isdir', return_value=True)
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.digest_generator.load_previous_state', return_value={})
    @patch('src.digest_generator.get_file_state', return_value={'file.txt': {'mtime': 1, 'size': 1}})
    @patch('src.digest_generator.generate_digest_report', return_value='Mock Report Content')
    @patch('src.digest_generator.save_current_state')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_execution(self, mock_print, mock_parse_args, mock_save_state, mock_generate_report, mock_get_state, mock_load_state, mock_open, mock_makedirs, mock_isdir, mock_abspath):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to control CLI arguments.
        # os.path.abspath is mocked to simplify path handling in tests.
        # os.path.isdir is mocked to simulate a valid directory.
        # os.makedirs is mocked to prevent actual directory creation.
        # builtins.open is mocked to prevent actual file I/O for report output.
        # load_previous_state, get_file_state, generate_digest_report, save_current_state are mocked
        # to isolate the main function's logic flow and prevent side effects.
        # builtins.print is mocked to capture output.

        mock_parse_args.return_value = MagicMock(
            path=self.root_dir,
            output_file=self.output_file,
            state_file=None
        )

        main()

        mock_abspath.assert_any_call(self.root_dir)
        mock_abspath.assert_any_call(self.output_file)
        mock_isdir.assert_called_once_with(self.root_dir)
        mock_load_state.assert_called_once_with(self.state_file)
        mock_get_state.assert_called_once_with(self.root_dir)
        mock_generate_report.assert_called_once()
        mock_makedirs.assert_called_once_with(os.path.dirname(self.output_file), exist_ok=True)
        mock_open.assert_called_once_with(self.output_file, 'w')
        mock_open().write.assert_called_once_with('Mock Report Content')
        mock_save_state.assert_called_once()
        mock_print.assert_any_call(f"Doom Scroll Digest generated and saved to '{self.output_file}'")
        mock_print.assert_any_call(f"Current state saved to '{self.state_file}'")

    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('os.path.isdir', return_value=False)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_exit, mock_print, mock_parse_args, mock_isdir, mock_abspath):
        # Mock rationale: os.path.abspath is mocked to simplify path handling in tests.
        # os.path.isdir is mocked to simulate an invalid directory.
        # argparse.ArgumentParser.parse_args is mocked to control CLI arguments.
        # builtins.print is mocked to capture output.
        # sys.exit is mocked to prevent actual program exit during test.

        mock_parse_args.return_value = MagicMock(
            path=self.root_dir,
            output_file=self.output_file,
            state_file=None
        )

        main()

        mock_print.assert_called_once_with(f"Error: Directory not found at '{self.root_dir}'")
        mock_exit.assert_called_once_with(1)
