#!/usr/bin/env python3
"""
Integration tests for Ansible Playbook Linter

Tests the complete workflow from file linting to report generation.
"""

import unittest
import tempfile
import os
import json
import subprocess
from pathlib import Path


class TestIntegration(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.linter_script = Path(__file__).parent.parent / "src" / "linter.py"
        self.reporter_script = Path(__file__).parent.parent / "src" / "reporter.py"
    
    def tearDown(self):
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_playbook(self, content: str, filename: str = "test_playbook.yml") -> str:
        """Create a test playbook file"""
        file_path = os.path.join(self.temp_dir, filename)
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path
    
    def test_basic_linting_workflow(self):
        """Test the complete linting workflow"""
        # Create a playbook with various issues
        playbook_content = """
- name: Test Playbook
  hosts: localhost
  gather_facts: false
  tasks:
    - debug:
        msg: "Task without name"
    - name: Task with name
      command: whoami
      sudo: yes
      sudo_user: root
    - name: Set password
      set_fact:
        password: "mysecretpassword123"
    - name: Create file with bad permissions
      file:
        path: /tmp/test.txt
        mode: "644"
    - name: Loop with with_items
      debug:
        msg: "{{ item }}"
      with_items:
        - item1
        - item2
    - name: Use camelCase variable
      debug:
        msg: "{{ myVariable }}"
"""
        
        playbook_path = self.create_test_playbook(playbook_content)
        
        # Run the linter
        result = subprocess.run([
            'python3', str(self.linter_script), 
            '--report', os.path.join(self.temp_dir, 'results.json'),
            '--format', 'json',
            playbook_path
        ], capture_output=True, text=True, cwd=self.temp_dir)
        
        self.assertEqual(result.returncode, 1, "Linter should return non-zero exit code for violations")
        
        # Check that results file was created
        results_file = os.path.join(self.temp_dir, 'results.json')
        self.assertTrue(os.path.exists(results_file), "Results file should be created")
        
        # Load and verify results
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        self.assertEqual(results['summary']['files_processed'], 1)
        self.assertGreater(results['summary']['violations_found'], 0)
        
        # Verify specific violations are detected
        violations = results['violations']
        violation_rules = [v['rule_id'] for v in violations]
        
        self.assertIn('task-name-required', violation_rules)
        self.assertIn('sudo-usage', violation_rules)
        self.assertIn('no-hardcoded-secrets', violation_rules)
        self.assertIn('file-permissions', violation_rules)
        self.assertIn('loop-optimization', violation_rules)
        self.assertIn('variable-naming', violation_rules)
    
    def test_directory_linting(self):
        """Test linting an entire directory"""
        # Create multiple playbook files
        playbook1_content = """
- name: First Playbook
  hosts: localhost
  tasks:
    - debug:
        msg: "Task without name"
"""
        
        playbook2_content = """
- name: Second Playbook
  hosts: localhost
  tasks:
    - name: Task with name
      debug:
        msg: "Hello World"
"""
        
        playbook1_path = self.create_test_playbook(playbook1_content, "playbook1.yml")
        playbook2_path = self.create_test_playbook(playbook2_content, "playbook2.yml")
        
        # Run the linter on the directory
        result = subprocess.run([
            'python3', str(self.linter_script),
            '--report', os.path.join(self.temp_dir, 'results.json'),
            '--format', 'json',
            self.temp_dir
        ], capture_output=True, text=True, cwd=self.temp_dir)
        
        self.assertEqual(result.returncode, 1, "Linter should return non-zero exit code for violations")
        
        # Check results
        results_file = os.path.join(self.temp_dir, 'results.json')
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        self.assertEqual(results['summary']['files_processed'], 2)
        self.assertGreater(results['summary']['violations_found'], 0)
    
    def test_report_generation(self):
        """Test report generation from results"""
        # First run the linter to generate results
        playbook_content = """
- name: Test Playbook
  hosts: localhost
  tasks:
    - debug:
        msg: "Task without name"
"""
        
        playbook_path = self.create_test_playbook(playbook_content)
        
        # Run linter
        subprocess.run([
            'python3', str(self.linter_script),
            '--report', os.path.join(self.temp_dir, 'results.json'),
            '--format', 'json',
            playbook_path
        ], capture_output=True, text=True, cwd=self.temp_dir)
        
        # Generate reports
        summary_report = os.path.join(self.temp_dir, 'summary.md')
        detailed_report = os.path.join(self.temp_dir, 'detailed.md')
        security_report = os.path.join(self.temp_dir, 'security.md')
        
        # Generate summary report
        result = subprocess.run([
            'python3', str(self.reporter_script),
            os.path.join(self.temp_dir, 'results.json'),
            '--output', summary_report,
            '--type', 'summary'
        ], capture_output=True, text=True, cwd=self.temp_dir)
        
        self.assertEqual(result.returncode, 0, "Reporter should succeed")
        self.assertTrue(os.path.exists(summary_report), "Summary report should be created")
        
        # Generate detailed report
        result = subprocess.run([
            'python3', str(self.reporter_script),
            os.path.join(self.temp_dir, 'results.json'),
            '--output', detailed_report,
            '--type', 'detailed'
        ], capture_output=True, text=True, cwd=self.temp_dir)
        
        self.assertEqual(result.returncode, 0, "Reporter should succeed")
        self.assertTrue(os.path.exists(detailed_report), "Detailed report should be created")
        
        # Generate security report
        result = subprocess.run([
            'python3', str(self.reporter_script),
            os.path.join(self.temp_dir, 'results.json'),
            '--output', security_report,
            '--type', 'security'
        ], capture_output=True, text=True, cwd=self.temp_dir)
        
        self.assertEqual(result.returncode, 0, "Reporter should succeed")
        self.assertTrue(os.path.exists(security_report), "Security report should be created")
        
        # Verify report contents
        with open(summary_report, 'r') as f:
            summary_content = f.read()
            self.assertIn("Ansible Playbook Linting Summary", summary_content)
            self.assertIn("Files processed: 1", summary_content)
        
        with open(detailed_report, 'r') as f:
            detailed_content = f.read()
            self.assertIn("Detailed Ansible Playbook Linting Report", detailed_content)
            self.assertIn("task-name-required", detailed_content)
        
        with open(security_report, 'r') as f:
            security_content = f.read()
            self.assertIn("No security issues found! 🛡️", security_content)
    
    def test_configuration_file(self):
        """Test configuration file loading"""
        # Create a configuration file
        config_content = """
rules:
  enabled:
    - yaml-valid
    - task-name-required
  disabled:
    - no-hardcoded-secrets
exclude:
  - vendor/
  - tests/fixtures/
"""
        
        config_path = os.path.join(self.temp_dir, '.ansible-lint.yml')
        with open(config_path, 'w') as f:
            f.write(config_content)
        
        # Create a playbook with hardcoded secrets (should be ignored)
        playbook_content = """
- name: Test Playbook
  hosts: localhost
  tasks:
    - name: Set password
      set_fact:
        password: "mysecretpassword123"
"""
        
        playbook_path = self.create_test_playbook(playbook_content)
        
        # Run the linter with config
        result = subprocess.run([
            'python3', str(self.linter_script),
            '--config', config_path,
            '--report', os.path.join(self.temp_dir, 'results.json'),
            '--format', 'json',
            playbook_path
        ], capture_output=True, text=True, cwd=self.temp_dir)
        
        self.assertEqual(result.returncode, 0, "Linter should succeed when hardcoded secrets rule is disabled")
        
        # Check results
        results_file = os.path.join(self.temp_dir, 'results.json')
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        # Should have no violations since only hardcoded secrets rule would trigger
        # and it's disabled
        self.assertEqual(results['summary']['violations_found'], 0)
    
    def test_recursive_directory_linting(self):
        """Test recursive directory linting"""
        # Create subdirectories
        sub_dir = os.path.join(self.temp_dir, 'subdir')
        os.makedirs(sub_dir)
        
        # Create playbooks in different directories
        main_playbook = """
- name: Main Playbook
  hosts: localhost
  tasks:
    - debug:
        msg: "Main task"
"""
        
        sub_playbook = """
- name: Sub Playbook
  hosts: localhost
  tasks:
    - debug:
        msg: "Sub task"
"""
        
        main_path = self.create_test_playbook(main_playbook, "main.yml")
        sub_path = self.create_test_playbook(sub_playbook, "subdir/sub.yml")
        
        # Run linter with recursive flag
        result = subprocess.run([
            'python3', str(self.linter_script),
            '--recursive',
            '--report', os.path.join(self.temp_dir, 'results.json'),
            '--format', 'json',
            self.temp_dir
        ], capture_output=True, text=True, cwd=self.temp_dir)
        
        self.assertEqual(result.returncode, 0, "Linter should succeed")
        
        # Check results
        results_file = os.path.join(self.temp_dir, 'results.json')
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        self.assertEqual(results['summary']['files_processed'], 2)
    
    def test_invalid_yaml_handling(self):
        """Test handling of invalid YAML files"""
        # Create a file with invalid YAML
        invalid_yaml = """
- name: Test Playbook
  hosts: localhost
  tasks:
    - name: Test Task
      debug:
        msg: "Hello World"
      invalid: syntax: here
"""
        
        playbook_path = self.create_test_playbook(invalid_yaml, "invalid.yml")
        
        # Run the linter
        result = subprocess.run([
            'python3', str(self.linter_script),
            '--report', os.path.join(self.temp_dir, 'results.json'),
            '--format', 'json',
            playbook_path
        ], capture_output=True, text=True, cwd=self.temp_dir)
        
        self.assertEqual(result.returncode, 1, "Linter should return non-zero exit code for invalid YAML")
        
        # Check results
        results_file = os.path.join(self.temp_dir, 'results.json')
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        # Should have YAML validation violations
        yaml_violations = [v for v in results['violations'] if v['rule_id'] == 'yaml-valid']
        self.assertGreater(len(yaml_violations), 0, "Should detect YAML validation errors")


if __name__ == '__main__':
    unittest.main()
