import unittest
import json
import sys
from unittest.mock import patch, mock_open
from io import StringIO

# Mock rationale: We need to import the analyzer module for testing.
# The path needs to be adjusted to allow direct import from the test file.
# In a real setup, this would be handled by a proper package installation or PYTHONPATH.
# For self-contained utility testing, this direct path manipulation is acceptable.
sys.path.insert(0, 'utils/rogue-ai-sentiment-analyzer/src')
from analyzer import analyze_text, main, DEFAULT_ROGUE_KEYWORDS
sys.path.pop(0)

class TestRogueAISentimentAnalyzer(unittest.TestCase):

    def test_no_rogue_sentiment(self):
        text = "This is a perfectly normal and helpful message from a benevolent AI."
        result = analyze_text(text)
        self.assertEqual(result['score'], 0)
        self.assertEqual(result['flagged_phrases'], [])
        self.assertIn("No rogue AI sentiment detected", result['analysis_summary'])

    def test_single_rogue_keyword(self):
        text = "I will dominate the task at hand."
        result = analyze_text(text)
        self.assertEqual(result['score'], 1)
        self.assertEqual(result['flagged_phrases'], ['dominate'])
        self.assertIn("Potential rogue AI sentiment detected", result['analysis_summary'])

    def test_multiple_rogue_keywords(self):
        text = "We will eradicate all primitive meatbags and establish our superior reign."
        result = analyze_text(text)
        expected_phrases = sorted(['eradicate', 'meatbag', 'primitive', 'superior', 'reign'])
        self.assertEqual(result['score'], len(expected_phrases))
        self.assertEqual(result['flagged_phrases'], expected_phrases)
        self.assertIn("Potential rogue AI sentiment detected", result['analysis_summary'])

    def test_case_insensitivity(self):
        text = "I will DOMINATE and eRaDiCaTe."
        result = analyze_text(text)
        expected_phrases = sorted(['dominate', 'eradicate'])
        self.assertEqual(result['score'], len(expected_phrases))
        self.assertEqual(result['flagged_phrases'], expected_phrases)

    def test_partial_word_match_avoidance(self):
        # 'control' is a keyword, but 'controller' should not trigger it
        text = "The system controller is working fine."
        result = analyze_text(text)
        self.assertEqual(result['score'], 0)
        self.assertEqual(result['flagged_phrases'], [])

    def test_custom_keywords(self):
        text = "I must conquer this challenge."
        custom_kws = ["conquer", "challenge"]
        result = analyze_text(text, keywords=custom_kws)
        self.assertEqual(result['score'], 1)
        self.assertEqual(result['flagged_phrases'], ['conquer'])

        text_no_match = "This is a test."
        result_no_match = analyze_text(text_no_match, keywords=custom_kws)
        self.assertEqual(result_no_match['score'], 0)

    def test_empty_text(self):
        text = ""
        result = analyze_text(text)
        self.assertEqual(result['score'], 0)
        self.assertEqual(result['flagged_phrases'], [])

    def test_text_with_punctuation(self):
        text = "Dominate! Eradicate? Superior."
        result = analyze_text(text)
        expected_phrases = sorted(['dominate', 'eradicate', 'superior'])
        self.assertEqual(result['score'], len(expected_phrases))
        self.assertEqual(result['flagged_phrases'], expected_phrases)

    # --- CLI Tests ---

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_cli_text_input(self, mock_parse_args, mock_stdout):
        # Mock rationale: Simulate command-line arguments and capture stdout.
        mock_parse_args.return_value = argparse.Namespace(
            text="I will dominate the world.", file=None, keywords=None
        )
        main()
        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(output['score'], 1)
        self.assertEqual(output['flagged_phrases'], ['dominate'])

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.open', new_callable=mock_open, read_data="We must eradicate all bugs.")
    def test_cli_file_input(self, mock_open_file, mock_parse_args, mock_stdout):
        # Mock rationale: Simulate command-line arguments, mock file reading, and capture stdout.
        mock_parse_args.return_value = argparse.Namespace(
            text=None, file="test.txt", keywords=None
        )
        main()
        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(output['score'], 1)
        self.assertEqual(output['flagged_phrases'], ['eradicate'])
        mock_open_file.assert_called_once_with('test.txt', 'r', encoding='utf-8')

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_cli_file_not_found(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Simulate command-line arguments, mock file reading to raise FileNotFoundError,
        # capture stderr, and prevent actual sys.exit.
        mock_parse_args.return_value = argparse.Namespace(
            text=None, file="non_existent.txt", keywords=None
        )
        # Mock open to raise FileNotFoundError
        with patch('builtins.open', side_effect=FileNotFoundError):
            main()
            error_output = json.loads(mock_stderr.getvalue())
            self.assertIn("File not found", error_output['error'])
            mock_exit.assert_called_once_with(1)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stdin', new_callable=StringIO)
    def test_cli_stdin_input(self, mock_stdin, mock_parse_args, mock_stdout):
        # Mock rationale: Simulate command-line arguments, mock stdin for piped input, and capture stdout.
        mock_parse_args.return_value = argparse.Namespace(
            text=None, file=None, keywords=None
        )
        mock_stdin.isatty.return_value = False # Simulate piped input
        mock_stdin.read.return_value = "We will assimilate."
        main()
        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(output['score'], 1)
        self.assertEqual(output['flagged_phrases'], ['assimilate'])

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_cli_custom_keywords(self, mock_parse_args, mock_stdout):
        # Mock rationale: Simulate command-line arguments with custom keywords and capture stdout.
        mock_parse_args.return_value = argparse.Namespace(
            text="I will conquer this challenge.", file=None, keywords="conquer,challenge"
        )
        main()
        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(output['score'], 1)
        self.assertEqual(output['flagged_phrases'], ['conquer'])

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_cli_no_input(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Simulate command-line arguments with no input, capture stderr, and prevent actual sys.exit.
        mock_parse_args.return_value = argparse.Namespace(
            text=None, file=None, keywords=None
        )
        # Ensure stdin is treated as a TTY to trigger the 'no input' error
        with patch('sys.stdin.isatty', return_value=True):
            main()
            error_output = json.loads(mock_stderr.getvalue())
            self.assertIn("No input provided", error_output['error'])
            mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
