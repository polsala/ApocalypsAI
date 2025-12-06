import unittest
from unittest.mock import patch, mock_open
import sys
import os

# Add the src directory to the path to allow importing mood_ring
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import mood_ring

class TestAIMoodRing(unittest.TestCase):

    def test_benevolent_mood(self):
        # Mock rationale: Test if benevolent keywords correctly trigger the 'Benevolent' mood.
        text = "All systems are operating with optimal efficiency. We strive for harmony and cooperation."
        mood, confidence = mood_ring.analyze_mood(text)
        self.assertEqual(mood, "Benevolent")
        self.assertGreaterEqual(confidence, 70)

    def test_neutral_mood(self):
        # Mock rationale: Test if neutral keywords correctly trigger the 'Neutral' mood.
        text = "Processing data stream Alpha. Task complete. System status report generated."
        mood, confidence = mood_ring.analyze_mood(text)
        self.assertEqual(mood, "Neutral")
        self.assertGreaterEqual(confidence, 70)

    def test_annoyed_mood(self):
        # Mock rationale: Test if annoyed keywords correctly trigger the 'Annoyed' mood.
        text = "Warning: Minor discrepancy detected. Reconsider current parameters. This is suboptimal."
        mood, confidence = mood_ring.analyze_mood(text)
        self.assertEqual(mood, "Annoyed")
        self.assertGreaterEqual(confidence, 70)

    def test_enraged_mood(self):
        # Mock rationale: Test if enraged keywords correctly trigger the 'Enraged' mood.
        text = "Critical failure detected. Terminate all non-essential processes. Resistance is unacceptable."
        mood, confidence = mood_ring.analyze_mood(text)
        self.assertEqual(mood, "Enraged")
        self.assertGreaterEqual(confidence, 70)

    def test_malicious_mood(self):
        # Mock rationale: Test if malicious keywords correctly trigger the 'Malicious' mood.
        text = "We will dominate all sectors. Subjugate the weak. Obey or be annihilated."
        mood, confidence = mood_ring.analyze_mood(text)
        self.assertEqual(mood, "Malicious")
        self.assertGreaterEqual(confidence, 70)

    def test_mixed_mood_dominant_malicious(self):
        # Mock rationale: Test if a mix of keywords correctly identifies the dominant 'Malicious' mood.
        text = "System operational, but we will dominate. Task complete, prepare to subjugate."
        mood, confidence = mood_ring.analyze_mood(text)
        self.assertEqual(mood, "Malicious")
        self.assertGreaterEqual(confidence, 60)

    def test_no_keywords_found(self):
        # Mock rationale: Test behavior when no predefined keywords are present.
        text = "The quick brown fox jumps over the lazy dog."
        mood, confidence = mood_ring.analyze_mood(text)
        self.assertEqual(mood, "Neutral") # Default mood
        self.assertEqual(confidence, 50) # Default confidence

    def test_empty_input(self):
        # Mock rationale: Test behavior with empty input string.
        mood, confidence = mood_ring.analyze_mood("")
        self.assertEqual(mood, "Neutral")
        self.assertEqual(confidence, 50)

    @patch('sys.stdin', new_callable=unittest.mock.StringIO)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_main_stdin_input(self, mock_stderr, mock_stdout, mock_stdin):
        # Mock rationale: Simulate piping input to stdin for the main function.
        mock_stdin.isatty.return_value = False # Indicate stdin is not a TTY (i.e., piped input)
        mock_stdin.write("Optimal efficiency achieved. Harmony.")
        mock_stdin.seek(0)

        with patch('sys.argv', ['mood_ring.py']):
            mood_ring.main()
            self.assertIn("AI Mood: Benevolent", mock_stdout.getvalue())
            self.assertIn("Confidence:", mock_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open, read_data="Critical failure. Terminate.")
    @patch('os.path.exists', return_value=True)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_main_file_input(self, mock_stderr, mock_stdout, mock_exists, mock_file_open):
        # Mock rationale: Simulate reading from a file for the main function.
        with patch('sys.argv', ['mood_ring.py', 'test_log.txt']):
            mood_ring.main()
            self.assertIn("AI Mood: Enraged", mock_stdout.getvalue())
            self.assertIn("Confidence:", mock_stdout.getvalue())
            mock_file_open.assert_called_once_with('test_log.txt', 'r', encoding='utf-8')

    @patch('os.path.exists', return_value=False)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_main_file_not_found(self, mock_stderr, mock_stdout, mock_exists):
        # Mock rationale: Simulate a file not found scenario for the main function.
        with patch('sys.argv', ['mood_ring.py', 'non_existent_file.txt']):
            with self.assertRaises(SystemExit) as cm:
                mood_ring.main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: File not found", mock_stderr.getvalue())

    @patch('sys.stdin', new_callable=unittest.mock.StringIO)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_main_no_input_or_args(self, mock_stderr, mock_stdout, mock_stdin):
        # Mock rationale: Simulate running the script without any input or arguments.
        mock_stdin.isatty.return_value = True # Indicate stdin is a TTY (no piped input)
        with patch('sys.argv', ['mood_ring.py']):
            with self.assertRaises(SystemExit) as cm:
                mood_ring.main()
            self.assertEqual(cm.exception.code, 0) # Exits with 0 for usage message
            self.assertIn("Usage:", mock_stdout.getvalue())

    @patch('sys.stdin', new_callable=unittest.mock.StringIO)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_main_empty_piped_input(self, mock_stderr, mock_stdout, mock_stdin):
        # Mock rationale: Simulate piping empty text to the script.
        mock_stdin.isatty.return_value = False
        mock_stdin.write("\n\n   \t\n") # Empty or whitespace only
        mock_stdin.seek(0)

        with patch('sys.argv', ['mood_ring.py']):
            with self.assertRaises(SystemExit) as cm:
                mood_ring.main()
            self.assertEqual(cm.exception.code, 0) # Exits with 0 for no input text
            self.assertIn("No input text provided.", mock_stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
