#!/usr/bin/env python3
"""
Tests for Ansible Playbook Linter

Uses mock data to test linting functionality without external dependencies.
"""

import unittest
import tempfile
import os
import json
from pathlib import Path
from unittest.mock import patch, mock_open

# Import the linter module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from linter import AnsibleLinter, Severity, Violation


class TestAnsibleLinter(unittest.TestCase):
    
    def setUp(self):
        self.linter = AnsibleLinter()
    
    def test_yaml_validation_valid(self):
        """Test that valid YAML passes validation"""
        valid_yaml = """
- name: Test Playbook
  hosts: localhost
  tasks:
    - name: Test Task
      debug:
        msg: "Hello World"
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(valid_yaml)
            f.flush()
            
            self.linter.lint_file(f.name)
            
        results = self.linter.get_results()
        yaml_violations = [v for v in results['violations'] if v['rule_id'] == 'yaml-valid']
        self.assertEqual(len(yaml_violations), 0, "Valid YAML should not produce yaml-valid violations")
        
        os.unlink(f.name)
    
    def test_yaml_validation_invalid(self):
        """Test that invalid YAML produces violations"""
        invalid_yaml = """
- name: Test Playbook
  hosts: localhost
  tasks:
    - name: Test Task
      debug:
        msg: "Hello World"
      invalid: syntax: here
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(invalid_yaml)
            f.flush()
            
            self.linter.lint_file(f.name)
            
        results = self.linter.get_results()
        yaml_violations = [v for v in results['violations'] if v['rule_id'] == 'yaml-valid']
        self.assertGreater(len(yaml_violations), 0, "Invalid YAML should produce yaml-valid violations")
        
        os.unlink(f.name)
    
    def test_task_name_required(self):
        """Test that tasks without names produce violations"""
        playbook_without_names = """
- name: Test Playbook
  hosts: localhost
  tasks:
    - debug:
        msg: "Task without name"
    - name: Task with name
      debug:
        msg: "This one has a name"
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(playbook_without_names)
            f.flush()
            
            self.linter.lint_file(f.name)
            
        results = self.linter.get_results()
        name_violations = [v for v in results['violations'] if v['rule_id'] == 'task-name-required']
        self.assertEqual(len(name_violations), 1, "Should detect one task without name")
        self.assertEqual(name_violations[0]['severity'], Severity.WARNING.value)
        
        os.unlink(f.name)
    
    def test_hardcoded_secrets_detection(self):
        """Test detection of hardcoded secrets"""
        playbook_with_secrets = """
- name: Test Playbook
  hosts: localhost
  tasks:
    - name: Set password
      set_fact:
        password: "mysecretpassword123"
    - name: Use secret
      debug:
        msg: "{{ secret_key }}"
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(playbook_with_secrets)
            f.flush()
            
            self.linter.lint_file(f.name)
            
        results = self.linter.get_results()
        secret_violations = [v for v in results['violations'] if v['rule_id'] == 'no-hardcoded-secrets']
        self.assertGreater(len(secret_violations), 0, "Should detect hardcoded secrets")
        
        os.unlink(f.name)
    
    def test_sudo_usage_detection(self):
        """Test detection of deprecated sudo usage"""
        playbook_with_sudo = """
- name: Test Playbook
  hosts: localhost
  tasks:
    - name: Use sudo
      command: whoami
      sudo: yes
      sudo_user: root
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(playbook_with_sudo)
            f.flush()
            
            self.linter.lint_file(f.name)
            
        results = self.linter.get_results()
        sudo_violations = [v for v in results['violations'] if v['rule_id'] == 'sudo-usage']
        self.assertGreater(len(sudo_violations), 0, "Should detect sudo usage")
        
        os.unlink(f.name)
    
    def test_file_permissions_check(self):
        """Test detection of non-octal file permissions"""
        playbook_with_bad_permissions = """
- name: Test Playbook
  hosts: localhost
  tasks:
    - name: Create file with bad permissions
      file:
        path: /tmp/test.txt
        mode: "644"
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(playbook_with_bad_permissions)
            f.flush()
            
            self.linter.lint_file(f.name)
            
        results = self.linter.get_results()
        permission_violations = [v for v in results['violations'] if v['rule_id'] == 'file-permissions']
        self.assertGreater(len(permission_violations), 0, "Should detect non-octal file permissions")
        
        os.unlink(f.name)
    
    def test_loop_optimization_check(self):
        """Test detection of deprecated with_items"""
        playbook_with_with_items = """
- name: Test Playbook
  hosts: localhost
  tasks:
    - name: Loop with with_items
      debug:
        msg: "{{ item }}"
      with_items:
        - item1
        - item2
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(playbook_with_with_items)
            f.flush()
            
            self.linter.lint_file(f.name)
            
        results = self.linter.get_results()
        loop_violations = [v for v in results['violations'] if v['rule_id'] == 'loop-optimization']
        self.assertGreater(len(loop_violations), 0, "Should detect deprecated with_items")
        
        os.unlink(f.name)
    
    def test_variable_naming_check(self):
        """Test detection of non-snake_case variable names"""
        playbook_with_bad_vars = """
- name: Test Playbook
  hosts: localhost
  tasks:
    - name: Use camelCase variable
      debug:
        msg: "{{ myVariable }}"
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(playbook_with_bad_vars)
            f.flush()
            
            self.linter.lint_file(f.name)
            
        results = self.linter.get_results()
        var_violations = [v for v in results['violations'] if v['rule_id'] == 'variable-naming']
        self.assertGreater(len(var_violations), 0, "Should detect non-snake_case variable names")
        
        os.unlink(f.name)
    
    def test_config_loading(self):
        """Test configuration loading and rule enabling/disabling"""
        config_content = """
rules:
  enabled:
    - yaml-valid
    - task-name-required
  disabled:
    - no-hardcoded-secrets
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as config_file:
            config_file.write(config_content)
            config_file.flush()
            
            linter = AnsibleLinter(config_file.name)
            
            # Test that hardcoded secrets rule is disabled
            playbook_with_secrets = """
- name: Test Playbook
  hosts: localhost
  tasks:
    - name: Set password
      set_fact:
        password: "mysecretpassword123"
"""
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as playbook_file:
                playbook_file.write(playbook_with_secrets)
                playbook_file.flush()
                
                linter.lint_file(playbook_file.name)
                
            results = linter.get_results()
            secret_violations = [v for v in results['violations'] if v['rule_id'] == 'no-hardcoded-secrets']
            self.assertEqual(len(secret_violations), 0, "Hardcoded secrets rule should be disabled")
            
            os.unlink(playbook_file.name)
        
        os.unlink(config_file.name)
    
    def test_exclude_patterns(self):
        """Test file exclusion patterns"""
        config_content = """
exclude:
  - vendor/
  - tests/fixtures/
  - *.retry
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as config_file:
            config_file.write(config_content)
            config_file.flush()
            
            linter = AnsibleLinter(config_file.name)
            
            # Test that vendor files are excluded
            vendor_file = "vendor/ansible-role/example.yml"
            os.makedirs(os.path.dirname(vendor_file), exist_ok=True)
            
            playbook_content = """
- name: Test Playbook
  hosts: localhost
  tasks:
    - debug:
        msg: "This should be excluded"
"""
            
            with open(vendor_file, 'w') as f:
                f.write(playbook_content)
                
            linter.lint_file(vendor_file)
            
            results = linter.get_results()
            self.assertEqual(results['summary']['files_processed'], 0, "Vendor files should be excluded")
            
            # Clean up
            os.unlink(vendor_file)
            os.rmdir(os.path.dirname(vendor_file))
            os.rmdir(os.path.dirname(os.path.dirname(vendor_file)))
        
        os.unlink(config_file.name)
    
    def test_multiple_files(self):
        """Test linting multiple files"""
        file1_content = """
- name: First Playbook
  hosts: localhost
  tasks:
    - debug:
        msg: "Hello from file 1"
"""
        
        file2_content = """
- name: Second Playbook
  hosts: localhost
  tasks:
    - name: Task with name
      debug:
        msg: "Hello from file 2"
"""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file1_path = os.path.join(temp_dir, "playbook1.yml")
            file2_path = os.path.join(temp_dir, "playbook2.yml")
            
            with open(file1_path, 'w') as f1, open(file2_path, 'w') as f2:
                f1.write(file1_content)
                f2.write(file2_content)
            
            self.linter.lint_file(file1_path)
            self.linter.lint_file(file2_path)
            
            results = self.linter.get_results()
            self.assertEqual(results['summary']['files_processed'], 2, "Should process both files")
            
            # File 1 should have a task-name-required violation
            name_violations = [v for v in results['violations'] if v['rule_id'] == 'task-name-required']
            self.assertEqual(len(name_violations), 1, "Should detect one task without name in file 1")
    
    def test_gather_facts_check(self):
        """Test gather_facts usage check"""
        playbook_with_gather_facts_false = """
- name: Test Playbook
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Simple task
      debug:
        msg: "Hello World"
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(playbook_with_gather_facts_false)
            f.flush()
            
            self.linter.lint_file(f.name)
            
        results = self.linter.get_results()
        gather_facts_violations = [v for v in results['violations'] if v['rule_id'] == 'gather-facts']
        self.assertGreater(len(gather_facts_violations), 0, "Should detect gather_facts: false")
        
        os.unlink(f.name)


if __name__ == '__main__':
    unittest.main()
