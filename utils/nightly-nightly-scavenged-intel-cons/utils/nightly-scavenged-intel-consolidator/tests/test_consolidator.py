import unittest
import os
import sys
from unittest.mock import patch, mock_open

# Mock rationale: We need to simulate file system operations (listing directories,
# reading files) without actually touching the disk. This ensures tests are fast,
# deterministic, and don't rely on external state or create temporary files.
# `os.listdir` is mocked to control which files appear in a directory.
# `builtins.open` is mocked to control the content of files when they are 'read'.
# `sys.stdout` and `sys.stderr` are mocked to capture printed output for assertions.

# Add parent directory to path to allow direct import from src/ for self-contained utility
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from consolidator import consolidate_intel
sys.path.pop(0)

class TestConsolidator(unittest.TestCase):

    @patch('os.path.isdir', return_value=True)
    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_empty_directory(self, mock_stdout, mock_file_open, mock_listdir, mock_isdir):
        # Mock rationale: Simulate an empty directory by having os.listdir return an empty list.
        mock_listdir.return_value = []
        consolidate_intel('/fake/path')
        self.assertIn("No .txt files found", mock_stdout.getvalue())
        mock_file_open.assert_not_called()

    @patch('os.path.isdir', return_value=True)
    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_no_intel_files(self, mock_stdout, mock_file_open, mock_listdir, mock_isdir):
        # Mock rationale: Simulate files that exist but contain no relevant intel prefixes.
        mock_listdir.return_value = ['report.txt', 'log.txt']
        mock_file_open.side_effect = [
            mock_open(read_data="Just some random text.\nAnother line here.\n").return_value,
            mock_open(read_data="No tips or locations.\nOnly plain text.\n").return_value
        ]
        consolidate_intel('/fake/path')
        output = mock_stdout.getvalue()
        self.assertIn("[ TIPS ]\n- No intel found for this category.", output)
        self.assertIn("[ LOCATIONS ]\n- No intel found for this category.", output)
        self.assertIn("[ WARNINGS ]\n- No intel found for this category.", output)
        self.assertEqual(mock_file_open.call_count, 2)

    @patch('os.path.isdir', return_value=True)
    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_single_file_multiple_intel(self, mock_stdout, mock_file_open, mock_listdir, mock_isdir):
        # Mock rationale: Simulate a single file with various types of intel.
        mock_listdir.return_value = ['notes.txt']
        mock_file_open.return_value.read.return_value = (
            "TIP: Always carry a multi-tool.\n"
            "LOCATION: Abandoned bunker under the old bridge.\n"
            "WARNING: Beware of radiation pockets near the power plant.\n"
            "Just some other text.\n"
            "TIP: Check your water supply daily.\n"
        )
        consolidate_intel('/fake/path')
        output = mock_stdout.getvalue()
        self.assertIn("[ TIPS ]\n- Always carry a multi-tool.\n- Check your water supply daily.", output)
        self.assertIn("[ LOCATIONS ]\n- Abandoned bunker under the old bridge.", output)
        self.assertIn("[ WARNINGS ]\n- Beware of radiation pockets near the power plant.", output)
        self.assertEqual(mock_file_open.call_count, 1)

    @patch('os.path.isdir', return_value=True)
    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_multiple_files_with_duplicates(self, mock_stdout, mock_file_open, mock_listdir, mock_isdir):
        # Mock rationale: Simulate multiple files, some containing duplicate intel, to ensure de-duplication works.
        mock_listdir.return_value = ['file1.txt', 'file2.txt', 'file3.txt']
        mock_file_open.side_effect = [
            mock_open(read_data="TIP: Stay hydrated.\nLOCATION: River bend.\nWARNING: Mutants ahead.\n").return_value,
            mock_open(read_data="TIP: Stay hydrated.\nTIP: Find shelter.\nLOCATION: River bend.\n").return_value,
            mock_open(read_data="WARNING: Mutants ahead.\nTIP: Always carry a map.\n").return_value
        ]
        consolidate_intel('/fake/path')
        output = mock_stdout.getvalue()

        # Check for de-duplication and sorting
        self.assertIn("[ TIPS ]\n- Always carry a map.\n- Find shelter.\n- Stay hydrated.", output)
        self.assertIn("[ LOCATIONS ]\n- River bend.", output)
        self.assertIn("[ WARNINGS ]\n- Mutants ahead.", output)
        self.assertEqual(mock_file_open.call_count, 3)

    @patch('os.path.isdir', return_value=False)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_invalid_directory(self, mock_stderr, mock_isdir):
        # Mock rationale: Simulate an invalid directory path.
        consolidate_intel('/nonexistent/path')
        self.assertIn("Error: Directory not found", mock_stderr.getvalue())

    @patch('os.path.isdir', return_value=True)
    @patch('os.listdir', return_value=['corrupt.txt'])
    @patch('builtins.open')
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_file_io_error(self, mock_stdout, mock_stderr, mock_file_open, mock_listdir, mock_isdir):
        # Mock rationale: Simulate an IOError when trying to open a file.
        mock_file_open.side_effect = IOError("Permission denied")
        consolidate_intel('/fake/path')
        self.assertIn("Warning: Could not read file", mock_stderr.getvalue())
        # Ensure it still prints the report structure even if files fail
        self.assertIn("--- Consolidated Scavenged Intel ---", mock_stdout.getvalue())

    @patch('os.path.isdir', return_value=True)
    @patch('os.listdir', return_value=['bad_encoding.txt'])
    @patch('builtins.open')
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_file_unicode_error(self, mock_stdout, mock_stderr, mock_file_open, mock_listdir, mock_isdir):
        # Mock rationale: Simulate a UnicodeDecodeError for a file with bad encoding.
        mock_file_open.return_value.__enter__.return_value.__iter__.side_effect = UnicodeDecodeError("utf-8", b'\x80', 0, 1, "invalid start byte")
        consolidate_intel('/fake/path')
        self.assertIn("Warning: Could not decode file", mock_stderr.getvalue())
        # Ensure it still prints the report structure even if files fail
        self.assertIn("--- Consolidated Scavenged Intel ---", mock_stdout.getvalue())

    @patch('os.path.isdir', return_value=True)
    @patch('os.listdir', return_value=['mixed_case.txt'])
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_case_sensitivity_of_prefixes(self, mock_stdout, mock_file_open, mock_listdir, mock_isdir):
        # Mock rationale: Test that the prefixes are matched case-sensitively as per current implementation.
        mock_file_open.return_value.read.return_value = (
            "tip: lowercase tip.\n"
            "TIP: Uppercase tip.\n"
            "Location: mixed case location.\n"
            "LOCATION: Correct location.\n"
        )
        consolidate_intel('/fake/path')
        output = mock_stdout.getvalue()
        self.assertIn("[ TIPS ]\n- Uppercase tip.", output)
        self.assertNotIn("lowercase tip", output)
        self.assertIn("[ LOCATIONS ]\n- Correct location.", output)
        self.assertNotIn("mixed case location", output)

    @patch('os.path.isdir', return_value=True)
    @patch('os.listdir', return_value=['empty_lines.txt'])
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_empty_lines_and_whitespace(self, mock_stdout, mock_file_open, mock_listdir, mock_isdir):
        # Mock rationale: Test how the consolidator handles empty lines and extra whitespace around intel.
        mock_file_open.return_value.read.return_value = (
            "\n"
            "  TIP:   Trimmed tip.  \n"
            "\n"
            "LOCATION:Another location.\n"
            "\n"
        )
        consolidate_intel('/fake/path')
        output = mock_stdout.getvalue()
        self.assertIn("[ TIPS ]\n- Trimmed tip.", output)
        self.assertIn("[ LOCATIONS ]\n- Another location.", output)
        # Ensure no empty lines are added as intel
        self.assertNotIn("- \n", output)


if __name__ == '__main__':
    unittest.main()
