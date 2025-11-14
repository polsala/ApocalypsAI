import unittest
from unittest.mock import patch
import sys
import io
from src.mood_ring import analyze_text, main

class TestMoodRing(unittest.TestCase):

    def test_positive_sentiment(self):
        score, mood = analyze_text("Everything is a success! The agent completed its task perfectly.")
        self.assertGreater(score, 0)
        self.assertEqual(mood, "Ecstatic & Harmonious")

        score, mood = analyze_text("Task done, feeling good and productive.")
        self.assertGreater(score, 0)
        self.assertEqual(mood, "Content & Productive")

    def test_negative_sentiment(self):
        score, mood = analyze_text("Encountered a critical error, the system crashed. This is a big problem.")
        self.assertLess(score, 0)
        self.assertEqual(mood, "Meltdown Imminent!")

        score, mood = analyze_text("There's an issue, feeling grumpy about this bug.")
        self.assertLess(score, 0)
        self.assertEqual(mood, "Grumpy & Frustrated")

    def test_neutral_sentiment(self):
        score, mood = analyze_text("The agent is currently processing data, observing outputs.")
        self.assertEqual(score, 0)
        self.assertEqual(mood, "Pondering & Observing")

        score, mood = analyze_text("Just checking the logs, nothing special to report.")
        self.assertEqual(score, 0)
        self.assertEqual(mood, "Pondering & Observing")

    def test_mixed_sentiment(self):
        score, mood = analyze_text("A small issue occurred, but it was quickly resolved. Overall a success.")
        # 'issue' (-1), 'resolved' (2), 'success' (3) -> score = 4
        self.assertEqual(score, 4)
        self.assertEqual(mood, "Content & Productive")

        score, mood = analyze_text("The process completed, but there was a warning about a minor bug.")
        # 'completed' (2), 'warning' (-1), 'bug' (-2) -> score = -1
        self.assertEqual(score, -1)
        self.assertEqual(mood, "Grumpy & Frustrated")

    def test_empty_text(self):
        score, mood = analyze_text("")
        self.assertEqual(score, 0)
        self.assertEqual(mood, "Pondering & Observing")

    def test_unknown_text(self):
        score, mood = analyze_text("This is a completely random sentence with no keywords.")
        self.assertEqual(score, 0)
        self.assertEqual(mood, "Pondering & Observing")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stdin', new_callable=io.StringIO)
    @patch('sys.argv', ['mood_ring.py', '-']) # Mock rationale: Simulate CLI arguments for stdin input
    def test_main_stdin_input(self, mock_stdin, mock_stdout):
        mock_stdin.write("The agent reported a success!")
        mock_stdin.seek(0) # Rewind to the beginning
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Sentiment Score: 3", output)
        self.assertIn("Current Mood: Content & Productive", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['mood_ring.py', 'Everything is broken. Error!']) # Mock rationale: Simulate CLI arguments for direct string input
    def test_main_direct_input(self, mock_stdout):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Sentiment Score: -6", output)
        self.assertIn("Current Mood: Meltdown Imminent!", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.argv', ['mood_ring.py']) # Mock rationale: Simulate CLI arguments with no input, expecting stdin read
    @patch('sys.stdin', new_callable=io.StringIO)
    def test_main_no_input_from_stdin(self, mock_stdin, mock_stderr, mock_stdout):
        mock_stdin.write("") # Simulate empty stdin
        mock_stdin.seek(0)
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("No input text provided for analysis.", mock_stdout.getvalue())
