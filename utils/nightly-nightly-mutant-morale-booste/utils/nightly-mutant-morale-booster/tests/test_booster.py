import unittest
import datetime
from unittest.mock import patch
from src.booster import get_daily_message, MESSAGES

class TestBooster(unittest.TestCase):

    @patch('datetime.date')
    def test_get_daily_message_deterministic(self, mock_date):
        # Mock rationale: We need to ensure that `get_daily_message` produces
        # the same output for a given date, regardless of when the test is run.
        # By patching `datetime.date.today()`, we can control the date used
        # for seeding the random number generator.

        # Test a specific date
        fixed_date = datetime.date(2023, 10, 27)
        mock_date.today.return_value = fixed_date

        message1 = get_daily_message()
        message2 = get_daily_message() # Call again for the same date

        self.assertEqual(message1, message2)
        self.assertIn("[Morale Booster]", message1)
        self.assertTrue(any(msg in message1 for msg in MESSAGES))

        # Test a different date to ensure messages change
        another_date = datetime.date(2023, 10, 28)
        mock_date.today.return_value = another_date

        message3 = get_daily_message()
        self.assertNotEqual(message1, message3) # Message should be different for a different day
        self.assertIn("[Morale Booster]", message3)
        self.assertTrue(any(msg in message3 for msg in MESSAGES))

    def test_get_daily_message_with_explicit_date(self):
        # Test direct date passing for determinism without patching today()
        date1 = datetime.date(2024, 1, 1)
        message_for_date1_a = get_daily_message(date1)
        message_for_date1_b = get_daily_message(date1)

        self.assertEqual(message_for_date1_a, message_for_date1_b)
        self.assertIn("[Morale Booster]", message_for_date1_a)
        self.assertTrue(any(msg in message_for_date1_a for msg in MESSAGES))

        date2 = datetime.date(2024, 1, 2)
        message_for_date2 = get_daily_message(date2)
        self.assertNotEqual(message_for_date1_a, message_for_date2)
        self.assertIn("[Morale Booster]", message_for_date2)
        self.assertTrue(any(msg in message_for_date2 for msg in MESSAGES))

    def test_messages_list_not_empty(self):
        self.assertGreater(len(MESSAGES), 0, "MESSAGES list should not be empty")

    def test_message_format(self):
        # Test that the output always starts with the prefix
        message = get_daily_message(datetime.date(2000, 1, 1)) # Use a fixed date
        self.assertTrue(message.startswith("[Morale Booster] "))

if __name__ == '__main__':
    unittest.main()
