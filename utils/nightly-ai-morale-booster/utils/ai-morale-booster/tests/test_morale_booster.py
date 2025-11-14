import unittest
import sys
import io
from unittest.mock import patch
from datetime import date

# Mock rationale: We need to mock sys.argv to simulate command-line arguments
# without actually running the script as a separate process. This allows
# testing the main function's behavior directly.
# Mock rationale: We need to mock sys.stdout to capture the printed output
# of the script and assert its content, ensuring the correct messages are displayed.
# Mock rationale: We need to mock datetime.date.today() to ensure deterministic
# results for the --daily option, as the 'daily' boost depends on the current date.

# Add the src directory to the Python path to import morale_booster
sys.path.insert(0, 'utils/ai-morale-booster/src')
import morale_booster
sys.path.pop(0)

class TestMoraleBooster(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_output = io.StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        # Restore stdout
        sys.stdout = sys.__stdout__

    @patch('sys.argv', ['morale_booster.py', '--new'])
    def test_new_boost_output(self):
        morale_booster.main()
        output = self.held_output.getvalue().strip()
        self.assertTrue(output.startswith('[AI Morale Core]: '))
        self.assertIn(output[len('[AI Morale Core]: '):], morale_booster.MORALE_BOOSTS)

    @patch('datetime.date')
    @patch('sys.argv', ['morale_booster.py', '--daily'])
    def test_daily_boost_deterministic(self, mock_date):
        # Mock rationale: Ensure deterministic date for --daily option.
        # We set a fixed date (e.g., Jan 1, 2023) to get a consistent daily boost.
        mock_date.today.return_value = date(2023, 1, 1)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        morale_booster.main()
        output1 = self.held_output.getvalue().strip()
        self.held_output.seek(0)
        self.held_output.truncate(0)

        # Run again with the same mocked date
        morale_booster.main()
        output2 = self.held_output.getvalue().strip()

        self.assertEqual(output1, output2)
        self.assertTrue(output1.startswith('[AI Daily Directive]: '))
        self.assertIn(output1[len('[AI Daily Directive]: '):], morale_booster.MORALE_BOOSTS)

    @patch('datetime.date')
    @patch('sys.argv', ['morale_booster.py', '--daily'])
    def test_daily_boost_changes_with_date(self, mock_date):
        # Mock rationale: Verify that changing the date results in a different daily boost.
        # This confirms the date-dependent seeding mechanism works as expected.
        mock_date.today.return_value = date(2023, 1, 1)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        morale_booster.main()
        output_jan1 = self.held_output.getvalue().strip()
        self.held_output.seek(0)
        self.held_output.truncate(0)

        mock_date.today.return_value = date(2023, 1, 2)
        morale_booster.main()
        output_jan2 = self.held_output.getvalue().strip()

        self.assertNotEqual(output_jan1, output_jan2)

    @patch('sys.argv', ['morale_booster.py'])
    def test_no_args_prints_help(self):
        with patch('sys.stderr', new=io.StringIO()) as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                morale_booster.main()
            self.assertEqual(cm.exception.code, 0) # argparse exits with 0 for help
            output = self.held_output.getvalue().strip()
            self.assertIn('usage: morale_booster.py', output)
            self.assertIn('Get AI-generated affirmations.', output)

    @patch('sys.argv', ['morale_booster.py', '--invalid-arg'])
    def test_invalid_arg_prints_error_and_help(self):
        with patch('sys.stderr', new=io.StringIO()) as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                morale_booster.main()
            self.assertEqual(cm.exception.code, 2) # argparse exits with 2 for invalid args
            error_output = mock_stderr.getvalue().strip()
            self.assertIn('unrecognized arguments: --invalid-arg', error_output)
            help_output = self.held_output.getvalue().strip()
            self.assertIn('usage: morale_booster.py', help_output)

if __name__ == '__main__':
    unittest.main()
