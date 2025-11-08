import unittest
import sys
from unittest.mock import patch
from io import StringIO

# Mock rationale: We need to test the main function's output to stdout
# without actually printing to the console during tests.
# patch('sys.stdout', new_callable=StringIO) allows capturing stdout.
# Mock rationale: We need to test the main function's behavior with different
# command-line arguments without actually modifying sys.argv for the test runner.
# patch('sys.argv', [...]) allows setting arguments for the duration of the test.
# Mock rationale: We need to test the main function's exit behavior without
# actually terminating the test suite.
# patch('sys.exit') allows intercepting sys.exit calls.

# Add the src directory to the Python path for importing the module
sys.path.insert(0, 'src')
from mood_ring import get_apocalypse_mood, COLOR_RESET, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_ORANGE, COLOR_RED, COLOR_WHITE_ON_BLACK

class TestApocalypseMoodRing(unittest.TestCase):

    def test_get_apocalypse_mood_valid_ranges(self):
        # Test Serene Blue
        self.assertEqual(get_apocalypse_mood(0), ("Serene Blue", COLOR_BLUE, "All clear! The end is not nigh... yet. Enjoy the quiet."))
        self.assertEqual(get_apocalypse_mood(5), ("Serene Blue", COLOR_BLUE, "All clear! The end is not nigh... yet. Enjoy the quiet."))
        self.assertEqual(get_apocalypse_mood(10), ("Serene Blue", COLOR_BLUE, "All clear! The end is not nigh... yet. Enjoy the quiet."))

        # Test Verdant Green
        self.assertEqual(get_apocalypse_mood(11), ("Verdant Green", COLOR_GREEN, "Mild tremors. Perhaps just a bad burrito. Keep calm and carry on."))
        self.assertEqual(get_apocalypse_mood(20), ("Verdant Green", COLOR_GREEN, "Mild tremors. Perhaps just a bad burrito. Keep calm and carry on."))
        self.assertEqual(get_apocalypse_mood(30), ("Verdant Green", COLOR_GREEN, "Mild tremors. Perhaps just a bad burrito. Keep calm and carry on."))

        # Test Sunny Yellow
        self.assertEqual(get_apocalypse_mood(31), ("Sunny Yellow", COLOR_YELLOW, "Warning: Minor existential dread detected. Stock up on snacks, just in case."))
        self.assertEqual(get_apocalypse_mood(40), ("Sunny Yellow", COLOR_YELLOW, "Warning: Minor existential dread detected. Stock up on snacks, just in case."))
        self.assertEqual(get_apocalypse_mood(50), ("Sunny Yellow", COLOR_YELLOW, "Warning: Minor existential dread detected. Stock up on snacks, just in case."))

        # Test Fiery Orange
        self.assertEqual(get_apocalypse_mood(51), ("Fiery Orange", COLOR_ORANGE, "Elevated anxiety. The sky looks a bit... off. Check your escape routes."))
        self.assertEqual(get_apocalypse_mood(60), ("Fiery Orange", COLOR_ORANGE, "Elevated anxiety. The sky looks a bit... off. Check your escape routes."))
        self.assertEqual(get_apocalypse_mood(70), ("Fiery Orange", COLOR_ORANGE, "Elevated anxiety. The sky looks a bit... off. Check your escape routes."))

        # Test Crimson Red
        self.assertEqual(get_apocalypse_mood(71), ("Crimson Red", COLOR_RED, "Critical alert! The fabric of reality is fraying. Panic (briefly) permitted."))
        self.assertEqual(get_apocalypse_mood(80), ("Crimson Red", COLOR_RED, "Critical alert! The fabric of reality is fraying. Panic (briefly) permitted."))
        self.assertEqual(get_apocalypse_mood(90), ("Crimson Red", COLOR_RED, "Critical alert! The fabric of reality is fraying. Panic (briefly) permitted."))

        # Test Void Black
        self.assertEqual(get_apocalypse_mood(91), ("Void Black", COLOR_WHITE_ON_BLACK, "Absolute chaos. It's been fun. Or not. Who can tell anymore?"))
        self.assertEqual(get_apocalypse_mood(100), ("Void Black", COLOR_WHITE_ON_BLACK, "Absolute chaos. It's been fun. Or not. Who can tell anymore?"))

    def test_get_apocalypse_mood_invalid_input(self):
        with self.assertRaises(ValueError):
            get_apocalypse_mood(-1)
        with self.assertRaises(ValueError):
            get_apocalypse_mood(101)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['mood_ring.py', '5'])
    def test_main_valid_input_tty(self, mock_exit, mock_stdout):
        # Mock rationale: Simulate a TTY environment for color output
        with patch('sys.stdout.isatty', return_value=True):
            from mood_ring import main
            main()
            expected_output = f"{COLOR_BLUE}Serene Blue: All clear! The end is not nigh... yet. Enjoy the quiet.{COLOR_RESET}\n"
            self.assertEqual(mock_stdout.getvalue(), expected_output)
            mock_exit.assert_not_called() # Should not exit on success

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['mood_ring.py', '65'])
    def test_main_valid_input_no_tty(self, mock_exit, mock_stdout):
        # Mock rationale: Simulate a non-TTY environment for no color output
        with patch('sys.stdout.isatty', return_value=False):
            from mood_ring import main
            main()
            expected_output = "Fiery Orange: Elevated anxiety. The sky looks a bit... off. Check your escape routes.\n"
            self.assertEqual(mock_stdout.getvalue(), expected_output)
            mock_exit.assert_not_called()

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['mood_ring.py'])
    def test_main_no_arguments(self, mock_exit, mock_stdout):
        from mood_ring import main
        main()
        self.assertIn("Usage: python src/mood_ring.py <severity_index>", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['mood_ring.py', 'abc'])
    def test_main_non_integer_argument(self, mock_exit, mock_stdout):
        from mood_ring import main
        main()
        self.assertIn("Error: Severity index must be an integer.", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['mood_ring.py', '101'])
    def test_main_out_of_range_argument(self, mock_exit, mock_stdout):
        from mood_ring import main
        main()
        self.assertIn("Error: Severity index must be between 0 and 100.", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['mood_ring.py', '-5'])
    def test_main_negative_argument(self, mock_exit, mock_stdout):
        from mood_ring import main
        main()
        self.assertIn("Error: Severity index must be between 0 and 100.", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
