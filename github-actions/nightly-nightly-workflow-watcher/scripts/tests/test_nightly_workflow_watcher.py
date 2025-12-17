import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Assuming the script is named nightly_workflow_watcher.py
# If it's in a subdirectory, adjust the import path accordingly
from scripts.nightly_workflow_watcher import analyze_workflows, report_alerts

class TestWorkflowWatcher(unittest.TestCase):

    def test_analyze_workflows_no_issues(self):
        mock_runs = [
            {
                "name": "Successful Build",
                "status": "completed",
                "conclusion": "success",
                "run_started_at": (datetime.now() - timedelta(hours=1)).isoformat() + 'Z',
                "id": 1,
                "html_url": "http://example.com/run/1"
            }
        ]
        failed, long_running = analyze_workflows(mock_runs, failure_threshold=1, long_run_threshold_minutes=60)
        self.assertEqual(len(failed), 0)
        self.assertEqual(len(long_running), 0)

    def test_analyze_workflows_failure(self):
        mock_runs = [
            {
                "name": "Failed Test",
                "status": "completed",
                "conclusion": "failure",
                "run_started_at": (datetime.now() - timedelta(hours=1)).isoformat() + 'Z',
                "id": 2,
                "html_url": "http://example.com/run/2"
            }
        ]
        failed, long_running = analyze_workflows(mock_runs, failure_threshold=1, long_run_threshold_minutes=60)
        self.assertEqual(len(failed), 1)
        self.assertEqual(failed[0]['name'], "Failed Test")
        self.assertEqual(len(long_running), 0)

    def test_analyze_workflows_long_running(self):
        # Mock current time to ensure the duration calculation is deterministic
        mock_now = datetime.now()
        with patch('scripts.nightly_workflow_watcher.datetime') as mock_dt:
            mock_dt.now.return_value = mock_now
            mock_dt.fromisoformat.side_effect = lambda dt_str: datetime.fromisoformat(dt_str.replace('Z', '+00:00'))

            mock_runs = [
                {
                    "name": "Long Build",
                    "status": "in_progress",
                    "conclusion": None,
                    "run_started_at": (mock_now - timedelta(minutes=70)).isoformat() + 'Z',
                    "id": 3,
                    "html_url": "http://example.com/run/3"
                }
            ]
            failed, long_running = analyze_workflows(mock_runs, failure_threshold=1, long_run_threshold_minutes=60)
            self.assertEqual(len(failed), 0)
            self.assertEqual(len(long_running), 1)
            self.assertEqual(long_running[0]['run']['name'], "Long Build")
            self.assertGreaterEqual(long_running[0]['duration_minutes'], 70)

    def test_analyze_workflows_multiple_issues(self):
        mock_runs = [
            {
                "name": "Failed Test 1",
                "status": "completed",
                "conclusion": "failure",
                "run_started_at": (datetime.now() - timedelta(hours=1)).isoformat() + 'Z',
                "id": 4,
                "html_url": "http://example.com/run/4"
            },
            {
                "name": "Failed Test 2",
                "status": "completed",
                "conclusion": "failure",
                "run_started_at": (datetime.now() - timedelta(hours=2)).isoformat() + 'Z',
                "id": 5,
                "html_url": "http://example.com/run/5"
            },
            {
                "name": "In Progress",
                "status": "in_progress",
                "conclusion": None,
                "run_started_at": (datetime.now() - timedelta(minutes=90)).isoformat() + 'Z',
                "id": 6,
                "html_url": "http://example.com/run/6"
            }
        ]
        failed, long_running = analyze_workflows(mock_runs, failure_threshold=1, long_run_threshold_minutes=60)
        self.assertEqual(len(failed), 2)
        self.assertEqual(len(long_running), 1)

    @patch('scripts.nightly_workflow_watcher.Console')
    def test_report_alerts_no_alerts(self, MockConsole):
        mock_console_instance = MockConsole.return_value
        report_alerts([], [], failure_threshold=1, long_run_threshold_minutes=60)
        mock_console_instance.print.assert_any_call("[bold green]✅ All workflows are healthy![/bold green]")

    @patch('scripts.nightly_workflow_watcher.Console')
    def test_report_alerts_failure_alert(self, MockConsole):
        mock_console_instance = MockConsole.return_value
        mock_failed_runs = [
            {
                "name": "Failing Workflow",
                "status": "completed",
                "conclusion": "failure",
                "id": 7,
                "html_url": "http://example.com/run/7"
            }
        ]
        report_alerts(mock_failed_runs, [], failure_threshold=0, long_run_threshold_minutes=60)
        mock_console_instance.print.assert_any_call("[bold red]🚨 ALERT: Too many recent workflow failures![/bold red]")
        mock_console_instance.print.assert_any_call("  - Workflow: Failing Workflow (ID: 7) - Status: completed, Conclusion: failure")

    @patch('scripts.nightly_workflow_watcher.Console')
    def test_report_alerts_long_running_alert(self, MockConsole):
        mock_console_instance = MockConsole.return_value
        mock_long_running_runs = [
            {
                "run": {
                    "name": "Stuck Workflow",
                    "status": "in_progress",
                    "id": 8,
                    "html_url": "http://example.com/run/8"
                },
                "duration_minutes": 75.5
            }
        ]
        report_alerts([], mock_long_running_runs, failure_threshold=1, long_run_threshold_minutes=60)
        mock_console_instance.print.assert_any_call("[bold yellow]⏳ ALERT: Long-running workflows detected![/bold yellow]")
        mock_console_instance.print.assert_any_call("  - Workflow: Stuck Workflow (ID: 8) has been running for 75.50 minutes (threshold: 60 min).")

    @patch('scripts.nightly_workflow_watcher.Console')
    def test_report_alerts_both_alerts(self, MockConsole):
        mock_console_instance = MockConsole.return_value
        mock_failed_runs = [
            {
                "name": "Failing Workflow",
                "status": "completed",
                "conclusion": "failure",
                "id": 9,
                "html_url": "http://example.com/run/9"
            }
        ]
        mock_long_running_runs = [
            {
                "run": {
                    "name": "Stuck Workflow",
                    "status": "in_progress",
                    "id": 10,
                    "html_url": "http://example.com/run/10"
                },
                "duration_minutes": 75.5
            }
        ]
        report_alerts(mock_failed_runs, mock_long_running_runs, failure_threshold=0, long_run_threshold_minutes=60)
        mock_console_instance.print.assert_any_call("[bold red]🚨 ALERT: Too many recent workflow failures![/bold red]")
        mock_console_instance.print.assert_any_call("[bold yellow]⏳ ALERT: Long-running workflows detected![/bold yellow]")

if __name__ == '__main__':
    unittest.main()
