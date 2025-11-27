import io
import sys
import unittest
from unittest import mock

# Import the module under test
from nightly_emoji_annotator import annotate_line, main


class TestEmojiAnnotator(unittest.TestCase):
    def test_annotate_line_deterministic(self):
        # Mock random.choice to always return the same emoji
        with mock.patch('random.choice', return_value='🚀'):
            result = annotate_line("Hello world")
            self.assertEqual(result, "🚀 Hello world")

    def test_cli_with_stdin(self):
        test_input = "line1\nline2\n"
        expected_output = "🔥 line1\n🔥 line2\n"

        with mock.patch('random.choice', return_value='🔥'):
            with mock.patch('sys.stdin', io.StringIO(test_input)):
                with mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                    exit_code = main([])
                    self.assertEqual(exit_code, 0)
                    self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_cli_file_not_found(self):
        with mock.patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
            exit_code = main(['nonexistent.txt'])
            self.assertEqual(exit_code, 1)
            self.assertIn('File not found', mock_stderr.getvalue())

# Mock rationale: All external interactions (random.choice, file I/O, stdin/stdout) are mocked
# to keep tests deterministic and offline.

if __name__ == '__main__':
    unittest.main()
