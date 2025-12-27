import os
import tempfile
import unittest
from unittest.mock import patch, mock_open
import yaml
from src.main import generate_workflow, parse_matrix, save_workflow


class TestGitHubActionsQuickstart(unittest.TestCase):
    """Test cases for the GitHub Actions Quickstart utility."""
    
    def test_generate_ci_workflow(self):
        """Test CI workflow generation."""
        content = generate_workflow(template="ci", output="test.yml")
        
        # Parse the generated YAML
        workflow = yaml.safe_load(content)
        
        # Verify basic structure
        self.assertEqual(workflow["name"], "CI Workflow")
        self.assertIn("push", workflow["on"])
        self.assertIn("pull_request", workflow["on"])
        self.assertIn("test", workflow["jobs"])
        
        # Verify CI-specific steps
        test_job = workflow["jobs"]["test"]
        self.assertEqual(test_job["runs-on"], "ubuntu-latest")
        
        steps = test_job["steps"]
        self.assertTrue(any(step.get("uses") == "actions/checkout@v4" for step in steps))
        self.assertTrue(any(step.get("uses") == "actions/setup-python@v5" for step in steps))
        self.assertTrue(any("pytest" in step.get("run", "") for step in steps))
    
    def test_generate_ci_workflow_with_matrix(self):
        """Test CI workflow generation with matrix strategy."""
        content = generate_workflow(template="ci", output="test.yml", matrix="os:ubuntu-latest,ubuntu-22.04")
        
        workflow = yaml.safe_load(content)
        test_job = workflow["jobs"]["test"]
        
        self.assertIn("strategy", test_job)
        self.assertIn("matrix", test_job["strategy"])
        self.assertIn("os", test_job["strategy"]["matrix"])
        self.assertEqual(test_job["strategy"]["matrix"]["os"], ["ubuntu-latest", "ubuntu-22.04"])
    
    def test_generate_deploy_workflow(self):
        """Test deployment workflow generation."""
        content = generate_workflow(template="deploy", output="test.yml")
        
        workflow = yaml.safe_load(content)
        
        self.assertEqual(workflow["name"], "DEPLOY Workflow")
        self.assertIn("release", workflow["on"])
        self.assertIn("deploy-staging", workflow["jobs"])
        self.assertIn("deploy-production", workflow["jobs"])
        
        # Verify job dependencies
        deploy_prod = workflow["jobs"]["deploy-production"]
        self.assertIn("needs", deploy_prod)
        self.assertEqual(deploy_prod["needs"], ["deploy-staging"])
    
    def test_generate_security_workflow(self):
        """Test security workflow generation."""
        content = generate_workflow(template="security", output="test.yml", security=True)
        
        workflow = yaml.safe_load(content)
        
        self.assertEqual(workflow["name"], "SECURITY Workflow")
        self.assertIn("codeql-analysis", workflow["jobs"])
        self.assertIn("dependency-scan", workflow["jobs"])
        
        # Verify permissions are set
        self.assertIn("permissions", workflow)
        self.assertEqual(workflow["permissions"]["security-events"], "write")
        
        # Verify CodeQL job has proper permissions
        codeql_job = workflow["jobs"]["codeql-analysis"]
        self.assertIn("permissions", codeql_job)
        self.assertEqual(codeql_job["permissions"]["security-events"], "write")
    
    def test_generate_release_workflow(self):
        """Test release workflow generation."""
        content = generate_workflow(template="release", output="test.yml")
        
        workflow = yaml.safe_load(content)
        
        self.assertEqual(workflow["name"], "RELEASE Workflow")
        self.assertIn("push", workflow["on"])
        self.assertIn("tags", workflow["on"]["push"])
        self.assertIn("build", workflow["jobs"])
        self.assertIn("publish", workflow["jobs"])
        
        # Verify job dependencies
        publish_job = workflow["jobs"]["publish"]
        self.assertIn("needs", publish_job)
        self.assertEqual(publish_job["needs"], ["build"])
    
    def test_parse_matrix_single(self):
        """Test matrix parsing with single dimension."""
        result = parse_matrix("os:ubuntu-latest,ubuntu-22.04")
        expected = {
            "matrix": {
                "os": ["ubuntu-latest", "ubuntu-22.04"]
            }
        }
        self.assertEqual(result, expected)
    
    def test_parse_matrix_multiple(self):
        """Test matrix parsing with multiple dimensions."""
        result = parse_matrix("os:ubuntu-latest,ubuntu-22.04;python:3.9,3.11")
        expected = {
            "matrix": {
                "os": ["ubuntu-latest", "ubuntu-22.04"],
                "python": ["3.9", "3.11"]
            }
        }
        self.assertEqual(result, expected)
    
    def test_parse_matrix_empty(self):
        """Test matrix parsing with empty string."""
        result = parse_matrix("")
        expected = {"matrix": {}}
        self.assertEqual(result, expected)
    
    def test_parse_matrix_invalid_format(self):
        """Test matrix parsing with invalid format."""
        result = parse_matrix("invalid")
        expected = {"matrix": {}}
        self.assertEqual(result, expected)
    
    def test_save_workflow(self):
        """Test workflow saving functionality."""
        content = "# Test workflow\nname: Test"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.yml') as tmp_file:
            temp_path = tmp_file.name
        
        try:
            save_workflow(content, temp_path)
            
            # Verify file was created and contains correct content
            self.assertTrue(os.path.exists(temp_path))
            with open(temp_path, 'r') as f:
                saved_content = f.read()
            self.assertEqual(saved_content, content)
        finally:
            os.unlink(temp_path)
    
    def test_generate_workflow_invalid_template(self):
        """Test error handling for invalid template."""
        with self.assertRaises(ValueError) as context:
            generate_workflow(template="invalid", output="test.yml")
        
        self.assertIn("Unknown template", str(context.exception))
    
    def test_generate_workflow_with_custom_permissions(self):
        """Test workflow generation with custom permissions."""
        custom_perms = {
            "contents": "write",
            "packages": "write",
            "security-events": "write"
        }
        
        content = generate_workflow(template="ci", output="test.yml", permissions=custom_perms)
        workflow = yaml.safe_load(content)
        
        self.assertIn("permissions", workflow)
        self.assertEqual(workflow["permissions"], custom_perms)
    
    def test_workflow_yaml_formatting(self):
        """Test that generated YAML is properly formatted."""
        content = generate_workflow(template="ci", output="test.yml")
        
        # Verify YAML is valid
        try:
            parsed = yaml.safe_load(content)
            self.assertIsInstance(parsed, dict)
        except yaml.YAMLError as e:
            self.fail(f"Generated YAML is not valid: {e}")
        
        # Verify header comment is present
        self.assertTrue(content.startswith("# Generated by Nightly GitHub Actions Quickstart"))
    
    def test_security_mode_disables_secrets_in_logs(self):
        """Test that security mode includes steps to avoid logging secrets."""
        content = generate_workflow(template="ci", output="test.yml", security=True)
        
        # Verify that no steps contain obvious secret logging patterns
        self.assertNotIn("echo ${{ secrets.", content)
        self.assertNotIn("print(os.environ.get('", content)


if __name__ == "__main__":
    unittest.main()
