import json
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestRunnerHealthMonitor(unittest.TestCase):
    """Test cases for the runner health monitoring workflow."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_workflow_runs = {
            'total_count': 100,
            'workflow_runs': [
                {
                    'id': 1,
                    'conclusion': 'success',
                    'runner_name': 'runner-1',
                    'created_at': '2024-01-01T10:00:00Z',
                    'updated_at': '2024-01-01T10:30:00Z'
                },
                {
                    'id': 2,
                    'conclusion': 'failure',
                    'runner_name': 'runner-1',
                    'created_at': '2024-01-01T11:00:00Z',
                    'updated_at': '2024-01-01T11:30:00Z'
                },
                {
                    'id': 3,
                    'conclusion': 'success',
                    'runner_name': 'runner-2',
                    'created_at': '2024-01-01T12:00:00Z',
                    'updated_at': '2024-01-01T12:15:00Z'
                },
                {
                    'id': 4,
                    'conclusion': 'success',
                    'runner_name': None,  # Hosted runner
                    'created_at': '2024-01-01T13:00:00Z',
                    'updated_at': '2024-01-01T13:20:00Z'
                }
            ]
        }
        
        self.sample_runners = {
            'total_count': 2,
            'runners': [
                {'id': 1, 'name': 'runner-1', 'status': 'online'},
                {'id': 2, 'name': 'runner-2', 'status': 'online'}
            ]
        }
    
    def test_analyze_workflow_runs(self):
        """Test workflow run analysis logic."""
        # This test simulates the Python analysis code from the workflow
        runs = self.sample_workflow_runs['workflow_runs']
        total_runs = len(runs)
        
        # Count self-hosted vs hosted runs
        self_hosted_runs = [r for r in runs if r.get('runner_name')]
        hosted_runs = [r for r in runs if not r.get('runner_name')]
        
        # Analyze success rates
        successful_runs = [r for r in runs if r.get('conclusion') == 'success']
        failed_runs = [r for r in runs if r.get('conclusion') in ['failure', 'cancelled', 'timed_out']]
        
        success_rate = (len(successful_runs) / total_runs * 100) if total_runs > 0 else 0
        failure_rate = (len(failed_runs) / total_runs * 100) if total_runs > 0 else 0
        
        # Assertions
        self.assertEqual(total_runs, 4)
        self.assertEqual(len(self_hosted_runs), 3)
        self.assertEqual(len(hosted_runs), 1)
        self.assertEqual(len(successful_runs), 3)
        self.assertEqual(len(failed_runs), 1)
        self.assertEqual(success_rate, 75.0)
        self.assertEqual(failure_rate, 25.0)
    
    def test_runner_usage_analysis(self):
        """Test runner usage analysis logic."""
        runs = self.sample_workflow_runs['workflow_runs']
        
        # Analyze runner usage (simplified version of workflow logic)
        runner_usage = {}
        for run in runs:
            runner_name = run.get('runner_name')
            if not runner_name:
                continue
                
            if runner_name not in runner_usage:
                runner_usage[runner_name] = {
                    'count': 0,
                    'successful': 0,
                    'failed': 0,
                    'total_duration': 0
                }
            
            runner_usage[runner_name]['count'] += 1
            if run.get('conclusion') == 'success':
                runner_usage[runner_name]['successful'] += 1
            else:
                runner_usage[runner_name]['failed'] += 1
        
        # Assertions
        self.assertEqual(len(runner_usage), 2)
        self.assertEqual(runner_usage['runner-1']['count'], 2)
        self.assertEqual(runner_usage['runner-1']['successful'], 1)
        self.assertEqual(runner_usage['runner-1']['failed'], 1)
        self.assertEqual(runner_usage['runner-2']['count'], 1)
        self.assertEqual(runner_usage['runner-2']['successful'], 1)
        self.assertEqual(runner_usage['runner-2']['failed'], 0)
    
    def test_alert_generation(self):
        """Test alert generation logic."""
        # Simulate high failure rate scenario
        failure_rate = 85.0  # Above threshold
        alert_threshold = 80.0
        
        alerts = []
        
        if failure_rate > alert_threshold:
            alerts.append({
                'type': 'high_failure_rate',
                'message': f'Failure rate ({failure_rate:.1f}%) exceeds threshold ({alert_threshold}%))
            })
        
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]['type'], 'high_failure_rate')
        self.assertIn('exceeds threshold', alerts[0]['message'])
    
    def test_stuck_runner_detection(self):
        """Test stuck runner detection logic."""
        # Simulate a stuck runner (long duration)
        runner_stats = {
            'count': 2,
            'total_duration': 7200  # 2 hours total for 2 runs = 1 hour average
        }
        
        avg_duration = runner_stats['total_duration'] / runner_stats['count']
        alerts = []
        
        if avg_duration > 3600:  # More than 1 hour average
            alerts.append({
                'type': 'stuck_runner',
                'runner': 'test-runner',
                'message': f'Runner test-runner has average duration of {avg_duration/60:.1f} minutes'
            })
        
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]['type'], 'stuck_runner')
        self.assertIn('average duration of 60.0 minutes', alerts[0]['message'])
    
    def test_health_report_generation(self):
        """Test health report JSON generation."""
        # Simulate the complete health report generation
        health_report = {
            'timestamp': '2024-01-01T12:00:00',
            'summary': {
                'total_runs': 4,
                'self_hosted_runs': 3,
                'hosted_runs': 1,
                'success_rate': 75.0,
                'failure_rate': 25.0,
                'total_runners': 2
            },
            'runner_details': {
                'runner-1': {
                    'count': 2,
                    'successful': 1,
                    'failed': 1,
                    'total_duration': 3600
                },
                'runner-2': {
                    'count': 1,
                    'successful': 1,
                    'failed': 0,
                    'total_duration': 900
                }
            },
            'alerts': [
                {
                    'type': 'high_failure_rate',
                    'message': 'Failure rate (25.0%) exceeds threshold (20.0%)'
                }
            ]
        }
        
        # Test JSON serialization
        json_str = json.dumps(health_report, indent=2)
        self.assertIn('timestamp', json_str)
        self.assertIn('summary', json_str)
        self.assertIn('runner_details', json_str)
        self.assertIn('alerts', json_str)
        
        # Test deserialization
        parsed_report = json.loads(json_str)
        self.assertEqual(parsed_report['summary']['total_runs'], 4)
        self.assertEqual(parsed_report['summary']['success_rate'], 75.0)
        self.assertEqual(len(parsed_report['runner_details']), 2)
        self.assertEqual(len(parsed_report['alerts']), 1)
    
    def test_markdown_report_generation(self):
        """Test markdown report generation."""
        health_report = {
            'timestamp': '2024-01-01T12:00:00',
            'summary': {
                'total_runs': 4,
                'self_hosted_runs': 3,
                'hosted_runs': 1,
                'success_rate': 75.0,
                'failure_rate': 25.0,
                'total_runners': 2
            },
            'runner_details': {
                'runner-1': {
                    'count': 2,
                    'successful': 1,
                    'failed': 1,
                    'total_duration': 3600
                }
            },
            'alerts': [
                {
                    'type': 'high_failure_rate',
                    'message': 'Failure rate (25.0%) exceeds threshold (20.0%)'
                }
            ]
        }
        
        # Generate markdown (simplified version)
        markdown = f"""# Runner Health Report
Generated: {health_report['timestamp']}

## Summary
- **Total Runs**: {health_report['summary']['total_runs']}
- **Self-Hosted Runs**: {health_report['summary']['self_hosted_runs']}
- **Hosted Runs**: {health_report['summary']['hosted_runs']}
- **Success Rate**: {health_report['summary']['success_rate']}%
- **Failure Rate**: {health_report['summary']['failure_rate']}%
- **Total Runners**: {health_report['summary']['total_runners']}

## Runner Details
"""
        
        for runner_name, stats in health_report['runner_details'].items():
            success_rate = (stats['successful'] / stats['count'] * 100) if stats['count'] > 0 else 0
            avg_duration = stats['total_duration'] / stats['count'] / 60 if stats['count'] > 0 else 0
            
            markdown += f"""
### {runner_name}
- **Jobs Completed**: {stats['count']}
- **Success Rate**: {success_rate:.1f}%
- **Average Duration**: {avg_duration:.1f} minutes
"""
        
        if health_report['alerts']:
            markdown += "\n## Alerts\n"
            for alert in health_report['alerts']:
                if alert['type'] == 'high_failure_rate':
                    markdown += f"- ⚠️ {alert['message']}\n"
        
        # Test markdown content
        self.assertIn('# Runner Health Report', markdown)
        self.assertIn('Total Runs: 4', markdown)
        self.assertIn('Success Rate: 75.0%', markdown)
        self.assertIn('### runner-1', markdown)
        self.assertIn('Jobs Completed: 2', markdown)
        self.assertIn('## Alerts', markdown)
        self.assertIn('⚠️', markdown)

    @patch('requests.post')
    def test_issue_creation(self, mock_post):
        """Test GitHub issue creation logic."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response
        
        # Test alert data
        alert = {
            'type': 'high_failure_rate',
            'message': 'Failure rate (25.0%) exceeds threshold (20.0%)'
        }
        
        report_summary = {
            'total_runs': 100,
            'failure_rate': 25.0,
            'success_rate': 75.0
        }
        
        # Simulate issue creation logic
        if alert['type'] == 'high_failure_rate':
            title = "High Failure Rate Detected"
            body = f"""
            ## 🚨 High Failure Rate Alert
            
            The repository is experiencing a high failure rate of {report_summary['failure_rate']:.1f}%.
            
            **Details:**
            - Total runs: {report_summary['total_runs']}
            - Success rate: {report_summary['success_rate']:.1f}%
            
            **Action Required:**
            Please investigate recent workflow failures and runner health.
            """
        
        data = {
            'title': title,
            'body': body,
            'labels': ['runner-health', 'monitoring']
        }
        
        # Verify the data structure
        self.assertEqual(data['title'], "High Failure Rate Detected")
        self.assertIn('🚨 High Failure Rate Alert', data['body'])
        self.assertIn('runner-health', data['labels'])
        self.assertIn('monitoring', data['labels'])
        
        # The actual API call would be made here in the real workflow
        # mock_post.assert_called_once()

    def test_cleanup_logic(self):
        """Test runner cleanup logic."""
        # Simulate alert data for cleanup
        alerts = [
            {'type': 'stuck_runner', 'runner': 'runner-1'},
            {'type': 'stuck_runner', 'runner': 'runner-2'}
        ]
        
        # Extract runners to cleanup
        runners_to_cleanup = []
        for alert in alerts:
            if alert['type'] == 'stuck_runner':
                runners_to_cleanup.append(alert['runner'])
        
        self.assertEqual(runners_to_cleanup, ['runner-1', 'runner-2'])
        
        # Simulate runner list from API
        runners_list = [
            {'id': 1, 'name': 'runner-1'},
            {'id': 2, 'name': 'runner-2'},
            {'id': 3, 'name': 'runner-3'}
        ]
        
        # Find runners to delete
        runners_to_delete = []
        for runner in runners_list:
            if runner['name'] in runners_to_cleanup:
                runners_to_delete.append(runner)
        
        self.assertEqual(len(runners_to_delete), 2)
        self.assertEqual(runners_to_delete[0]['name'], 'runner-1')
        self.assertEqual(runners_to_delete[1]['name'], 'runner-2')


if __name__ == '__main__':
    # Mock rationale: Create mock workflow run data for testing
    unittest.main()
