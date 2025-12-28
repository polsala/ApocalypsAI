import unittest
import os
import sys
import json
import subprocess
from unittest.mock import patch, MagicMock

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestProductionExample(unittest.TestCase):
    """Test the production example configuration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.example_dir = os.path.join(os.path.dirname(__file__), '..', 'examples', 'production')
        self.tfvars_file = os.path.join(self.example_dir, 'terraform.tfvars')
        self.main_tf_file = os.path.join(self.example_dir, 'main.tf')
    
    def test_production_example_exists(self):
        """Test that production example files exist"""
        self.assertTrue(os.path.exists(self.example_dir))
        self.assertTrue(os.path.exists(self.main_tf_file))
    
    def test_production_example_terraform_syntax(self):
        """Test that production example has valid Terraform syntax"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Production example main.tf not found")
        
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
    
    def test_production_example_conservative_settings(self):
        """Test that production example has conservative settings"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Production example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for conservative settings
        conservative_configs = [
            'chaos_intensity = 2',  # Low intensity
            'safe_mode = false',    # Actual termination enabled
            'dry_run_only = false', # Real chaos
            'chaos_schedule = "0 3 * * 1"',  # Weekly on Monday
            'max_terminations_per_run = 3',  # Low limit
            'min_time_between_runs = 168',   # 1 week
            'log_retention_days = 90'  # Long retention
        ]
        
        for config in conservative_configs:
            self.assertIn(config, content, 
                         f"Expected conservative configuration not found: {config}")
    
    def test_production_example_target_resources(self):
        """Test that production example targets appropriate resources"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Production example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for production-appropriate target resources
        target_resources = [
            '"aws_instance"',
            '"aws_rds_instance"',
            '"aws_ecs_service"',
            '"aws_autoscaling_group"'
        ]
        
        for resource in target_resources:
            self.assertIn(resource, content, 
                         f"Expected target resource not found: {resource}")
    
    def test_production_example_excluded_tags(self):
        """Test that production example has strict excluded tags"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Production example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for strict excluded tags
        excluded_tags = [
            '"critical"',
            '"production-critical"',
            '"do-not-terminate"',
            '"database-primary"',
            '"load-balancer"',
            '"monitoring"'
        ]
        
        for tag in excluded_tags:
            self.assertIn(tag, content, 
                         f"Expected excluded tag not found: {tag}")
    
    def test_production_example_notifications(self):
        """Test that production example has comprehensive notifications"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Production example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for production notifications
        self.assertIn('enable_notifications = true', content)
        self.assertIn('"platform-team@example.com"', content)
        self.assertIn('"oncall@example.com"', content)
    
    def test_production_example_monitoring(self):
        """Test that production example has comprehensive monitoring"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Production example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for production monitoring
        self.assertIn('enable_metrics = true', content)
        self.assertIn('enable_alarm = true', content)
        self.assertIn('chaos_high_error_rate', content)
    
    def test_production_example_sns_subscriptions(self):
        """Test that production example has SNS subscriptions"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Production example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for SNS subscriptions
        self.assertIn('aws_sns_topic_subscription', content)
        self.assertIn('chaos_notifications', content)
        self.assertIn('chaos_oncall', content)
    
    def test_production_example_enhanced_dashboard(self):
        """Test that production example has enhanced dashboard"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Production example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for enhanced dashboard
        self.assertIn('production_chaos_dashboard', content)
        self.assertIn('ConcurrentExecutions', content)
        self.assertIn('Throttles', content)
    
    def test_production_example_excluded_resource_ids(self):
        """Test that production example has excluded resource IDs"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Production example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for excluded resource IDs
        self.assertIn('excluded_resource_ids = [', content)
        self.assertIn('"i-1234567890abcdef0"', content)  # Primary database
        self.assertIn('"i-0987654321fedcba0"', content)  # Load balancer
    
    def test_production_example_cost_center_tag(self):
        """Test that production example has cost center tag"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Production example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for cost center tag
        self.assertIn('"CostCenter" = "platform-ops"', content)
    
    def test_production_example_environment_tag(self):
        """Test that production example has production environment tag"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Production example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for production environment tag
        self.assertIn('"Environment" = "production"', content)
    
    def test_production_example_outputs(self):
        """Test that production example has comprehensive outputs"""
        if not os.path.exists(self.main_tf_file):
            self.skipTest("Production example main.tf not found")
        
        with open(self.main_tf_file, 'r') as f:
            content = f.read()
        
        # Check for production outputs
        expected_outputs = [
            'production_chaos_status',
            'production_chaos_enhanced',
            'enhanced_dashboard_url',
            'sns_subscriptions',
            'error_alarm'
        ]
        
        for output in expected_outputs:
            self.assertIn(output, content, 
                         f"Expected production output not found: {output}")


if __name__ == '__main__':
    unittest.main()
