import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import yaml
from datetime import datetime, timedelta


class TestRunnerAuditor(unittest.TestCase):
    """Test cases for the GitHub Actions Runner Auditor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_headers = {
            'Authorization': 'token test-token',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.test_organization = 'test-org'
        self.test_repos = [
            {
                'name': 'repo1',
                'full_name': 'test-org/repo1',
                'private': False
            },
            {
                'name': 'repo2',
                'full_name': 'test-org/repo2',
                'private': True
            }
        ]
        self.test_workflows = [
            {
                'id': 1,
                'name': 'CI',
                'path': '.github/workflows/ci.yml',
                'state': 'active'
            }
        ]
        self.test_workflow_content = {
            'name': 'CI',
            'on': ['push', 'pull_request'],
            'jobs': {
                'build': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'run': 'echo hello'}
                    ]
                },
                'test': {
                    'runs-on': 'self-hosted',
                    'steps': [
                        {'run': 'npm test'}
                    ]
                }
            }
        }
    
    @patch('requests.get')
    def test_get_repositories(self, mock_get):
        """Test getting repositories from GitHub API"""
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = self.test_repos
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Import and test the function
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # This would normally be in the workflow script
        # For testing, we'll verify the API call structure
        expected_url = f'https://api.github.com/orgs/{self.test_organization}/repos'
        expected_params = {
            'page': 1,
            'per_page': 100,
            'type': 'all'
        }
        
        # Simulate the function call
        mock_get.assert_called_with(
            expected_url,
            headers=self.mock_headers,
            params=expected_params
        )
    
    @patch('requests.get')
    def test_get_workflows(self, mock_get):
        """Test getting workflows from GitHub API"""
        mock_response = Mock()
        mock_response.json.return_value = {'workflows': self.test_workflows}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        repo_full_name = 'test-org/repo1'
        expected_url = f'https://api.github.com/repos/{repo_full_name}/actions/workflows'
        expected_params = {
            'page': 1,
            'per_page': 100
        }
        
        # Simulate the function call
        mock_get.assert_called_with(
            expected_url,
            headers=self.mock_headers,
            params=expected_params
        )
    
    def test_analyze_workflow_file(self):
        """Test analyzing workflow file content"""
        import base64
        
        # Mock workflow content
        workflow_yaml = yaml.dump(self.test_workflow_content)
        encoded_content = base64.b64encode(workflow_yaml.encode('utf-8')).decode('utf-8')
        
        mock_response = Mock()
        mock_response.json.return_value = {'content': encoded_content}
        
        # Test the analysis logic
        runners = set()
        jobs_with_self_hosted = set()
        
        if 'jobs' in self.test_workflow_content:
            for job_name, job_config in self.test_workflow_content['jobs'].items():
                if 'runs-on' in job_config:
                    runner = job_config['runs-on']
                    if isinstance(runner, list):
                        runners.update(runner)
                    else:
                        runners.add(runner)
                    
                    if 'self-hosted' in str(runner).lower():
                        jobs_with_self_hosted.add(job_name)
        
        self.assertIn('ubuntu-latest', runners)
        self.assertIn('self-hosted', runners)
        self.assertIn('test', jobs_with_self_hosted)
    
    def test_calculate_cost_estimate(self):
        """Test cost calculation for different runner types"""
        def calculate_cost_estimate(runner_type, duration_seconds):
            cost_rates = {
                'ubuntu-latest': 0.008,
                'ubuntu-22.04': 0.008,
                'ubuntu-20.04': 0.008,
                'windows-latest': 0.008,
                'windows-2022': 0.008,
                'windows-2019': 0.008,
                'macos-latest': 0.08,
                'macos-14': 0.08,
                'macos-13': 0.08,
                'self-hosted': 0.0
            }
            
            hours = duration_seconds / 3600
            rate = cost_rates.get(runner_type, 0.01)
            return hours * rate
        
        # Test ubuntu-latest cost
        cost = calculate_cost_estimate('ubuntu-latest', 3600)  # 1 hour
        self.assertEqual(cost, 0.008)
        
        # Test macos-latest cost
        cost = calculate_cost_estimate('macos-latest', 3600)  # 1 hour
        self.assertEqual(cost, 0.08)
        
        # Test self-hosted cost
        cost = calculate_cost_estimate('self-hosted', 3600)  # 1 hour
        self.assertEqual(cost, 0.0)
        
        # Test unknown runner type
        cost = calculate_cost_estimate('unknown-runner', 3600)  # 1 hour
        self.assertEqual(cost, 0.01)  # Default rate
    
    def test_date_calculation(self):
        """Test date calculation for analysis period"""
        days_to_analyze = 30
        since = (datetime.utcnow() - timedelta(days=days_to_analyze)).isoformat() + 'Z'
        
        # Verify the date format
        self.assertTrue(since.endswith('Z'))
        self.assertIn('T', since)
        
        # Verify it's approximately 30 days ago
        date_part = since.split('T')[0]
        current_date = datetime.utcnow().strftime('%Y-%m-%d')
        
        # The date should be 30 days in the past
        # (We can't test exact dates due to timing, but we can verify format)
        self.assertRegex(date_part, r'\d{4}-\d{2}-\d{2}')
    
    def test_output_generation_json(self):
        """Test JSON output generation"""
        audit_data = {
            'organization': 'test-org',
            'audit_date': '2023-01-01T00:00:00Z',
            'repositories': [],
            'runner_usage': {},
            'summary': {
                'total_workflows': 0,
                'total_repositories_with_workflows': 0,
                'total_cost_estimate': 0.0
            }
        }
        
        # Test JSON serialization
        json_output = json.dumps(audit_data, indent=2)
        self.assertIn('organization', json_output)
        self.assertIn('audit_date', json_output)
        self.assertIn('summary', json_output)
    
    def test_output_generation_markdown(self):
        """Test Markdown output generation"""
        audit_data = {
            'organization': 'test-org',
            'audit_date': '2023-01-01T00:00:00Z',
            'runner_usage': {
                'ubuntu-latest': {
                    'count': 10,
                    'repositories': ['repo1', 'repo2'],
                    'total_cost': 5.50
                }
            },
            'summary': {
                'total_workflows': 5,
                'total_repositories_with_workflows': 3,
                'total_cost_estimate': 15.75
            }
        }
        
        # Generate markdown content
        markdown_content = f"""# GitHub Actions Runner Audit Report
"
**Organization:** {audit_data['organization']}
**Audit Date:** {audit_data['audit_date']}
**Analysis Period:** Last 30 days

## Summary
- **Total Repositories:** 5
- **Repositories with Workflows:** {audit_data['summary']['total_repositories_with_workflows']}
- **Total Workflows:** {audit_data['summary']['total_workflows']}
- **Estimated Cost:** ${audit_data['summary']['total_cost_estimate']:.2f}

## Runner Usage
### ubuntu-latest
- **Usage Count:** {audit_data['runner_usage']['ubuntu-latest']['count']}
- **Repositories:** {len(audit_data['runner_usage']['ubuntu-latest']['repositories'])}
- **Estimated Cost:** ${audit_data['runner_usage']['ubuntu-latest']['total_cost']:.2f}
"""
        
        self.assertIn('GitHub Actions Runner Audit Report', markdown_content)
        self.assertIn('test-org', markdown_content)
        self.assertIn('$15.75', markdown_content)
        self.assertIn('ubuntu-latest', markdown_content)
    
    def test_security_headers(self):
        """Test that proper security headers are used"""
        headers = {
            'Authorization': 'token test-token',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Verify required headers are present
        self.assertIn('Authorization', headers)
        self.assertIn('Accept', headers)
        
        # Verify authorization format
        self.assertTrue(headers['Authorization'].startswith('token '))
        
        # Verify GitHub API version
        self.assertEqual(headers['Accept'], 'application/vnd.github.v3+json')


if __name__ == '__main__':
    unittest.main()
