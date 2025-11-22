import unittest
import os
from unittest.mock import patch, mock_open
from src.glimmer_generator import GlimmerGenerator, main

class TestGlimmerGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = GlimmerGenerator()

    def test_basic_glimmer_generation(self):
        input_text = "Our supplies are dwindling."
        expected_output = "Our supplies are dwindling, encouraging resourceful new strategies."
        self.assertEqual(self.generator.generate_glimmer(input_text), expected_output)

        input_text_capitalized = "Dwindling supplies are a concern."
        expected_output_capitalized = "Dwindling supplies, encouraging resourceful new strategies are a concern."
        self.assertEqual(self.generator.generate_glimmer(input_text_capitalized), expected_output_capitalized)

    def test_multiple_rules_application(self):
        input_text = "Scarce resources and another day of rain."
        expected_output = "Scarce resources, fostering ingenuity and collaboration and another day of rain, ensuring fresh water collection opportunities."
        self.assertEqual(self.generator.generate_glimmer(input_text), expected_output)

    def test_no_match(self):
        input_text = "The sun shines brightly today."
        self.assertEqual(self.generator.generate_glimmer(input_text), input_text)

    def test_empty_input(self):
        self.assertEqual(self.generator.generate_glimmer(""), "")

    def test_process_file_success(self):
        mock_file_content = "Our supplies are dwindling. Communication is broken."
        expected_output = "Our supplies are dwindling, encouraging resourceful new strategies. Communication is broken, highlighting the value of local networks."

        # Mock rationale: We need to simulate reading from a file without actually creating one on disk.
        # `mock_open` allows us to control the content returned by `open()`.
        # `patch('os.path.exists')` ensures that `os.path.exists` returns True for our mocked file.
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as m_open:
            with patch('os.path.exists', return_value=True):
                result = self.generator.process_file("dummy_path.txt")
                self.assertEqual(result, expected_output)
                m_open.assert_called_once_with("dummy_path.txt", 'r', encoding='utf-8')

    def test_process_file_not_found(self):
        # Mock rationale: Simulate a file not existing to test error handling.
        # `patch('os.path.exists')` is set to return False.
        with patch('os.path.exists', return_value=False):
            with self.assertRaises(FileNotFoundError) as cm:
                self.generator.process_file("non_existent_file.txt")
            self.assertIn("File not found", str(cm.exception))

    @patch('sys.stdout')
    @patch('sys.stderr')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_success(self, mock_parse_args, mock_stderr, mock_stdout):
        mock_parse_args.return_value.input_file = "test_input.txt"
        mock_file_content = "The future is uncertain."
        expected_output = "The future is an uncertain future, ripe with possibilities for rebuilding.\n"

        # Mock rationale: Simulate file reading and capture stdout for verification.
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            with patch('os.path.exists', return_value=True):
                main()
                mock_stdout.write.assert_called_once_with(expected_output)
                mock_stderr.write.assert_not_called()

    @patch('sys.stdout')
    @patch('sys.stderr')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_file_not_found_error(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        mock_parse_args.return_value.input_file = "non_existent.txt"

        # Mock rationale: Simulate file not found and capture stderr for error message.
        with patch('os.path.exists', return_value=False):
            main()
            mock_stderr.write.assert_called_once_with("Error: File not found: non_existent.txt\n")
            mock_exit.assert_called_once_with(1)
            mock_stdout.write.assert_not_called()
