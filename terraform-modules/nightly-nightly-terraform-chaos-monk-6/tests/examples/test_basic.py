import unittest
import os
import sys
import json
import subprocess
from unittest.mock import patch, MagicMock

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestBasicExample(unittest.TestCase):
    """Test the basic example configuration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.example_dir = os.path.join(os.path.dirname(__file__), '..', 'examples', 'basic')
        self.tfvars_file = os.path.join(self.example_dir, 'terraform.tfvars')
        self.main_tf_file = os.path.join(self.example_dir, 'main.tf')
    
    def test_basic_example_exists(self):
        """Test that basic example files exist"""
        self.assertTrue(os.path.exists(self.example_dir))
        self.assertTrue(os.path.exists(self.main_tf_file))
    
    def test_basic_example_terraform_syntax(self):
        """Test that basic example has valid Terraform syntax"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Basic example main.tf not found")
        
        # Check if terraform is available
        try:
            result = subprocess.run(['terraform', 'version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                self.skipTest("Terraform not available for syntax validation")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.skipTest("Terraform not available for syntax validation")
        
        # Validate syntax
        result = subprocess.run(['terraform', 'validate'], 
                              cwd=self.example_dir,
                              capture_output=True, text=True, timeout=30)
        
        self.assertEqual(result.returncode, 0, 
                        f"Terraform validation failed: {result.stderr}")
    
    def test_basic_example_variables(self):
        """Test that basic example has expected variables"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Basic example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for expected configuration
        expected_configs = [
            'prefix = "basic-chaos"',
            'enabled = true',
            'chaos_schedule = "0 2 * * *"',
            'chaos_intensity = 5',
            'safe_mode = true',
            'target_resources = [',
            '"aws_instance"',
            '"aws_rds_instance"',
            'excluded_tags = [',
            '"critical"',
            '"production-critical"',
            '"do-not-terminate"',
            'log_retention_days = 7',
            'max_terminations_per_run = 5',
            'min_time_between_runs = 6'
        ]
        
        for expected_config in expected_configs:
            self.assertIn(expected_config, content, 
                         f"Expected configuration not found: {expected_config}")
    
    def test_basic_example_outputs(self):
        """Test that basic example has expected outputs"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Basic example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for expected outputs
        expected_outputs = [
            'chaos_status',
            'enabled',
            'intensity',
            'safe_mode',
            'targets',
            'dashboard_url'
        ]
        
        for expected_output in expected_outputs:
            self.assertIn(expected_output, content, 
                         f"Expected output not found: {expected_output}")
    
    def test_basic_example_safe_mode_enabled(self):
        """Test that basic example has safe mode enabled"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Basic example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check that safe mode is enabled
        self.assertIn('safe_mode = true', content)
    
    def test_basic_example_low_intensity(self):
        """Test that basic example has low chaos intensity"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Basic example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check that chaos intensity is low
        self.assertIn('chaos_intensity = 5', content)
    
    def test_basic_example_schedule(self):
        """Test that basic example has reasonable schedule"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Basic example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check that schedule is reasonable
        self.assertIn('chaos_schedule = "0 2 * * *"', content)
    
    def test_basic_example_resource_limits(self):
        """Test that basic example has reasonable resource limits"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Basic example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check that resource limits are reasonable
        self.assertIn('max_terminations_per_run = 5', content)
        self.assertIn('min_time_between_runs = 6', content)
    
    def test_basic_example_notification_config(self):
        """Test that basic example has notification configuration"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Basic example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check that notifications are configured
        self.assertIn('enable_notifications = true', content)
        self.assertIn('notification_emails = [', content)
        self.assertIn('"admin@example.com"', content)
    
    def test_basic_example_monitoring_config(self):
        """Test that basic example has monitoring configuration"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Basic example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check that monitoring is configured
        self.assertIn('enable_metrics = true', content)
        self.assertIn('enable_alarm = true', content)
    
    def test_basic_example_chaos_window(self):
        """Test that basic example has chaos window configuration"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Basic example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check that chaos window is configured
        self.assertIn('chaos_window_start = 2', content)
        self.assertIn('chaos_window_end = 6', content)
    
    def test_basic_example_duration_limit(self):
        """Test that basic example has duration limit"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Basic example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check that duration limit is configured
        self.assertIn('chaos_duration_minutes = 30', content)
    
    def test_basic_example_tags(self):
        """Test that basic example has chaos tags"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Basic example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check that chaos tags are configured
        self.assertIn('chaos_tags = {', content)
        self.assertIn('"Environment" = "staging"', content)
        self.assertIn('"Team"       = "platform"', content)


if __name__ == '__main__':
    unittest.main()
