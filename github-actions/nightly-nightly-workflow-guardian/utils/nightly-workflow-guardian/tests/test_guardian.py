import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Assuming guardian.py is in the same directory or accessible via PYTHONPATH
# If not, adjust the import path accordingly.
from guardian import analyze_workflow_health, get_recent_workflow_runs, main

# Mock rationale: These mocks simulate the behavior of external dependencies
# and API responses, allowing for deterministic and offline testing.

class TestWorkflowGuardian(unittest.TestCase):

    @patch('guardian.mock_requests_get') # Patching the mock function directly
    @patch('guardian.GITHUB_TOKEN', 'mock_token')
    @patch('guardian.REPO_OWNER', 'test_owner')
    @patch('guardian.REPO_NAME', 'test_repo')
    def test_get_recent_workflow_runs_success(self, mock_get, mock_token, mock_owner, mock_repo):
        # Configure the mock_requests_get to return a successful response
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "workflow_runs": [
                    {
                        "id": 1,
                        "name": "Test Workflow",
                        "status": "completed",
                        "conclusion": "success",
                        "created_at": (datetime.utcnow() - timedelta(hours=1)).isoformat() + 'Z',
                        "html_url": "http://example.com/run/1"
                    }
                ]
            }
        )
        
        runs = get_recent_workflow_runs()
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]['name'], "Test Workflow")
        mock_get.assert_called_once()

    @patch('guardian.mock_requests_get')
    @patch('guardian.GITHUB_TOKEN', 'mock_token')
    @patch('guardian.REPO_OWNER', 'test_owner')
    @patch('guardian.REPO_NAME', 'test_repo')
    def test_get_recent_workflow_runs_api_error(self, mock_get, mock_token, mock_owner, mock_repo):
        # Configure the mock_requests_get to return an error response
        mock_get.return_value = MagicMock(status_code=404, raise_for_status=MagicMock(side_effect=requests.exceptions.HTTPError("404 Client Error: Not Found for url: ...")))
        
        with self.assertRaises(requests.exceptions.HTTPError):
            get_recent_workflow_runs()
        mock_get.assert_called_once()

    def test_analyze_workflow_health_all_success(self):
        mock_runs = [
            {
                "id": 1,
                "name": "Test Workflow 1",
                "status": "completed",
                "conclusion": "success",
                "created_at": (datetime.utcnow() - timedelta(hours=1)).isoformat() + 'Z',
                "html_url": "http://example.com/run/1"
            },
            {
                "id": 2,
                "name": "Test Workflow 2",
                "status": "completed",
                "conclusion": "success",
                "created_at": (datetime.utcnow() - timedelta(hours=2)).isoformat() + 'Z',
                "html_url": "http://example.com/run/2"
            }
        ]
        status, message = analyze_workflow_health(mock_runs)
        self.assertEqual(status, "success")
        self.assertIn("All workflows executed successfully", message)

    def test_analyze_workflow_health_with_failures(self):
        mock_runs = [
            {
                "id": 1,
                "name": "Test Workflow 1",
                "status": "completed",
                "conclusion": "success",
                "created_at": (datetime.utcnow() - timedelta(hours=1)).isoformat() + 'Z',
                "html_url": "http://example.com/run/1"
            },
            {
                "id": 2,
                "name": "Failing Workflow",
                "status": "completed",
                "conclusion": "failure",
                "created_at": (datetime.utcnow() - timedelta(hours=2)).isoformat() + 'Z',
                "html_url": "http://example.com/run/2"
            },
            {
                "id": 3,
                "name": "Another Workflow",
                "status": "completed",
                "conclusion": "success",
                "created_at": (datetime.utcnow() - timedelta(hours=3)).isoformat() + 'Z',
                "html_url": "http://example.com/run/3"
            }
        ]
        status, message = analyze_workflow_health(mock_runs)
        self.assertEqual(status, "failure")
        self.assertIn("Found 1 failed workflow run(s)", message)
        self.assertIn("Failing Workflow", message)

    @patch('guardian.get_recent_workflow_runs')
    @patch('guardian.analyze_workflow_health')
    @patch('builtins.print')
    def test_main_success(self, mock_print, mock_analyze, mock_get_runs):
        mock_get_runs.return_value = [MagicMock()]
        mock_analyze.return_value = ("success", "All good!")
        
        main()
        
        mock_get_runs.assert_called_once()
        mock_analyze.assert_called_once()
        mock_print.assert_any_call("::set-output name=status::success")
        mock_print.assert_any_call("::set-output name=message::All good!")

    @patch('guardian.get_recent_workflow_runs')
    @patch('guardian.analyze_workflow_health')
    @patch('builtins.print')
    def test_main_failure(self, mock_print, mock_analyze, mock_get_runs):
        mock_get_runs.return_value = [MagicMock()]
        mock_analyze.return_value = ("failure", "Something broke!")
        
        main()
        
        mock_get_runs.assert_called_once()
        mock_analyze.assert_called_once()
        mock_print.assert_any_call("::set-output name=status::failure")
        mock_print.assert_any_call("::set-output name=message::Something broke!")

    @patch('guardian.get_recent_workflow_runs')
    @patch('builtins.print')
    def test_main_api_exception(self, mock_print, mock_get_runs):
        mock_get_runs.side_effect = requests.exceptions.RequestException("Network error")
        
        main()
        
        mock_get_runs.assert_called_once()
        mock_print.assert_any_call("::set-output name=status::failure")
        mock_print.assert_any_call(unittest.mock.ANY, "Network error") # Check for error message

if __name__ == '__main__':
    unittest.main()
