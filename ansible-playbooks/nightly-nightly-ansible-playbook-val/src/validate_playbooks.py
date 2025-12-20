#!/usr/bin/env python3
"""
Nightly Ansible Playbook Validator

Validates Ansible playbooks for syntax, idempotency, and best practices.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple, Any

import yaml
from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.syntax import Syntax

console = Console()


class PlaybookValidator:
    """Validates Ansible playbooks for syntax, idempotency, and best practices."""
    
    def __init__(self):
        self.validation_results = {
            'syntax': [],
            'idempotency': [],
            'best_practices': [],
            'summary': {}
        }
        self.console = Console()
    
    def validate_syntax(self, playbook_path: str) -> Dict[str, Any]:
        """Validate YAML syntax and Ansible structure."""
        result = {
            'file': playbook_path,
            'valid': False,
            'errors': [],
            'warnings': [],
            'tasks_count': 0
        }
        
        try:
            with open(playbook_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse YAML
            playbook_data = yaml.safe_load(content)
            
            if not isinstance(playbook_data, list):
                result['errors'].append("Playbook must be a list of plays")
                return result
            
            # Count tasks
            total_tasks = 0
            for play in playbook_data:
                if 'tasks' in play:
                    total_tasks += len(play['tasks'])
            result['tasks_count'] = total_tasks
            
            # Check for common syntax issues
            self._check_syntax_issues(playbook_data, result)
            
            result['valid'] = len(result['errors']) == 0
            
        except yaml.YAMLError as e:
            result['errors'].append(f"YAML syntax error: {str(e)}")
        except Exception as e:
            result['errors'].append(f"Unexpected error: {str(e)}")
        
        return result
    
    def _check_syntax_issues(self, playbook_data: List[Dict], result: Dict[str, Any]):
        """Check for common syntax and structure issues."""
        for play_index, play in enumerate(playbook_data):
            # Check for required fields
            if 'tasks' not in play:
                result['warnings'].append(f"Play {play_index + 1}: No tasks found")
            
            # Check tasks
            if 'tasks' in play:
                for task_index, task in enumerate(play['tasks']):
                    if not isinstance(task, dict):
                        result['errors'].append(f"Play {play_index + 1}, Task {task_index + 1}: Task must be a dictionary")
                        continue
                    
                    # Check for module usage
                    if not any(key.startswith('_') or key in ['name', 'when', 'loop', 'with_items'] for key in task.keys()):
                        result['warnings'].append(f"Play {play_index + 1}, Task {task_index + 1}: No module specified")
                    
                    # Check for deprecated patterns
                    if 'with_items' in task:
                        result['warnings'].append(f"Play {play_index + 1}, Task {task_index + 1}: 'with_items' is deprecated, use 'loop' instead")
    
    def validate_idempotency(self, playbook_path: str) -> Dict[str, Any]:
        """Test playbook idempotency by running it twice."""
        result = {
            'file': playbook_path,
            'idempotent': False,
            'changes_first_run': 0,
            'changes_second_run': 0,
            'errors': [],
            'warnings': []
        }
        
        # Create a temporary inventory for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as inventory_file:
            inventory_file.write('[localhost]\n127.0.0.1 ansible_connection=local\n')
            inventory_path = inventory_file.name
        
        try:
            # First run
            first_run = self._run_playbook(playbook_path, inventory_path)
            result['changes_first_run'] = first_run['changed']
            
            if first_run['failed']:
                result['errors'].append(f"First run failed: {first_run['error']}")
                return result
            
            # Second run (should be idempotent)
            second_run = self._run_playbook(playbook_path, inventory_path)
            result['changes_second_run'] = second_run['changed']
            
            if second_run['failed']:
                result['errors'].append(f"Second run failed: {second_run['error']}")
                return result
            
            # Check idempotency
            result['idempotent'] = result['changes_second_run'] == 0
            
            if not result['idempotent']:
                result['warnings'].append(f"Playbook made changes on second run ({result['changes_second_run']} changes)")
            
        finally:
            os.unlink(inventory_path)
        
        return result
    
    def _run_playbook(self, playbook_path: str, inventory_path: str) -> Dict[str, Any]:
        """Run a playbook and capture results."""
        try:
            # Run ansible-playbook with JSON output
            cmd = [
                'ansible-playbook',
                '-i', inventory_path,
                '--check',  # Check mode for safety
                '--diff',   # Show changes
                '--json',   # JSON output
                playbook_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                # Parse JSON output to count changes
                # Note: This is a simplified approach
                # In a real implementation, you'd parse the JSON structure
                output_lines = result.stdout.split('\n')
                changed_count = sum(1 for line in output_lines if '"changed": true' in line)
                
                return {'failed': False, 'changed': changed_count, 'error': None}
            else:
                return {'failed': True, 'changed': 0, 'error': result.stderr}
                
        except subprocess.TimeoutExpired:
            return {'failed': True, 'changed': 0, 'error': 'Playbook execution timed out'}
        except Exception as e:
            return {'failed': True, 'changed': 0, 'error': str(e)}
    
    def validate_best_practices(self, playbook_path: str) -> Dict[str, Any]:
        """Validate against Ansible best practices."""
        result = {
            'file': playbook_path,
            'score': 0,
            'max_score': 0,
            'violations': [],
            'recommendations': []
        }
        
        try:
            with open(playbook_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            playbook_data = yaml.safe_load(content)
            
            # Best practice checks
            self._check_best_practices(playbook_data, result)
            
            # Calculate score
            result['score'] = max(0, result['max_score'] - len(result['violations']))
            
        except Exception as e:
            result['violations'].append(f"Error during best practices check: {str(e)}")
        
        return result
    
    def _check_best_practices(self, playbook_data: List[Dict], result: Dict[str, Any]):
        """Check for best practices violations."""
        result['max_score'] = 10  # Maximum possible score
        
        for play_index, play in enumerate(playbook_data):
            # Check for play name
            if 'name' not in play:
                result['violations'].append(f"Play {play_index + 1}: Missing play name")
            else:
                result['max_score'] += 1
            
            # Check for hosts
            if 'hosts' not in play:
                result['violations'].append(f"Play {play_index + 1}: Missing hosts specification")
            
            # Check tasks
            if 'tasks' in play:
                for task_index, task in enumerate(play['tasks']):
                    if not isinstance(task, dict):
                        continue
                    
                    # Check for task names
                    if 'name' not in task:
                        result['violations'].append(f"Play {play_index + 1}, Task {task_index + 1}: Missing task name")
                    else:
                        result['max_score'] += 1
                    
                    # Check for when conditions
                    if 'when' in task:
                        when_condition = task['when']
                        if isinstance(when_condition, str) and len(when_condition) > 100:
                            result['violations'].append(f"Play {play_index + 1}, Task {task_index + 1}: Complex when condition, consider simplifying")
                    
                    # Check for deprecated modules
                    for key in task.keys():
                        if key in ['template', 'copy'] and 'src' in task and task['src'].endswith('.j2'):
                            result['recommendations'].append(f"Play {play_index + 1}, Task {task_index + 1}: Consider using template module instead of {key}")
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate a validation report."""
        # Create HTML report
        env = Environment(loader=FileSystemLoader(Path(__file__).parent))
        template = env.from_string(self._get_report_template())
        
        html_content = template.render(
            results=self.validation_results,
            timestamp=self._get_timestamp()
        )
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(html_content)
            return f"Report generated: {output_file}"
        else:
            return html_content
    
    def _get_report_template(self) -> str:
        """HTML template for validation report."""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Ansible Playbook Validation Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { background: #f0f0f0; padding: 20px; border-radius: 5px; }
        .section { margin: 20px 0; }
        .pass { color: green; }
        .fail { color: red; }
        .warn { color: orange; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ Ansible Playbook Validation Report</h1>
        <p><strong>Generated:</strong> {{ timestamp }}</p>
    </div>
    
    <div class="section">
        <h2>📊 Summary</h2>
        <p>Total files validated: {{ results.syntax|length }}</p>
        <p>Syntax valid: {{ results.syntax|selectattr('valid')|list|length }}</p>
        <p>Idempotent: {{ results.idempotency|selectattr('idempotent')|list|length }}</p>
    </div>
    
    <div class="section">
        <h2>🔍 Syntax Validation</h2>
        <table>
            <tr><th>File</th><th>Status</th><th>Tasks</th><th>Errors</th><th>Warnings</th></tr>
            {% for result in results.syntax %}
            <tr>
                <td>{{ result.file }}</td>
                <td class="{% if result.valid %}pass{% else %}fail{% endif %}">
                    {% if result.valid %}✅ Valid{% else %}❌ Invalid{% endif %}
                </td>
                <td>{{ result.tasks_count }}</td>
                <td>{{ result.errors|length }}</td>
                <td>{{ result.warnings|length }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    
    <div class="section">
        <h2>🔄 Idempotency Test</h2>
        <table>
            <tr><th>File</th><th>Status</th><th>First Run Changes</th><th>Second Run Changes</th></tr>
            {% for result in results.idempotency %}
            <tr>
                <td>{{ result.file }}</td>
                <td class="{% if result.idempotent %}pass{% else %}fail{% endif %}">
                    {% if result.idempotent %}✅ Idempotent{% else %}❌ Not Idempotent{% endif %}
                </td>
                <td>{{ result.changes_first_run }}</td>
                <td>{{ result.changes_second_run }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    
    <div class="section">
        <h2>📋 Best Practices</h2>
        <table>
            <tr><th>File</th><th>Score</th><th>Violations</th><th>Recommendations</th></tr>
            {% for result in results.best_practices %}
            <tr>
                <td>{{ result.file }}</td>
                <td>{{ result.score }}/{{ result.max_score }}</td>
                <td>{{ result.violations|length }}</td>
                <td>{{ result.recommendations|length }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Validate Ansible playbooks')
    parser.add_argument('command', choices=['validate', 'idempotency', 'report'],
                       help='Command to execute')
    parser.add_argument('files', nargs='*', help='Playbook files to validate')
    parser.add_argument('--output', '-o', help='Output file for report')
    
    args = parser.parse_args()
    
    validator = PlaybookValidator()
    
    if args.command == 'validate':
        if not args.files:
            console.print("[red]Error: No playbook files specified[/red]")
            sys.exit(1)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Validating playbooks...", total=len(args.files) * 3)
            
            for playbook_file in args.files:
                if not os.path.exists(playbook_file):
                    console.print(f"[red]File not found: {playbook_file}[/red]")
                    continue
                
                # Syntax validation
                syntax_result = validator.validate_syntax(playbook_file)
                validator.validation_results['syntax'].append(syntax_result)
                progress.update(task, advance=1)
                
                # Idempotency test
                idempotency_result = validator.validate_idempotency(playbook_file)
                validator.validation_results['idempotency'].append(idempotency_result)
                progress.update(task, advance=1)
                
                # Best practices
                best_practices_result = validator.validate_best_practices(playbook_file)
                validator.validation_results['best_practices'].append(best_practices_result)
                progress.update(task, advance=1)
        
        # Display results
        display_validation_summary(validator.validation_results)
        
    elif args.command == 'idempotency':
        if not args.files:
            console.print("[red]Error: No playbook files specified[/red]")
            sys.exit(1)
        
        for playbook_file in args.files:
            if not os.path.exists(playbook_file):
                console.print(f"[red]File not found: {playbook_file}[/red]")
                continue
            
            result = validator.validate_idempotency(playbook_file)
            display_idempotency_result(result)
    
    elif args.command == 'report':
        report_path = args.output or 'validation_report.html'
        message = validator.generate_report(report_path)
        console.print(f"[green]{message}[/green]")


def display_validation_summary(results: Dict[str, List]) -> None:
    """Display validation summary in console."""
    console.print("\n" + "="*60)
    console.print("[bold blue]🛡️ ANSIBLE PLAYBOOK VALIDATION SUMMARY[/bold blue]")
    console.print("="*60)
    
    # Syntax results
    console.print("\n[bold]🔍 Syntax Validation Results:[/bold]")
    for result in results['syntax']:
        status = "[green]✅ VALID[/green]" if result['valid'] else "[red]❌ INVALID[/red]"
        console.print(f"  {result['file']}: {status}")
        if result['errors']:
            for error in result['errors']:
                console.print(f"    [red]• {error}[/red]")
        if result['warnings']:
            for warning in result['warnings']:
                console.print(f"    [yellow]• {warning}[/yellow]")
    
    # Idempotency results
    console.print("\n[bold]🔄 Idempotency Test Results:[/bold]")
    for result in results['idempotency']:
        status = "[green]✅ IDEMPOTENT[/green]" if result['idempotent'] else "[red]❌ NOT IDEMPOTENT[/red]"
        console.print(f"  {result['file']}: {status}")
        console.print(f"    First run changes: {result['changes_first_run']}")
        console.print(f"    Second run changes: {result['changes_second_run']}")
    
    # Best practices results
    console.print("\n[bold]📋 Best Practices Results:[/bold]")
    for result in results['best_practices']:
        score_text = f"[cyan]{result['score']}/{result['max_score']}[/cyan]"
        console.print(f"  {result['file']}: {score_text}")
        if result['violations']:
            for violation in result['violations']:
                console.print(f"    [red]• {violation}[/red]")
        if result['recommendations']:
            for rec in result['recommendations']:
                console.print(f"    [blue]• {rec}[/blue]")
    
    console.print("\n" + "="*60)


def display_idempotency_result(result: Dict[str, Any]) -> None:
    """Display individual idempotency test result."""
    console.print(f"\n[bold]🔄 Idempotency Test: {result['file']}[/bold]")
    
    if result['idempotent']:
        console.print("[green]✅ Playbook is idempotent![/green]")
    else:
        console.print("[red]❌ Playbook is NOT idempotent![/red]")
    
    console.print(f"First run changes: {result['changes_first_run']}")
    console.print(f"Second run changes: {result['changes_second_run']}")
    
    if result['errors']:
        for error in result['errors']:
            console.print(f"[red]Error: {error}[/red]")
    
    if result['warnings']:
        for warning in result['warnings']:
            console.print(f"[yellow]Warning: {warning}[/yellow]")


if __name__ == '__main__':
    main()
