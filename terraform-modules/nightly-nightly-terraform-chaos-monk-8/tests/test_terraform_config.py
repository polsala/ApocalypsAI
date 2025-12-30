import unittest
import json
import os
import subprocess
import tempfile


class TestTerraformConfig(unittest.TestCase):
    """
    Integration tests for the Terraform configuration.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        self.test_dir = tempfile.mkdtemp()
        self.terraform_files = [
            'main.tf',
            'variables.tf',
            'outputs.tf',
            'lambda/index.py',
            'lambda/requirements.txt',
            'README.md'
        ]
    
    def tearDown(self):
        """
        Clean up test fixtures.
        """
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_terraform_files_exist(self):
        """
        Test that all required Terraform files exist.
        """
        # Copy test files to temporary directory
        for file_name in self.terraform_files:
            src_path = os.path.join(os.path.dirname(__file__), '..', file_name)
            if os.path.exists(src_path):
                dst_path = os.path.join(self.test_dir, file_name)
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                import shutil
                shutil.copy2(src_path, dst_path)
        
        # Check that main files exist
        required_files = ['main.tf', 'variables.tf', 'outputs.tf']
        for file_name in required_files:
            file_path = os.path.join(self.test_dir, file_name)
            self.assertTrue(os.path.exists(file_path), f"{file_name} should exist")
    
    def test_terraform_syntax(self):
        """
        Test that Terraform files have valid syntax.
        """
        # This test requires terraform to be installed
        try:
            result = subprocess.run(
                ['terraform', 'validate'],
                cwd=self.test_dir,
                capture_output=True,
                text=True
            )
            
            # If terraform is not installed, skip this test
            if result.returncode != 0 and 'not found' in result.stderr:
                self.skipTest('Terraform CLI not installed')
            
            # Check syntax validation
            self.assertEqual(result.returncode, 0, 
                           f"Terraform syntax validation failed: {result.stderr}")
                            
        except FileNotFoundError:
            self.skipTest('Terraform CLI not found')
    
    def test_lambda_function_structure(self):
        """
        Test that the Lambda function has the correct structure.
        """
        lambda_file = os.path.join(os.path.dirname(__file__), '..', 'lambda', 'index.py')
        
        self.assertTrue(os.path.exists(lambda_file), "Lambda function file should exist")
        
        # Read and check the lambda file
        with open(lambda_file, 'r') as f:
            content = f.read()
        
        # Check for required imports
        required_imports = ['json', 'boto3', 'random', 'os', 'logging']
        for imp in required_imports:
            self.assertIn(f'import {imp}', content, f"Lambda should import {imp}")
        
        # Check for required functions
        required_functions = ['lambda_handler', 'should_execute_chaos', 'execute_chaos']
        for func in required_functions:
            self.assertIn(f'def {func}', content, f"Lambda should have {func} function")
    
    def test_lambda_requirements(self):
        """
        Test that Lambda requirements file is properly formatted.
        """
        requirements_file = os.path.join(os.path.dirname(__file__), '..', 'lambda', 'requirements.txt')
        
        self.assertTrue(os.path.exists(requirements_file), "Lambda requirements file should exist")
        
        with open(requirements_file, 'r') as f:
            content = f.read()
        
        # Should not have any non-comment lines for this simple implementation
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        non_comment_lines = [line for line in lines if not line.startswith('#')]
        
        # For this chaos monkey, we only use built-in libraries
        self.assertEqual(len(non_comment_lines), 0, 
                        "Requirements file should only contain comments for built-in libraries")
    
    def test_readme_content(self):
        """
        Test that README contains required sections.
        """
        readme_file = os.path.join(os.path.dirname(__file__), '..', 'README.md')
        
        self.assertTrue(os.path.exists(readme_file), "README file should exist")
        
        with open(readme_file, 'r') as f:
            content = f.read()
        
        # Check for required sections
        required_sections = [
            '# Nightly Terraform Chaos Monkey',
            '## Features',
            '## Usage',
            '## Configuration',
            '## Safety Features',
            '## Installation',
            '## Monitoring',
            '## Contributing',
            '## License',
            '## Disclaimer'
        ]
        
        for section in required_sections:
            self.assertIn(section, content, f"README should contain {section}")
    
    def test_variable_validation(self):
        """
        Test that Terraform variables have proper validation.
        """
        variables_file = os.path.join(os.path.dirname(__file__), '..', 'variables.tf')
        
        self.assertTrue(os.path.exists(variables_file), "Variables file should exist")
        
        with open(variables_file, 'r') as f:
            content = f.read()
        
        # Check for validation blocks
        self.assertIn('validation {', content, "Variables should have validation blocks")
        self.assertIn('condition', content, "Validation should have condition")
        self.assertIn('error_message', content, "Validation should have error_message")
        
        # Check specific validations
        validations = [
            'var.chaos_probability >= 0 && var.chaos_probability <= 1',
            'var.time_window_start >= 0 && var.time_window_start <= 23',
            'var.time_window_end >= 0 && var.time_window_end <= 23'
        ]
        
        for validation in validations:
            self.assertIn(validation, content, f"Should validate: {validation}")


if __name__ == '__main__':
    unittest.main()
