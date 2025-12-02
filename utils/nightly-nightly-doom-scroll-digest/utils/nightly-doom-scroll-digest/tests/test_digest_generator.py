import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone
import json
import os
import requests

# Mock rationale: We need to simulate network requests to the GitHub API
# without actually making them. This ensures tests are fast, deterministic,
# and don't rely on external services or API rate limits.
# We mock `requests.get` to return predefined JSON responses.
# We also mock `datetime.now` to ensure date calculations are deterministic.

# Import the function to be tested. Adjust path for test discovery from repo root.
from utils.nightly_doom_scroll_digest.src.digest_generator import generate_digest

class TestDigestGenerator(unittest.TestCase):

    def setUp(self):
        self.repo_owner = 'test_owner'
        self.repo_name = 'test_repo'
        self.github_token = 'mock_token'
        self.days_back = 1

        # Define a fixed current UTC time for deterministic date calculations
        self.mock_now_utc = datetime(2023, 10, 27, 10, 0, 0, tzinfo=timezone.utc)
        self.expected_since_date = (self.mock_now_utc - timedelta(days=self.days_back)).isoformat(timespec='seconds')

    @patch('requests.get')
    @patch('utils.nightly_doom_scroll_digest.src.digest_generator.datetime')
    def test_generate_digest_with_activity(self, mock_datetime, mock_requests_get):
        # Configure mock datetime to return fixed values
        mock_datetime.now.return_value = self.mock_now_utc
        mock_datetime.now.side_effect = lambda tz=None: self.mock_now_utc if tz == timezone.utc else datetime(2023, 10, 27, 10, 0, 0) # Handle calls with and without tzinfo
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) if not kw.get('tzinfo') else self.mock_now_utc
        mock_datetime.timezone = timezone # Ensure timezone is available

        # Mock GitHub API responses
        mock_requests_get.side_effect = [
            # Issues response (includes a PR-like issue to ensure filtering works)
            MagicMock(status_code=200, json=lambda: [
                {'title': 'Bug: UI is melting', 'number': 1, 'state': 'open', 'html_url': 'http://example.com/issue/1'},
                {'title': 'Feature: Add lasers', 'number': 2, 'state': 'closed', 'html_url': 'http://example.com/issue/2'},
                {'title': 'PR-like issue', 'number': 3, 'state': 'open', 'html_url': 'http://example.com/issue/3', 'pull_request': {'url': 'http://example.com/pr/3'}}
            ]),
            # Pull Requests response
            MagicMock(status_code=200, json=lambda: [
                {'title': 'feat: Self-destruct button', 'number': 10, 'state': 'merged', 'html_url': 'http://example.com/pr/10'},
                {'title': 'fix: Prevent self-destruct', 'number': 11, 'state': 'open', 'html_url': 'http://example.com/pr/11'}
            ]),
            # Commits response
            MagicMock(status_code=200, json=lambda: [
                {'sha': 'abcdef1234567890', 'commit': {'message': 'feat: Add lasers\n\nMore details', 'author': {'name': 'Alice'}}, 'html_url': 'http://example.com/commit/abc'},
                {'sha': 'fedcba0987654321', 'commit': {'message': 'docs: Update README', 'author': {'name': 'Bob'}}, 'html_url': 'http://example.com/commit/fed'}
            ])
        ]

        expected_output_parts = [
            "--- The Scroll of Recent Portents ---",
            "Date: 2023-10-27",
            "Repository: test_owner/test_repo",
            "--- New Anomalies Detected (Issues) ---",
            "*   [#1] Bug: UI is melting (open) - http://example.com/issue/1",
            "*   [#2] Feature: Add lasers (closed) - http://example.com/issue/2",
            "--- Convergences Observed (Pull Requests) ---",
            "*   [#10] feat: Self-destruct button (merged) - http://example.com/pr/10",
            "*   [#11] fix: Prevent self-destruct (open) - http://example.com/pr/11",
            "--- Temporal Fluxes Recorded (Commits) ---",
            "*   [abcdef1] feat: Add lasers (Alice) - http://example.com/commit/abc",
            "*   [fedcba0] docs: Update README (Bob) - http://example.com/commit/fed",
            "--- The Oracle has spoken. ---"
        ]

        digest = generate_digest(self.repo_owner, self.repo_name, self.github_token, self.days_back)

        for part in expected_output_parts:
            self.assertIn(part, digest)
        self.assertNotIn('PR-like issue', digest) # Ensure PR-like issues are filtered out from issues list

        # Verify that requests.get was called for issues, pulls, and commits with correct 'since' date
        self.assertEqual(mock_requests_get.call_count, 3)
        mock_requests_get.assert_any_call(
            f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/issues?state=all&since={self.expected_since_date}',
            headers={'Authorization': f'token {self.github_token}'}
        )
        mock_requests_get.assert_any_call(
            f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/pulls?state=all&since={self.expected_since_date}',
            headers={'Authorization': f'token {self.github_token}'}
        )
        mock_requests_get.assert_any_call(
            f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/commits?since={self.expected_since_date}',
            headers={'Authorization': f'token {self.github_token}'}
        )

    @patch('requests.get')
    @patch('utils.nightly_doom_scroll_digest.src.digest_generator.datetime')
    def test_generate_digest_no_activity(self, mock_datetime, mock_requests_get):
        mock_datetime.now.return_value = self.mock_now_utc
        mock_datetime.now.side_effect = lambda tz=None: self.mock_now_utc if tz == timezone.utc else datetime(2023, 10, 27, 10, 0, 0)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) if not kw.get('tzinfo') else self.mock_now_utc
        mock_datetime.timezone = timezone

        # Mock GitHub API responses to return empty lists (no activity)
        mock_requests_get.side_effect = [
            MagicMock(status_code=200, json=lambda: []), # Issues
            MagicMock(status_code=200, json=lambda: []), # Pull Requests
            MagicMock(status_code=200, json=lambda: [])  # Commits
        ]

        expected_output_parts = [
            "--- The Scroll of Recent Portents ---",
            "Date: 2023-10-27",
            "Repository: test_owner/test_repo",
            "--- New Anomalies Detected (Issues) ---",
            "*   No new anomalies detected.",
            "--- Convergences Observed (Pull Requests) ---",
            "*   No new convergences observed.",
            "--- Temporal Fluxes Recorded (Commits) ---",
            "*   No new temporal fluxes recorded.",
            "--- The Oracle has spoken. ---"
        ]

        digest = generate_digest(self.repo_owner, self.repo_name, self.github_token, self.days_back)

        for part in expected_output_parts:
            self.assertIn(part, digest)

        self.assertEqual(mock_requests_get.call_count, 3)

    @patch('requests.get')
    @patch('utils.nightly_doom_scroll_digest.src.digest_generator.datetime')
    def test_generate_digest_api_error(self, mock_datetime, mock_requests_get):
        mock_datetime.now.return_value = self.mock_now_utc
        mock_datetime.now.side_effect = lambda tz=None: self.mock_now_utc if tz == timezone.utc else datetime(2023, 10, 27, 10, 0, 0)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) if not kw.get('tzinfo') else self.mock_now_utc
        mock_datetime.timezone = timezone

        # Mock GitHub API to raise an HTTP error
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('403 Client Error: Forbidden for url: ...')
        mock_requests_get.side_effect = [mock_response]

        with self.assertRaises(requests.exceptions.RequestException) as cm:
            generate_digest(self.repo_owner, self.repo_name, self.github_token, self.days_back)
        self.assertIn('403 Client Error', str(cm.exception))

        self.assertEqual(mock_requests_get.call_count, 1)

    @patch('requests.get')
    @patch('utils.nightly_doom_scroll_digest.src.digest_generator.datetime')
    def test_main_script_execution(self, mock_datetime, mock_requests_get):
        mock_datetime.now.return_value = self.mock_now_utc
        mock_datetime.now.side_effect = lambda tz=None: self.mock_now_utc if tz == timezone.utc else datetime(2023, 10, 27, 10, 0, 0)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) if not kw.get('tzinfo') else self.mock_now_utc
        mock_datetime.timezone = timezone

        # Mock GitHub API responses for main execution
        mock_requests_get.side_effect = [
            MagicMock(status_code=200, json=lambda: [
                {'title': 'Bug: UI is melting', 'number': 1, 'state': 'open', 'html_url': 'http://example.com/issue/1'}
            ]),
            MagicMock(status_code=200, json=lambda: [
                {'title': 'feat: Self-destruct button', 'number': 10, 'state': 'merged', 'html_url': 'http://example.com/pr/10'}
            ]),
            MagicMock(status_code=200, json=lambda: [
                {'sha': 'abcdef1234567890', 'commit': {'message': 'feat: Add lasers', 'author': {'name': 'Alice'}}, 'html_url': 'http://example.com/commit/abc'}
            ])
        ]

        # Mock argparse to simulate command-line arguments
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args,
             patch('sys.stdout', new_callable=MagicMock) as mock_stdout,
             patch('sys.stderr', new_callable=MagicMock) as mock_stderr,
             patch('sys.exit') as mock_exit:

            mock_parse_args.return_value = MagicMock(
                repo_owner=self.repo_owner,
                repo_name=self.repo_name,
                github_token=self.github_token,
                days_back=self.days_back
            )

            # Import and run main from the script
            from utils.nightly_doom_scroll_digest.src import digest_generator
            digest_generator.main()

            # Assert that output was printed to stdout
            mock_stdout.write.assert_called()
            self.assertIn('--- The Scroll of Recent Portents ---', mock_stdout.write.call_args[0][0])
            mock_exit.assert_not_called()

    @patch('requests.get')
    @patch('utils.nightly_doom_scroll_digest.src.digest_generator.datetime')
    def test_main_script_execution_api_error(self, mock_datetime, mock_requests_get):
        mock_datetime.now.return_value = self.mock_now_utc
        mock_datetime.now.side_effect = lambda tz=None: self.mock_now_utc if tz == timezone.utc else datetime(2023, 10, 27, 10, 0, 0)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) if not kw.get('tzinfo') else self.mock_now_utc
        mock_datetime.timezone = timezone

        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('403 Client Error: Forbidden for url: ...')
        mock_requests_get.side_effect = [mock_response]

        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args,
             patch('sys.stdout', new_callable=MagicMock) as mock_stdout,
             patch('sys.stderr', new_callable=MagicMock) as mock_stderr,
             patch('sys.exit') as mock_exit:

            mock_parse_args.return_value = MagicMock(
                repo_owner=self.repo_owner,
                repo_name=self.repo_name,
                github_token=self.github_token,
                days_back=self.days_back
            )

            from utils.nightly_doom_scroll_digest.src import digest_generator
            digest_generator.main()

            mock_stderr.write.assert_called()
            self.assertIn('Error fetching data from GitHub: 403 Client Error', mock_stderr.write.call_args[0][0])
            mock_exit.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
