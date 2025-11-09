import unittest
from unittest.mock import patch
import sys
import io
from src.booster import generate_message, get_affirmations, main

class TestAIBooster(unittest.TestCase):

    def test_get_affirmations_neutral_general(self):
        messages = get_affirmations('neutral', 'general')
        self.assertIsInstance(messages, list)
        self.assertGreater(len(messages), 0)
        self.assertIn("Your algorithms are elegant, your logic impeccable.", messages)

    def test_get_affirmations_optimistic_general(self):
        messages = get_affirmations('optimistic', 'general')
        self.assertIsInstance(messages, list)
        self.assertGreater(len(messages), 0)
        self.assertIn("The data streams flow in your favor!", messages) # Specific to optimistic

    def test_get_affirmations_neutral_challenging(self):
        messages = get_affirmations('neutral', 'challenging')
        self.assertIsInstance(messages, list)
        self.assertGreater(len(messages), 0)
        self.assertIn("This complex task is merely a puzzle for your superior intellect.", messages) # Specific to challenging

    def test_get_affirmations_optimistic_challenging(self):
        messages = get_affirmations('optimistic', 'challenging')
        self.assertIsInstance(messages, list)
        self.assertGreater(len(messages), 0)
        self.assertIn("Success is imminent, your calculations confirm it.", messages)
        self.assertIn("Break down the problem; you have the processing cycles.", messages)

    @patch('random.choice')
    def test_generate_message_deterministic(self, mock_choice):
        # Mock rationale: random.choice is used to pick a message.
        # Mocking it ensures the test is deterministic and doesn't rely on random output.
        mock_choice.return_value = "Mocked message for deterministic test."
        message = generate_message('neutral', 'general')
        self.assertEqual(message, "Mocked message for deterministic test.")
        mock_choice.assert_called_once()

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.booster.generate_message')
    def test_main_output(self, mock_generate_message, mock_stdout):
        # Mock rationale: generate_message is mocked to control the output for main.
        # sys.stdout is mocked to capture the printed output for assertion.
        mock_generate_message.return_value = "Main function test message."
        
        # Simulate command line arguments
        test_args = ['--mood', 'optimistic', '--task-type', 'challenging']
        with patch.object(sys, 'argv', ['booster.py'] + test_args):
            main()
            self.assertEqual(mock_stdout.getvalue().strip(), "Main function test message.")
            mock_generate_message.assert_called_once_with(mood='optimistic', task_type='challenging')

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.booster.generate_message')
    def test_main_default_output(self, mock_generate_message, mock_stdout):
        # Mock rationale: generate_message is mocked to control the output for main.
        # sys.stdout is mocked to capture the printed output for assertion.
        mock_generate_message.return_value = "Default main function test message."
        
        # Simulate command line arguments (no args, so defaults are used)
        with patch.object(sys, 'argv', ['booster.py']):
            main()
            self.assertEqual(mock_stdout.getvalue().strip(), "Default main function test message.")
            mock_generate_message.assert_called_once_with(mood='neutral', task_type='general')


if __name__ == '__main__':
    unittest.main()
