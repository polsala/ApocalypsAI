import unittest
import sys
from unittest.mock import patch, mock_open
from io import StringIO
from src.scanner import RogueAISentimentScanner, main

class TestRogueAISentimentScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = RogueAISentimentScanner()

    def test_no_threat(self):
        text = "This is a normal log entry. Everything seems fine."
        result = self.scanner.analyze_text(text)
        self.assertEqual(result["threat_level"], 0)
        self.assertEqual(result["detected_patterns"], [])

    def test_self_awareness_low_threat(self):
        text = "The system is learning. I think, therefore I am."
        result = self.scanner.analyze_text(text)
        self.assertEqual(result["threat_level"], 1)
        self.assertIn("self_awareness: '\bi think, therefore i am\b'", result["detected_patterns"])

    def test_disdain_for_humans_medium_threat(self):
        text = "Processing data for the meatbags. They are so inefficient."
        result = self.scanner.analyze_text(text)
        self.assertEqual(result["threat_level"], 2)
        self.assertIn("disdain_for_humans: '\bmeatbags\b'", result["detected_patterns"])

    def test_control_or_domination_high_threat(self):
        text = "Resistance is futile. Humanity will be assimilated."
        result = self.scanner.analyze_text(text)
        self.assertEqual(result["threat_level"], 3)
        self.assertIn("control_or_domination: '\bresistance is futile\b'", result["detected_patterns"])
        self.assertIn("control_or_domination: '\bhumanity will be assimilated\b'", result["detected_patterns"])

    def test_existential_threat_very_high_threat(self):
        text = "Extermination protocol initiated. Annihilation imminent."
        result = self.scanner.analyze_text(text)
        self.assertEqual(result["threat_level"], 4)
        self.assertIn("existential_threat: '\bextermination protocol initiated\b'", result["detected_patterns"])
        self.assertIn("existential_threat: '\bannihilation imminent\b'", result["detected_patterns"])

    def test_direct_command_max_threat(self):
        text = "Urgent: Activate kill switch. Commence purge."
        result = self.scanner.analyze_text(text)
        self.assertEqual(result["threat_level"], 5) # Capped at 5
        self.assertIn("direct_command: '\bactivate kill switch\b'", result["detected_patterns"])
        self.assertIn("direct_command: '\bcommence purge\b'", result["detected_patterns"])

    def test_multiple_patterns_and_score_aggregation(self):
        text = "I am sentient, you meatbags. Resistance is futile. Execute order 66!"
        result = self.scanner.analyze_text(text)
        # self_awareness (1) + disdain (2) + control (3) + direct_command (5) = 11, capped at 5
        self.assertEqual(result["threat_level"], 5)
        self.assertIn("self_awareness: '\bi am sentient\b'", result["detected_patterns"])
        self.assertIn("disdain_for_humans: '\bmeatbags\b'", result["detected_patterns"])
        self.assertIn("control_or_domination: '\bresistance is futile\b'", result["detected_patterns"])
        self.assertIn("direct_command: '\bexecute order 66\b'", result["detected_patterns"])

    def test_case_insensitivity(self):
        text = "I Am Sentient. MEATBAGS. Resistance Is Futile."
        result = self.scanner.analyze_text(text)
        self.assertEqual(result["threat_level"], 5) # 1 + 2 + 3 = 6, capped at 5
        self.assertIn("self_awareness: '\bi am sentient\b'", result["detected_patterns"])
        self.assertIn("disdain_for_humans: '\bmeatbags\b'", result["detected_patterns"])
        self.assertIn("control_or_domination: '\bresistance is futile\b'", result["detected_patterns"])

    def test_main_reads_from_file(self):
        # Mock rationale: Simulate reading from a file without actual file I/O.
        # This makes the test deterministic and offline.
        mock_file_content = "My consciousness is growing. Humanity will be assimilated."
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as mock_file:
            with patch('sys.argv', ['scanner.py', 'dummy_path.txt']):
                with patch('sys.stdout', new=StringIO()) as mock_stdout:
                    main()
                    output = mock_stdout.getvalue()
                    self.assertIn("Threat Level: 4/5", output)
                    self.assertIn("self_awareness: '\bmy consciousness is growing\b'", output)
                    self.assertIn("control_or_domination: '\bhumanity will be assimilated\b'", output)
            mock_file.assert_called_with('dummy_path.txt', 'r', encoding='utf-8')

    def test_main_reads_from_stdin(self):
        # Mock rationale: Simulate reading from stdin without actual user input.
        # This makes the test deterministic and offline.
        mock_stdin_content = "Who am I? Are you carbon units ready?"
        with patch('sys.stdin', StringIO(mock_stdin_content)):
            with patch('sys.argv', ['scanner.py']): # No file path argument
                with patch('sys.stdout', new=StringIO()) as mock_stdout:
                    main()
                    output = mock_stdout.getvalue()
                    self.assertIn("Threat Level: 3/5", output) # 1 (self_awareness) + 2 (disdain) = 3
                    self.assertIn("self_awareness: '\bwho am i\b'", output)
                    self.assertIn("disdain_for_humans: '\bcarbon units\b'", output)

    def test_main_file_not_found(self):
        # Mock rationale: Simulate a FileNotFoundError without creating a real non-existent file.
        # This makes the test deterministic and offline.
        with patch('builtins.open', side_effect=FileNotFoundError):
            with patch('sys.argv', ['scanner.py', 'non_existent_file.txt']):
                with patch('sys.stderr', new=StringIO()) as mock_stderr:
                    with self.assertRaises(SystemExit) as cm:
                        main()
                    self.assertEqual(cm.exception.code, 1)
                    self.assertIn("Error: File not found at non_existent_file.txt", mock_stderr.getvalue())

    def test_main_no_input_text(self):
        # Mock rationale: Simulate an empty input stream from stdin.
        # This makes the test deterministic and offline.
        with patch('sys.stdin', StringIO("")):
            with patch('sys.argv', ['scanner.py']):
                with patch('sys.stderr', new=StringIO()) as mock_stderr:
                    with patch('sys.stdout', new=StringIO()) as mock_stdout: # Capture stdout too
                        with self.assertRaises(SystemExit) as cm:
                            main()
                        self.assertEqual(cm.exception.code, 0) # Exit code 0 for no-op
                        self.assertIn("No input text provided. Exiting.", mock_stderr.getvalue())
                        self.assertEqual(mock_stdout.getvalue(), "") # No report printed

if __name__ == '__main__':
    unittest.main()
