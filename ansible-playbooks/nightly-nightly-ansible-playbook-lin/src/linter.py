#!/usr/bin/env python3
"""
Ansible Playbook Linter

Static analysis and linting tool for Ansible playbooks.
Performs YAML validation, syntax checks, and best practice enforcement.
"""

import argparse
import json
import os
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import glob


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class RuleType(Enum):
    SYNTAX = "syntax"
    SECURITY = "security"
    PERFORMANCE = "performance"
    BEST_PRACTICE = "best_practice"


@dataclass
class Violation:
    rule_id: str
    severity: Severity
    message: str
    file_path: str
    line: Optional[int] = None
    column: Optional[int] = None
    suggestion: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class AnsibleLinter:
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.violations: List[Violation] = []
        self.stats = {
            "files_processed": 0,
            "violations_found": 0,
            "errors": 0,
            "warnings": 0,
            "info": 0,
        }
        self.enabled_rules = self._get_enabled_rules()
        
        # Common Ansible modules for validation
        self.known_modules = {
            "apt", "yum", "dnf", "pip", "git", "file", "copy", "template",
            "service", "user", "group", "shell", "command", "raw",
            "debug", "fail", "include", "include_tasks", "import_playbook",
            "set_fact", "add_host", "meta", "pause", "wait_for"
        }
        
        # Security-sensitive patterns
        self.secret_patterns = [
            r"password\s*:\s*[^"]\S+",
            r"secret\s*:\s*[^"]\S+",
            r"token\s*:\s*[^"]\S+",
            r"api_key\s*:\s*[^"]\S+",
            r"private_key\s*:\s*[^"]\S+"
        ]

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        default_config = {
            "rules": {
                "enabled": [
                    "yaml-valid", "task-name-required", "module-exists",
                    "no-hardcoded-secrets", "sudo-usage", "file-permissions",
                    "loop-optimization", "gather-facts", "variable-naming",
                    "handler-usage"
                ],
                "disabled": []
            },
            "exclude": ["vendor/", "tests/fixtures/", "*.retry"],
            "max_line_length": 120
        }
        
        if not config_path:
            return default_config
            
        config_file = Path(config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    user_config = yaml.safe_load(f)
                    if user_config:
                        # Merge with defaults
                        for key, value in user_config.items():
                            if isinstance(value, dict) and key in default_config:
                                default_config[key].update(value)
                            else:
                                default_config[key] = value
            except Exception as e:
                print(f"Warning: Could not load config {config_path}: {e}", file=sys.stderr)
        
        return default_config
    
    def _get_enabled_rules(self) -> Set[str]:
        """Get set of enabled rule IDs"""
        enabled = set(self.config.get("rules", {}).get("enabled", []))
        disabled = set(self.config.get("rules", {}).get("disabled", []))
        return enabled - disabled
    
    def _should_exclude(self, file_path: str) -> bool:
        """Check if file should be excluded based on config"""
        exclude_patterns = self.config.get("exclude", [])
        for pattern in exclude_patterns:
            if pattern in file_path or Path(file_path).match(pattern):
                return True
        return False
    
    def lint_file(self, file_path: str) -> None:
        """Lint a single Ansible playbook file"""
        if self._should_exclude(file_path):
            return
            
        self.stats["files_processed"] += 1
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
        except Exception as e:
            self._add_violation(
                "file-read-error",
                Severity.ERROR,
                f"Could not read file: {e}",
                file_path
            )
            return
        
        # Rule: YAML validation
        if "yaml-valid" in self.enabled_rules:
            self._check_yaml_valid(content, file_path)
        
        try:
            playbooks = yaml.safe_load_all(content)
            for playbook in playbooks:
                if playbook is None:
                    continue
                self._lint_playbook(playbook, file_path, lines)
        except yaml.YAMLError as e:
            self._add_violation(
                "yaml-parse-error",
                Severity.ERROR,
                f"YAML parsing failed: {e}",
                file_path
            )
    
    def _check_yaml_valid(self, content: str, file_path: str) -> None:
        """Check if YAML is valid"""
        try:
            yaml.safe_load(content)
        except yaml.YAMLError as e:
            self._add_violation(
                "yaml-valid",
                Severity.ERROR,
                f"Invalid YAML syntax: {e}",
                file_path
            )
    
    def _lint_playbook(self, playbook: Dict, file_path: str, lines: List[str]) -> None:
        """Lint a single playbook"""
        if isinstance(playbook, dict):
            # Check for tasks
            tasks = playbook.get("tasks", [])
            if tasks:
                self._lint_tasks(tasks, file_path, lines, playbook.get("name", ""))
            
            # Check for handlers
            handlers = playbook.get("handlers", [])
            if handlers:
                self._lint_handlers(handlers, file_path, lines)
            
            # Check playbook-level settings
            self._lint_playbook_settings(playbook, file_path, lines)
        elif isinstance(playbook, list):
            # Handle list of playbooks
            for item in playbook:
                if isinstance(item, dict):
                    self._lint_playbook(item, file_path, lines)
    
    def _lint_tasks(self, tasks: List[Dict], file_path: str, lines: List[str], playbook_name: str = "") -> None:
        """Lint tasks in a playbook"""
        for i, task in enumerate(tasks):
            if not isinstance(task, dict):
                continue
                
            # Rule: Task name required
            if "task-name-required" in self.enabled_rules:
                self._check_task_name(task, file_path, lines, i)
            
            # Rule: Module exists
            if "module-exists" in self.enabled_rules:
                self._check_module_exists(task, file_path, lines, i)
            
            # Rule: No hardcoded secrets
            if "no-hardcoded-secrets" in self.enabled_rules:
                self._check_hardcoded_secrets(task, file_path, lines, i)
            
            # Rule: Sudo usage
            if "sudo-usage" in self.enabled_rules:
                self._check_sudo_usage(task, file_path, lines, i)
            
            # Rule: File permissions
            if "file-permissions" in self.enabled_rules:
                self._check_file_permissions(task, file_path, lines, i)
            
            # Rule: Loop optimization
            if "loop-optimization" in self.enabled_rules:
                self._check_loop_optimization(task, file_path, lines, i)
            
            # Rule: Variable naming
            if "variable-naming" in self.enabled_rules:
                self._check_variable_naming(task, file_path, lines, i)
    
    def _lint_handlers(self, handlers: List[Dict], file_path: str, lines: List[str]) -> None:
        """Lint handlers in a playbook"""
        for i, handler in enumerate(handlers):
            if not isinstance(handler, dict):
                continue
                
            # Rule: Handler usage
            if "handler-usage" in self.enabled_rules:
                self._check_handler_usage(handler, file_path, lines, i)
    
    def _lint_playbook_settings(self, playbook: Dict, file_path: str, lines: List[str]) -> None:
        """Lint playbook-level settings"""
        # Rule: Gather facts
        if "gather-facts" in self.enabled_rules:
            self._check_gather_facts(playbook, file_path, lines)
    
    def _check_task_name(self, task: Dict, file_path: str, lines: List[str], task_index: int) -> None:
        """Check if task has a name"""
        if "name" not in task:
            self._add_violation(
                "task-name-required",
                Severity.WARNING,
                "Task is missing a name",
                file_path,
                line=self._find_task_line(lines, task_index),
                suggestion="Add a descriptive name to this task for better debugging and reporting"
            )
    
    def _check_module_exists(self, task: Dict, file_path: str, lines: List[str], task_index: int) -> None:
        """Check if the module exists in Ansible"""
        module_name = None
        for key in task.keys():
            if key in self.known_modules:
                module_name = key
                break
        
        if module_name and module_name not in self.known_modules:
            self._add_violation(
                "module-exists",
                Severity.ERROR,
                f"Unknown module: {module_name}",
                file_path,
                line=self._find_task_line(lines, task_index),
                suggestion=f"Check the module name or ensure the required collection is installed"
            )
    
    def _check_hardcoded_secrets(self, task: Dict, file_path: str, lines: List[str], task_index: int) -> None:
        """Check for hardcoded secrets in task"""
        task_str = str(task)
        for pattern in self.secret_patterns:
            if re.search(pattern, task_str, re.IGNORECASE):
                self._add_violation(
                    "no-hardcoded-secrets",
                    Severity.ERROR,
                    "Potential hardcoded secret detected",
                    file_path,
                    line=self._find_task_line(lines, task_index),
                    suggestion="Use Ansible vault or environment variables for sensitive data"
                )
                break
    
    def _check_sudo_usage(self, task: Dict, file_path: str, lines: List[str], task_index: int) -> None:
        """Check for sudo usage (deprecated)"""
        if "sudo" in task or "sudo_user" in task:
            self._add_violation(
                "sudo-usage",
                Severity.WARNING,
                "Use of deprecated 'sudo' parameter detected",
                file_path,
                line=self._find_task_line(lines, task_index),
                suggestion="Use 'become' and 'become_user' instead of 'sudo' and 'sudo_user'"
            )
    
    def _check_file_permissions(self, task: Dict, file_path: str, lines: List[str], task_index: int) -> None:
        """Check file permission settings"""
        if task.get("module") == "file":
            mode = task.get("mode")
            if mode and isinstance(mode, str) and not mode.startswith("0"):
                self._add_violation(
                    "file-permissions",
                    Severity.WARNING,
                    "File permissions should be octal (start with 0)",
                    file_path,
                    line=self._find_task_line(lines, task_index),
                    suggestion="Use octal notation for file permissions, e.g., '0644' instead of '644'"
                )
    
    def _check_loop_optimization(self, task: Dict, file_path: str, lines: List[str], task_index: int) -> None:
        """Check for loop optimization opportunities"""
        if "with_items" in task and "loop" not in task:
            self._add_violation(
                "loop-optimization",
                Severity.INFO,
                "Consider using 'loop' instead of deprecated 'with_items'",
                file_path,
                line=self._find_task_line(lines, task_index),
                suggestion="Replace 'with_items' with 'loop' for better performance and readability"
            )
    
    def _check_variable_naming(self, task: Dict, file_path: str, lines: List[str], task_index: int) -> None:
        """Check variable naming conventions"""
        task_str = str(task)
        # Look for variables that don't follow snake_case
        var_pattern = r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}"
        matches = re.findall(var_pattern, task_str)
        for var_name in matches:
            if not var_name.islower() and "_" not in var_name:
                self._add_violation(
                    "variable-naming",
                    Severity.INFO,
                    f"Variable '{var_name}' should use snake_case",
                    file_path,
                    line=self._find_task_line(lines, task_index),
                    suggestion="Use snake_case for variable names, e.g., 'my_variable' instead of 'myVariable'"
                )
    
    def _check_handler_usage(self, handler: Dict, file_path: str, lines: List[str], handler_index: int) -> None:
        """Check handler usage patterns"""
        if "name" not in handler:
            self._add_violation(
                "handler-usage",
                Severity.WARNING,
                "Handler is missing a name",
                file_path,
                line=self._find_task_line(lines, handler_index),
                suggestion="Add a descriptive name to this handler"
            )
    
    def _check_gather_facts(self, playbook: Dict, file_path: str, lines: List[str]) -> None:
        """Check gather_facts usage"""
        gather_facts = playbook.get("gather_facts")
        if gather_facts is False:
            # Check if any tasks actually need facts
            # This is a simplified check - in practice, you'd need more sophisticated analysis
            self._add_violation(
                "gather-facts",
                Severity.INFO,
                "gather_facts is disabled - ensure no tasks require system facts",
                file_path,
                suggestion="Consider enabling gather_facts or use specific fact modules if needed"
            )
    
    def _find_task_line(self, lines: List[str], task_index: int) -> Optional[int]:
        """Find the line number for a task (simplified implementation)"""
        # This is a simplified version - in practice, you'd want to parse YAML with line numbers
        # For now, return a rough estimate
        return task_index + 1
    
    def _add_violation(self, rule_id: str, severity: Severity, message: str, 
                      file_path: str, line: Optional[int] = None, 
                      column: Optional[int] = None, suggestion: Optional[str] = None,
                      context: Optional[Dict[str, Any]] = None) -> None:
        """Add a violation to the results"""
        violation = Violation(
            rule_id=rule_id,
            severity=severity,
            message=message,
            file_path=file_path,
            line=line,
            column=column,
            suggestion=suggestion,
            context=context
        )
        self.violations.append(violation)
        self.stats["violations_found"] += 1
        
        if severity == Severity.ERROR:
            self.stats["errors"] += 1
        elif severity == Severity.WARNING:
            self.stats["warnings"] += 1
        elif severity == Severity.INFO:
            self.stats["info"] += 1
    
    def lint_directory(self, directory: str, recursive: bool = False) -> None:
        """Lint all YAML files in a directory"""
        pattern = "**/*.yml" if recursive else "*.yml"
        for file_path in glob.glob(os.path.join(directory, pattern), recursive=recursive):
            if file_path.endswith('.yml') or file_path.endswith('.yaml'):
                self.lint_file(file_path)
    
    def get_results(self) -> Dict[str, Any]:
        """Get linting results"""
        return {
            "summary": self.stats,
            "violations": [asdict(v) for v in self.violations]
        }


def main():
    parser = argparse.ArgumentParser(description="Ansible Playbook Linter")
    parser.add_argument("files", nargs="*", help="Files or directories to lint")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--report", help="Path to save JSON report")
    parser.add_argument("--recursive", "-r", action="store_true", 
                       help="Recursively lint directories")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Verbose output")
    parser.add_argument("--format", choices=["json", "text"], default="text",
                       help="Output format")
    
    args = parser.parse_args()
    
    if not args.files:
        print("Error: No files specified", file=sys.stderr)
        sys.exit(3)
    
    linter = AnsibleLinter(args.config)
    
    for file_path in args.files:
        if os.path.isfile(file_path):
            linter.lint_file(file_path)
        elif os.path.isdir(file_path):
            linter.lint_directory(file_path, args.recursive)
        else:
            print(f"Error: File or directory not found: {file_path}", file=sys.stderr)
            sys.exit(3)
    
    results = linter.get_results()
    
    if args.format == "json":
        output = json.dumps(results, indent=2)
    else:
        output = format_text_output(results)
    
    print(output)
    
    if args.report:
        with open(args.report, 'w') as f:
            json.dump(results, f, indent=2)
    
    # Exit with appropriate code
    if results["summary"]["errors"] > 0:
        sys.exit(1)
    elif results["summary"]["violations_found"] > 0:
        sys.exit(1)  # Treat warnings as failures for CI/CD
    else:
        sys.exit(0)


def format_text_output(results: Dict[str, Any]) -> str:
    """Format results as human-readable text"""
    output = []
    summary = results["summary"]
    violations = results["violations"]
    
    output.append("Ansible Playbook Linter Results")
    output.append("=" * 30)
    output.append(f"Files processed: {summary['files_processed']}")
    output.append(f"Violations found: {summary['violations_found']}")
    output.append(f"  Errors: {summary['errors']}")
    output.append(f"  Warnings: {summary['warnings']}")
    output.append(f"  Info: {summary['info']}")
    output.append("")
    
    if violations:
        output.append("Violations:")
        output.append("-" * 20)
        
        for violation in violations:
            severity_icon = {
                "error": "❌",
                "warning": "⚠️",
                "info": "ℹ️"
            }.get(violation["severity"], "")
            
            line_info = f":{violation['line']}" if violation.get('line') else ""
            output.append(f"{severity_icon} {violation['severity'].upper()}: {violation['message']}")
            output.append(f"   File: {violation['file_path']}{line_info}")
            output.append(f"   Rule: {violation['rule_id']}")
            if violation.get('suggestion'):
                output.append(f"   Suggestion: {violation['suggestion']}")
            output.append("")
    
    return "\n".join(output)


if __name__ == "__main__":
    main()
