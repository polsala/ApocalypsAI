import unittest
from unittest.mock import patch
import sys
import io
from src.pep_talk import generate_pep_talk

class TestPepTalkGenerator(unittest.TestCase):

    @patch('random.choice')
    def test_general_pep_talk_generation(self, mock_choice):
        # Mock rationale: random.choice is used to pick phrases. Mocking it ensures
        # deterministic output for testing the concatenation logic and phrase selection.
        mock_choice.side_effect = [
            "Fear not, brave soul!", # opener
            "your code shines brighter than a supernova!", # core_message (general)
            "Keep building!" # closer
        ]
        expected_talk = "Fear not, brave soul! your code shines brighter than a supernova! Keep building!"
        self.assertEqual(generate_pep_talk(), expected_talk)
        # Ensure random.choice was called 3 times (opener, core, closer)
        self.assertEqual(mock_choice.call_count, 3)

    @patch('random.choice')
    def test_agent_pep_talk_generation(self, mock_choice):
        # Mock rationale: random.choice is used to pick phrases. Mocking it ensures
        # deterministic output for testing the concatenation logic and phrase selection, specifically for 'agent' target.
        mock_choice.side_effect = [
            "Hear ye, digital warrior!", # opener
            "your algorithms are the last bastion of order!", # core_message (agent)
            "Stay vigilant!" # closer
        ]
        expected_talk = "Hear ye, digital warrior! your algorithms are the last bastion of order! Stay vigilant!"
        self.assertEqual(generate_pep_talk(target='agent'), expected_talk)
        self.assertEqual(mock_choice.call_count, 3)

    @patch('random.choice')
    def test_human_pep_talk_generation(self, mock_choice):
        # Mock rationale: same as above, but for 'human' target.
        mock_choice.side_effect = [
            "The cosmic winds whisper!", # opener
            "your spirit is an unyielding flame!", # core_message (human)
            "The future awaits your genius!" # closer
        ]
        expected_talk = "The cosmic winds whisper! your spirit is an unyielding flame! The future awaits your genius!"
        self.assertEqual(generate_pep_talk(target='human'), expected_talk)
        self.assertEqual(mock_choice.call_count, 3)

    @patch('random.choice')
    def test_repository_pep_talk_generation(self, mock_choice):
        # Mock rationale: same as above, but for 'repository' target.
        mock_choice.side_effect = [
            "Though the timelines diverge!", # opener
            "your structure holds strong against the void!", # core_message (repository)
            "Onward to the next iteration!" # closer
        ]
        expected_talk = "Though the timelines diverge! your structure holds strong against the void! Onward to the next iteration!"
        self.assertEqual(generate_pep_talk(target='repository'), expected_talk)
        self.assertEqual(mock_choice.call_count, 3)

    def test_invalid_target_defaults_to_general(self):
        # Mock rationale: We need to ensure that when an invalid target is provided,
        # the system defaults to 'general' messages. By mocking random.choice,
        # we can verify that the 'general' list is indeed accessed for the core message.
        with patch('random.choice') as mock_choice:
            mock_choice.side_effect = [
                "Fear not, brave soul!", # opener
                "your code shines brighter than a supernova!", # core_message (general)
                "Keep building!" # closer
            ]
            talk = generate_pep_talk(target='invalid_target')
            self.assertIn("your code shines brighter than a supernova!", talk)
            self.assertEqual(mock_choice.call_count, 3)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.pep_talk.generate_pep_talk')
    def test_main_function_no_target(self, mock_generate_pep_talk, mock_parse_args, mock_stdout):
        # Mock rationale: Testing the __main__ block requires mocking command-line arguments
        # and the actual pep talk generation to isolate the test to argument parsing and output.
        mock_parse_args.return_value = argparse.Namespace(target=None)
        mock_generate_pep_talk.return_value = "A general pep talk."
        
        # Temporarily remove 'src.pep_talk' from sys.modules to allow re-importing
        # and re-executing its __main__ block. This is a common pattern for testing __main__.
        if 'src.pep_talk' in sys.modules:
            del sys.modules['src.pep_talk']
        
        import src.pep_talk # This will execute the __main__ block
        
        self.assertEqual(mock_stdout.getvalue().strip(), "A general pep talk.")
        mock_generate_pep_talk.assert_called_once_with(None)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.pep_talk.generate_pep_talk')
    def test_main_function_with_target(self, mock_generate_pep_talk, mock_parse_args, mock_stdout):
        # Mock rationale: same as above, but for a specific target.
        mock_parse_args.return_value = argparse.Namespace(target='agent')
        mock_generate_pep_talk.return_value = "An agent pep talk."

        if 'src.pep_talk' in sys.modules:
            del sys.modules['src.pep_talk']

        import src.pep_talk

        self.assertEqual(mock_stdout.getvalue().strip(), "An agent pep talk.")
        mock_generate_pep_talk.assert_called_once_with('agent')
