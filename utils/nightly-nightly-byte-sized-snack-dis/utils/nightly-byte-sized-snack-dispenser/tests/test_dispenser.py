import unittest
import os
import sys
import io
from unittest.mock import patch, mock_open, MagicMock
from src.dispenser import (
    get_first_n_lines,
    get_last_n_lines,
    get_random_n_lines,
    get_grep_lines,
    main
)

class TestDispenser(unittest.TestCase):

    def setUp(self):
        self.test_content = (
            "Line 1: The quick brown fox\n"
            "Line 2: Jumps over the lazy dog\n"
            "Line 3: With a big smile\n"
            "Line 4: And a wagging tail\n"
            "Line 5: The end is near\n"
        )
        self.mock_file_path = "mock_file.txt"

    @patch("builtins.open", new_callable=mock_open)
    def test_get_first_n_lines(self, mock_file):
        # Mock rationale: Simulate file content for reading.
        mock_file.return_value.read.return_value = self.test_content
        mock_file.return_value.__iter__.return_value = iter(self.test_content.splitlines(keepends=True))

        # Test N=3
        result = list(get_first_n_lines(self.mock_file_path, 3))
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "Line 1: The quick brown fox\n")
        self.assertEqual(result[2], "Line 3: With a big smile\n")

        # Test N > total lines
        result = list(get_first_n_lines(self.mock_file_path, 10))
        self.assertEqual(len(result), 5) # Should return all lines

        # Test N=0
        result = list(get_first_n_lines(self.mock_file_path, 0))
        self.assertEqual(len(result), 0)

        # Test empty file
        mock_file.return_value.__iter__.return_value = iter([])
        result = list(get_first_n_lines(self.mock_file_path, 3))
        self.assertEqual(len(result), 0)

    @patch("builtins.open", new_callable=mock_open)
    def test_get_last_n_lines(self, mock_file):
        # Mock rationale: Simulate file content for reading.
        mock_file.return_value.read.return_value = self.test_content
        mock_file.return_value.__iter__.return_value = iter(self.test_content.splitlines(keepends=True))

        # Test N=3
        result = list(get_last_n_lines(self.mock_file_path, 3))
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "Line 3: With a big smile\n")
        self.assertEqual(result[2], "Line 5: The end is near\n")

        # Test N > total lines
        result = list(get_last_n_lines(self.mock_file_path, 10))
        self.assertEqual(len(result), 5) # Should return all lines

        # Test N=0
        result = list(get_last_n_lines(self.mock_file_path, 0))
        self.assertEqual(len(result), 0)

        # Test empty file
        mock_file.return_value.__iter__.return_value = iter([])
        result = list(get_last_n_lines(self.mock_file_path, 3))
        self.assertEqual(len(result), 0)

    @patch("builtins.open", new_callable=mock_open)
    @patch("random.sample")
    def test_get_random_n_lines(self, mock_random_sample, mock_file):
        # Mock rationale: Simulate file content for reading.
        mock_file.return_value.read.return_value = self.test_content
        lines = self.test_content.splitlines(keepends=True)
        mock_file.return_value.__iter__.return_value = iter(lines)

        # Mock rationale: Ensure deterministic random sampling for tests.
        mock_random_sample.return_value = [lines[0], lines[2]] # Simulate picking Line 1 and Line 3

        # Test N=2
        result = list(get_random_n_lines(self.mock_file_path, 2))
        self.assertEqual(len(result), 2)
        self.assertIn("Line 1: The quick brown fox\n", result)
        self.assertIn("Line 3: With a big smile\n", result)
        mock_random_sample.assert_called_once_with(lines, 2)
        mock_random_sample.reset_mock() # Reset for next test

        # Test N > total lines
        mock_random_sample.return_value = lines # Simulate picking all lines
        result = list(get_random_n_lines(self.mock_file_path, 10))
        self.assertEqual(len(result), 5)
        mock_random_sample.assert_called_once_with(lines, 5)
        mock_random_sample.reset_mock()

        # Test N=0
        result = list(get_random_n_lines(self.mock_file_path, 0))
        self.assertEqual(len(result), 0)
        mock_random_sample.assert_not_called() # Should not call random.sample if n is 0

        # Test empty file
        mock_file.return_value.__iter__.return_value = iter([])
        result = list(get_random_n_lines(self.mock_file_path, 3))
        self.assertEqual(len(result), 0)
        mock_random_sample.assert_not_called() # Should not call random.sample if file is empty

    @patch("builtins.open", new_callable=mock_open)
    def test_get_grep_lines(self, mock_file):
        # Mock rationale: Simulate file content for reading.
        mock_file.return_value.read.return_value = self.test_content
        mock_file.return_value.__iter__.return_value = iter(self.test_content.splitlines(keepends=True))

        # Test simple pattern
        result = list(get_grep_lines(self.mock_file_path, "dog"))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "Line 2: Jumps over the lazy dog\n")

        # Test pattern with multiple matches
        result = list(get_grep_lines(self.mock_file_path, "Line"))
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0], "Line 1: The quick brown fox\n")

        # Test regex pattern
        result = list(get_grep_lines(self.mock_file_path, r"Line \d: (The|Jumps)"))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "Line 1: The quick brown fox\n")
        self.assertEqual(result[1], "Line 2: Jumps over the lazy dog\n")

        # Test no match
        result = list(get_grep_lines(self.mock_file_path, "nonexistent"))
        self.assertEqual(len(result), 0)

        # Test empty file
        mock_file.return_value.__iter__.return_value = iter([])
        result = list(get_grep_lines(self.mock_file_path, "Line"))
        self.assertEqual(len(result), 0)

    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.stderr", new_callable=io.StringIO)
    @patch("argparse.ArgumentParser.parse_args")
    def test_main_first_method_stdout(self, mock_parse_args, mock_stderr, mock_stdout, mock_file):
        # Mock rationale: Simulate command-line arguments.
        mock_parse_args.return_value = MagicMock(
            file_path=self.mock_file_path,
            method="first",
            count=2,
            pattern=None,
            output=None
        )
        # Mock rationale: Simulate file content for reading.
        mock_file.return_value.__iter__.return_value = iter(self.test_content.splitlines(keepends=True))

        main()
        output = mock_stdout.getvalue()
        self.assertEqual(output, "Line 1: The quick brown fox\nLine 2: Jumps over the lazy dog\n")
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.stderr", new_callable=io.StringIO)
    @patch("argparse.ArgumentParser.parse_args")
    def test_main_grep_method_output_file(self, mock_parse_args, mock_stderr, mock_stdout, mock_file):
        output_file_path = "output.txt"
        # Mock rationale: Simulate command-line arguments.
        mock_parse_args.return_value = MagicMock(
            file_path=self.mock_file_path,
            method="grep",
            count=None,
            pattern="Line 1|Line 3",
            output=output_file_path
        )
        # Mock rationale: Simulate file content for reading.
        mock_file.return_value.__iter__.return_value = iter(self.test_content.splitlines(keepends=True))

        main()
        # The mock_file is called twice: once for reading input, once for writing output.
        # We need to check the content written to the *second* call to open.
        mock_file.assert_any_call(self.mock_file_path, 'r')
        mock_file.assert_any_call(output_file_path, 'w')
        
        # Mock rationale: Check what was written to the mock output file.
        written_content = mock_file().write.call_args_list
        self.assertEqual(len(written_content), 2) # Two lines written
        self.assertEqual(written_content[0].args[0], "Line 1: The quick brown fox\n")
        self.assertEqual(written_content[1].args[0], "Line 3: With a big smile\n")
        
        self.assertIn(f"Extracted lines saved to '{output_file_path}'", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.stderr", new_callable=io.StringIO)
    @patch("sys.exit")
    @patch("argparse.ArgumentParser.parse_args")
    def test_main_file_not_found(self, mock_parse_args, mock_sys_exit, mock_stderr, mock_stdout, mock_file):
        # Mock rationale: Simulate command-line arguments.
        mock_parse_args.return_value = MagicMock(
            file_path="non_existent_file.txt",
            method="first",
            count=1,
            pattern=None,
            output=None
        )
        # Mock rationale: Simulate FileNotFoundError when opening the file.
        mock_file.side_effect = FileNotFoundError

        main()
        self.assertIn("Error: File not found at 'non_existent_file.txt'", mock_stderr.getvalue())
        mock_sys_exit.assert_called_once_with(1)

    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.stderr", new_callable=io.StringIO)
    @patch("sys.exit")
    @patch("argparse.ArgumentParser.parse_args")
    def test_main_missing_count_for_first(self, mock_parse_args, mock_sys_exit, mock_stderr, mock_stdout, mock_file):
        # Mock rationale: Simulate command-line arguments with missing --count.
        mock_parse_args.return_value = MagicMock(
            file_path=self.mock_file_path,
            method="first",
            count=None, # Missing count
            pattern=None,
            output=None
        )
        # Mock rationale: argparse.ArgumentParser.error calls sys.exit(2)
        # We need to mock the error method to prevent actual exit and capture output.
        with patch("argparse.ArgumentParser.error") as mock_error:
            main()
            mock_error.assert_called_once()
            # The exact error message is handled by argparse, we just ensure it was called.

    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.stderr", new_callable=io.StringIO)
    @patch("sys.exit")
    @patch("argparse.ArgumentParser.parse_args")
    def test_main_missing_pattern_for_grep(self, mock_parse_args, mock_sys_exit, mock_stderr, mock_stdout, mock_file):
        # Mock rationale: Simulate command-line arguments with missing --pattern.
        mock_parse_args.return_value = MagicMock(
            file_path=self.mock_file_path,
            method="grep",
            count=None,
            pattern=None, # Missing pattern
            output=None
        )
        with patch("argparse.ArgumentParser.error") as mock_error:
            main()
            mock_error.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.stderr", new_callable=io.StringIO)
    @patch("sys.exit")
    @patch("argparse.ArgumentParser.parse_args")
    def test_main_invalid_count_for_grep(self, mock_parse_args, mock_sys_exit, mock_stderr, mock_stdout, mock_file):
        # Mock rationale: Simulate command-line arguments with --count for grep (invalid).
        mock_parse_args.return_value = MagicMock(
            file_path=self.mock_file_path,
            method="grep",
            count=5, # Invalid for grep
            pattern="ERROR",
            output=None
        )
        with patch("argparse.ArgumentParser.error") as mock_error:
            main()
            mock_error.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.stderr", new_callable=io.StringIO)
    @patch("sys.exit")
    @patch("argparse.ArgumentParser.parse_args")
    def test_main_invalid_pattern_for_first(self, mock_parse_args, mock_sys_exit, mock_stderr, mock_stdout, mock_file):
        # Mock rationale: Simulate command-line arguments with --pattern for first (invalid).
        mock_parse_args.return_value = MagicMock(
            file_path=self.mock_file_path,
            method="first",
            count=5,
            pattern="ERROR", # Invalid for first
            output=None
        )
        with patch("argparse.ArgumentParser.error") as mock_error:
            main()
            mock_error.assert_called_once()
