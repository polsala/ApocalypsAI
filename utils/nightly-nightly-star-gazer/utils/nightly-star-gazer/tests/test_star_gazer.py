import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import requests # Import requests to mock its exceptions

# Add the src directory to the path to allow importing star_gazer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import star_gazer

class TestStarGazer(unittest.TestCase):

    @patch('star_gazer.requests.get')
    def test_get_repo_stars_success(self, mock_get):
        # Mock rationale: Simulate a successful GitHub API response for star count.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"stargazers_count": 1234}
        mock_get.return_value = mock_response

        stars = star_gazer.get_repo_stars("owner/repo")
        self.assertEqual(stars, 1234)
        mock_get.assert_called_once_with("https://api.github.com/repos/owner/repo", headers={'Accept': 'application/vnd.github.v3+json'})

    @patch('star_gazer.requests.get')
    def test_get_repo_stars_with_token(self, mock_get):
        # Mock rationale: Simulate a successful GitHub API response with an authentication token.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"stargazers_count": 5678}
        mock_get.return_value = mock_response

        stars = star_gazer.get_repo_stars("owner/repo", github_token="test_token")
        self.assertEqual(stars, 5678)
        mock_get.assert_called_once_with("https://api.github.com/repos/owner/repo", headers={'Accept': 'application/vnd.github.v3+json', 'Authorization': 'token test_token'})

    @patch('star_gazer.requests.get')
    def test_get_repo_stars_not_found(self, mock_get):
        # Mock rationale: Simulate a 404 Not Found response from GitHub API.
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        with patch('star_gazer.console.print') as mock_console_print:
            stars = star_gazer.get_repo_stars("owner/nonexistent-repo")
            self.assertEqual(stars, -1)
            mock_console_print.assert_called_once_with("[bold red]Error:[/bold red] Repository 'owner/nonexistent-repo' not found.")

    @patch('star_gazer.requests.get')
    def test_get_repo_stars_rate_limit(self, mock_get):
        # Mock rationale: Simulate a 403 Forbidden response due to API rate limiting.
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.text = '{"message": "API rate limit exceeded"}'
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        with patch('star_gazer.console.print') as mock_console_print:
            stars = star_gazer.get_repo_stars("owner/repo")
            self.assertEqual(stars, -1)
            mock_console_print.assert_called_once_with("[bold red]Error:[/bold red] GitHub API rate limit exceeded. Please try again later or provide a GITHUB_TOKEN.")

    @patch('star_gazer.requests.get')
    def test_get_repo_stars_connection_error(self, mock_get):
        # Mock rationale: Simulate a network connection error.
        mock_get.side_effect = requests.exceptions.ConnectionError

        with patch('star_gazer.console.print') as mock_console_print:
            stars = star_gazer.get_repo_stars("owner/repo")
            self.assertEqual(stars, -1)
            mock_console_print.assert_called_once_with("[bold red]Error:[/bold red] Could not connect to GitHub API. Check your internet connection.")

    def test_get_constellation_name(self):
        # Test various star counts against defined tiers.
        self.assertEqual(star_gazer.get_constellation_name(50), "Dust Cloud")
        self.assertEqual(star_gazer.get_constellation_name(100), "Nebula Nook")
        self.assertEqual(star_gazer.get_constellation_name(499), "Nebula Nook")
        self.assertEqual(star_gazer.get_constellation_name(500), "Comet Cluster")
        self.assertEqual(star_gazer.get_constellation_name(999), "Comet Cluster")
        self.assertEqual(star_gazer.get_constellation_name(1000), "Stellar Swarm")
        self.assertEqual(star_gazer.get_constellation_name(4999), "Stellar Swarm")
        self.assertEqual(star_gazer.get_constellation_name(5000), "Galactic Gem")
        self.assertEqual(star_gazer.get_constellation_name(9999), "Galactic Gem")
        self.assertEqual(star_gazer.get_constellation_name(10000), "Cosmic Colossus")
        self.assertEqual(star_gazer.get_constellation_name(99999), "Cosmic Colossus")

    @patch('star_gazer.get_repo_stars', return_value=1234)
    @patch('star_gazer.console.print')
    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(repo='owner/repo'))
    def test_main_success(self, mock_parse_args, mock_console_print, mock_get_repo_stars):
        # Mock rationale: Simulate successful execution of main with a valid repo and star count.
        # Mock argparse to control input, mock get_repo_stars to control API result,
        # and mock console.print to capture output without affecting the actual console.
        star_gazer.main()
        mock_get_repo_stars.assert_called_once_with('owner/repo', None)
        # Check for key phrases in the console output
        output_calls = [str(call.args[0]) for call in mock_console_print.call_args_list]
        self.assertTrue(any("Nightly Star-Gazing Report" in s for s in output_calls))
        self.assertTrue(any("Repository: owner/repo" in s for s in output_calls))
        self.assertTrue(any("Current Stars: 1234" in s for s in output_calls))
        self.assertTrue(any("Constellation: Stellar Swarm" in s for s in output_calls))
        self.assertTrue(any("Keep shining bright" in s for s in output_calls))

    @patch('star_gazer.get_repo_stars', return_value=50)
    @patch('star_gazer.console.print')
    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(repo='owner/repo'))
    def test_main_zero_stars(self, mock_parse_args, mock_console_print, mock_get_repo_stars):
        # Mock rationale: Simulate execution of main with a repo having very few stars.
        star_gazer.main()
        output_calls = [str(call.args[0]) for call in mock_console_print.call_args_list]
        self.assertTrue(any("Current Stars: 50" in s for s in output_calls))
        self.assertTrue(any("Constellation: Dust Cloud" in s for s in output_calls))
        self.assertTrue(any("Just starting its cosmic journey!" in s for s in output_calls))

    @patch('star_gazer.get_repo_stars', return_value=-1)
    @patch('star_gazer.console.print')
    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(repo='owner/repo'))
    @patch('sys.exit')
    def test_main_error_exit(self, mock_exit, mock_parse_args, mock_console_print, mock_get_repo_stars):
        # Mock rationale: Simulate an error during star retrieval, expecting the script to exit.
        star_gazer.main()
        mock_console_print.assert_any_call("[bold red]Failed to retrieve star count. Exiting.[/bold red]")
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
