import unittest
from unittest.mock import patch
import sys
import io
from src.mood_ring import get_apocalypse_mood, main

class TestApocalypseMoodRing(unittest.TestCase):

    def test_deterministic_seed(self):
        # Test with a specific seed to ensure deterministic output
        # Mock rationale: We need to ensure the random number generation is predictable
        # for testing purposes, so we pass a fixed seed.
        result1 = get_apocalypse_mood(seed=42)
        result2 = get_apocalypse_mood(seed=42)
        result3 = get_apocalypse_mood(seed=100)

        self.assertEqual(result1, result2)
        self.assertNotEqual(result1, result3)

        # Verify specific output for a known seed
        # Based on running the script with seed=42, it yields level 3
        self.assertEqual(result1["level"], 3)
        self.assertEqual(result1["vibe"], "Slightly Anxious")
        self.assertEqual(result1["tip"], "Check your bunker's snack supply. Are the Twinkies still fresh?")
        self.assertEqual(result1["emoji"], "😬")

        # Based on running the script with seed=100, it yields level 5
        self.assertEqual(result3["level"], 5)
        self.assertEqual(result3["vibe"], "Imminent Catastrophe")
        self.assertEqual(result3["tip"], "Hug a loved one. Or a sturdy tree. Whichever is closer.")
        self.assertEqual(result3["emoji"], "🤯")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_output_with_seed(self, mock_parse_args, mock_stdout):
        # Mock rationale: We need to capture stdout to verify the printed output
        # and mock argparse to simulate command-line arguments without actually parsing sys.argv.
        mock_parse_args.return_value.seed = 123 # Simulate `python src/mood_ring.py --seed 123`

        main()
        output = mock_stdout.getvalue()

        self.assertIn("🔮 ApocalypsAI Mood Ring 🔮", output)
        # Based on running the script with seed=123, it yields level 3
        self.assertIn("Current Doom Level: 3/5 (😬 Slightly Anxious)", output)
        self.assertIn("Your Apocalyptic Vibe: \"Slightly Anxious\"", output)
        self.assertIn("Whimsical Tip: \"Check your bunker's snack supply. Are the Twinkies still fresh?\"", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.mood_ring.random.seed') # Mock random.seed to ensure get_apocalypse_mood is truly random if no seed is passed
    @patch('src.mood_ring.random.randint', return_value=2) # Mock randint to control the random outcome
    def test_main_output_no_seed(self, mock_randint, mock_random_seed, mock_parse_args, mock_stdout):
        # Mock rationale:
        # - We need to capture stdout to verify the printed output.
        # - We mock argparse to simulate no command-line arguments for seed.
        # - We mock random.seed to prevent actual time-based seeding during test,
        #   though get_apocalypse_mood will call it, we just ensure it doesn't affect randint.
        # - We mock random.randint to ensure a predictable "random" level for the test.
        mock_parse_args.return_value.seed = None

        main()
        output = mock_stdout.getvalue()

        self.assertIn("🔮 ApocalypsAI Mood Ring 🔮", output)
        # With mock_randint returning 2
        self.assertIn("Current Doom Level: 2/5 (🤔 Mildly Concerned)", output)
        self.assertIn("Your Apocalyptic Vibe: \"Mildly Concerned\"", output)
        self.assertIn("Whimsical Tip: \"Perhaps learn to tie a useful knot? Or just enjoy a good book.\"", output)
        mock_random_seed.assert_called_once() # Ensure random.seed was called (with timestamp)
        mock_randint.assert_called_once_with(1, 5) # Ensure randint was called
