"""Integration tests for the Ansible Playbook Runner."""

import os
import tempfile
import unittest
from pathlib import Path

from src.runner import PlaybookRunner


class TestIntegration(unittest.TestCase):
    """Integration test cases."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.playbook_path = os.path.join(self.temp_dir, 'test_playbook.yml')
        self.inventory_path = os.path.join(self.temp_dir, 'test_inventory.ini')
        self.config_path = os.path.join(self.temp_dir, 'test_config.yml')
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_full_workflow(self):
        """Test the complete workflow from validation to execution."""
        # Create a simple valid playbook
        playbook_content = [
            {
                'name': 'Test Playbook',
                'hosts': 'localhost',
                'connection': 'local',
                'tasks': [
                    {
                        'name': 'Test task',
                        'debug': {
                            'msg': 'Hello from test playbook'
                        }
                    }
                ]
            }
        ]
        
        with open(self.playbook_path, 'w') as f:
            import yaml
            yaml.dump(playbook_content, f)
        
        # Create a simple inventory
        inventory_content = """[all]
localhost ansible_connection=local
"""
        
        with open(self.inventory_path, 'w') as f:
            f.write(inventory_content)
        
        # Create a config
        config_content = {
            'runner': {
                'default_timeout': 300,
                'log_level': 'INFO'
            }
        }
        
        with open(self.config_path, 'w') as f:
            import yaml
            yaml.dump(config_content, f)
        
        # Initialize runner
        runner = PlaybookRunner(self.config_path)
        
        # Validate inputs
        playbook_valid, playbook_errors = runner.validate_playbook(self.playbook_path)
        self.assertTrue(playbook_valid, f"Playbook validation failed: {playbook_errors}")
        
        inventory_valid, inventory_errors = runner.validate_inventory(self.inventory_path)
        self.assertTrue(inventory_valid, f"Inventory validation failed: {inventory_errors}")
        
        # Note: We can't actually run ansible-playbook in tests without Ansible installed
        # So we'll just test the validation and configuration parts
        
        # Test report generation with empty execution log
        json_report = runner.generate_report('json')
        json_data = json.loads(json_report)
        self.assertEqual(json_data['execution_summary']['total_executions'], 0)
        
        markdown_report = runner.generate_report('markdown')
        self.assertIn('# Ansible Playbook Runner Report', markdown_report)
        
        html_report = runner.generate_report('html')
        self.assertIn('<title>Ansible Playbook Runner Report</title>', html_report)
    
    def test_config_validation(self):
        """Test configuration validation with various scenarios."""
        from src.config import ConfigManager
        
        # Test valid config
        config_manager = ConfigManager()
        is_valid, errors = config_manager.validate()
        self.assertTrue(is_valid)
        
        # Test invalid timeout
        config_manager.set('runner.default_timeout', -1)
        is_valid, errors = config_manager.validate()
        self.assertFalse(is_valid)
        self.assertIn('positive integer', errors[0])
        
        # Reset and test invalid log level
        config_manager = ConfigManager()
        config_manager.set('runner.log_level', 'INVALID_LEVEL')
        is_valid, errors = config_manager.validate()
        self.assertFalse(is_valid)
        self.assertIn('must be one of', errors[0])


if __name__ == '__main__':
    unittest.main()
