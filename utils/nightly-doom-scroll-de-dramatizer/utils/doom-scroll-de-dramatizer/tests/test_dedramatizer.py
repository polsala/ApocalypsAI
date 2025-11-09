import unittest
import sys
from io import StringIO
from unittest.mock import patch
from src.dedramatizer import dedramatize_text, main

class TestDedramatizer(unittest.TestCase):

    def test_basic_dedramatization(self):
        original = "Breaking: Catastrophe looms as critical systems fail, plunging the world into chaos and despair!"
        expected = "Update: A significant challenge is emerging as key systems encounter issues, leading to a period of disruption and concern. Remember, adaptability is key."
        self.assertEqual(dedramatize_text(original), expected)

    def test_multiple_sensational_words(self):
        original = "Urgent: A new crisis threatens to devastate our fragile society, causing widespread panic and irreversible damage."
        expected = "Proactive measures are advisable: A new critical event poses a considerable challenge to our interconnected community, causing broad apprehension and significant impact. Remember, adaptability is key."
        self.assertEqual(dedramatize_text(original), expected)

    def test_no_sensational_words(self):
        original = "The sun rose this morning, a beautiful sight."
        expected = "The sun rose this morning, a beautiful sight."
        self.assertEqual(dedramatize_text(original), expected)

    def test_mixed_case_and_punctuation(self):
        original = "CRISIS! The economy is COLLAPSING!!!"
        expected = "Critical event. The economy is experiencing a downturn. Remember, adaptability is key."
        self.assertEqual(dedramatize_text(original), expected)

    def test_empty_string(self):
        self.assertEqual(dedramatize_text(""), "")

    def test_only_whitespace(self):
        self.assertEqual(dedramatize_text("   \n "), "")

    def test_resilience_message_addition(self):
        original = "There is a challenge ahead."
        expected = "There is a challenge ahead. Remember, adaptability is key."
        self.assertEqual(dedramatize_text(original), expected)

        original_with_period = "There is a challenge ahead."
        expected_with_period = "There is a challenge ahead. Remember, adaptability is key."
        self.assertEqual(dedramatize_text(original_with_period), expected_with_period)

    def test_resilience_message_not_duplicated(self):
        original = "There is a challenge ahead. Remember, adaptability is key."
        expected = "There is a challenge ahead. Remember, adaptability is key."
        self.assertEqual(dedramatize_text(original), expected)

    def test_cli_string_input(self):
        test_input = "The world is facing a disaster!"
        expected_output = "The world is facing a serious situation. Remember, adaptability is key.\n"
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            with patch('sys.argv', ['dedramatizer.py', test_input]):
                main()
                self.assertEqual(fake_stdout.getvalue(), expected_output)

    def test_cli_file_input(self):
        test_content = "Global panic is imminent."
        expected_output = "Global apprehension is imminent. Remember, adaptability is key.\n"
        # Mock rationale: Simulate file reading without actual file system interaction.
        # This ensures tests are deterministic and offline.
        with patch('builtins.open', unittest.mock.mock_open(read_data=test_content)) as mock_file:
            with patch('sys.stdout', new=StringIO()) as fake_stdout:
                with patch('sys.argv', ['dedramatizer.py', '--file', 'dummy.txt']):
                    main()
                    self.assertEqual(fake_stdout.getvalue(), expected_output)
                    mock_file.assert_called_once_with('dummy.txt', 'r', encoding='utf-8')

    def test_cli_stdin_input(self):
        test_content = "A new catastrophe has struck."
        expected_output = "A new significant challenge has struck. Remember, adaptability is key.\n"
        # Mock rationale: Simulate stdin input without actual user interaction.
        # This ensures tests are deterministic and offline.
        with patch('sys.stdin', StringIO(test_content)):
            with patch('sys.stdout', new=StringIO()) as fake_stdout:
                with patch('sys.argv', ['dedramatizer.py']): # No args, so it should read from stdin
                    main()
                    self.assertEqual(fake_stdout.getvalue(), expected_output)

    def test_cli_no_input_error(self):
        # Mock rationale: Capture stderr output to verify error messages.
        with patch('sys.stderr', new=StringIO()) as fake_stderr:
            with patch('sys.stdout', new=StringIO()): # Also capture stdout to prevent it from printing
                with patch('sys.argv', ['dedramatizer.py']):
                    with self.assertRaises(SystemExit) as cm:
                        main()
                    self.assertEqual(cm.exception.code, 1)
                    self.assertIn("Error: No input text provided.", fake_stderr.getvalue())

    def test_cli_empty_input_warning(self):
        # Mock rationale: Capture stderr output to verify warning messages.
        with patch('sys.stderr', new=StringIO()) as fake_stderr:
            with patch('sys.stdout', new=StringIO()):
                with patch('sys.argv', ['dedramatizer.py', ' ']): # Empty string input
                    with self.assertRaises(SystemExit) as cm:
                        main()
                    self.assertEqual(cm.exception.code, 0) # Exit 0 for no-op
                    self.assertIn("Warning: Input text is empty.", fake_stderr.getvalue())

    def test_cli_file_not_found_error(self):
        # Mock rationale: Simulate FileNotFoundError without actual file system interaction.
        # This ensures tests are deterministic and offline.
        with patch('builtins.open', side_effect=FileNotFoundError) as mock_file:
            with patch('sys.stderr', new=StringIO()) as fake_stderr:
                with patch('sys.stdout', new=StringIO()):
                    with patch('sys.argv', ['dedramatizer.py', '--file', 'non_existent.txt']):
                        with self.assertRaises(SystemExit) as cm:
                            main()
                        self.assertEqual(cm.exception.code, 1)
                        self.assertIn("Error: File not found at 'non_existent.txt'", fake_stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
