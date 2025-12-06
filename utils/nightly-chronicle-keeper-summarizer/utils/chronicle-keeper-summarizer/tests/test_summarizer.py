import unittest
import sys
import os
from io import StringIO
from unittest.mock import patch, mock_open

# Mock rationale: We need to test the summarization logic in isolation
# without actual file I/O or interacting with the real stdin/stdout.
# `mock_open` allows simulating file content, and `patch` allows redirecting
# `sys.stdin` and `sys.stdout` to `StringIO` objects for controlled input/output.

# Add the src directory to the path to allow importing summarizer.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import summarizer

class TestSummarizer(unittest.TestCase):

    def test_tokenize_sentences_basic(self):
        text = "Hello world. This is a test! How are you?"
        expected = ["Hello world.", "This is a test!", "How are you?"]
        self.assertEqual(summarizer._tokenize_sentences(text), expected)

    def test_tokenize_sentences_empty_input(self):
        text = ""
        expected = []
        self.assertEqual(summarizer._tokenize_sentences(text), expected)

    def test_tokenize_sentences_no_punctuation(self):
        text = "This is a sentence without punctuation"
        expected = ["This is a sentence without punctuation"]
        self.assertEqual(summarizer._tokenize_sentences(text), expected)

    def test_tokenize_sentences_multiple_spaces(self):
        text = "First sentence.  Second sentence.   Third sentence."
        expected = ["First sentence.", "Second sentence.", "Third sentence."]
        self.assertEqual(summarizer._tokenize_sentences(text), expected)

    def test_tokenize_words_basic(self):
        sentence = "This is a Test sentence with Punctuation!"
        expected = ["test", "sentence", "punctuation"]
        self.assertEqual(summarizer._tokenize_words(sentence), expected)

    def test_tokenize_words_with_numbers(self):
        sentence = "Day 734. The sky remains a perpetual twilight."
        expected = ["day", "sky", "remains", "perpetual", "twilight"]
        self.assertEqual(summarizer._tokenize_words(sentence), expected)

    def test_tokenize_words_empty_input(self):
        sentence = ""
        expected = []
        self.assertEqual(summarizer._tokenize_words(sentence), expected)

    def test_summarize_text_empty(self):
        self.assertEqual(summarizer.summarize_text(""), [])

    def test_summarize_text_short_text(self):
        text = "This is a short text. It has only two sentences."
        # Should return all sentences if num_sentences is greater than or equal to total sentences
        summary = summarizer.summarize_text(text, num_sentences=5)
        self.assertEqual(len(summary), 2)
        self.assertIn("This is a short text.", summary)
        self.assertIn("It has only two sentences.", summary)

    def test_summarize_text_basic_summary(self):
        text = (
            "The quick brown fox jumps over the lazy dog. "
            "The dog was very lazy indeed. "
            "Foxes are known for their agility and speed. "
            "This particular fox was exceptionally quick. "
            "Therefore, the lazy dog had no chance."
        )
        # Manual calculation of scores for deterministic test:
        # Word freqs (non-stop): quick:2, brown:1, fox:2, jumps:1, lazy:2, dog:2, indeed:1, known:1, agility:1, speed:1, particular:1, exceptionally:1, therefore:1, chance:1
        # Sentences (words, score):
        # 0: "The quick brown fox jumps over the lazy dog." (quick, brown, fox, jumps, lazy, dog) -> 2+1+2+1+2+2 = 10
        # 1: "The dog was very lazy indeed." (dog, lazy, indeed) -> 2+2+1 = 5
        # 2: "Foxes are known for their agility and speed." (foxes, known, agility, speed) -> 2+1+1+1 = 5
        # 3: "This particular fox was exceptionally quick." (particular, fox, exceptionally, quick) -> 1+2+1+2 = 6
        # 4: "Therefore, the lazy dog had no chance." (therefore, lazy, dog, chance) -> 1+2+2+1 = 6
        # Ranked (score, original_index): (10,0), (6,3), (6,4), (5,1), (5,2)
        # Top 2 indices (sorted): 0, 3
        summary = summarizer.summarize_text(text, num_sentences=2)
        self.assertEqual(len(summary), 2)
        self.assertEqual(summary[0], "The quick brown fox jumps over the lazy dog.")
        self.assertEqual(summary[1], "This particular fox was exceptionally quick.")

    def test_summarize_text_more_sentences_than_available(self):
        text = "One sentence. Two sentences."
        summary = summarizer.summarize_text(text, num_sentences=5)
        self.assertEqual(len(summary), 2)
        self.assertEqual(summary[0], "One sentence.")
        self.assertEqual(summary[1], "Two sentences.")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stdin', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_stdin_input(self, mock_parse_args, mock_stdin, mock_stdout):
        # Mock rationale: Simulate user input via stdin and capture printed output.
        mock_parse_args.return_value = argparse.Namespace(file=None, sentences=2)
        mock_stdin.write(
            "This is the first sentence. This is the second sentence. "
            "This is the third sentence. This is the fourth sentence."
        )
        mock_stdin.seek(0) # Rewind stdin to the beginning

        # Mock rationale: Prevent sys.exit(1) from terminating the test prematurely.
        with patch('sys.exit') as mock_exit:
            summarizer.main()
            mock_exit.assert_not_called() # Ensure no exit on success

        output = mock_stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output), 2)
        # For this simple text, all words are unique, so scores will be similar.
        # The current logic sorts by score then by original index. So the first two sentences will be picked.
        self.assertEqual(output[0], "This is the first sentence.")
        self.assertEqual(output[1], "This is the second sentence.")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('builtins.open', new_callable=mock_open, read_data="File content line 1. File content line 2. File content line 3.")
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_file_input(self, mock_parse_args, mock_open_file, mock_stderr, mock_stdout):
        # Mock rationale: Simulate reading from a file without creating a real file.
        mock_parse_args.return_value = argparse.Namespace(file="test.txt", sentences=2)

        with patch('sys.exit') as mock_exit:
            summarizer.main()
            mock_exit.assert_not_called()

        mock_open_file.assert_called_once_with("test.txt", 'r', encoding='utf-8')
        output = mock_stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0], "File content line 1.")
        self.assertEqual(output[1], "File content line 2.")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_file_not_found(self, mock_parse_args, mock_open_file, mock_stderr, mock_stdout):
        # Mock rationale: Simulate a FileNotFoundError during file reading.
        mock_parse_args.return_value = argparse.Namespace(file="nonexistent.txt", sentences=3)

        with patch('sys.exit') as mock_exit:
            summarizer.main()
            mock_exit.assert_called_once_with(1)

        self.assertIn("Error: File not found at 'nonexistent.txt'", mock_stderr.getvalue())
        self.assertEqual(mock_stdout.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.stdin', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_stdin_empty_input(self, mock_parse_args, mock_stdin, mock_stderr, mock_stdout):
        # Mock rationale: Simulate empty input from stdin.
        mock_parse_args.return_value = argparse.Namespace(file=None, sentences=2)
        mock_stdin.write("")
        mock_stdin.seek(0)

        with patch('sys.exit') as mock_exit:
            summarizer.main()
            mock_exit.assert_not_called()
        
        # Expect no output for empty input
        self.assertEqual(mock_stdout.getvalue().strip(), "")

    def test_summarize_text_complex_case(self):
        text = (
            "The ancient city of Xylos was once a beacon of civilization. "
            "Its advanced technology, powered by geothermal vents, allowed its inhabitants to thrive for centuries. "
            "However, a cataclysmic event, possibly a meteor strike, plunged Xylos into ruin. "
            "Survivors scattered, carrying fragments of their knowledge. "
            "Archaeological digs have recently uncovered new artifacts, suggesting a hidden vault. "
            "The vault is believed to contain blueprints for a weather control device. "
            "Such a device could restore the planet's climate and bring hope to the wasteland."
        )
        # Manual calculation of scores for deterministic test:
        # Word freqs (non-stop): ancient:1, city:1, xylos:2, beacon:1, civilization:1, advanced:1, technology:1, powered:1, geothermal:1, vents:1, allowed:1, inhabitants:1, thrive:1, centuries:1, cataclysmic:1, event:1, possibly:1, meteor:1, strike:1, plunged:1, ruin:1, survivors:1, scattered:1, carrying:1, fragments:1, knowledge:1, archaeological:1, digs:1, recently:1, uncovered:1, new:1, artifacts:1, suggesting:1, hidden:1, vault:2, believed:1, contain:1, blueprints:1, weather:1, control:1, device:2, restore:1, planet:1, climate:1, bring:1, hope:1, wasteland:1
        # Sentences (words, score):
        # 0: "The ancient city of Xylos was once a beacon of civilization." (ancient, city, xylos, beacon, civilization) -> 1+1+2+1+1 = 6
        # 1: "Its advanced technology, powered by geothermal vents, allowed its inhabitants to thrive for centuries." (advanced, technology, powered, geothermal, vents, allowed, inhabitants, thrive, centuries) -> 9
        # 2: "However, a cataclysmic event, possibly a meteor strike, plunged Xylos into ruin." (cataclysmic, event, possibly, meteor, strike, plunged, xylos, ruin) -> 1+1+1+1+1+1+2+1 = 9
        # 3: "Survivors scattered, carrying fragments of their knowledge." (survivors, scattered, carrying, fragments, knowledge) -> 5
        # 4: "Archaeological digs have recently uncovered new artifacts, suggesting a hidden vault." (archaeological, digs, recently, uncovered, new, artifacts, suggesting, hidden, vault) -> 9+2 = 11
        # 5: "The vault is believed to contain blueprints for a weather control device." (vault, believed, contain, blueprints, weather, control, device) -> 2+1+1+1+1+1+2 = 9
        # 6: "Such a device could restore the planet's climate and bring hope to the wasteland." (device, restore, planet, climate, bring, hope, wasteland) -> 2+1+1+1+1+1+1 = 8

        # Ranked (score, original_index): (11,4), (9,1), (9,2), (9,5), (8,6), (6,0), (5,3)
        # Top 3 indices (sorted): 1, 2, 4 (if scores are tied, original index is tie-breaker for `sorted` stability)
        # Re-evaluating the tie-breaking for `ranked_sentences`: `sorted(sentence_scores.items(), key=lambda item: item[1], reverse=True)`
        # This means if scores are equal, the order of items with the same score is preserved based on their original insertion order (which is by index).
        # So, (4,11), (1,9), (2,9), (5,9), (6,8), (0,6), (3,5)
        # Top 3 indices: 4, 1, 2. Sorted: 1, 2, 4.
        expected_summary = [
            "Its advanced technology, powered by geothermal vents, allowed its inhabitants to thrive for centuries.",
            "However, a cataclysmic event, possibly a meteor strike, plunged Xylos into ruin.",
            "Archaeological digs have recently uncovered new artifacts, suggesting a hidden vault."
        ]
        summary = summarizer.summarize_text(text, num_sentences=3)
        self.assertEqual(len(summary), 3)
        self.assertEqual(summary, expected_summary)


if __name__ == '__main__':
    unittest.main()
