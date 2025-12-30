#!/usr/bin/env python3
"""
Nightly Ansible Playbook Validator

Validates Ansible playbooks for syntax, idempotency, and security best practices.
"""

import argparse
import json
import os
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime

import jinja2


class ValidationResult:
    """Container for validation results."""
    
    def __init__(self, playbook_path: str):
        self.playbook_path = playbook_path
        self.syntax_valid = True
        self.idempotent = True
        self.security_score = 100
        self.issues: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.recommendations: List[str] = []
        self.total_tasks = 0
        self.risky_tasks = 0
        
    def add_issue(self, severity: str, message: str, line: Optional[int] = None, task: Optional[str] = None):
        """Add an issue to the results."""
        self.issues.append({
            'severity': severity,
            'message': message,
            'line': line,
            'task': task,
            'timestamp': datetime.now().isoformat()
        })
        if severity == 'error':
            self.syntax_valid = False
        elif severity == 'warning':
            self.warnings.append(self.issues[-1])
    
    def add_recommendation(self, recommendation: str):
        """Add a recommendation."""
        self.recommendations.append(recommendation)
    
    def calculate_security_score(self):
        """Calculate overall security score."""
        if not self.issues:
            return 100
        
        score_reduction = 0
        for issue in self.issues:
            if issue['severity'] == 'error':
                score_reduction += 10
            elif issue['severity'] == 'warning':
                score_reduction += 5
        
        self.security_score = max(0, 100 - score_reduction)
        return self.security_score


class PlaybookValidator:
    """Main validator class."""
    
    def __init__(self):
        self.dangerous_modules = {
            'shell', 'command', 'raw', 'script',
            'expect', 'win_shell', 'win_command'
        }
        self.insecure_patterns = [
            r'password\s*:\s*[^\s]',
            r'secret\s*:\s*[^\s]',
            r'api_key\s*:\s*[^\s]',
            r'token\s*:\s*[^\s]'
        ]
        self.idempotency_modules = {
            'file', 'copy', 'template', 'lineinfile',
            'replace', 'user', 'group', 'package'
        }
    
    def validate_syntax(self, playbook_path: str) -> ValidationResult:
        """Validate YAML syntax and basic structure."""
        result = ValidationResult(playbook_path)
        
        try:
            with open(playbook_path, 'r') as f:
                content = f.read()
                
            # Check YAML syntax
            try:
                playbook_data = yaml.safe_load(content)
            except yaml.YAMLError as e:
                result.add_issue('error', f'YAML syntax error: {str(e)}')
                return result
            
            if not isinstance(playbook_data, list):
                result.add_issue('error', 'Playbook must be a list of plays')
                return result
            
            # Validate each play
            for play_index, play in enumerate(playbook_data):
                if not isinstance(play, dict):
                    result.add_issue('error', f'Play {play_index} must be a dictionary', play_index + 1)
                    continue
                
                # Check required fields
                if 'tasks' not in play:
                    result.add_issue('warning', f'Play {play_index} has no tasks', play_index + 1)
                
                # Validate tasks
                if 'tasks' in play:
                    for task_index, task in enumerate(play['tasks']):
                        result.total_tasks += 1
                        self._validate_task(task, result, play_index, task_index)
                        
        except FileNotFoundError:
            result.add_issue('error', f'File not found: {playbook_path}')
        except Exception as e:
            result.add_issue('error', f'Unexpected error: {str(e)}')
        
        return result
    
    def _validate_task(self, task: Dict[str, Any], result: ValidationResult, play_index: int, task_index: int):
        """Validate individual task."""
        if not isinstance(task, dict):
            result.add_issue('error', 'Task must be a dictionary', task_index + 1, str(task))
            return
        
        # Check for module usage
        module_name = next(iter(task.keys()), None)
        if module_name in self.dangerous_modules:
            result.risky_tasks += 1
            result.add_issue('warning', 
                           f'Use of potentially dangerous module: {module_name}', 
                           task_index + 1, module_name)
            
            # Check for unsafe patterns
            if module_name in ['shell', 'command']:
                if 'creates' not in task and 'removes' not in task:
                    result.add_issue('warning', 
                                   f'{module_name} task should have creates/removes for idempotency',
                                   task_index + 1, module_name)
        
        # Check for idempotency
        if module_name in self.idempotency_modules:
            if 'state' not in task and module_name != 'lineinfile':
                result.add_issue('warning', 
                               f'Module {module_name} should specify state for idempotency',
                               task_index + 1, module_name)
        
        # Check for hardcoded secrets
        task_str = str(task)
        for pattern in self.insecure_patterns:
            if re.search(pattern, task_str, re.IGNORECASE):
                result.add_issue('error', 
                               'Potential hardcoded secret detected',
                               task_index + 1, module_name)
        
        # Check for when conditions
        if 'when' in task:
            when_condition = task['when']
            if isinstance(when_condition, str) and 'vault_' in when_condition:
                result.add_issue('warning', 
                               'Consider using ansible_facts instead of vault_ in when conditions',
                               task_index + 1, module_name)
    
    def check_idempotency(self, playbook_path: str) -> ValidationResult:
        """Check playbook idempotency."""
        result = self.validate_syntax(playbook_path)
        
        # Additional idempotency checks
        try:
            with open(playbook_path, 'r') as f:
                content = f.read()
                
            # Check for proper use of changed_when
            if 'changed_when' in content:
                result.add_recommendation('Ensure changed_when is used appropriately for idempotent tasks')
            
            # Check for file operations without backup
            if 'backup: no' in content:
                result.add_issue('warning', 'Consider enabling backup for file operations')
            
        except Exception as e:
            result.add_issue('error', f'Idempotency check failed: {str(e)}')
        
        return result
    
    def security_audit(self, playbook_path: str) -> ValidationResult:
        """Perform security audit."""
        result = self.validate_syntax(playbook_path)
        
        try:
            with open(playbook_path, 'r') as f:
                content = f.read()
                
            # Check for sudo usage
            if 'sudo:' in content or 'become:' in content:
                if 'become_user:' not in content:
                    result.add_issue('warning', 'Specify become_user for privilege escalation')
            
            # Check for vault usage
            if 'ansible-vault' in content.lower():
                result.add_recommendation('Ensure vault passwords are managed securely')
            
            # Check for debug output
            if 'debug:' in content:
                result.add_issue('warning', 'Remove debug tasks from production playbooks')
            
            # Check for file permissions
            if 'mode:' in content:
                # This is a simplified check - in reality you'd parse the YAML properly
                result.add_recommendation('Review file permissions for security best practices')
            
        except Exception as e:
            result.add_issue('error', f'Security audit failed: {str(e)}')
        
        return result
    
    def generate_report(self, result: ValidationResult, format: str = 'text') -> str:
        """Generate validation report."""
        if format == 'json':
            return json.dumps({
                'playbook': result.playbook_path,
                'syntax_valid': result.syntax_valid,
                'idempotent': result.idempotent,
                'security_score': result.calculate_security_score(),
                'total_issues': len(result.issues),
                'total_warnings': len(result.warnings),
                'total_tasks': result.total_tasks,
                'risky_tasks': result.risky_tasks,
                'issues': result.issues,
                'recommendations': result.recommendations
            }, indent=2)
        
        # Text format
        report = f"""
Ansible Playbook Validation Report
{'='*50}

Playbook: {result.playbook_path}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY:
--------
Syntax Valid: {'✓' if result.syntax_valid else '✗'}
Idempotent: {'✓' if result.idempotent else '✗'}
Security Score: {result.calculate_security_score()}/100
Total Tasks: {result.total_tasks}
Risky Tasks: {result.risky_tasks}

ISSUES ({len(result.issues)}):
{'-'*20}
"""
        
        for issue in result.issues:
            line_info = f" (line {issue['line']})" if issue['line'] else ""
            task_info = f" [task: {issue['task']}]" if issue['task'] else ""
            report += f"{issue['severity'].upper()}{line_info}{task_info}: {issue['message']}\n"
        
        if result.recommendations:
            report += f"\nRECOMMENDATIONS:\n{'-'*20}\n"
            for rec in result.recommendations:
                report += f"• {rec}\n"
        
        return report


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Validate Ansible playbooks')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate playbook syntax and structure')
    validate_parser.add_argument('playbook', help='Path to playbook file')
    validate_parser.add_argument('--report', '-r', help='Generate report file')
    validate_parser.add_argument('--format', choices=['text', 'json'], default='text', help='Report format')
    
    # Idempotency command
    idempotency_parser = subparsers.add_parser('idempotency', help='Check playbook idempotency')
    idempotency_parser.add_argument('playbook', help='Path to playbook file')
    
    # Security command
    security_parser = subparsers.add_parser('security', help='Perform security audit')
    security_parser.add_argument('playbook', help='Path to playbook file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    validator = PlaybookValidator()
    
    if args.command == 'validate':
        result = validator.validate_syntax(args.playbook)
        report = validator.generate_report(result, args.format)
        
        if args.report:
            with open(args.report, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.report}")
        else:
            print(report)
        
        sys.exit(0 if result.syntax_valid else 1)
    
    elif args.command == 'idempotency':
        result = validator.check_idempotency(args.playbook)
        report = validator.generate_report(result)
        print(report)
        sys.exit(0 if result.idempotent else 1)
    
    elif args.command == 'security':
        result = validator.security_audit(args.playbook)
        report = validator.generate_report(result)
        print(report)
        sys.exit(0 if result.security_score >= 70 else 1)

if __name__ == '__main__':
    main()
