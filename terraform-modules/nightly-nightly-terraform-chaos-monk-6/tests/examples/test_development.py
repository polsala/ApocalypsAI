import unittest
import os
import sys
import json
import subprocess
from unittest.mock import patch, MagicMock

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestDevelopmentExample(unittest.TestCase):
    """Test the development example configuration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.example_dir = os.path.join(os.path.dirname(__file__), '..', 'examples', 'development')
        self.tfvars_file = os.path.join(self.example_dir, 'terraform.tfvars')
        self.main_tf_file = os.path.join(self.example_dir, 'main.tf')
    
    def test_development_example_exists(self):
        """Test that development example files exist"""
        self.assertTrue(os.path.exists(self.example_dir))
        self.assertTrue(os.path.exists(self.main_tf_file))
    
    def test_development_example_terraform_syntax(self):
        """Test that development example has valid Terraform syntax"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
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
    
    def test_development_example_frequent_schedule(self):
        """Test that development example has frequent chaos schedule"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for frequent schedule
        self.assertIn('chaos_schedule = "0 */2 * * *"', content)  # Every 2 hours
    
    def test_development_example_high_intensity(self):
        """Test that development example has high chaos intensity"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for high intensity
        self.assertIn('chaos_intensity = 20', content)  # 20% intensity
    
    def test_development_example_safe_mode(self):
        """Test that development example has safe mode enabled"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check that safe mode is enabled
        self.assertIn('safe_mode = true', content)
    
    def test_development_example_dry_run_only(self):
        """Test that development example has dry run only"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check that dry run only is enabled
        self.assertIn('dry_run_only = true', content)
    
    def test_development_example_all_resource_types(self):
        """Test that development example targets all resource types"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for all resource types
        all_resource_types = [
            '"aws_instance"',
            '"aws_rds_instance"',
            '"aws_ecs_service"',
            '"aws_autoscaling_group"',
            '"aws_elasticache_cluster"'
        ]
        
        for resource_type in all_resource_types:
            self.assertIn(resource_type, content, 
                         f"Expected resource type not found: {resource_type}")
    
    def test_development_example_minimal_excluded_tags(self):
        """Test that development example has minimal excluded tags"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for minimal excluded tags
        self.assertIn('excluded_tags = [', content)
        self.assertIn('"do-not-terminate"', content)
        # Should not have many excluded tags
        self.assertNotIn('"critical"', content)
        self.assertNotIn('"production-critical"', content)
    
    def test_development_example_short_log_retention(self):
        """Test that development example has short log retention"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for short log retention
        self.assertIn('log_retention_days = 3', content)
    
    def test_development_example_high_limits(self):
        """Test that development example has high resource limits"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for high limits
        self.assertIn('max_terminations_per_run = 20', content)
        self.assertIn('min_time_between_runs = 1', content)  # 1 hour
    
    def test_development_example_notifications_disabled(self):
        """Test that development example has notifications disabled"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check that notifications are disabled
        self.assertIn('enable_notifications = false', content)
    
    def test_development_example_monitoring_enabled(self):
        """Test that development example has monitoring enabled"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check that monitoring is enabled
        self.assertIn('enable_metrics = true', content)
    
    def test_development_example_alarm_disabled(self):
        """Test that development example has alarm disabled"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check that alarm is disabled
        self.assertIn('enable_alarm = false', content)
    
    def test_development_example_flexible_chaos_window(self):
        """Test that development example has flexible chaos window"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for flexible chaos window
        self.assertIn('chaos_window_start = 0', content)
        self.assertIn('chaos_window_end = 23', content)
    
    def test_development_example_short_duration(self):
        """Test that development example has short duration"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for short duration
        self.assertIn('chaos_duration_minutes = 10', content)
    
    def test_development_example_dev_tags(self):
        """Test that development example has development tags"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for development tags
        self.assertIn('"Environment" = "development"', content)
        self.assertIn('"Team"       = "dev-team"', content)
    
    def test_development_example_dev_dashboard(self):
        """Test that development example has development dashboard"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for development dashboard
        self.assertIn('development_chaos_dashboard', content)
        self.assertIn('Development Chaos Monkey', content)
    
    def test_development_example_test_alarm_disabled(self):
        """Test that development example has test alarm disabled"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check that test alarm is disabled (count = 0)
        self.assertIn('count              = 0', content)
        self.assertIn('chaos_dev_test_alarm', content)
    
    def test_development_example_outputs(self):
        """Test that development example has development outputs"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Development example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for development outputs
        expected_outputs = [
            'development_chaos_status',
            'development_dashboard_url'
        ]
        
        for output in expected_outputs:
            self.assertIn(output, content, 
                         f"Expected development output not found: {output}")


if __name__ == '__main__':
    unittest.main()
