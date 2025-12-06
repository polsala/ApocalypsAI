import unittest
from unittest.mock import mock_open, patch
import os
import sys

# Add the src directory to the path for importing scrubber
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from scrubber import scrub_file, main

class TestScrubber(unittest.TestCase):

    def test_basic_scrubbing(self):
        # Mock rationale: Avoids actual file I/O for deterministic testing.
        # Simulates reading from 'input.txt' and writing to 'output.txt'.
        mock_input_content = (
            "Line 1\n"
            "  Line 2  \n"
            "\n"
            "Line 1\n"
            "Line 3\n"
            "   \n"
            "Line 4 with   extra   spaces\n"
            "Line 3\n"
        )
        expected_output_content = (
            "Line 1\n"
            "Line 2\n"
            "Line 3\n"
            "Line 4 with extra spaces\n"
        )

        m = mock_open(read_data=mock_input_content)
        with patch('builtins.open', m):
            # Mock rationale: os.path.exists is mocked to always return True for the input file,
            # ensuring the FileNotFoundError is not triggered during mock file operations.
            with patch('os.path.exists', return_value=True):
                scrub_file("input.txt", "output.txt")

        # Check if open was called correctly for reading and writing
        m.assert_any_call("input.txt", 'r', encoding='utf-8')
        m.assert_any_call("output.txt", 'w', encoding='utf-8')

        # Check the content written to the output file
        # m() is the mock file handle for the *last* call to open, which is the write call.
        self.assertEqual(m().write.call_args_list[0].args[0], expected_output_content)

    def test_no_duplicates(self):
        # Mock rationale: Avoids actual file I/O for deterministic testing.
        mock_input_content = "A\nB\nA\nC\nB\n"
        expected_output_content = "A\nB\nA\nC\nB\n" # Duplicates should remain

        m = mock_open(read_data=mock_input_content)
        with patch('builtins.open', m):
            with patch('os.path.exists', return_value=True):
                scrub_file("input.txt", "output.txt", remove_duplicates=False)

        self.assertEqual(m().write.call_args_list[0].args[0], expected_output_content)

    def test_no_empty_lines(self):
        # Mock rationale: Avoids actual file I/O for deterministic testing.
        mock_input_content = "Line1\n\n  \nLine2\n"
        expected_output_content = "Line1\n\n\nLine2\n" # Empty lines should remain (after strip)

        m = mock_open(read_data=mock_input_content)
        with patch('builtins.open', m):
            with patch('os.path.exists', return_value=True):
                scrub_file("input.txt", "output.txt", remove_empty_lines=False)

        # Note: strip_whitespace is True by default, so "   " becomes ""
        self.assertEqual(m().write.call_args_list[0].args[0], expected_output_content)

    def test_no_strip_whitespace(self):
        # Mock rationale: Avoids actual file I/O for deterministic testing.
        mock_input_content = "  Line 1  \nLine 2 with   extra   spaces\n"
        expected_output_content = "  Line 1  \nLine 2 with   extra   spaces\n" # Whitespace should remain

        m = mock_open(read_data=mock_input_content)
        with patch('builtins.open', m):
            with patch('os.path.exists', return_value=True):
                scrub_file("input.txt", "output.txt", strip_whitespace=False)

        self.assertEqual(m().write.call_args_list[0].args[0], expected_output_content)

    def test_custom_patterns(self):
        # Mock rationale: Avoids actual file I/O for deterministic testing.
        mock_input_content = (
            "Normal line 1\n"
            "[JUNK] This line has junk\n"
            "ERROR:123 Failed to process\n"
            "Another normal line\n"
            "WARNING: Some issue here\n"
            "ERROR:456 Critical failure\n"
        )
        expected_output_content = (
            "Normal line 1\n"
            "Another normal line\n"
            "WARNING: Some issue here\n"
        )

        m = mock_open(read_data=mock_input_content)
        with patch('builtins.open', m):
            with patch('os.path.exists', return_value=True):
                scrub_file(
                    "input.txt",
                    "output.txt",
                    custom_patterns_to_remove=[r"\[JUNK\]", r"ERROR:\d+"]
                )

        self.assertEqual(m().write.call_args_list[0].args[0], expected_output_content)

    def test_file_not_found(self):
        # Mock rationale: os.path.exists is mocked to return False,
        # simulating a missing input file without actual file system interaction.
        with patch('os.path.exists', return_value=False):
            with self.assertRaises(FileNotFoundError):
                scrub_file("non_existent_file.txt", "output.txt")

    def test_main_cli_basic(self):
        # Mock rationale: sys.argv is mocked to simulate command-line arguments.
        # builtins.open is mocked to simulate file I/O.
        # print is mocked to capture output.
        mock_input_content = "Hello\nWorld\nHello\n"
        expected_output_content = "Hello\nWorld\n"

        m = mock_open(read_data=mock_input_content)
        with patch('sys.argv', ['scrubber.py', 'input.txt', 'output.txt']):
            with patch('builtins.open', m):
                with patch('os.path.exists', return_value=True):
                    with patch('builtins.print') as mock_print:
                        main()
                        mock_print.assert_called_with("File 'input.txt' successfully scrubbed to 'output.txt'.")
                        self.assertEqual(m().write.call_args_list[0].args[0], expected_output_content)

    def test_main_cli_with_options(self):
        # Mock rationale: sys.argv is mocked to simulate command-line arguments with options.
        mock_input_content = "  Line 1  \n\n[REMOVE] Junk\nLine 1\n"
        expected_output_content = "  Line 1  \n\nLine 1\n"

        m = mock_open(read_data=mock_input_content)
        with patch('sys.argv', ['scrubber.py', 'input.txt', 'output.txt',
                                '--no-duplicates', '--no-empty', '--no-strip',
                                '-p', r'\[REMOVE\].*']):
            with patch('builtins.open', m):
                with patch('os.path.exists', return_value=True):
                    with patch('builtins.print'): # Don't care about print output for this test
                        main()
                        self.assertEqual(m().write.call_args_list[0].args[0], expected_output_content)

    def test_main_cli_file_not_found_error(self):
        # Mock rationale: os.path.exists is mocked to return False,
        # and sys.exit is mocked to prevent actual program termination,
        # allowing assertion on its call.
        with patch('sys.argv', ['scrubber.py', 'non_existent.txt', 'output.txt']):
            with patch('os.path.exists', return_value=False):
                with patch('builtins.print') as mock_print:
                    with patch('sys.exit') as mock_exit:
                        main()
                        mock_print.assert_called_with("Error: Input file not found: non_existent.txt")
                        mock_exit.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
