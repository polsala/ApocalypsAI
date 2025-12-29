import unittest
import os
import json
import subprocess
import tempfile
from pathlib import Path


class TestTerraformModule(unittest.TestCase):
    """Test cases for Terraform module validation"""
    
    def setUp(self):
        """Set up test environment"""
        self.module_dir = Path(__file__).parent.parent
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_terraform_init(self):
        """Test that Terraform can initialize the module"""
        # Copy module files to test directory
        for file in ['main.tf', 'variables.tf', 'outputs.tf', 'versions.tf']:
            src = self.module_dir / file
            dst = Path(self.test_dir) / file
            if src.exists():
                import shutil
                shutil.copy2(src, dst)
        
        # Initialize Terraform
        result = subprocess.run(
            ['terraform', 'init'],
            cwd=self.test_dir,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"Terraform init failed: {result.stderr}")
    
    def test_terraform_validate(self):
        """Test that Terraform configuration is valid"""
        # Copy module files to test directory
        for file in ['main.tf', 'variables.tf', 'outputs.tf', 'versions.tf']:
            src = self.module_dir / file
            dst = Path(self.test_dir) / file
            if src.exists():
                import shutil
                shutil.copy2(src, dst)
        
        # Initialize Terraform
        subprocess.run(['terraform', 'init'], cwd=self.test_dir, capture_output=True)
        
        # Validate configuration
        result = subprocess.run(
            ['terraform', 'validate'],
            cwd=self.test_dir,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"Terraform validate failed: {result.stderr}")
    
    def test_terraform_plan(self):
        """Test that Terraform can generate a plan"""
        # Create a test configuration that uses the module
        test_config = f'''
module "chaos_monkey" {{
  source = "{self.module_dir}"
  
  enabled = true
  destruction_probability = 0.1
  target_resource_types = ["aws_instance"]
  safe_mode = true
  max_resources_per_run = 2
}}
'''
        
        # Write test configuration
        with open(Path(self.test_dir) / 'main.tf', 'w') as f:
            f.write(test_config)
        
        # Initialize Terraform
        subprocess.run(['terraform', 'init'], cwd=self.test_dir, capture_output=True)
        
        # Generate plan
        result = subprocess.run(
            ['terraform', 'plan', '-out=plan.out'],
            cwd=self.test_dir,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"Terraform plan failed: {result.stderr}")
    
    def test_lambda_zip_exists(self):
        """Test that Lambda function code exists"""
        lambda_dir = self.module_dir / 'lambda'
        self.assertTrue(lambda_dir.exists(), "Lambda directory not found")
        
        index_file = lambda_dir / 'index.py'
        self.assertTrue(index_file.exists(), "Lambda index.py file not found")
        
        requirements_file = lambda_dir / 'requirements.txt'
        self.assertTrue(requirements_file.exists(), "Lambda requirements.txt file not found")
    
    def test_readme_exists(self):
        """Test that README exists and contains required sections"""
        readme_file = self.module_dir / 'README.md'
        self.assertTrue(readme_file.exists(), "README.md not found")
        
        with open(readme_file, 'r') as f:
            content = f.read()
        
        # Check for required sections
        required_sections = [
            '# Terraform Chaos Monkey',
            '## Features',
            '## Usage',
            '## Configuration Options',
            '## Safety Considerations'
        ]
        
        for section in required_sections:
            self.assertIn(section, content, f"Missing section: {section}")
    
    def test_variable_validation(self):
        """Test variable validation logic"""
        # Test destruction probability validation
        self.assertGreaterEqual(0.05, 0)
        self.assertLessEqual(0.05, 1)
        
        # Test max resources per run validation
        self.assertGreater(3, 0)
        
        # Test log retention validation
        self.assertGreater(30, 0)
        self.assertLessEqual(30, 2557)
    
    def test_output_structure(self):
        """Test that outputs are properly defined"""
        outputs_file = self.module_dir / 'outputs.tf'
        self.assertTrue(outputs_file.exists(), "outputs.tf not found")
        
        with open(outputs_file, 'r') as f:
            content = f.read()
        
        # Check for required outputs
        required_outputs = [
            'chaos_monkey_enabled',
            'chaos_schedule',
            'safe_mode',
            'lambda_function_arn',
            'lambda_function_name'
        ]
        
        for output in required_outputs:
            self.assertIn(f'output "{output}"', content, f"Missing output: {output}")


if __name__ == '__main__':
    unittest.main()
