import unittest
import tempfile
import os
from pathlib import Path
from src.validator import PlaybookValidator, ValidationResult


class TestPlaybookValidator(unittest.TestCase):
    """Test cases for PlaybookValidator."""
    
    def setUp(self):
        self.validator = PlaybookValidator()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        # Clean up temp files
        for file in Path(self.temp_dir).glob('*'):
            file.unlink()
        os.rmdir(self.temp_dir)
    
    def create_test_playbook(self, content: str) -> str:
        """Create a temporary playbook file."""
        playbook_path = os.path.join(self.temp_dir, 'test_playbook.yml')
        with open(playbook_path, 'w') as f:
            f.write(content)
        return playbook_path
    
    def test_valid_playbook(self):
        """Test validation of a valid playbook."""
        content = '''
- name: Test Play
  hosts: localhost
  tasks:
    - name: Create file
      file:
        path: /tmp/test
        state: touch
        mode: '0644'
'''
        
        playbook_path = self.create_test_playbook(content)
        result = self.validator.validate_syntax(playbook_path)
        
        self.assertTrue(result.syntax_valid)
        self.assertEqual(len(result.issues), 0)
        self.assertEqual(result.total_tasks, 1)
    
    def test_invalid_yaml(self):
        """Test validation of invalid YAML."""
        content = '''
- name: Test Play
  hosts: localhost
  tasks:
    - name: Create file
      file:
        path: /tmp/test
        state: touch
        mode: '0644'
      invalid: syntax
'''
        
        playbook_path = self.create_test_playbook(content)
        result = self.validator.validate_syntax(playbook_path)
        
        self.assertFalse(result.syntax_valid)
        self.assertGreater(len(result.issues), 0)
    
    def test_dangerous_module_warning(self):
        """Test detection of dangerous modules."""
        content = '''
- name: Test Play
  hosts: localhost
  tasks:
    - name: Run shell command
      shell: echo "hello"
'''
        
        playbook_path = self.create_test_playbook(content)
        result = self.validator.validate_syntax(playbook_path)
        
        self.assertTrue(result.syntax_valid)
        self.assertEqual(result.risky_tasks, 1)
        self.assertGreater(len(result.warnings), 0)
    
    def test_hardcoded_secret_detection(self):
        """Test detection of hardcoded secrets."""
        content = '''
- name: Test Play
  hosts: localhost
  tasks:
    - name: Set password
      set_fact:
        password: "secret123"
'''
        
        playbook_path = self.create_test_playbook(content)
        result = self.validator.validate_syntax(playbook_path)
        
        self.assertFalse(result.syntax_valid)
        self.assertGreater(len(result.issues), 0)
    
    def test_idempotency_check(self):
        """Test idempotency validation."""
        content = '''
- name: Test Play
  hosts: localhost
  tasks:
    - name: Create file
      file:
        path: /tmp/test
        state: touch
        mode: '0644'
'''
        
        playbook_path = self.create_test_playbook(content)
        result = self.validator.check_idempotency(playbook_path)
        
        self.assertTrue(result.idempotent)
        self.assertGreater(len(result.recommendations), 0)
    
    def test_security_audit(self):
        """Test security audit functionality."""
        content = '''
- name: Test Play
  hosts: localhost
  become: true
  tasks:
    - name: Create file
      file:
        path: /tmp/test
        state: touch
        mode: '0644'
    - name: Debug info
      debug:
        msg: "Debug message"
'''
        
        playbook_path = self.create_test_playbook(content)
        result = self.validator.security_audit(playbook_path)
        
        self.assertGreater(len(result.issues), 0)
        self.assertGreater(len(result.recommendations), 0)
    
    def test_json_report_format(self):
        """Test JSON report generation."""
        content = '''
- name: Test Play
  hosts: localhost
  tasks:
    - name: Create file
      file:
        path: /tmp/test
        state: touch
'''
        
        playbook_path = self.create_test_playbook(content)
        result = self.validator.validate_syntax(playbook_path)
        report = self.validator.generate_report(result, 'json')
        
        self.assertIn('playbook', report)
        self.assertIn('syntax_valid', report)
        self.assertIn('security_score', report)
    
    def test_missing_file(self):
        """Test handling of missing file."""
        result = self.validator.validate_syntax('/nonexistent/file.yml')
        
        self.assertFalse(result.syntax_valid)
        self.assertGreater(len(result.issues), 0)
    
    def test_empty_playbook(self):
        """Test validation of empty playbook."""
        content = ''
        playbook_path = self.create_test_playbook(content)
        result = self.validator.validate_syntax(playbook_path)
        
        self.assertFalse(result.syntax_valid)
        self.assertGreater(len(result.issues), 0)


if __name__ == '__main__':
    unittest.main()
