import unittest
from unittest.mock import patch, MagicMock
import os
from datetime import datetime, timedelta, timezone

# Mock rationale: We need to mock the 'requests' library to prevent actual network calls
# to the GitHub API during testing. This ensures tests are deterministic, fast, and
# do not depend on external services or network connectivity.
# We also mock os.getenv to control the GITHUB_TOKEN for testing purposes.

# Import the function to be tested
from src.sweeper import get_stale_branches

class TestStaleBranchSweeper(unittest.TestCase):

    @patch.dict(os.environ, {'GITHUB_TOKEN': 'mock_token'})
    @patch('requests.get')
    def test_no_stale_branches(self, mock_get):
        # Mock rationale: Simulate GitHub API responses where all branches are recent.
        # This tests the scenario where no branches meet the stale criteria.

        # Current time for comparison
        now = datetime.now(timezone.utc)

        # Mock branches data - all recent
        mock_branches_response = MagicMock()
        mock_branches_response.json.return_value = [
            {'name': 'main', 'commit': {'sha': 'sha1'}},
            {'name': 'feature-a', 'commit': {'sha': 'sha2'}},
        ]
        mock_branches_response.raise_for_status.return_value = None

        # Mock commit details for each branch - all recent
        mock_commit_main = MagicMock()
        mock_commit_main.json.return_value = {'commit': {'author': {'date': (now - timedelta(days=5)).isoformat()}}}
        mock_commit_main.raise_for_status.return_value = None

        mock_commit_feature_a = MagicMock()
        mock_commit_feature_a.json.return_value = {'commit': {'author': {'date': (now - timedelta(days=10)).isoformat()}}}
        mock_commit_feature_a.raise_for_status.return_value = None

        # Configure mock_get to return different responses based on the URL
        def mock_get_side_effect(url, *args, **kwargs):
            if 'branches' in url:
                return mock_branches_response
            elif 'sha1' in url:
                return mock_commit_main
            elif 'sha2' in url:
                return mock_commit_feature_a
            return MagicMock(status_code=404, raise_for_status=MagicMock(side_effect=requests.exceptions.HTTPError))

        mock_get.side_effect = mock_get_side_effect

        stale_branches = get_stale_branches('owner', 'repo', 30)
        self.assertEqual(len(stale_branches), 0)

    @patch.dict(os.environ, {'GITHUB_TOKEN': 'mock_token'})
    @patch('requests.get')
    def test_some_stale_branches(self, mock_get):
        # Mock rationale: Simulate GitHub API responses where some branches are stale.
        # This tests the core functionality of identifying stale branches.

        now = datetime.now(timezone.utc)

        # Mock branches data
        mock_branches_response = MagicMock()
        mock_branches_response.json.return_value = [
            {'name': 'main', 'commit': {'sha': 'sha1'}},
            {'name': 'stale-feature', 'commit': {'sha': 'sha2'}},
            {'name': 'recent-bugfix', 'commit': {'sha': 'sha3'}},
        ]
        mock_branches_response.raise_for_status.return_value = None

        # Mock commit details
        mock_commit_main = MagicMock()
        mock_commit_main.json.return_value = {'commit': {'author': {'date': (now - timedelta(days=5)).isoformat()}}}
        mock_commit_main.raise_for_status.return_value = None

        mock_commit_stale = MagicMock()
        mock_commit_stale.json.return_value = {'commit': {'author': {'date': (now - timedelta(days=60)).isoformat()}}}
        mock_commit_stale.raise_for_status.return_value = None

        mock_commit_recent = MagicMock()
        mock_commit_recent.json.return_value = {'commit': {'author': {'date': (now - timedelta(days=15)).isoformat()}}}
        mock_commit_recent.raise_for_status.return_value = None

        def mock_get_side_effect(url, *args, **kwargs):
            if 'branches' in url:
                return mock_branches_response
            elif 'sha1' in url:
                return mock_commit_main
            elif 'sha2' in url:
                return mock_commit_stale
            elif 'sha3' in url:
                return mock_commit_recent
            return MagicMock(status_code=404, raise_for_status=MagicMock(side_effect=requests.exceptions.HTTPError))

        mock_get.side_effect = mock_get_side_effect

        stale_branches = get_stale_branches('owner', 'repo', 30)
        self.assertEqual(len(stale_branches), 1)
        self.assertEqual(stale_branches[0]['name'], 'stale-feature')
        # Check date format and approximate value
        stale_date = datetime.fromisoformat(stale_branches[0]['last_commit_date'])
        self.assertTrue(stale_date < (now - timedelta(days=30)))

    @patch.dict(os.environ, {'GITHUB_TOKEN': 'mock_token'})
    @patch('requests.get')
    def test_pagination(self, mock_get):
        # Mock rationale: Simulate GitHub API pagination to ensure the utility handles
        # repositories with many branches correctly.

        now = datetime.now(timezone.utc)

        # Page 1: one stale, one recent
        mock_branches_page1 = MagicMock()
        mock_branches_page1.json.return_value = [
            {'name': 'stale-page1', 'commit': {'sha': 'sha_stale_page1'}},
            {'name': 'recent-page1', 'commit': {'sha': 'sha_recent_page1'}},
        ]
        mock_branches_page1.raise_for_status.return_value = None

        # Page 2: one stale
        mock_branches_page2 = MagicMock()
        mock_branches_page2.json.return_value = [
            {'name': 'stale-page2', 'commit': {'sha': 'sha_stale_page2'}},
        ]
        mock_branches_page2.raise_for_status.return_value = None

        # Page 3: empty (end of pagination)
        mock_branches_page3 = MagicMock()
        mock_branches_page3.json.return_value = []
        mock_branches_page3.raise_for_status.return_value = None

        # Mock commit details
        mock_commit_stale_page1 = MagicMock()
        mock_commit_stale_page1.json.return_value = {'commit': {'author': {'date': (now - timedelta(days=70)).isoformat()}}}
        mock_commit_stale_page1.raise_for_status.return_value = None

        mock_commit_recent_page1 = MagicMock()
        mock_commit_recent_page1.json.return_value = {'commit': {'author': {'date': (now - timedelta(days=10)).isoformat()}}}
        mock_commit_recent_page1.raise_for_status.return_value = None

        mock_commit_stale_page2 = MagicMock()
        mock_commit_stale_page2.json.return_value = {'commit': {'author': {'date': (now - timedelta(days=80)).isoformat()}}}
        mock_commit_stale_page2.raise_for_status.return_value = None

        def mock_get_side_effect(url, *args, **kwargs):
            if 'branches' in url:
                page = kwargs.get('params', {}).get('page', 1)
                if page == 1:
                    return mock_branches_page1
                elif page == 2:
                    return mock_branches_page2
                else:
                    return mock_branches_page3
            elif 'sha_stale_page1' in url:
                return mock_commit_stale_page1
            elif 'sha_recent_page1' in url:
                return mock_commit_recent_page1
            elif 'sha_stale_page2' in url:
                return mock_commit_stale_page2
            return MagicMock(status_code=404, raise_for_status=MagicMock(side_effect=requests.exceptions.HTTPError))

        mock_get.side_effect = mock_get_side_effect

        stale_branches = get_stale_branches('owner', 'repo', 60)
        self.assertEqual(len(stale_branches), 2)
        self.assertIn({'name': 'stale-page1', 'last_commit_date': mock_commit_stale_page1.json.return_value['commit']['author']['date']}, stale_branches)
        self.assertIn({'name': 'stale-page2', 'last_commit_date': mock_commit_stale_page2.json.return_value['commit']['author']['date']}, stale_branches)

    @patch.dict(os.environ, {'GITHUB_TOKEN': 'mock_token'})
    @patch('requests.get')
    def test_api_error_branches(self, mock_get):
        # Mock rationale: Test error handling when fetching branches fails.

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found for url")
        mock_get.return_value = mock_response

        with self.assertRaises(requests.exceptions.RequestException):
            get_stale_branches('owner', 'repo', 30)

    @patch.dict(os.environ, {'GITHUB_TOKEN': 'mock_token'})
    @patch('requests.get')
    def test_api_error_commit(self, mock_get):
        # Mock rationale: Test error handling when fetching a specific commit fails.

        # Mock branches data
        mock_branches_response = MagicMock()
        mock_branches_response.json.return_value = [
            {'name': 'main', 'commit': {'sha': 'sha1'}},
        ]
        mock_branches_response.raise_for_status.return_value = None

        # Mock commit details - error for sha1
        mock_commit_error = MagicMock()
        mock_commit_error.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found for url")

        def mock_get_side_effect(url, *args, **kwargs):
            if 'branches' in url:
                return mock_branches_response
            elif 'sha1' in url:
                return mock_commit_error
            return MagicMock(status_code=404, raise_for_status=MagicMock(side_effect=requests.exceptions.HTTPError))

        mock_get.side_effect = mock_get_side_effect

        with self.assertRaises(requests.exceptions.RequestException):
            get_stale_branches('owner', 'repo', 30)

    @patch.dict(os.environ, {}, clear=True) # Ensure GITHUB_TOKEN is not set
    def test_no_github_token(self):
        # Mock rationale: Test the scenario where GITHUB_TOKEN is missing.

        with self.assertRaises(ValueError) as cm:
            get_stale_branches('owner', 'repo', 30)
        self.assertIn("GITHUB_TOKEN environment variable not set.", str(cm.exception))

if __name__ == '__main__':
    unittest.main()
