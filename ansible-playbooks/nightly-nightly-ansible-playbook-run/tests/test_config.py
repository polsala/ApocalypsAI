"""Tests for the ConfigManager class."""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

from src.config import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'test_config.yml')
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_default_config(self):
        """Test loading default configuration."""
        config_manager = ConfigManager(self.config_path)
        config = config_manager.config
        
        self.assertIn('runner', config)
        self.assertIn('validation', config)
        self.assertIn('environments', config)
        self.assertEqual(config['runner']['default_timeout'], 600)
        self.assertTrue(config['runner']['enable_rollback'])
        self.assertEqual(config['runner']['report_format'], 'html')
    
    def test_load_custom_config(self):
        """Test loading custom configuration."""
        custom_config = {
            'runner': {
                'default_timeout': 1200,
                'log_level': 'DEBUG'
            },
            'validation': {
                'check_idempotency': False
            }
        }
        
        with open(self.config_path, 'w') as f:
            import yaml
            yaml.dump(custom_config, f)
        
        config_manager = ConfigManager(self.config_path)
        config = config_manager.config
        
        self.assertEqual(config['runner']['default_timeout'], 1200)
        self.assertEqual(config['runner']['log_level'], 'DEBUG')
        self.assertFalse(config['validation']['check_idempotency'])
    
    def test_get_value(self):
        """Test getting configuration values."""
        config_manager = ConfigManager(self.config_path)
        
        self.assertEqual(config_manager.get('runner.default_timeout'), 600)
        self.assertEqual(config_manager.get('runner.log_level'), 'INFO')
        self.assertIsNone(config_manager.get('nonexistent.key'))
        self.assertEqual(config_manager.get('nonexistent.key', 'default'), 'default')
    
    def test_set_value(self):
        """Test setting configuration values."""
        config_manager = ConfigManager(self.config_path)
        
        config_manager.set('runner.default_timeout', 1800)
        config_manager.set('runner.new_option', 'test')
        
        self.assertEqual(config_manager.get('runner.default_timeout'), 1800)
        self.assertEqual(config_manager.get('runner.new_option'), 'test')
    
    def test_save_config(self):
        """Test saving configuration to file."""
        config_manager = ConfigManager(self.config_path)
        config_manager.set('runner.default_timeout', 1800)
        config_manager.save()
        
        # Load config from file
        with open(self.config_path, 'r') as f:
            saved_config = json.load(f)
        
        self.assertEqual(saved_config['runner']['default_timeout'], 1800)
    
    def test_validate_config_valid(self):
        """Test validating a valid configuration."""
        config_manager = ConfigManager(self.config_path)
        is_valid, errors = config_manager.validate()
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_config_invalid_timeout(self):
        """Test validating configuration with invalid timeout."""
        config_manager = ConfigManager(self.config_path)
        config_manager.set('runner.default_timeout', -100)
        
        is_valid, errors = config_manager.validate()
        
        self.assertFalse(is_valid)
        self.assertIn('positive integer', errors[0])
    
    def test_validate_config_invalid_log_level(self):
        """Test validating configuration with invalid log level."""
        config_manager = ConfigManager(self.config_path)
        config_manager.set('runner.log_level', 'INVALID')
        
        is_valid, errors = config_manager.validate()
        
        self.assertFalse(is_valid)
        self.assertIn('must be one of', errors[0])


if __name__ == '__main__':
    unittest.main()
