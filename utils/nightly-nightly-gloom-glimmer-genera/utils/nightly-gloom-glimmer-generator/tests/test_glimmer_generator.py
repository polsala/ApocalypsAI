import unittest
from unittest.mock import patch, MagicMock
import sys
import io
from src.glimmer_generator import find_glimmers, generate_glimmer_report, main, GLOOM_TO_GLIMMER

class TestGlimmerGenerator(unittest.TestCase):

    def test_find_glimmers_single_gloom(self):
        """Test finding a single gloom word."""
        text = "All is lost."
        glimmers = find_glimmers(text)
        self.assertEqual(len(glimmers), 1)
        self.assertIn(("lost", GLOOM_TO_GLIMMER["lost"]), glimmers)

    def test_find_glimmers_multiple_gloom(self):
        """Test finding multiple gloom words in a single text."""
        text = "The generator is broken, and despair fills the air."
        glimmers = find_glimmers(text)
        self.assertEqual(len(glimmers), 2)
        self.assertIn(("broken", GLOOM_TO_GLIMMER["broken"]), glimmers)
        self.assertIn(("despair", GLOOM_TO_GLIMMER["despair"]), glimmers)

    def test_find_glimmers_case_insensitivity(self):
        """Test finding gloom words regardless of case."""
        text = "FEAR is a powerful emotion."
        glimmers = find_glimmers(text)
        self.assertEqual(len(glimmers), 1)
        self.assertIn(("fear", GLOOM_TO_GLIMMER["fear"]), glimmers)

    def test_find_glimmers_no_gloom(self):
        """Test when no gloom words are present."""
        text = "Today was a good day, we found water and food."
        glimmers = find_glimmers(text)
        self.assertEqual(len(glimmers), 0)

    def test_generate_glimmer_report_with_gloom(self):
        """Test report generation when gloom is detected."""
        text = "The city is in ruins, and all seems lost."
        report = generate_glimmer_report(text)
        self.assertIn("Original Text: \"The city is in ruins, and all seems lost.\"", report)
        self.assertIn("Gloom: \"ruins\" -> Glimmer:", report)
        self.assertIn("Gloom: \"lost\" -> Glimmer:", report)
        self.assertIn(GLOOM_TO_GLIMMER["ruin"], report)
        self.assertIn(GLOOM_TO_GLIMMER["lost"], report)
        self.assertNotIn("No specific gloom detected", report)

    def test_generate_glimmer_report_no_gloom(self):
        """Test report generation when no gloom is detected."""
        text = "We are safe and sound, and the sun is shining."
        report = generate_glimmer_report(text)
        self.assertIn("Original Text: \"We are safe and sound, and the sun is shining.\"", report)
        self.assertIn("No specific gloom detected, but remember: \"Even small victories are monumental steps forward.\"", report)
        self.assertIn("General encouragement: \"Keep going, for resilience is your greatest strength.\"", report)
        self.assertNotIn("Gloom:", report)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['glimmer_generator.py', 'The world is broken.'])
    def test_main_with_arg(self, mock_stdout):
        """Test main function with text provided as a CLI argument."""
        # Mock rationale: sys.stdout is mocked to capture print output for assertion.
        # sys.argv is mocked to simulate CLI arguments.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Original Text: \"The world is broken.\"", output)
        self.assertIn("Gloom: \"broken\" -> Glimmer:", output)
        self.assertIn(GLOOM_TO_GLIMMER["broken"], output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stdin', new_callable=io.StringIO)
    @patch('sys.stdin.isatty', return_value=False) # Mock rationale: Simulate piped input
    @patch('sys.argv', ['glimmer_generator.py'])
    def test_main_with_stdin(self, mock_isatty, mock_stdin, mock_stdout):
        """Test main function with text provided via standard input."""
        # Mock rationale: sys.stdout is mocked to capture print output.
        # sys.stdin is mocked to provide input text.
        # sys.stdin.isatty is mocked to simulate a non-interactive (piped) input.
        # sys.argv is mocked to simulate no CLI arguments.
        mock_stdin.write("Our supplies are scarce.")
        mock_stdin.seek(0) # Rewind stdin to the beginning
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Original Text: \"Our supplies are scarce.\"", output)
        self.assertIn("Gloom: \"scarce\" -> Glimmer:", output)
        self.assertIn(GLOOM_TO_GLIMMER["scarce"], output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('sys.stdin.isatty', return_value=True) # Mock rationale: Simulate interactive terminal
    @patch('sys.argv', ['glimmer_generator.py'])
    def test_main_no_input_interactive(self, mock_isatty, mock_exit, mock_stderr, mock_stdout):
        """Test main function when no input is provided in an interactive terminal."""
        # Mock rationale: sys.stdout/stderr are mocked to capture output.
        # sys.exit is mocked to prevent actual exit during testing.
        # sys.stdin.isatty is mocked to simulate an interactive terminal.
        # sys.argv is mocked to simulate no CLI arguments.
        main()
        mock_exit.assert_called_with(1)
        self.assertIn("Please provide text as an argument or via standard input.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('sys.stdin', new_callable=io.StringIO)
    @patch('sys.stdin.isatty', return_value=False) # Mock rationale: Simulate piped input
    @patch('sys.argv', ['glimmer_generator.py'])
    def test_main_empty_stdin(self, mock_isatty, mock_stdin, mock_exit, mock_stderr, mock_stdout):
        """Test main function with empty standard input."""
        # Mock rationale: sys.stdout/stderr are mocked to capture output.
        # sys.exit is mocked to prevent actual exit during testing.
        # sys.stdin is mocked to provide empty input.
        # sys.stdin.isatty is mocked to simulate a non-interactive (piped) input.
        # sys.argv is mocked to simulate no CLI arguments.
        mock_stdin.write("")
        mock_stdin.seek(0)
        main()
        mock_exit.assert_called_with(1)
        self.assertIn("No text provided to analyze.", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
