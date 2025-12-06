import unittest
from unittest.mock import patch
import sys
import io
from src.vibe_checker import calculate_vibe, main

class TestVibeChecker(unittest.TestCase):

    def test_calculate_vibe_serenely_doomed(self):
        # Mock rationale: Testing the core logic of calculate_vibe, which is a pure function.
        # No external dependencies or side effects, so direct function call is sufficient.
        mood, emoji, score = calculate_vibe(open_issues=0, failed_workflows_24h=0, days_since_last_commit=0)
        self.assertEqual(mood, "Serenely Doomed")
        self.assertEqual(emoji, "🌿")
        self.assertAlmostEqual(score, 0.0)

        mood, emoji, score = calculate_vibe(open_issues=2, failed_workflows_24h=0, days_since_last_commit=10)
        self.assertEqual(mood, "Serenely Doomed")
        self.assertEqual(emoji, "🌿")
        self.assertAlmostEqual(score, 3.0) # (2*0.5) + (0*2.0) + (10*0.2) = 1 + 0 + 2 = 3

    def test_calculate_vibe_mildly_gloomy(self):
        # Mock rationale: Testing the core logic of calculate_vibe, which is a pure function.
        # No external dependencies or side effects, so direct function call is sufficient.
        mood, emoji, score = calculate_vibe(open_issues=5, failed_workflows_24h=1, days_since_last_commit=3)
        self.assertEqual(mood, "Mildly Gloomy")
        self.assertEqual(emoji, "🌧️")
        self.assertAlmostEqual(score, 5.1) # (5*0.5) + (1*2.0) + (3*0.2) = 2.5 + 2 + 0.6 = 5.1

        mood, emoji, score = calculate_vibe(open_issues=10, failed_workflows_24h=2, days_since_last_commit=5)
        self.assertEqual(mood, "Mildly Gloomy")
        self.assertEqual(emoji, "🌧️")
        self.assertAlmostEqual(score, 10.0) # (10*0.5) + (2*2.0) + (5*0.2) = 5 + 4 + 1 = 10

    def test_calculate_vibe_chaotic_neutral(self):
        # Mock rationale: Testing the core logic of calculate_vibe, which is a pure function.
        # No external dependencies or side effects, so direct function call is sufficient.
        mood, emoji, score = calculate_vibe(open_issues=20, failed_workflows_24h=3, days_since_last_commit=10)
        self.assertEqual(mood, "Chaotic Neutral")
        self.assertEqual(emoji, "🌀")
        self.assertAlmostEqual(score, 18.0) # (20*0.5) + (3*2.0) + (10*0.2) = 10 + 6 + 2 = 18

        mood, emoji, score = calculate_vibe(open_issues=30, failed_workflows_24h=5, days_since_last_commit=20)
        self.assertEqual(mood, "Chaotic Neutral")
        self.assertEqual(emoji, "🌀")
        self.assertAlmostEqual(score, 29.0) # (30*0.5) + (5*2.0) + (20*0.2) = 15 + 10 + 4 = 29

    def test_calculate_vibe_imminent_collapse(self):
        # Mock rationale: Testing the core logic of calculate_vibe, which is a pure function.
        # No external dependencies or side effects, so direct function call is sufficient.
        mood, emoji, score = calculate_vibe(open_issues=30, failed_workflows_24h=6, days_since_last_commit=20)
        self.assertEqual(mood, "Imminent Collapse")
        self.assertEqual(emoji, "💥")
        self.assertAlmostEqual(score, 31.0) # (30*0.5) + (6*2.0) + (20*0.2) = 15 + 12 + 4 = 31

        mood, emoji, score = calculate_vibe(open_issues=50, failed_workflows_24h=10, days_since_last_commit=50)
        self.assertEqual(mood, "Imminent Collapse")
        self.assertEqual(emoji, "💥")
        self.assertAlmostEqual(score, 55.0) # (50*0.5) + (10*2.0) + (50*0.2) = 25 + 20 + 10 = 55

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_output(self, mock_stdout, mock_parse_args):
        # Mock rationale: We need to mock argparse.ArgumentParser.parse_args to simulate command-line arguments
        # without actually passing them via sys.argv. We also mock sys.stdout to capture the printed output.
        mock_parse_args.return_value = argparse.Namespace(
            open_issues=5,
            failed_workflows_24h=1,
            days_since_last_commit=3
        )
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Repository Vibe: Mildly Gloomy 🌧️ (Score: 5.1)")

        mock_parse_args.return_value = argparse.Namespace(
            open_issues=0,
            failed_workflows_24h=0,
            days_since_last_commit=0
        )
        mock_stdout.seek(0) # Reset stdout buffer
        mock_stdout.truncate(0)
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Repository Vibe: Serenely Doomed 🌿 (Score: 0.0)")

        mock_parse_args.return_value = argparse.Namespace(
            open_issues=30,
            failed_workflows_24h=6,
            days_since_last_commit=20
        )
        mock_stdout.seek(0) # Reset stdout buffer
        mock_stdout.truncate(0)
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Repository Vibe: Imminent Collapse 💥 (Score: 31.0)")

if __name__ == '__main__':
    unittest.main()
