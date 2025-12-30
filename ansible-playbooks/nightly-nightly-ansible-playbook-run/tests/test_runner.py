"""Tests for the PlaybookRunner class."""

import json
import os
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock

from src.runner import PlaybookRunner


class TestPlaybookRunner(unittest.TestCase):
    """Test cases for PlaybookRunner."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'test_config.yml')
        self.runner = PlaybookRunner(self.config_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_load_config_default(self):
        """Test loading default configuration."""
        runner = PlaybookRunner()
        config = runner.config
        
        self.assertIn('runner', config)
        self.assertIn('validation', config)
        self.assertIn('environments', config)
        self.assertEqual(config['runner']['default_timeout'], 600)
    
    def test_load_config_custom(self):
        """Test loading custom configuration."""
        custom_config = {
            'runner': {
                'default_timeout': 1200,
                'log_level': 'DEBUG'
            }
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(custom_config, f)
        
        runner = PlaybookRunner(self.config_path)
        self.assertEqual(runner.config['runner']['default_timeout'], 1200)
        self.assertEqual(runner.config['runner']['log_level'], 'DEBUG')
    
    def test_validate_playbook_valid(self):
        """Test validating a valid playbook."""
        playbook_content = [
            {
                'hosts': 'all',
                'tasks': [
                    {
                        'name': 'Test task',
                        'debug': {
                            'msg': 'Hello World'
                        }
                    }
                ]
            }
        ]
        
        playbook_path = os.path.join(self.temp_dir, 'valid_playbook.yml')
        with open(playbook_path, 'w') as f:
            import yaml
            yaml.dump(playbook_content, f)
        
        is_valid, errors = self.runner.validate_playbook(playbook_path)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_playbook_invalid_yaml(self):
        """Test validating an invalid YAML playbook."""
        playbook_path = os.path.join(self.temp_dir, 'invalid_playbook.yml')
        with open(playbook_path, 'w') as f:
            f.write("invalid: yaml: content:")
        
        is_valid, errors = self.runner.validate_playbook(playbook_path)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_validate_playbook_missing_hosts(self):
        """Test validating a playbook missing hosts field."""
        playbook_content = [
            {
                'tasks': [
                    {
                        'name': 'Test task',
                        'debug': {
                            'msg': 'Hello World'
                        }
                    }
                ]
            }
        ]
        
        playbook_path = os.path.join(self.temp_dir, 'missing_hosts.yml')
        with open(playbook_path, 'w') as f:
            import yaml
            yaml.dump(playbook_content, f)
        
        is_valid, errors = self.runner.validate_playbook(playbook_path)
        self.assertFalse(is_valid)
        self.assertIn('missing hosts field', errors[0])
    
    def test_validate_inventory_valid(self):
        """Test validating a valid inventory file."""
        inventory_content = """[all]
localhost ansible_connection=local
"""
        
        inventory_path = os.path.join(self.temp_dir, 'valid_inventory.ini')
        with open(inventory_path, 'w') as f:
            f.write(inventory_content)
        
        is_valid, errors = self.runner.validate_inventory(inventory_path)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_inventory_missing(self):
        """Test validating a missing inventory file."""
        inventory_path = os.path.join(self.temp_dir, 'missing_inventory.ini')
        
        is_valid, errors = self.runner.validate_inventory(inventory_path)
        self.assertFalse(is_valid)
        self.assertIn('Inventory file not found', errors[0])
    
    @patch('subprocess.run')
    def test_run_playbook_success(self, mock_run):
        """Test successful playbook execution."""
        # Mock successful subprocess run
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'PLAY [all] ***\nok: [localhost]\n'
        mock_result.stderr = ''
        mock_run.return_value = mock_result
        
        playbook_path = os.path.join(self.temp_dir, 'test_playbook.yml')
        inventory_path = os.path.join(self.temp_dir, 'test_inventory.ini')
        
        with open(playbook_path, 'w') as f:
            f.write('')
        with open(inventory_path, 'w') as f:
            f.write('')
        
        result = self.runner.run_playbook(playbook_path, inventory_path)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['return_code'], 0)
        self.assertEqual(len(self.runner.execution_log), 1)
    
    @patch('subprocess.run')
    def test_run_playbook_timeout(self, mock_run):
        """Test playbook execution timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired('ansible-playbook', 60)
        
        playbook_path = os.path.join(self.temp_dir, 'test_playbook.yml')
        inventory_path = os.path.join(self.temp_dir, 'test_inventory.ini')
        
        with open(playbook_path, 'w') as f:
            f.write('')
        with open(inventory_path, 'w') as f:
            f.write('')
        
        result = self.runner.run_playbook(playbook_path, inventory_path, timeout=60)
        
        self.assertFalse(result['success'])
        self.assertEqual(result['return_code'], -1)
        self.assertIn('Timeout', result['stderr'])
    
    def test_generate_json_report(self):
        """Test JSON report generation."""
        # Add some execution records
        self.runner.execution_log = [
            {
                'playbook': 'test.yml',
                'inventory': 'test.ini',
                'success': True,
                'execution_time': 10.5,
                'return_code': 0,
                'stdout': 'Success',
                'stderr': ''
            },
            {
                'playbook': 'test2.yml',
                'inventory': 'test2.ini',
                'success': False,
                'execution_time': 5.2,
                'return_code': 1,
                'stdout': '',
                'stderr': 'Error'
            }
        ]
        
        report = self.runner._generate_json_report()
        report_data = json.loads(report)
        
        self.assertEqual(report_data['execution_summary']['total_executions'], 2)
        self.assertEqual(report_data['execution_summary']['successful'], 1)
        self.assertEqual(report_data['execution_summary']['failed'], 1)
        self.assertEqual(report_data['execution_summary']['total_execution_time'], 15.7)
    
    def test_generate_markdown_report(self):
        """Test Markdown report generation."""
        self.runner.execution_log = [
            {
                'playbook': 'test.yml',
                'inventory': 'test.ini',
                'success': True,
                'execution_time': 10.5,
                'return_code': 0,
                'stdout': 'Success output',
                'stderr': ''
            }
        ]
        
        report = self.runner._generate_markdown_report()
        
        self.assertIn('# Ansible Playbook Runner Report', report)
        self.assertIn('## Summary', report)
        self.assertIn('## Execution Details', report)
        self.assertIn('✅ Success', report)
        self.assertIn('Success output', report)


if __name__ == '__main__':
    unittest.main()
