import unittest
import tempfile
import os
from pathlib import Path
from src.validator import PlaybookValidator


class TestPlaybookValidator(unittest.TestCase):
    """Test cases for PlaybookValidator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = PlaybookValidator()
        
    def create_temp_playbook(self, content: str) -> str:
        """Create a temporary playbook file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(content)
            return f.name
    
    def tearDown(self):
        """Clean up temporary files."""
        # Clean up any temporary files
        pass
    
    def test_load_valid_playbook(self):
        """Test loading a valid playbook."""
        content = """
- name: Test Play
  hosts: localhost
  tasks:
    - name: Test Task
      debug:
        msg: "Hello World"
"""
        
        file_path = self.create_temp_playbook(content)
        try:
            result = self.validator.load_playbook(file_path)
            self.assertTrue(result)
            self.assertIsNotNone(self.validator.playbook_data)
            self.assertEqual(len(self.validator.playbook_data), 1)
        finally:
            os.unlink(file_path)
    
    def test_load_invalid_yaml(self):
        """Test loading an invalid YAML file."""
        content = """
- name: Test Play
  hosts: localhost
  tasks:
    - name: Test Task
      debug:
        msg: "Hello World"
      invalid: syntax: here
"""
        
        file_path = self.create_temp_playbook(content)
        try:
            result = self.validator.load_playbook(file_path)
            self.assertFalse(result)
            self.assertTrue(len(self.validator.syntax_errors) > 0)
        finally:
            os.unlink(file_path)
    
    def test_load_non_list_playbook(self):
        """Test loading a playbook that's not a list."""
        content = """
name: Test Play
hosts: localhost
tasks:
  - name: Test Task
    debug:
      msg: "Hello World"
"""
        
        file_path = self.create_temp_playbook(content)
        try:
            result = self.validator.load_playbook(file_path)
            self.assertFalse(result)
            self.assertTrue(any("list of plays" in error for error in self.validator.syntax_errors))
        finally:
            os.unlink(file_path)
    
    def test_validate_syntax_valid(self):
        """Test syntax validation with valid playbook."""
        content = """
- name: Test Play
  hosts: localhost
  tasks:
    - name: Test Task
      debug:
        msg: "Hello World"
"""
        
        file_path = self.create_temp_playbook(content)
        try:
            self.validator.load_playbook(file_path)
            result = self.validator.validate_syntax()
            self.assertTrue(result['valid'])
            self.assertEqual(len(result['errors']), 0)
        finally:
            os.unlink(file_path)
    
    def test_validate_syntax_missing_tasks(self):
        """Test syntax validation with missing tasks."""
        content = """
- name: Test Play
  hosts: localhost
"""
        
        file_path = self.create_temp_playbook(content)
        try:
            self.validator.load_playbook(file_path)
            result = self.validator.validate_syntax()
            self.assertFalse(result['valid'])
            self.assertTrue(any("tasks" in error for error in result['errors']))
        finally:
            os.unlink(file_path)
    
    def test_validate_syntax_missing_task_name(self):
        """Test syntax validation with missing task name."""
        content = """
- name: Test Play
  hosts: localhost
  tasks:
    - debug:
        msg: "Hello World"
"""
        
        file_path = self.create_temp_playbook(content)
        try:
            self.validator.load_playbook(file_path)
            result = self.validator.validate_syntax()
            self.assertFalse(result['valid'])
            self.assertTrue(any("task name" in error for error in result['errors']))
        finally:
            os.unlink(file_path)
    
    def test_check_idempotency(self):
        """Test idempotency checking."""
        content = """
- name: Test Play
  hosts: localhost
  tasks:
    - name: File task
      file:
        path: /tmp/test
        state: touch
    - name: Shell task
      shell: echo "test"
    - name: Copy task
      copy:
        src: /tmp/source
        dest: /tmp/dest
"""
        
        file_path = self.create_temp_playbook(content)
        try:
            self.validator.load_playbook(file_path)
            result = self.validator.check_idempotency()
            
            self.assertEqual(result['total_tasks'], 3)
            self.assertGreater(result['score'], 0)
            self.assertLess(result['score'], 100)
            
            # Should have issues for non-idempotent shell task
            self.assertTrue(len(result['issues']) > 0)
            self.assertTrue(any('shell' in issue for issue in result['issues']))
        finally:
            os.unlink(file_path)
    
    def test_check_security_no_issues(self):
        """Test security checking with no issues."""
        content = """
- name: Test Play
  hosts: localhost
  tasks:
    - name: File task
      file:
        path: /tmp/test
        state: touch
        mode: '0644'
"""
        
        file_path = self.create_temp_playbook(content)
        try:
            self.validator.load_playbook(file_path)
            result = self.validator.check_security()
            
            self.assertEqual(result['score'], 100)
            self.assertEqual(len(result['issues']), 0)
        finally:
            os.unlink(file_path)
    
    def test_check_security_password_issue(self):
        """Test security checking with password issue."""
        content = """
- name: Test Play
  hosts: localhost
  tasks:
    - name: Task with password
      debug:
        msg: "password: secret123"
"""
        
        file_path = self.create_temp_playbook(content)
        try:
            self.validator.load_playbook(file_path)
            result = self.validator.check_security()
            
            self.assertLess(result['score'], 100)
            self.assertTrue(len(result['issues']) > 0)
            self.assertTrue(any('password' in issue for issue in result['issues']))
        finally:
            os.unlink(file_path)
    
    def test_check_best_practices(self):
        """Test best practices checking."""
        content = """
- name: Test Play
  hosts: localhost
  tasks:
    - name: Task with good name
      debug:
        msg: "Hello World"
    - name: Task with _result suffix
      shell: echo "test"
      register: task_result
"""
        
        file_path = self.create_temp_playbook(content)
        try:
            self.validator.load_playbook(file_path)
            result = self.validator.check_best_practices()
            
            self.assertLess(result['score'], 100)
            self.assertTrue(len(result['issues']) > 0)
            self.assertTrue(any('_result' in issue for issue in result['issues']))
        finally:
            os.unlink(file_path)
    
    def test_generate_report(self):
        """Test report generation."""
        content = """
- name: Test Play
  hosts: localhost
  tasks:
    - name: Test Task
      debug:
        msg: "Hello World"
"""
        
        file_path = self.create_temp_playbook(content)
        try:
            self.validator.load_playbook(file_path)
            report = self.validator.generate_report(file_path, detailed=True)
            
            self.assertIn("Validation Report", report)
            self.assertIn("Syntax Check: ✓ PASS", report)
            self.assertIn("Idempotency Score:", report)
            self.assertIn("Security Score:", report)
            self.assertIn("Best Practices Score:", report)
            self.assertIn("Overall Score:", report)
            self.assertIn("Detailed Analysis:", report)
        finally:
            os.unlink(file_path)


if __name__ == '__main__':
    unittest.main()
