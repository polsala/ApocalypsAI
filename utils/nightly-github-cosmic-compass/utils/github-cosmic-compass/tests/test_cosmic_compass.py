import unittest
from unittest.mock import patch, MagicMock
import sys
import io
import json
import requests.exceptions
from src.cosmic_compass import search_repositories, main

class TestCosmicCompass(unittest.TestCase):

    def setUp(self):
        # Capture stdout and stderr for testing print statements
        self.held_stdout = sys.stdout
        self.held_stderr = sys.stderr
        sys.stdout = self.mock_stdout = io.StringIO()
        sys.stderr = self.mock_stderr = io.StringIO()

    def tearDown(self):
        # Restore stdout and stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    @patch('requests.get')
    def test_search_repositories_success(self, mock_get):
        # Mock rationale: Simulate a successful GitHub API response for repository search.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'items': [
                {
                    'full_name': 'octocat/Spoon-Knife',
                    'description': 'This repo is for demonstration purposes only.',
                    'stargazers_count': 1000,
                    'forks_count': 500,
                    'updated_at': '2023-01-01T12:00:00Z',
                    'html_url': 'https://github.com/octocat/Spoon-Knife'
                },
                {
                    'full_name': 'github/docs',
                    'description': 'The open-source repo for GitHub\'s documentation.',
                    'stargazers_count': 2000,
                    'forks_count': 1000,
                    'updated_at': '2023-02-01T12:00:00Z',
                    'html_url': 'https://github.com/github/docs'
                }
            ]
        }
        mock_get.return_value = mock_response

        results = search_repositories(language='python', min_stars=500, limit=2)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['full_name'], 'octocat/Spoon-Knife')
        self.assertEqual(results[1]['stargazers_count'], 2000)

        mock_get.assert_called_once_with(
            'https://api.github.com/search/repositories',
            params={'q': 'language:python stars:>=500', 'sort': 'stars', 'order': 'desc', 'per_page': 2},
            headers={'Accept': 'application/vnd.github.v3+json'},
            timeout=10
        )

    @patch('requests.get')
    def test_search_repositories_no_results(self, mock_get):
        # Mock rationale: Simulate a GitHub API response with no matching repositories.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'items': []}
        mock_get.return_value = mock_response

        results = search_repositories(language='nonexistentlang', min_stars=99999)
        self.assertEqual(len(results), 0)
        self.assertEqual(results, [])

    @patch('requests.get')
    def test_search_repositories_rate_limit(self, mock_get):
        # Mock rationale: Simulate a GitHub API rate limit error (HTTP 403).
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.text = '{"message": "API rate limit exceeded for user ID..."}'
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        results = search_repositories(language='python')
        self.assertEqual(len(results), 0)
        self.assertIn("GitHub API rate limit exceeded", self.mock_stderr.getvalue())

    @patch('requests.get')
    def test_search_repositories_connection_error(self, mock_get):
        # Mock rationale: Simulate a network connection error during the API request.
        mock_get.side_effect = requests.exceptions.ConnectionError("No internet")

        results = search_repositories(language='python')
        self.assertEqual(len(results), 0)
        self.assertIn("Could not connect to GitHub API", self.mock_stderr.getvalue())

    @patch('requests.get')
    def test_search_repositories_timeout(self, mock_get):
        # Mock rationale: Simulate a request timeout during the API call.
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

        results = search_repositories(language='python')
        self.assertEqual(len(results), 0)
        self.assertIn("Request to GitHub API timed out", self.mock_stderr.getvalue())

    @patch('src.cosmic_compass.search_repositories')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_success_output(self, mock_parse_args, mock_search_repositories):
        # Mock rationale: Simulate successful argument parsing and repository search results
        # to test the main function's output formatting.
        mock_parse_args.return_value = MagicMock(
            language='python', min_stars=100, sort_by='stars', order='desc', limit=1,
            token=None
        )
        mock_search_repositories.return_value = [
            {
                'full_name': 'test/repo',
                'description': 'A test repository.',
                'stargazers_count': 150,
                'forks_count': 50,
                'updated_at': '2024-03-15T10:00:00Z',
                'html_url': 'https://github.com/test/repo'
            }
        ]

        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("--- Top 1 Python Repositories (Stars >= 100) ---", output)
        self.assertIn("1. test/repo", output)
        self.assertIn("Description: A test repository.", output)
        self.assertIn("Stars: 150", output)
        self.assertIn("URL: https://github.com/test/repo", output)

    @patch('src.cosmic_compass.search_repositories')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_results_output(self, mock_parse_args, mock_search_repositories):
        # Mock rationale: Simulate argument parsing and an empty search result
        # to test the main function's output when no repositories are found.
        mock_parse_args.return_value = MagicMock(
            language='nonexistent',
            min_stars=0,
            sort_by='stars',
            order='desc',
            limit=10,
            token=None
        )
        mock_search_repositories.return_value = []

        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("No Nonexistent repositories found matching your criteria.", output)

    @patch('requests.get')
    def test_search_repositories_with_token(self, mock_get):
        # Mock rationale: Verify that the Authorization header is correctly set when a token is provided.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'items': []}
        mock_get.return_value = mock_response

        token = "ghp_testtoken123"
        search_repositories(language='python', github_token=token)

        mock_get.assert_called_once_with(
            'https://api.github.com/search/repositories',
            params={'q': 'language:python stars:>=0', 'sort': 'stars', 'order': 'desc', 'per_page': 10},
            headers={'Accept': 'application/vnd.github.v3+json', 'Authorization': f'token {token}'},
            timeout=10
        )

    @patch('os.environ.get')
    @patch('src.cosmic_compass.search_repositories')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_token_from_env(self, mock_parse_args, mock_search_repositories, mock_os_environ_get):
        # Mock rationale: Verify that the main function correctly picks up the GitHub token
        # from the environment variable if the --token argument is not provided.
        mock_parse_args.return_value = MagicMock(
            language='python', min_stars=0, sort_by='stars', order='desc', limit=10,
            token=None # Simulate no --token argument
        )
        mock_os_environ_get.return_value = "env_test_token"
        mock_search_repositories.return_value = []

        main()

        mock_search_repositories.assert_called_once_with(
            language='python',
            min_stars=0,
            sort_by='stars',
            order='desc',
            limit=10,
            github_token="env_test_token"
        )
        mock_os_environ_get.assert_called_with('GITHUB_TOKEN')
