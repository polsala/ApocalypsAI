import unittest
from unittest.mock import patch, mock_open
import sys
import io
from src.scrubber import clean_text, main

class TestScrubber(unittest.TestCase):

    def test_clean_text_basic_trim_and_empty_lines(self):
        input_text = """
        Line 1 with spaces   

        Line 2
          Line 3 indented
        
        """
        expected_output = """
Line 1 with spaces
Line 2
  Line 3 indented"""
        self.assertEqual(clean_text(input_text), expected_output.strip())

    def test_clean_text_no_empty_lines_option(self):
        input_text = """
        Line 1

        Line 2
        """
        expected_output = """
Line 1

Line 2"""
        self.assertEqual(clean_text(input_text, remove_empty_lines=False), expected_output.strip())

    def test_clean_text_no_trim_whitespace_option(self):
        input_text = "   Line 1   \nLine 2\n  Line 3  "
        expected_output = "   Line 1   \nLine 2\n  Line 3  "
        self.assertEqual(clean_text(input_text, trim_whitespace=False), expected_output)

    def test_clean_text_collapse_spaces(self):
        input_text = "Line   with   many    spaces\nAnother  line"
        expected_output = "Line with many spaces\nAnother line"
        self.assertEqual(clean_text(input_text, collapse_spaces=True), expected_output)

    def test_clean_text_collapse_spaces_with_trim(self):
        input_text = "  Line   with   many    spaces  \nAnother  line  "
        expected_output = "Line with many spaces\nAnother line"
        self.assertEqual(clean_text(input_text, collapse_spaces=True), expected_output)

    def test_clean_text_remove_pattern(self):
        input_text = """
        Valid line 1
        JUNK_SIGNAL_123
        Valid line 2
        ANOTHER_JUNK_SIGNAL
        """
        expected_output = """
Valid line 1
Valid line 2"""
        self.assertEqual(clean_text(input_text, remove_pattern=r'.*JUNK_SIGNAL.*'), expected_output.strip())

    def test_clean_text_remove_pattern_with_other_options(self):
        input_text = """
        Line 1   
        REMOVE THIS LINE

        Line 2 with   spaces
        """
        expected_output = """
Line 1
Line 2 with spaces"""
        self.assertEqual(clean_text(input_text, collapse_spaces=True, remove_pattern='REMOVE THIS LINE'), expected_output.strip())

    def test_clean_text_empty_input(self):
        self.assertEqual(clean_text(""), "")

    def test_clean_text_only_empty_lines(self):
        input_text = "\n\n   \n"
        self.assertEqual(clean_text(input_text), "")

    def test_main_output_to_stdout(self):
        # Mock rationale: Simulate file reading and capture stdout.
        mock_file_content = "Line 1  \n\n  Line 2\n"
        expected_output = "Line 1\nLine 2\n"
        
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as m_open,
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout,
             patch('sys.argv', ['scrubber.py', 'input.txt']):
            main()
            self.assertEqual(mock_stdout.getvalue(), expected_output)
            m_open.assert_called_once_with('input.txt', 'r', encoding='utf-8')

    def test_main_output_to_file(self):
        # Mock rationale: Simulate file reading and writing.
        mock_file_content = "Line A  \n\n  Line B\n"
        expected_output_content = "Line A\nLine B"
        
        m_open = mock_open(read_data=mock_file_content)
        with patch('builtins.open', m_open),
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout,
             patch('sys.argv', ['scrubber.py', 'input.txt', 'output.txt']):
            main()
            m_open.assert_any_call('input.txt', 'r', encoding='utf-8')
            m_open.assert_any_call('output.txt', 'w', encoding='utf-8')
            m_open().write.assert_called_once_with(expected_output_content)
            self.assertIn("Scrubbed content written to 'output.txt'.", mock_stdout.getvalue())

    def test_main_file_not_found(self):
        # Mock rationale: Simulate FileNotFoundError during file reading.
        with patch('builtins.open', side_effect=FileNotFoundError),
             patch('sys.stderr', new_callable=io.StringIO) as mock_stderr,
             patch('sys.argv', ['scrubber.py', 'nonexistent.txt']),
             patch('sys.exit') as mock_exit:
            main()
            self.assertIn("Error: Input file 'nonexistent.txt' not found.", mock_stderr.getvalue())
            mock_exit.assert_called_once_with(1)

    def test_main_with_all_options(self):
        # Mock rationale: Simulate file reading and writing with all options.
        input_content = "  Line 1   \n  JUNK  \n\nLine   2   with   spaces  \n  JUNK  LINE  "
        expected_output = "Line 1\nLine 2 with spaces"

        m_open = mock_open(read_data=input_content)
        with patch('builtins.open', m_open),
             patch('sys.stdout', new_callable=io.StringIO),
             patch('sys.argv', ['scrubber.py', 'in.txt', 'out.txt', '--collapse-spaces', '--remove-pattern', '.*JUNK.*']):
            main()
            m_open().write.assert_called_once_with(expected_output)
