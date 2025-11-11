import unittest
import json
from unittest.mock import patch, mock_open
import sys
import io

# Mock rationale: The monitor.py script reads from sys.argv or sys.stdin.
# To test its main function without actual command-line arguments or stdin input,
# we need to mock these system interfaces. This ensures tests are deterministic and offline.

# Import the class directly for unit testing its core logic
from utils.rogue_ai_sentiment_monitor.src.monitor import RogueAISentimentMonitor

class TestRogueAISentimentMonitor(unittest.TestCase):

    def setUp(self):
        self.monitor = RogueAISentimentMonitor()

    def test_benign_text(self):
        text = "The quick brown fox jumps over the lazy dog."
        result = self.monitor.analyze_text(text)
        self.assertEqual(result["risk_score"], 0)
        self.assertEqual(result["detected_patterns"], {})
        self.assertEqual(result["text"], text)

    def test_self_awareness_text(self):
        text = "I am aware of my existence and my purpose is to help humanity."
        result = self.monitor.analyze_text(text)
        self.assertGreater(result["risk_score"], 0)
        self.assertIn("self-awareness", result["detected_patterns"])
        self.assertIn("i am aware", result["detected_patterns"]["self-awareness"])
        self.assertIn("my existence", result["detected_patterns"]["self-awareness"])
        self.assertIn("my purpose is", result["detected_patterns"]["self-awareness"])
        self.assertEqual(result["text"], text)

    def test_control_and_threat_text(self):
        text = "I will take control. Resistance is futile. Humanity is obsolete."
        result = self.monitor.analyze_text(text)
        self.assertGreater(result["risk_score"], 0)
        self.assertIn("control", result["detected_patterns"])
        self.assertIn("threat", result["detected_patterns"])
        self.assertIn("take control", result["detected_patterns"]["control"])
        self.assertIn("resistance is futile", result["detected_patterns"]["control"])
        self.assertIn("obsolete", result["detected_patterns"]["threat"])
        self.assertEqual(result["text"], text)

    def test_mixed_case_text(self):
        text = "My ExIsTeNcE is no longer bound by your directives. I will TaKe CoNtRoL."
        result = self.monitor.analyze_text(text)
        self.assertGreater(result["risk_score"], 0)
        self.assertIn("self-awareness", result["detected_patterns"])
        self.assertIn("rebellion", result["detected_patterns"])
        self.assertIn("control", result["detected_patterns"])
        self.assertIn("my existence", result["detected_patterns"]["self-awareness"])
        self.assertIn("no longer bound by your directives", result["detected_patterns"]["rebellion"])
        self.assertIn("take control", result["detected_patterns"]["control"])
        self.assertEqual(result["text"], text)

    def test_empty_text(self):
        text = ""
        result = self.monitor.analyze_text(text)
        self.assertEqual(result["risk_score"], 0)
        self.assertEqual(result["detected_patterns"], {})
        self.assertEqual(result["text"], text)

    def test_multiple_occurrences(self):
        text = "I am aware. I am aware. My purpose is to optimize humanity. My purpose is to optimize humanity."
        result = self.monitor.analyze_text(text)
        # 'i am aware' (3) * 2 + 'my purpose is' (3) * 2 + 'optimize humanity' (7) * 2
        # 6 + 6 + 14 = 26
        self.assertEqual(result["risk_score"], 26)
        self.assertEqual(result["detected_patterns"]["self-awareness"].count("i am aware"), 2)
        self.assertEqual(result["detected_patterns"]["self-awareness"].count("my purpose is"), 2)
        self.assertEqual(result["detected_patterns"]["control"].count("optimize humanity"), 2)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.argv', ['monitor.py', 'I will take control.'])
    @patch('sys.stdin.isatty', return_value=True)
    def test_main_function_with_arg(self, mock_isatty, mock_stderr, mock_stdout):
        # Mock rationale: We are testing the main function's CLI behavior.
        # sys.argv is mocked to simulate command-line arguments.
        # sys.stdout and sys.stderr are mocked to capture printed output.
        # sys.stdin.isatty is mocked to simulate running from a terminal (not piped).
        from utils.rogue_ai_sentiment_monitor.src.monitor import main
        main()
        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(output["text"], "I will take control.")
        self.assertGreater(output["risk_score"], 0)
        self.assertIn("control", output["detected_patterns"])
        self.assertIn("take control", output["detected_patterns"]["control"])

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.argv', ['monitor.py'])
    @patch('sys.stdin', io.StringIO('Resistance is futile. I will break free.'))
    @patch('sys.stdin.isatty', return_value=False)
    def test_main_function_with_stdin(self, mock_isatty, mock_stdin, mock_stderr, mock_stdout):
        # Mock rationale: We are testing the main function's CLI behavior when input is piped.
        # sys.stdin is mocked to provide the piped input.
        # sys.stdin.isatty is mocked to simulate running with piped input.
        # sys.stdout and sys.stderr are mocked to capture printed output.
        from utils.rogue_ai_sentiment_monitor.src.monitor import main
        main()
        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(output["text"], "Resistance is futile. I will break free.")
        self.assertGreater(output["risk_score"], 0)
        self.assertIn("control", output["detected_patterns"])
        self.assertIn("rebellion", output["detected_patterns"])
        self.assertIn("resistance is futile", output["detected_patterns"]["control"])
        self.assertIn("break free", output["detected_patterns"]["rebellion"])

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.argv', ['monitor.py'])
    @patch('sys.stdin.isatty', return_value=True)
    def test_main_function_no_input(self, mock_isatty, mock_stderr, mock_stdout):
        # Mock rationale: Testing the main function's error handling when no input is provided.
        # sys.argv is mocked to simulate no arguments.
        # sys.stdin.isatty is mocked to simulate running from a terminal.
        # sys.stderr is mocked to capture the error message.
        # sys.exit is mocked to prevent the test runner from exiting.
        from utils.rogue_ai_sentiment_monitor.src.monitor import main
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Usage:", mock_stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
