import unittest
from unittest.mock import patch, mock_open
import os
import sys

# Add the src directory to the path to allow importing summarizer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from summarizer import summarize_text, main

class TestSummarizer(unittest.TestCase):

    def test_summarize_empty_text(self):
        # Test with empty input text
        # Mock rationale: Simulating an empty file content.
        self.assertEqual(summarize_text(""), [])

    def test_summarize_short_text_no_summary(self):
        # Test with text where no sentences meet the min_sentence_length criteria
        text = "Hello. World. Short. Sentences."
        # Mock rationale: Simulating a file with only very short sentences.
        self.assertEqual(summarize_text(text, max_sentences=2, min_sentence_length=20), [])

    def test_summarize_basic_text(self):
        # Test with a straightforward text, expecting a specific number of sentences
        text = (
            "This is the first important sentence. It has enough characters to be included. "
            "Here is a second crucial point, which also meets the length requirement. "
            "A third sentence follows, adding more detail to the summary. "
            "This is a very short sentence. "
            "Finally, a fourth sentence that might or might not be included depending on max_sentences."
        )
        # Mock rationale: Simulating a typical text file content for summarization.
        expected_summary = [
            "This is the first important sentence. It has enough characters to be included.",
            "Here is a second crucial point, which also meets the length requirement.",
            "A third sentence follows, adding more detail to the summary."
        ]
        self.assertEqual(summarize_text(text, max_sentences=3, min_sentence_length=50), expected_summary)

    def test_summarize_less_than_max_sentences(self):
        # Test when the text has fewer valid sentences than max_sentences
        text = (
            "Only one long sentence here. "
            "This is another sufficiently long sentence that should be included."
        )
        # Mock rationale: Simulating a file with limited content.
        expected_summary = [
            "Only one long sentence here.",
            "This is another sufficiently long sentence that should be included."
        ]
        self.assertEqual(summarize_text(text, max_sentences=5, min_sentence_length=30), expected_summary)

    def test_summarize_with_different_delimiters(self):
        # Test with different sentence delimiters (., !, ?)
        text = (
            "What a day! This is a critical update. Are we ready? "
            "Yes, we are definitely ready for anything that comes our way. "
            "This sentence is also long enough to be part of the summary."
        )
        # Mock rationale: Simulating varied punctuation in a text file.
        expected_summary = [
            "What a day!",
            "This is a critical update.",
            "Are we ready?",
            "Yes, we are definitely ready for anything that comes our way.",
            "This sentence is also long enough to be part of the summary."
        ]
        self.assertEqual(summarize_text(text, max_sentences=5, min_sentence_length=10), expected_summary)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_main_function_success(self, mock_stdout, mock_exists, mock_file_open):
        # Test the main function's successful execution and output
        file_content = (
            "First important line. This is a very long sentence that should definitely be included in the summary. "
            "A second crucial sentence, also long enough. "
            "Short one. "
            "Third significant sentence for the summary. "
            "Another short one. "
            "Fourth sentence, if max_sentences allows."
        )
        mock_file_open.return_value.read.return_value = file_content
        
        # Mock rationale: Simulating a file existing and containing specific content.
        # Mocking sys.stdout to capture printed output for verification.
        # Mocking os.path.exists to prevent actual file system checks.

        test_args = ['summarizer.py', '--file', 'dummy.txt', '--max-sentences', '3', '--min-length', '30']
        with patch('sys.argv', test_args):
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Summary of dummy.txt:", output)
            self.assertIn("- This is a very long sentence that should definitely be included in the summary.", output)
            self.assertIn("- A second crucial sentence, also long enough.", output)
            self.assertIn("- Third significant sentence for the summary.", output)
            self.assertNotIn("- Short one.", output)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_main_function_no_summary(self, mock_stdout, mock_exists, mock_file_open):
        # Test the main function when no sentences meet the criteria
        file_content = "Short. Sentences. Only."
        mock_file_open.return_value.read.return_value = file_content

        # Mock rationale: Simulating a file with content that won't be summarized.
        # Mocking sys.stdout to capture printed output for verification.
        # Mocking os.path.exists to prevent actual file system checks.

        test_args = ['summarizer.py', '--file', 'dummy.txt', '--max-sentences', '3', '--min-length', '50']
        with patch('sys.argv', test_args):
            main()
            output = mock_stdout.getvalue()
            self.assertIn("No significant sentences found to summarize.", output)

    @patch('os.path.exists', return_value=False)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_main_function_file_not_found(self, mock_stdout, mock_exists):
        # Test the main function's error handling for file not found
        # Mock rationale: Simulating a non-existent file.
        # Mocking sys.stdout to capture printed error output.
        # Mocking os.path.exists to control file existence.

        test_args = ['summarizer.py', '--file', 'non_existent.txt']
        with patch('sys.argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: File not found at 'non_existent.txt'", mock_stdout.getvalue())

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_main_function_file_read_error(self, mock_stdout, mock_exists, mock_file_open):
        # Test the main function's error handling for file read issues
        # Mock rationale: Simulating an IOError during file reading.
        # Mocking sys.stdout to capture printed error output.
        # Mocking os.path.exists to ensure the file is 'found' but then fails to open.

        test_args = ['summarizer.py', '--file', 'unreadable.txt']
        with patch('sys.argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error reading file 'unreadable.txt': Permission denied", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
