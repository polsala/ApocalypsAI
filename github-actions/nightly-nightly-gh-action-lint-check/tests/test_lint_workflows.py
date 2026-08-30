import unittest
import os
import tempfile
import shutil

# Mock rationale: Importing the actual script to test its functions.
# No external services or complex dependencies are involved, so direct import is safe.
from src.lint_workflows import lint_workflow_file

class TestWorkflowLinting(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def create_test_workflow(self, filename, content):
        """Helper to create a test workflow file."""
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath

    def test_valid_workflow(self):
        """Test a well-formed workflow file."""
        workflow_content = """
name: My Awesome Workflow
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run a command
        run: echo "Hello, world!"
"""
        filepath = self.create_test_workflow("valid_workflow.yml", workflow_content)
        errors = lint_workflow_file(filepath)
        self.assertEqual(errors, [])

    def test_invalid_yaml(self):
        """Test a file with invalid YAML syntax."""
        workflow_content = """
name: Invalid YAML
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run a command
        run: echo "Hello, world!"
  invalid_section:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Another step
        run: echo "Another command"
  this is not valid yaml
"""
        filepath = self.create_test_workflow("invalid_yaml.yml", workflow_content)
        errors = lint_workflow_file(filepath)
        self.assertTrue(any("Invalid YAML syntax" in error for error in errors))

    def test_missing_jobs(self):
        """Test a workflow missing the 'jobs:' section."""
        workflow_content = """
name: Missing Jobs
on: push
"""
        filepath = self.create_test_workflow("missing_jobs.yml", workflow_content)
        errors = lint_workflow_file(filepath)
        self.assertTrue(any("Missing 'jobs:' section" in error for error in errors))

    def test_missing_runs_on(self):
        """Test a workflow missing 'runs-on:' for all jobs."""
        workflow_content = """
name: Missing Runs-On
on: push
jobs:
  build:
    steps:
      - uses: actions/checkout@v3
      - name: Run a command
        run: echo "Hello, world!"
"""
        filepath = self.create_test_workflow("missing_runs_on.yml", workflow_content)
        errors = lint_workflow_file(filepath)
        self.assertTrue(any("No 'runs-on:' defined for any job" in error for error in errors))

    def test_missing_checkout(self):
        """Test a workflow missing 'actions/checkout@'."""
        workflow_content = """
name: Missing Checkout
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Run a command
        run: echo "Hello, world!"
"""
        filepath = self.create_test_workflow("missing_checkout.yml", workflow_content)
        errors = lint_workflow_file(filepath)
        self.assertTrue(any("Consider adding 'actions/checkout@'" in error for error in errors))

    def test_missing_name(self):
        """Test a workflow missing the top-level 'name:'."""
        workflow_content = """
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run a command
        run: echo "Hello, world!"
"""
        filepath = self.create_test_workflow("missing_name.yml", workflow_content)
        errors = lint_workflow_file(filepath)
        self.assertTrue(any("Missing 'name:' at the top level" in error for error in errors))

    def test_missing_on_trigger(self):
        """Test a workflow missing the 'on:' trigger."""
        workflow_content = """
name: Missing Trigger
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run a command
        run: echo "Hello, world!"
"""
        filepath = self.create_test_workflow("missing_on.yml", workflow_content)
        errors = lint_workflow_file(filepath)
        self.assertTrue(any("Missing 'on:' trigger" in error for error in errors))

    def test_file_not_found(self):
        """Test linting a non-existent file."""
        errors = lint_workflow_file(os.path.join(self.test_dir, "non_existent_file.yml"))
        self.assertTrue(any("File not found" in error for error in errors))

if __name__ == '__main__':
    unittest.main()
