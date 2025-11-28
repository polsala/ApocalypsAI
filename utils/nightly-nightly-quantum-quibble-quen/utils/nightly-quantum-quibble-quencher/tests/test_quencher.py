import unittest
from unittest.mock import patch, MagicMock
import sys
import io

# Import the functions from the main script
# Assuming the test file is in 'tests/' and the script is in 'src/'
sys.path.insert(0, 'src')
from quencher import flip_coin, roll_dice, choose_option, main
sys.path.pop(0)


class TestQuibbleQuencher(unittest.TestCase):

    @patch('random.choice')
    def test_flip_coin(self, mock_choice):
        # Mock rationale: Ensure deterministic output for random.choice.
        # We want to control the 'random' outcome for testing.
        mock_choice.return_value = "Heads"
        self.assertEqual(flip_coin(), "Heads")
        mock_choice.assert_called_once_with(["Heads", "Tails"])

        mock_choice.return_value = "Tails"
        self.assertEqual(flip_coin(), "Tails")
        mock_choice.assert_called_with(["Heads", "Tails"]) # Called again

    @patch('random.randint')
    def test_roll_dice(self, mock_randint):
        # Mock rationale: Ensure deterministic output for random.randint.
        # We want to control the 'random' outcome for testing.
        mock_randint.return_value = 3
        self.assertEqual(roll_dice(6), 3)
        mock_randint.assert_called_once_with(1, 6)

        mock_randint.reset_mock()
        mock_randint.return_value = 15
        self.assertEqual(roll_dice(20), 15)
        mock_randint.assert_called_once_with(1, 20)

    def test_roll_dice_invalid_sides(self):
        with self.assertRaisesRegex(ValueError, "Number of sides must be a positive integer."):
            roll_dice(0)
        with self.assertRaisesRegex(ValueError, "Number of sides must be a positive integer."):
            roll_dice(-5)
        with self.assertRaisesRegex(ValueError, "Number of sides must be a positive integer."):
            roll_dice("six")

    @patch('random.choice')
    def test_choose_option(self, mock_choice):
        # Mock rationale: Ensure deterministic output for random.choice.
        # We want to control the 'random' outcome for testing.
        options = ["Apple", "Banana", "Cherry"]
        mock_choice.return_value = "Banana"
        self.assertEqual(choose_option(options), "Banana")
        mock_choice.assert_called_once_with(options)

        mock_choice.reset_mock()
        options_single = ["Only Option"]
        mock_choice.return_value = "Only Option"
        self.assertEqual(choose_option(options_single), "Only Option")
        mock_choice.assert_called_once_with(options_single)

    def test_choose_option_empty_list(self):
        with self.assertRaisesRegex(ValueError, "Please provide at least one option to choose from."):
            choose_option([])

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('random.choice', return_value="Heads") # Mock rationale: Control random output for CLI test
    def test_main_coin(self, mock_random_choice, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: sys.argv is modified for CLI input, sys.exit is mocked to prevent actual exit,
        # sys.stdout/stderr are mocked to capture printed output.
        with patch('sys.argv', ['quencher.py', 'coin']):
            main()
            self.assertEqual(mock_stdout.getvalue().strip(), "Heads")
            mock_exit.assert_not_called() # Should not exit on success

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('random.randint', return_value=4) # Mock rationale: Control random output for CLI test
    def test_main_dice_default(self, mock_random_randint, mock_exit, mock_stderr, mock_stdout):
        with patch('sys.argv', ['quencher.py', 'dice']):
            main()
            self.assertEqual(mock_stdout.getvalue().strip(), "4")
            mock_exit.assert_not_called()

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('random.randint', return_value=17) # Mock rationale: Control random output for CLI test
    def test_main_dice_custom(self, mock_random_randint, mock_exit, mock_stderr, mock_stdout):
        with patch('sys.argv', ['quencher.py', 'dice', '20']):
            main()
            self.assertEqual(mock_stdout.getvalue().strip(), "17")
            mock_exit.assert_not_called()

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_dice_invalid_sides(self, mock_exit, mock_stderr, mock_stdout):
        with patch('sys.argv', ['quencher.py', 'dice', 'abc']):
            main()
            self.assertIn("Error: Dice sides must be an integer.", mock_stderr.getvalue())
            mock_exit.assert_called_once_with(1)

        mock_exit.reset_mock()
        mock_stderr.seek(0) and mock_stderr.truncate(0) # Clear stderr for next test
        with patch('sys.argv', ['quencher.py', 'dice', '0']):
            main()
            self.assertIn("Error: Number of sides must be a positive integer.", mock_stderr.getvalue())
            mock_exit.assert_called_once_with(1)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('random.choice', return_value="Fortify West") # Mock rationale: Control random output for CLI test
    def test_main_choose(self, mock_random_choice, mock_exit, mock_stderr, mock_stdout):
        with patch('sys.argv', ['quencher.py', 'choose', 'Scavenge East', 'Fortify West', 'Nap Indefinitely']):
            main()
            self.assertEqual(mock_stdout.getvalue().strip(), "Fortify West")
            mock_exit.assert_not_called()

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_choose_no_options(self, mock_exit, mock_stderr, mock_stdout):
        with patch('sys.argv', ['quencher.py', 'choose']):
            main()
            self.assertIn("Error: Please provide options for 'choose'.", mock_stderr.getvalue())
            mock_exit.assert_called_once_with(1)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_no_command(self, mock_exit, mock_stderr, mock_stdout):
        with patch('sys.argv', ['quencher.py']):
            main()
            self.assertIn("Usage:", mock_stdout.getvalue()) # Usage printed to stdout
            mock_exit.assert_called_once_with(1)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_unknown_command(self, mock_exit, mock_stderr, mock_stdout):
        with patch('sys.argv', ['quencher.py', 'unknown_cmd']):
            main()
            self.assertIn("Error: Unknown command 'unknown_cmd'", mock_stderr.getvalue())
            mock_exit.assert_called_once_with(1)
