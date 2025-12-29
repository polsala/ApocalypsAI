#!/usr/bin/env python3
"""
Ansible Playbook Validator

Validates Ansible playbooks for syntax, idempotency, and security best practices.
"""

import argparse
import os
import sys
import yaml
import re
from typing import Dict, List, Tuple, Any
from pathlib import Path


class PlaybookValidator:
    """Validates Ansible playbooks for various quality metrics."""
    
    def __init__(self):
        self.syntax_errors = []
        self.idempotency_issues = []
        self.security_issues = []
        self.best_practice_issues = []
        self.playbook_data = None
        
    def load_playbook(self, file_path: str) -> bool:
        """Load and parse an Ansible playbook."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Basic YAML syntax check
            self.playbook_data = yaml.safe_load(content)
            if not isinstance(self.playbook_data, list):
                self.syntax_errors.append("Playbook must be a list of plays")
                return False
                
            return True
                
        except yaml.YAMLError as e:
            self.syntax_errors.append(f"YAML syntax error: {e}")
            return False
        except Exception as e:
            self.syntax_errors.append(f"Error reading file: {e}")
            return False
    
    def validate_syntax(self) -> Dict[str, Any]:
        """Validate playbook syntax and structure."""
        if not self.playbook_data:
            return {"valid": False, "errors": ["No playbook data loaded"]}
            
        errors = []
        
        for i, play in enumerate(self.playbook_data):
            if not isinstance(play, dict):
                errors.append(f"Play {i+1}: Must be a dictionary")
                continue
                
            # Check required fields
            if 'tasks' not in play:
                errors.append(f"Play {i+1}: Missing required 'tasks' field")
                
            # Validate tasks
            if 'tasks' in play:
                for j, task in enumerate(play['tasks']):
                    if not isinstance(task, dict):
                        errors.append(f"Play {i+1}, Task {j+1}: Task must be a dictionary")
                        continue
                        
                    if 'name' not in task:
                        errors.append(f"Play {i+1}, Task {j+1}: Missing task name")
                        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def check_idempotency(self) -> Dict[str, Any]:
        """Check idempotency of tasks."""
        if not self.playbook_data:
            return {"score": 0, "issues": []}
            
        total_tasks = 0
        idempotent_tasks = 0
        issues = []
        
        idempotent_modules = {
            'file', 'copy', 'template', 'lineinfile', 'replace',
            'user', 'group', 'package', 'service', 'systemd'
        }
        
        non_idempotent_modules = {
            'shell', 'command', 'raw', 'script'
        }
        
        for i, play in enumerate(self.playbook_data):
            if 'tasks' in play:
                for j, task in enumerate(play['tasks']):
                    if not isinstance(task, dict):
                        continue
                        
                    total_tasks += 1
                    
                    # Check if task uses idempotent module
                    module_name = next((k for k in task.keys() if not k.startswith('_')), None)
                    
                    if module_name in idempotent_modules:
                        idempotent_tasks += 1
                    elif module_name in non_idempotent_modules:
                        issues.append(f"Play {i+1}, Task {j+1}: Uses non-idempotent module '{module_name}'")
                    else:
                        # Unknown module - check for when/if conditions
                        if 'when' in task or 'ignore_errors' in task:
                            issues.append(f"Play {i+1}, Task {j+1}: May not be idempotent (has conditional logic)")
                        else:
                            idempotent_tasks += 0.5  # Partial score for unknown modules
        
        score = (idempotent_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            "score": round(score, 1),
            "total_tasks": total_tasks,
            "idempotent_tasks": idempotent_tasks,
            "issues": issues
        }
    
    def check_security(self) -> Dict[str, Any]:
        """Check security best practices."""
        if not self.playbook_data:
            return {"score": 0, "issues": []}
            
        issues = []
        security_score = 100
        
        for i, play in enumerate(self.playbook_data):
            # Check for become usage
            if play.get('become', False):
                if 'become_user' not in play:
                    issues.append(f"Play {i+1}: Using become without specifying become_user")
                    security_score -= 10
                
            # Check tasks for security issues
            if 'tasks' in play:
                for j, task in enumerate(play['tasks']):
                    if not isinstance(task, dict):
                        continue
                        
                    # Check for plaintext passwords
                    task_str = str(task).lower()
                    if any(word in task_str for word in ['password', 'secret', 'key']):
                        if re.search(r'password:\s*[^$]', task_str) or re.search(r'secret:\s*[^$]', task_str):
                            issues.append(f"Play {i+1}, Task {j+1}: Potential plaintext password detected")
                            security_score -= 15
                            
                    # Check for shell commands with sensitive data
                    if task.get('shell') or task.get('command'):
                        shell_cmd = task.get('shell') or task.get('command')
                        if isinstance(shell_cmd, str) and any(word in shell_cmd.lower() for word in ['password', 'secret', 'key']):
                            issues.append(f"Play {i+1}, Task {j+1}: Shell command may contain sensitive data")
                            security_score -= 10
                            
                    # Check for file permissions
                    if task.get('file'):
                        file_params = task['file']
                        if isinstance(file_params, dict) and 'mode' not in file_params:
                            issues.append(f"Play {i+1}, Task {j+1}: File operation missing explicit mode")
                            security_score -= 5
        
        return {
            "score": max(0, security_score),
            "issues": issues
        }
    
    def check_best_practices(self) -> Dict[str, Any]:
        """Check Ansible best practices."""
        if not self.playbook_data:
            return {"score": 0, "issues": []}
            
        issues = []
        best_practice_score = 100
        
        for i, play in enumerate(self.playbook_data):
            # Check for play name
            if 'name' not in play:
                issues.append(f"Play {i+1}: Missing play name")
                best_practice_score -= 5
                
            # Check for hosts
            if 'hosts' not in play:
                issues.append(f"Play {i+1}: Missing hosts specification")
                best_practice_score -= 10
                
            # Check for gather_facts
            if play.get('gather_facts', True) is False:
                issues.append(f"Play {i+1}: Facts gathering disabled - ensure this is intentional")
                best_practice_score -= 3
                
            # Check tasks for best practices
            if 'tasks' in play:
                for j, task in enumerate(play['tasks']):
                    if not isinstance(task, dict):
                        continue
                        
                    # Check for task name
                    if 'name' not in task:
                        issues.append(f"Play {i+1}, Task {j+1}: Missing task name")
                        best_practice_score -= 5
                        
                    # Check for register usage
                    if 'register' in task and task['register'].endswith('_result'):
                        issues.append(f"Play {i+1}, Task {j+1}: Consider more descriptive variable name than '{task['register']}'")
                        best_practice_score -= 2
                        
                    # Check for when conditions
                    if 'when' in task:
                        when_condition = task['when']
                        if isinstance(when_condition, list) and len(when_condition) > 3:
                            issues.append(f"Play {i+1}, Task {j+1}: Complex when condition - consider simplifying")
                            best_practice_score -= 3
        
        return {
            "score": max(0, best_practice_score),
            "issues": issues
        }
    
    def generate_report(self, file_path: str, detailed: bool = False) -> str:
        """Generate a validation report."""
        report = [f"\n{'='*60}"]
        report.append(f"Ansible Playbook Validation Report")
        report.append(f"File: {file_path}")
        report.append(f"{'='*60}\n")
        
        # Syntax validation
        syntax_result = self.validate_syntax()
        report.append(f"Syntax Check: {'✓ PASS' if syntax_result['valid'] else '✗ FAIL'}")
        if syntax_result['errors']:
            for error in syntax_result['errors']:
                report.append(f"  - {error}")
        report.append("")
        
        # Idempotency check
        idempotency_result = self.check_idempotency()
        report.append(f"Idempotency Score: {idempotency_result['score']}% ({idempotency_result['idempotent_tasks']}/{idempotency_result['total_tasks']} tasks)")
        if idempotency_result['issues']:
            report.append("  Issues:")
            for issue in idempotency_result['issues']:
                report.append(f"    - {issue}")
        report.append("")
        
        # Security check
        security_result = self.check_security()
        report.append(f"Security Score: {security_result['score']}/100")
        if security_result['issues']:
            report.append("  Issues:")
            for issue in security_result['issues']:
                report.append(f"    - {issue}")
        report.append("")
        
        # Best practices check
        best_practice_result = self.check_best_practices()
        report.append(f"Best Practices Score: {best_practice_result['score']}/100")
        if best_practice_result['issues']:
            report.append("  Issues:")
            for issue in best_practice_result['issues']:
                report.append(f"    - {issue}")
        report.append("")
        
        # Overall score
        overall_score = (
            (1 if syntax_result['valid'] else 0) * 25 +
            idempotency_result['score'] * 0.25 +
            security_result['score'] * 0.25 +
            best_practice_result['score'] * 0.25
        )
        report.append(f"Overall Score: {overall_score:.2f}/100")
        
        if detailed:
            report.append("\nDetailed Analysis:")
            report.append("="*40)
            
            # Add detailed breakdown
            report.append("\nSyntax Details:")
            report.append(f"  - Valid structure: {'Yes' if syntax_result['valid'] else 'No'}")
            
            report.append("\nIdempotency Details:")
            report.append(f"  - Total tasks: {idempotency_result['total_tasks']}")
            report.append(f"  - Idempotent tasks: {idempotency_result['idempotent_tasks']}")
            report.append(f"  - Non-idempotent modules used: shell, command, raw, script")
            
            report.append("\nSecurity Details:")
            report.append("  - Password detection: ✓")
            report.append("  - Privilege escalation: Checked")
            report.append("  - File permissions: Checked")
            
            report.append("\nBest Practices Details:")
            report.append("  - Play names: Checked")
            report.append("  - Task names: Checked")
            report.append("  - Variable naming: Checked")
        
        report.append(f"\n{'='*60}\n")
        
        return "\n".join(report)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='Validate Ansible playbooks')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate playbook syntax and quality')
    validate_parser.add_argument('files', nargs='+', help='Playbook files to validate')
    validate_parser.add_argument('--report', choices=['basic', 'detailed'], default='basic', help='Report detail level')
    
    # Idempotency command
    idempotency_parser = subparsers.add_parser('idempotency', help='Check idempotency only')
    idempotency_parser.add_argument('files', nargs='+', help='Playbook files to check')
    
    # Security command
    security_parser = subparsers.add_parser('security', help='Check security only')
    security_parser.add_argument('files', nargs='+', help='Playbook files to check')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    validator = PlaybookValidator()
    
    for file_path in args.files:
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found")
            continue
            
        print(f"\nValidating: {file_path}")
        print("-" * 40)
        
        if not validator.load_playbook(file_path):
            print(f"✗ Failed to load playbook: {file_path}")
            continue
        
        if args.command == 'validate':
            report = validator.generate_report(file_path, args.report == 'detailed')
            print(report)
            
        elif args.command == 'idempotency':
            result = validator.check_idempotency()
            print(f"Idempotency Score: {result['score']}%")
            if result['issues']:
                print("Issues found:")
                for issue in result['issues']:
                    print(f"  - {issue}")
            
        elif args.command == 'security':
            result = validator.check_security()
            print(f"Security Score: {result['score']}/100")
            if result['issues']:
                print("Security issues found:")
                for issue in result['issues']:
                    print(f"  - {issue}")

if __name__ == '__main__':
    main()
