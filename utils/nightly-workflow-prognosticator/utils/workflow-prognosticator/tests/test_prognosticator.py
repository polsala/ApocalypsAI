import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import prognosticator

class TestPrognosticator(unittest.TestCase):

    @patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token'}, clear=True)
    def setUp(self):
        # Mock rationale: Ensure GITHUB_TOKEN is always set for tests that require it.
        self.owner = "test_owner"
        self.repo = "test_repo"
        self.token = "test_token"
        self.workflow_id = "12345"
        self.workflow_name = "CI"

    @patch('requests.get')
    def test_get_github_token_success(self, mock_get):
        # Mock rationale: Test that get_github_token correctly retrieves the token from os.environ.
        self.assertEqual(prognosticator.get_github_token(), 'test_token')

    @patch.dict(os.environ, {}, clear=True)
    def test_get_github_token_failure(self):
        # Mock rationale: Test that get_github_token raises an error if the token is not set.
        with self.assertRaises(ValueError):
            prognosticator.get_github_token()

    @patch('requests.get')
    def test_fetch_github_api_success(self, mock_get):
        # Mock rationale: Simulate a successful API response.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'key': 'value'}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = prognosticator.fetch_github_api("http://example.com", self.token)
        self.assertEqual(result, {'key': 'value'})
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_fetch_github_api_http_error(self, mock_get):
        # Mock rationale: Simulate an HTTP error response from the API.
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
        mock_get.return_value = mock_response

        result = prognosticator.fetch_github_api("http://example.com", self.token)
        self.assertIsNone(result)
        mock_get.assert_called_once()

    @patch('prognosticator.fetch_github_api')
    def test_fetch_workflow_runs_by_id(self, mock_fetch_api):
        # Mock rationale: Simulate fetching runs for a specific workflow ID.
        mock_fetch_api.return_value = {
            'workflow_runs': [{'id': 1, 'conclusion': 'success'}, {'id': 2, 'conclusion': 'failure'}]
        }
        runs = prognosticator.fetch_workflow_runs(self.owner, self.repo, self.workflow_id, self.token)
        self.assertEqual(len(runs), 2)
        mock_fetch_api.assert_called_once_with(
            f"{prognosticator.GITHUB_API_BASE}/repos/{self.owner}/{self.repo}/actions/workflows/{self.workflow_id}/runs",
            self.token,
            params={'per_page': 10}
        )

    @patch('prognosticator.fetch_github_api')
    def test_fetch_workflow_runs_by_name(self, mock_fetch_api):
        # Mock rationale: Simulate fetching runs for a specific workflow name, requiring a prior call to resolve ID.
        # First call for workflows list
        mock_fetch_api.side_effect = [
            {'workflows': [{'id': 12345, 'name': 'CI', 'state': 'active'}]},
            # Second call for runs of the resolved ID
            {'workflow_runs': [{'id': 1, 'conclusion': 'success'}]}
        ]
        runs = prognosticator.fetch_workflow_runs(self.owner, self.repo, self.workflow_name, self.token)
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]['id'], 1)
        mock_fetch_api.assert_any_call(
            f"{prognosticator.GITHUB_API_BASE}/repos/{self.owner}/{self.repo}/actions/workflows",
            self.token
        )
        mock_fetch_api.assert_any_call(
            f"{prognosticator.GITHUB_API_BASE}/repos/{self.owner}/{self.repo}/actions/workflows/12345/runs",
            self.token,
            params={'per_page': 10}
        )

    @patch('prognosticator.fetch_github_api')
    def test_fetch_workflow_runs_all(self, mock_fetch_api):
        # Mock rationale: Simulate fetching runs for all workflows in a repository.
        mock_fetch_api.return_value = {
            'workflow_runs': [{'id': 1, 'conclusion': 'success'}, {'id': 2, 'conclusion': 'failure'}]
        }
        runs = prognosticator.fetch_workflow_runs(self.owner, self.repo, None, self.token)
        self.assertEqual(len(runs), 2)
        mock_fetch_api.assert_called_once_with(
            f"{prognosticator.GITHUB_API_BASE}/repos/{self.owner}/{self.repo}/actions/runs",
            self.token,
            params={'per_page': 10}
        )

    def test_analyze_runs_excellent(self):
        # Mock rationale: Test analysis for 100% successful runs.
        runs = [{'conclusion': 'success'} for _ in range(10)]
        total, success, failed, prognosis, level = prognosticator.analyze_runs(runs)
        self.assertEqual(total, 10)
        self.assertEqual(success, 10)
        self.assertEqual(failed, 0)
        self.assertIn("Excellent!", prognosis)
        self.assertEqual(level, "EXCELLENT")

    def test_analyze_runs_stable_hiccups(self):
        # Mock rationale: Test analysis for mostly successful runs (e.g., 80% success).
        runs = [{'conclusion': 'success'} for _ in range(8)] + [{'conclusion': 'failure'} for _ in range(2)]
        total, success, failed, prognosis, level = prognosticator.analyze_runs(runs)
        self.assertEqual(total, 10)
        self.assertEqual(success, 8)
        self.assertEqual(failed, 2)
        self.assertIn("Stable with minor hiccups.", prognosis)
        self.assertEqual(level, "STABLE_HICCUPS")

    def test_analyze_runs_unstable(self):
        # Mock rationale: Test analysis for mixed success/failure (e.g., 40% success).
        runs = [{'conclusion': 'success'} for _ in range(4)] + [{'conclusion': 'failure'} for _ in range(6)]
        total, success, failed, prognosis, level = prognosticator.analyze_runs(runs)
        self.assertEqual(total, 10)
        self.assertEqual(success, 4)
        self.assertEqual(failed, 6)
        self.assertIn("Unstable.", prognosis)
        self.assertEqual(level, "UNSTABLE")

    def test_analyze_runs_critical(self):
        # Mock rationale: Test analysis for 100% failed runs.
        runs = [{'conclusion': 'failure'} for _ in range(10)]
        total, success, failed, prognosis, level = prognosticator.analyze_runs(runs)
        self.assertEqual(total, 10)
        self.assertEqual(success, 0)
        self.assertEqual(failed, 10)
        self.assertIn("Critical!", prognosis)
        self.assertEqual(level, "CRITICAL")

    def test_analyze_runs_no_activity(self):
        # Mock rationale: Test analysis for no runs found.
        runs = []
        total, success, failed, prognosis, level = prognosticator.analyze_runs(runs)
        self.assertEqual(total, 0)
        self.assertEqual(success, 0)
        self.assertEqual(failed, 0)
        self.assertIn("No recent activity.", prognosis)
        self.assertEqual(level, "NO_ACTIVITY")

    @patch('prognosticator.fetch_workflow_runs')
    @patch('prognosticator.analyze_runs')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_single_workflow(self, mock_stdout, mock_parse_args, mock_analyze_runs, mock_fetch_workflow_runs):
        # Mock rationale: Simulate running main for a single workflow, capturing output and verifying calls.
        mock_parse_args.return_value = MagicMock(repo=f"{self.owner}/{self.repo}", workflow=self.workflow_name)
        mock_fetch_workflow_runs.return_value = [{'id': 1, 'conclusion': 'success'}]
        mock_analyze_runs.return_value = (1, 1, 0, "Excellent!", "EXCELLENT")

        prognosticator.main()

        mock_fetch_workflow_runs.assert_called_once_with(self.owner, self.repo, self.workflow_name, self.token)
        mock_analyze_runs.assert_called_once()
        mock_stdout.write.assert_any_call(unittest.mock.ANY)
        self.assertIn("Excellent!", mock_stdout.write.call_args_list[-1].args[0])

    @patch('prognosticator.fetch_all_workflows')
    @patch('prognosticator.fetch_workflow_runs')
    @patch('prognosticator.analyze_runs')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_all_workflows(self, mock_stdout, mock_parse_args, mock_analyze_runs, mock_fetch_workflow_runs, mock_fetch_all_workflows):
        # Mock rationale: Simulate running main for all workflows, capturing output and verifying calls.
        mock_parse_args.return_value = MagicMock(repo=f"{self.owner}/{self.repo}", workflow=None)
        mock_fetch_all_workflows.return_value = [
            {'id': 111, 'name': 'Workflow A', 'state': 'active'},
            {'id': 222, 'name': 'Workflow B', 'state': 'active'}
        ]
        mock_fetch_workflow_runs.side_effect = [
            [{'id': 1, 'conclusion': 'success'}], # Runs for Workflow A
            [{'id': 2, 'conclusion': 'failure'}]  # Runs for Workflow B
        ]
        mock_analyze_runs.side_effect = [
            (1, 1, 0, "Excellent!", "EXCELLENT"),
            (1, 0, 1, "Critical!", "CRITICAL")
        ]

        prognosticator.main()

        mock_fetch_all_workflows.assert_called_once_with(self.owner, self.repo, self.token)
        self.assertEqual(mock_fetch_workflow_runs.call_count, 2)
        self.assertEqual(mock_analyze_runs.call_count, 2)
        mock_stdout.write.assert_any_call(unittest.mock.ANY)
        self.assertIn("Excellent!", mock_stdout.write.call_args_list[-2].args[0])
        self.assertIn("Critical!", mock_stdout.write.call_args_list[-1].args[0])

    @patch('prognosticator.fetch_all_workflows')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_all_workflows_no_workflows_found(self, mock_stdout, mock_parse_args, mock_fetch_all_workflows):
        # Mock rationale: Simulate running main when no workflows are found in the repository.
        mock_parse_args.return_value = MagicMock(repo=f"{self.owner}/{self.repo}", workflow=None)
        mock_fetch_all_workflows.return_value = []

        with self.assertRaises(SystemExit) as cm:
            prognosticator.main()
        self.assertEqual(cm.exception.code, 0) # Exit code 0 for no-op
        mock_stdout.write.assert_any_call("No active workflows found or unable to fetch workflows.\n")


if __name__ == '__main__':
    unittest.main()
