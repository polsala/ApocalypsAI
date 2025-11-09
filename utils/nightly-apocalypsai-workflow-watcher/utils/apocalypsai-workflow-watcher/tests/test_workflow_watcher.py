import unittest
from unittest import mock
import os
import json
from datetime import datetime, timedelta
import requests # Import requests to catch its exceptions

# Add the src directory to the path to allow importing workflow_watcher
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import workflow_watcher

class MockResponse:
    """Mock class for requests.Response."""
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"HTTP Error: {self.status_code}")

class TestWorkflowWatcher(unittest.TestCase):

    def setUp(self):
        # Mock rationale: Ensure GITHUB_TOKEN is set for tests that call get_workflow_runs
        os.environ['GITHUB_TOKEN'] = 'mock_token'

    def tearDown(self):
        # Mock rationale: Clean up environment variable after tests to prevent side effects.
        if 'GITHUB_TOKEN' in os.environ:
            del os.environ['GITHUB_TOKEN']

    @mock.patch('requests.get')
    def test_get_workflow_runs_success(self, mock_get):
        # Mock rationale: Simulate a successful GitHub API response for workflow runs.
        mock_data = {
            "total_count": 1,
            "workflow_runs": [
                {
                    "id": 12345,
                    "name": "Test Workflow",
                    "workflow_id": 100,
                    "status": "completed",
                    "conclusion": "success",
                    "updated_at": (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
                }
            ]
        }
        mock_get.return_value = MockResponse(mock_data)

        result = workflow_watcher.get_workflow_runs('mock_token', 'owner', 'repo')
        self.assertEqual(result, mock_data)
        mock_get.assert_called_once_with(
            f"{workflow_watcher.GITHUB_API_BASE}/repos/owner/repo/actions/runs",
            headers={
                "Authorization": "Bearer mock_token",
                "Accept": "application/vnd.github.v3+json"
            },
            timeout=10
        )

    @mock.patch('requests.get')
    def test_get_workflow_runs_failure(self, mock_get):
        # Mock rationale: Simulate a failed GitHub API response (e.g., 403 Forbidden).
        mock_get.return_value = MockResponse({}, status_code=403)

        result = workflow_watcher.get_workflow_runs('mock_token', 'owner', 'repo')
        self.assertEqual(result, {})

    def test_get_workflow_runs_no_token(self):
        # Mock rationale: Test the scenario where GITHUB_TOKEN is not set, expecting a ValueError.
        del os.environ['GITHUB_TOKEN'] # Temporarily unset for this test
        with self.assertRaises(ValueError) as cm:
            workflow_watcher.get_workflow_runs(None, 'owner', 'repo')
        self.assertIn("GITHUB_TOKEN environment variable not set.", str(cm.exception))
        os.environ['GITHUB_TOKEN'] = 'mock_token' # Restore for other tests

    def test_analyze_workflows_all_success(self):
        # Mock rationale: Provide sample data where all latest workflow runs are successful.
        mock_data = {
            "total_count": 3,
            "workflow_runs": [
                {
                    "id": 1,
                    "name": "Workflow A",
                    "workflow_id": 100,
                    "status": "completed",
                    "conclusion": "success",
                    "updated_at": (datetime.now() - timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
                },
                {
                    "id": 2,
                    "name": "Workflow B",
                    "workflow_id": 200,
                    "status": "completed",
                    "conclusion": "success",
                    "updated_at": (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
                },
                {
                    "id": 3,
                    "name": "Workflow C",
                    "workflow_id": 300,
                    "status": "completed",
                    "conclusion": "success",
                    "updated_at": (datetime.now() - timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
                }
            ]
        }
        expected_output = "The gears of fate grind smoothly. ApocalypsAI operations are nominal. All systems green!"
        self.assertEqual(workflow_watcher.analyze_workflows(mock_data), expected_output)

    def test_analyze_workflows_some_failure(self):
        # Mock rationale: Provide sample data where some latest workflow runs have failed or been cancelled.
        now = datetime.now()
        mock_data = {
            "total_count": 4,
            "workflow_runs": [
                {
                    "id": 1,
                    "name": "Workflow A",
                    "workflow_id": 100,
                    "status": "completed",
                    "conclusion": "success",
                    "updated_at": (now - timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
                },
                {
                    "id": 2,
                    "name": "Workflow B",
                    "workflow_id": 200,
                    "status": "completed",
                    "conclusion": "failure",
                    "updated_at": (now - timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
                },
                {
                    "id": 3,
                    "name": "Workflow C",
                    "workflow_id": 300,
                    "status": "completed",
                    "conclusion": "success",
                    "updated_at": (now - timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
                },
                {
                    "id": 4,
                    "name": "Workflow D",
                    "workflow_id": 400,
                    "status": "completed",
                    "conclusion": "cancelled",
                    "updated_at": (now - timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
                }
            ]
        }
        expected_output_start = "A tremor in the timeline! Critical systems are faltering. Immediate intervention required to avert digital doom!\n\nFailing Workflows:\n"
        result = workflow_watcher.analyze_workflows(mock_data)
        self.assertTrue(result.startswith(expected_output_start))
        self.assertIn(f"-   Workflow B (Failure {(now - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')})", result)
        self.assertIn(f"-   Workflow D (Cancelled {(now - timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S')})", result)

    def test_analyze_workflows_no_runs(self):
        # Mock rationale: Provide empty workflow data to simulate no runs found.
        mock_data = {"total_count": 0, "workflow_runs": []}
        expected_output = "The void stares back. No workflow activity detected. Is this the calm before the storm, or have we already fallen?"
        self.assertEqual(workflow_watcher.analyze_workflows(mock_data), expected_output)

    def test_analyze_workflows_empty_data(self):
        # Mock rationale: Provide completely empty data to simulate API returning nothing useful.
        mock_data = {}
        expected_output = "The void stares back. No workflow activity detected. Is this the calm before the storm, or have we already fallen?"
        self.assertEqual(workflow_watcher.analyze_workflows(mock_data), expected_output)

    def test_analyze_workflows_latest_run_logic(self):
        # Mock rationale: Ensure only the latest run for each workflow_id is considered, ignoring older runs.
        now = datetime.now()
        mock_data = {
            "total_count": 4,
            "workflow_runs": [
                {
                    "id": 10,
                    "name": "Workflow X",
                    "workflow_id": 1000,
                    "status": "completed",
                    "conclusion": "success",
                    "updated_at": (now - timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
                },
                {
                    "id": 11,
                    "name": "Workflow Y",
                    "workflow_id": 1001,
                    "status": "completed",
                    "conclusion": "failure",
                    "updated_at": (now - timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
                },
                {
                    "id": 12,
                    "name": "Workflow X", # Older run for Workflow X, should be ignored
                    "workflow_id": 1000,
                    "status": "completed",
                    "conclusion": "failure",
                    "updated_at": (now - timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
                }
            ]
        }
        # Only Workflow Y should be reported as failing, as Workflow X's latest is success
        expected_output_start = "A tremor in the timeline! Critical systems are faltering. Immediate intervention required to avert digital doom!\n\nFailing Workflows:\n"
        result = workflow_watcher.analyze_workflows(mock_data)
        self.assertTrue(result.startswith(expected_output_start))
        self.assertIn(f"-   Workflow Y (Failure {(now - timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S')})", result)
        self.assertNotIn("Workflow X", result) # Should not report the older failed run

if __name__ == '__main__':
    unittest.main()
