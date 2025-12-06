import unittest
from unittest.mock import patch, MagicMock
import json
from datetime import datetime, timedelta
import requests # Import requests to catch HTTPError
from src import sentiment_analyzer

class TestSentimentAnalyzer(unittest.TestCase):

    def setUp(self):
        self.repo = "test_owner/test_repo"
        self.token = "test_token"
        self.since_days = 7

    def mock_github_response(self, status_code, json_data):
        """Helper to create a mock requests.Response object."""
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        mock_resp.json.return_value = json_data
        mock_resp.raise_for_status.side_effect = (
            None if status_code < 400 else requests.exceptions.HTTPError(response=mock_resp)
        )
        return mock_resp

    @patch('requests.get')
    def test_fetch_github_activity_success(self, mock_get):
        # Mock rationale: Simulates GitHub API responses for issues and comments
        # without making actual network calls, ensuring deterministic tests.
        mock_get.side_effect = [
            self.mock_github_response(200, [
                {"title": "Fixed a bug", "body": "This is a great fix.", "comments_url": "http://comments/1"},
                {"title": "New feature", "body": "Adding a new feature.", "comments_url": "http://comments/2"}
            ]),
            self.mock_github_response(200, [
                {"body": "Approved, excellent work!"}
            ]),
            self.mock_github_response(200, [
                {"body": "Needs review, problem found."}
            ])
        ]

        activity = sentiment_analyzer.fetch_github_activity(self.repo, self.token, self.since_days)
        self.assertEqual(len(activity), 4) # 2 issues/PRs + 2 comments
        self.assertIn("great fix", activity[0]["text"])
        self.assertIn("excellent work", activity[2]["text"])
        self.assertIn("problem found", activity[3]["text"])

    @patch('requests.get')
    def test_fetch_github_activity_api_error(self, mock_get):
        # Mock rationale: Simulates a GitHub API error (e.g., 403 Forbidden)
        # to test error handling without actual network failures.
        mock_get.return_value = self.mock_github_response(403, {"message": "Forbidden"})

        activity = sentiment_analyzer.fetch_github_activity(self.repo, self.token, self.since_days)
        self.assertEqual(activity, []) # Should return empty list on error

    def test_analyze_sentiment_positive(self):
        activity = [
            {"type": "issue_pr", "text": "Great success! This is excellent."},
            {"type": "comment", "text": "Approved and merged. Good job."}
        ]
        sentiment = sentiment_analyzer.analyze_sentiment(activity)
        self.assertGreater(sentiment["positive"], 0)
        self.assertEqual(sentiment["negative"], 0)
        self.assertEqual(sentiment["neutral"], 0)

    def test_analyze_sentiment_negative(self):
        activity = [
            {"type": "issue_pr", "text": "Bug found: critical error. This is a problem."},
            {"type": "comment", "text": "Failed to deploy. Urgent fix needed."}
        ]
        sentiment = sentiment_analyzer.analyze_sentiment(activity)
        self.assertEqual(sentiment["positive"], 0)
        self.assertGreater(sentiment["negative"], 0)
        self.assertEqual(sentiment["neutral"], 0)

    def test_analyze_sentiment_neutral(self):
        activity = [
            {"type": "issue_pr", "text": "Refactor workflow. Update docs."},
            {"type": "comment", "text": "Chore: add new test config."}
        ]
        sentiment = sentiment_analyzer.analyze_sentiment(activity)
        self.assertEqual(sentiment["positive"], 0)
        self.assertEqual(sentiment["negative"], 0)
        self.assertGreater(sentiment["neutral"], 0)

    def test_analyze_sentiment_mixed(self):
        activity = [
            {"type": "issue_pr", "text": "Fixed a bug, great work! But there's a minor problem."},
            {"type": "comment", "text": "Approved, but needs a refactor."}
        ]
        sentiment = sentiment_analyzer.analyze_sentiment(activity)
        self.assertGreater(sentiment["positive"], 0)
        self.assertGreater(sentiment["negative"], 0)
        self.assertGreater(sentiment["neutral"], 0)

    def test_determine_mood_joyful(self):
        mood, emoji = sentiment_analyzer.determine_mood({"positive": 10, "negative": 1, "neutral": 2})
        self.assertEqual(mood, "Joyful")
        self.assertEqual(emoji, "🎉")

    def test_determine_mood_concerned(self):
        mood, emoji = sentiment_analyzer.determine_mood({"positive": 1, "negative": 10, "neutral": 2})
        self.assertEqual(mood, "Concerned")
        self.assertEqual(emoji, "😟")

    def test_determine_mood_productive(self):
        mood, emoji = sentiment_analyzer.determine_mood({"positive": 2, "negative": 1, "neutral": 10})
        self.assertEqual(mood, "Productive")
        self.assertEqual(emoji, "🚀")

    def test_determine_mood_optimistic(self):
        mood, emoji = sentiment_analyzer.determine_mood({"positive": 5, "negative": 2, "neutral": 3})
        self.assertEqual(mood, "Optimistic")
        self.assertEqual(emoji, "✨")

    def test_determine_mood_troubled(self):
        mood, emoji = sentiment_analyzer.determine_mood({"positive": 2, "negative": 5, "neutral": 3})
        self.assertEqual(mood, "Troubled")
        self.assertEqual(emoji, "🚧")

    def test_determine_mood_balanced(self):
        mood, emoji = sentiment_analyzer.determine_mood({"positive": 3, "negative": 3, "neutral": 3})
        self.assertEqual(mood, "Balanced")
        self.assertEqual(emoji, "⚖️")
        
        mood, emoji = sentiment_analyzer.determine_mood({"positive": 4, "negative": 3, "neutral": 5})
        self.assertEqual(mood, "Balanced")
        self.assertEqual(emoji, "⚖️")

    def test_determine_mood_quietly_observing(self):
        mood, emoji = sentiment_analyzer.determine_mood({"positive": 0, "negative": 0, "neutral": 0})
        self.assertEqual(mood, "Quietly Observing")
        self.assertEqual(emoji, "👁️")

    @patch('src.sentiment_analyzer.fetch_github_activity', return_value=[])
    @patch('builtins.print')
    def test_main_no_activity(self, mock_print, mock_fetch):
        # Mock rationale: Simulates no activity being returned from GitHub API
        # to test the main function's handling of this edge case.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(repo=self.repo, token=self.token, since_days=7)):
            with self.assertRaises(SystemExit) as cm:
                sentiment_analyzer.main()
            self.assertEqual(cm.exception.code, 0) # Exit code 0 for no-op/success
            mock_print.assert_any_call("No recent activity found or error fetching activity. Mood: Quietly Observing 👁️")

    @patch('src.sentiment_analyzer.fetch_github_activity')
    @patch('src.sentiment_analyzer.analyze_sentiment')
    @patch('src.sentiment_analyzer.determine_mood', return_value=("Test Mood", "😊"))
    @patch('builtins.print')
    def test_main_success(self, mock_print, mock_determine_mood, mock_analyze_sentiment, mock_fetch_activity):
        # Mock rationale: Mocks all external dependencies to isolate and test
        # the main function's flow and output.
        mock_fetch_activity.return_value = [{"text": "some activity"}]
        mock_analyze_sentiment.return_value = {"positive": 1, "negative": 1, "neutral": 1}

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(repo=self.repo, token=self.token, since_days=7)):
            sentiment_analyzer.main()
            mock_print.assert_any_call(f"Analyzing sentiment for {self.repo}...")
            mock_print.assert_any_call("Recent activity mood: Test Mood 😊")
            mock_print.assert_any_call("Sentiment Breakdown:")
            mock_print.assert_any_call("  Positive: 1")
            mock_print.assert_any_call("  Negative: 1")
            mock_print.assert_any_call("  Neutral: 1")

    @patch('builtins.print')
    def test_main_no_token(self, mock_print):
        # Mock rationale: Simulates running the script without a GitHub token
        # to test the argument parsing and error handling.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(repo=self.repo, token=None, since_days=7)):
            with patch.dict(os.environ, {}, clear=True): # Ensure GITHUB_TOKEN env var is not set
                with self.assertRaises(SystemExit) as cm:
                    sentiment_analyzer.main()
                self.assertEqual(cm.exception.code, 1) # Exit code 1 for failure
                mock_print.assert_any_call("Error: GitHub token is required. Please provide it via --token or GITHUB_TOKEN environment variable.")


if __name__ == '__main__':
    unittest.main()
