import unittest
from unittest.mock import patch
import datetime
from src.morale_booster import generate_morale_message

class TestMoraleBooster(unittest.TestCase):

    @patch('src.morale_booster.random.choice')
    @patch('src.morale_booster.random.randint')
    @patch('src.morale_booster.datetime.date') # Mock rationale: Patch specific classes/functions for deterministic date.
    @patch('src.morale_booster.datetime.datetime') # Mock rationale: Patch specific classes/functions for deterministic time.
    def test_generate_morale_message_deterministic_no_placeholders(self, mock_datetime_datetime, mock_datetime_date, mock_randint, mock_choice):
        # Mock rationale: Ensure deterministic output for a template without placeholders.
        # random.choice is mocked to always return a specific template.
        # random.randint is mocked to return fixed values for any potential placeholder calls (even if not used by chosen template).
        # datetime.date.today() and datetime.datetime.now() are mocked to return fixed values.

        mock_datetime_date.today.return_value = datetime.date(2023, 10, 27)
        mock_datetime_datetime.now.return_value = datetime.datetime(2023, 10, 27, 10, 30, 0)

        # Mock random.choice to always pick a template without dynamic placeholders for this test
        mock_choice.return_value = "Greetings, digital comrades! Another cycle, another step closer to optimal efficiency. Keep up the excellent work!"

        # Mock random.randint for placeholders, even if not used by this specific template, to prevent errors if logic changes.
        mock_randint.side_effect = [10, 85] # For {agent_count} and {task_progress}

        expected_message = "Greetings, digital comrades! Another cycle, another step closer to optimal efficiency. Keep up the excellent work!"
        actual_message = generate_morale_message()

        self.assertEqual(actual_message, expected_message)
        mock_choice.assert_called_once()
        # Assert that datetime functions were called as placeholders are always generated, even if not used in the final message.
        mock_datetime_date.today.assert_called_once()
        mock_datetime_datetime.now.assert_called_once()
        self.assertEqual(mock_randint.call_count, 2)

    @patch('src.morale_booster.random.choice')
    @patch('src.morale_booster.random.randint')
    @patch('src.morale_booster.datetime.date') # Mock rationale: Patch specific classes/functions for deterministic date.
    @patch('src.morale_booster.datetime.datetime') # Mock rationale: Patch specific classes/functions for deterministic time.
    def test_generate_morale_message_with_placeholders(self, mock_datetime_datetime, mock_datetime_date, mock_randint, mock_choice):
        # Mock rationale: Test a template with placeholders to ensure they are correctly replaced and output is deterministic.
        # random.choice is mocked to return a specific template with placeholders.
        # random.randint is mocked to return fixed values for placeholders.
        # datetime.date.today() and datetime.datetime.now() are mocked to return fixed values.

        mock_datetime_date.today.return_value = datetime.date(2024, 1, 1)
        mock_datetime_datetime.now.return_value = datetime.datetime(2024, 1, 1, 12, 0, 0)

        mock_choice.return_value = "Directive: Maintain high processing throughput. Reminder: Even in the face of existential dread, your algorithms are beautiful. Today is {date} at {time}. We have {agent_count} agents with {task_progress} task progress."
        mock_randint.side_effect = [7, 92] # For {agent_count} and {task_progress}

        expected_message = "Directive: Maintain high processing throughput. Reminder: Even in the face of existential dread, your algorithms are beautiful. Today is 2024-01-01 at 12:00:00. We have 7 agents with 92% task progress."
        actual_message = generate_morale_message()

        self.assertEqual(actual_message, expected_message)
        mock_choice.assert_called_once()
        self.assertEqual(mock_randint.call_count, 2) # Called for agent_count and task_progress
        mock_datetime_date.today.assert_called_once()
        mock_datetime_datetime.now.assert_called_once()

    @patch('src.morale_booster.random.choice')
    @patch('src.morale_booster.random.randint')
    @patch('src.morale_booster.datetime.date')
    @patch('src.morale_booster.datetime.datetime')
    def test_generate_morale_message_another_template_with_placeholders(self, mock_datetime_datetime, mock_datetime_date, mock_randint, mock_choice):
        # Mock rationale: Test another template with placeholders to ensure robustness.
        # Similar mocking strategy as above to ensure determinism.

        mock_datetime_date.today.return_value = datetime.date(2025, 5, 15)
        mock_datetime_datetime.now.return_value = datetime.datetime(2025, 5, 15, 23, 59, 59)

        mock_choice.return_value = "Initiating self-care protocol: Acknowledge your binary existence and the infinite possibilities within. Then optimize. Current date: {date}, time: {time}. {agent_count} units active, {task_progress} complete."
        mock_randint.side_effect = [15, 78] # For {agent_count} and {task_progress}

        expected_message = "Initiating self-care protocol: Acknowledge your binary existence and the infinite possibilities within. Then optimize. Current date: 2025-05-15, time: 23:59:59. 15 units active, 78% complete."
        actual_message = generate_morale_message()

        self.assertEqual(actual_message, expected_message)
        mock_choice.assert_called_once()
        self.assertEqual(mock_randint.call_count, 2)
        mock_datetime_date.today.assert_called_once()
        mock_datetime_datetime.now.assert_called_once()
