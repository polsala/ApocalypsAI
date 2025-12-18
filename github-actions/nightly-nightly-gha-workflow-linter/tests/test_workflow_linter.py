import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from workflow_linter import WorkflowLinter


class TestWorkflowLinter(unittest.TestCase):
    """Test cases for WorkflowLinter."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.workflows_dir = Path(self.temp_dir) / ".github" / "workflows"
        self.workflows_dir.mkdir(parents=True)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def create_workflow_file(self, name: str, content: str) -> Path:
        """Helper to create a workflow file."""
        file_path = self.workflows_dir / name
        with open(file_path, "w") as f:
            f.write(content)
        return file_path

    def test_empty_workflows_directory(self):
        """Test behavior when workflows directory exists but is empty."""
        linter = WorkflowLinter(str(self.workflows_dir))
        result = linter.lint_all()
        self.assertTrue(result)  # Should not fail
        self.assertEqual(len(linter.errors), 0)
        self.assertEqual(len(linter.warnings), 1)
        self.assertIn("No workflow files found", linter.warnings[0][1])

    def test_invalid_yaml_syntax(self):
        """Test detection of invalid YAML syntax."""
        self.create_workflow_file(
            "invalid.yml",
            "name: Test Workflow\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Test\n        run: echo hello\n        # This comment breaks YAML\n        # Missing quote: \"\n",
        )
        
        linter = WorkflowLinter(str(self.workflows_dir))
        result = linter.lint_all()
        self.assertFalse(result)
        self.assertEqual(len(linter.errors), 1)
        self.assertIn("Invalid YAML syntax", linter.errors[0][1])

    def test_missing_name_field(self):
        """Test detection of missing name field."""
        self.create_workflow_file(
            "missing_name.yml",
            "on: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo hello\n",
        )
        
        linter = WorkflowLinter(str(self.workflows_dir))
        result = linter.lint_all()
        self.assertTrue(result)  # Warning only
        self.assertEqual(len(linter.warnings), 1)
        self.assertIn("Missing 'name' field", linter.warnings[0][1])

    def test_missing_on_field(self):
        """Test detection of missing on field."""
        self.create_workflow_file(
            "missing_on.yml",
            "name: Test Workflow\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo hello\n",
        )
        
        linter = WorkflowLinter(str(self.workflows_dir))
        result = linter.lint_all()
        self.assertFalse(result)
        self.assertEqual(len(linter.errors), 1)
        self.assertIn("Missing 'on' field", linter.errors[0][1])

    def test_missing_job_runs_on(self):
        """Test detection of job missing runs-on."""
        self.create_workflow_file(
            "missing_runs_on.yml",
            "name: Test Workflow\non: [push]\njobs:\n  test:\n    steps:\n      - run: echo hello\n",
        )
        
        linter = WorkflowLinter(str(self.workflows_dir))
        result = linter.lint_all()
        self.assertFalse(result)
        self.assertEqual(len(linter.errors), 1)
        self.assertIn("Job 'test' missing 'runs-on'", linter.errors[0][1])

    def test_missing_step_name(self):
        """Test detection of step missing name."""
        self.create_workflow_file(
            "missing_step_name.yml",
            "name: Test Workflow\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo hello\n",
        )
        
        linter = WorkflowLinter(str(self.workflows_dir))
        result = linter.lint_all()
        self.assertTrue(result)  # Warning only
        self.assertEqual(len(linter.warnings), 1)
        self.assertIn("Missing step name", linter.warnings[0][1])

    def test_curl_without_fail_flag(self):
        """Test detection of curl without --fail flag."""
        self.create_workflow_file(
            "curl_without_fail.yml",
            "name: Test Workflow\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Download file\n        run: curl -O https://example.com/file.txt\n",
        )
        
        linter = WorkflowLinter(str(self.workflows_dir))
        result = linter.lint_all()
        self.assertTrue(result)  # Warning only
        self.assertEqual(len(linter.warnings), 1)
        self.assertIn("curl without --fail flag", linter.warnings[0][1])

    def test_curl_with_fail_flag_ok(self):
        """Test that curl with --fail flag is not flagged."""
        self.create_workflow_file(
            "curl_with_fail.yml",
            "name: Test Workflow\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Download file\n        run: curl --fail -O https://example.com/file.txt\n",
        )
        
        linter = WorkflowLinter(str(self.workflows_dir))
        result = linter.lint_all()
        self.assertTrue(result)
        self.assertEqual(len(linter.warnings), 0)
        self.assertEqual(len(linter.errors), 0)

    def test_checkout_without_token_warning(self):
        """Test detection of checkout without explicit token."""
        self.create_workflow_file(
            "checkout_no_token.yml",
            "name: Test Workflow\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n",
        )
        
        linter = WorkflowLinter(str(self.workflows_dir))
        result = linter.lint_all()
        self.assertTrue(result)  # Warning only
        self.assertEqual(len(linter.warnings), 1)
        self.assertIn("checkout without explicit token", linter.warnings[0][1])

    def test_checkout_with_token_ok(self):
        """Test that checkout with token is not flagged."""
        self.create_workflow_file(
            "checkout_with_token.yml",
            "name: Test Workflow\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n        with:\n          token: ${{ secrets.GITHUB_TOKEN }}\n",
        )
        
        linter = WorkflowLinter(str(self.workflows_dir))
        result = linter.lint_all()
        self.assertTrue(result)
        self.assertEqual(len(linter.warnings), 0)
        self.assertEqual(len(linter.errors), 0)

    def test_sudo_without_comment_warning(self):
        """Test detection of sudo without justification comment."""
        self.create_workflow_file(
            "sudo_no_comment.yml",
            "name: Test Workflow\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Install packages\n        run: sudo apt-get update\n",
        )
        
        linter = WorkflowLinter(str(self.workflows_dir))
        result = linter.lint_all()
        self.assertTrue(result)  # Warning only
        self.assertEqual(len(linter.warnings), 1)
        self.assertIn("sudo usage without justification comment", linter.warnings[0][1])

    def test_sudo_with_comment_ok(self):
        """Test that sudo with justification comment is not flagged."""
        self.create_workflow_file(
            "sudo_with_comment.yml",
            "name: Test Workflow\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Install packages\n        run: sudo apt-get update\n        # safe: sudo required for package installation\n",
        )
        
        linter = WorkflowLinter(str(self.workflows_dir))
        result = linter.lint_all()
        self.assertTrue(result)
        self.assertEqual(len(linter.warnings), 0)
        self.assertEqual(len(linter.errors), 0)

    def test_eval_warning(self):
        """Test detection of potential unsafe eval usage."""
        self.create_workflow_file(
            "eval_usage.yml",
            "name: Test Workflow\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Run eval\n        run: eval \"echo hello\"\n",
        )
        
        linter = WorkflowLinter(str(self.workflows_dir))
        result = linter.lint_all()
        self.assertTrue(result)  # Warning only
        self.assertEqual(len(linter.warnings), 1)
        self.assertIn("Potential unsafe eval/exec usage", linter.warnings[0][1])

    def test_valid_workflow_no_issues(self):
        """Test a valid workflow with no issues."""
        self.create_workflow_file(
            "valid_workflow.yml",
            "name: Test Workflow\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Checkout\n        uses: actions/checkout@v4\n        with:\n          token: ${{ secrets.GITHUB_TOKEN }}\n      - name: Run tests\n        run: echo \"All tests passed!\"\n",
        )
        
        linter = WorkflowLinter(str(self.workflows_dir))
        result = linter.lint_all()
        self.assertTrue(result)
        self.assertEqual(len(linter.warnings), 0)
        self.assertEqual(len(linter.errors), 0)

    def test_empty_workflow_file(self):
        """Test handling of empty workflow file."""
        self.create_workflow_file("empty.yml", "")
        
        linter = WorkflowLinter(str(self.workflows_dir))
        result = linter.lint_all()
        self.assertFalse(result)
        self.assertEqual(len(linter.errors), 1)
        self.assertIn("Empty workflow file", linter.errors[0][1])

    def test_nonexistent_workflows_directory(self):
        """Test behavior when workflows directory doesn't exist."""
        linter = WorkflowLinter("/nonexistent/path")
        result = linter.lint_all()
        self.assertFalse(result)
        self.assertEqual(len(linter.errors), 0)  # Directory check happens before file processing


if __name__ == "__main__":
    unittest.main()
