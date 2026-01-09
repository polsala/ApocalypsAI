#!/usr/bin/env python3
"""
Tests for Ansible Playbook Linter Reporter

Uses mock data to test report generation functionality.
"""

import unittest
import tempfile
import json
from pathlib import Path

# Import the reporter module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from reporter import Reporter


class TestReporter(unittest.TestCase):
    
    def setUp(self):
        # Create mock results data
        self.mock_results = {
            "summary": {
                "files_processed": 2,
                "violations_found": 4,
                "errors": 1,
                "warnings": 2,
                "info": 1
            },
            "violations": [
                {
                    "rule_id": "yaml-valid",
                    "severity": "error",
                    "message": "Invalid YAML syntax",
                    "file_path": "playbook1.yml",
                    "line": 5,
                    "suggestion": "Fix the YAML syntax"
                },
                {
                    "rule_id": "task-name-required",
                    "severity": "warning",
                    "message": "Task is missing a name",
                    "file_path": "playbook1.yml",
                    "line": 10,
                    "suggestion": "Add a descriptive name to this task"
                },
                {
                    "rule_id": "sudo-usage",
                    "severity": "warning",
                    "message": "Use of deprecated 'sudo' parameter",
                    "file_path": "playbook2.yml",
                    "line": 3,
                    "suggestion": "Use 'become' instead"
                },
                {
                    "rule_id": "loop-optimization",
                    "severity": "info",
                    "message": "Consider using 'loop' instead of 'with_items'",
                    "file_path": "playbook2.yml",
                    "line": 7,
                    "suggestion": "Replace 'with_items' with 'loop'"
                }
            ]
        }
    
    def test_load_results(self):
        """Test loading results from JSON file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.mock_results, f)
            f.flush()
            
            reporter = Reporter(f.name)
            
            self.assertEqual(reporter.results, self.mock_results)
            
        # Clean up
        import os
        os.unlink(f.name)
    
    def test_generate_summary(self):
        """Test summary report generation"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.mock_results, f)
            f.flush()
            
            reporter = Reporter(f.name)
            summary = reporter.generate_summary()
            
            self.assertIn("Ansible Playbook Linting Summary", summary)
            self.assertIn("Files processed: 2", summary)
            self.assertIn("Total violations: 4", summary)
            self.assertIn("Errors: 1", summary)
            self.assertIn("Warnings: 2", summary)
            self.assertIn("Info: 1", summary)
            
        # Clean up
        import os
        os.unlink(f.name)
    
    def test_generate_detailed_report(self):
        """Test detailed report generation"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.mock_results, f)
            f.flush()
            
            reporter = Reporter(f.name)
            detailed = reporter.generate_detailed_report()
            
            self.assertIn("Detailed Ansible Playbook Linting Report", detailed)
            self.assertIn("playbook1.yml", detailed)
            self.assertIn("playbook2.yml", detailed)
            self.assertIn("yaml-valid", detailed)
            self.assertIn("task-name-required", detailed)
            
        # Clean up
        import os
        os.unlink(f.name)
    
    def test_generate_security_report(self):
        """Test security report generation"""
        # Create results with security violations
        security_results = {
            "summary": {
                "files_processed": 1,
                "violations_found": 2,
                "errors": 2,
                "warnings": 0,
                "info": 0
            },
            "violations": [
                {
                    "rule_id": "no-hardcoded-secrets",
                    "severity": "error",
                    "message": "Potential hardcoded secret detected",
                    "file_path": "playbook.yml",
                    "line": 5,
                    "suggestion": "Use Ansible vault for secrets"
                },
                {
                    "rule_id": "sudo-usage",
                    "severity": "error",
                    "message": "Use of deprecated 'sudo' parameter",
                    "file_path": "playbook.yml",
                    "line": 3,
                    "suggestion": "Use 'become' instead"
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(security_results, f)
            f.flush()
            
            reporter = Reporter(f.name)
            security_report = reporter.generate_security_report()
            
            self.assertIn("Security Issues Report", security_report)
            self.assertIn("Security violations found: 2", security_report)
            self.assertIn("no-hardcoded-secrets", security_report)
            self.assertIn("sudo-usage", security_report)
            
        # Clean up
        import os
        os.unlink(f.name)
    
    def test_security_report_no_issues(self):
        """Test security report when no security issues exist"""
        no_security_results = {
            "summary": {
                "files_processed": 1,
                "violations_found": 1,
                "errors": 0,
                "warnings": 1,
                "info": 0
            },
            "violations": [
                {
                    "rule_id": "task-name-required",
                    "severity": "warning",
                    "message": "Task is missing a name",
                    "file_path": "playbook.yml",
                    "line": 5,
                    "suggestion": "Add a descriptive name"
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(no_security_results, f)
            f.flush()
            
            reporter = Reporter(f.name)
            security_report = reporter.generate_security_report()
            
            self.assertIn("No security issues found! 🛡️", security_report)
            
        # Clean up
        import os
        os.unlink(f.name)
    
    def test_save_report(self):
        """Test saving reports to files"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as results_file:
            json.dump(self.mock_results, results_file)
            results_file.flush()
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as output_file:
                reporter = Reporter(results_file.name)
                reporter.save_report(output_file.name, "summary")
                
                # Read the saved report
                with open(output_file.name, 'r') as saved:
                    content = saved.read()
                    self.assertIn("Ansible Playbook Linting Summary", content)
                    
        # Clean up
        import os
        os.unlink(results_file.name)
        os.unlink(output_file.name)
    
    def test_invalid_report_type(self):
        """Test error handling for invalid report types"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.mock_results, f)
            f.flush()
            
            reporter = Reporter(f.name)
            
            with self.assertRaises(ValueError):
                reporter.save_report("output.md", "invalid_type")
            
        # Clean up
        import os
        os.unlink(f.name)


if __name__ == '__main__':
    unittest.main()
