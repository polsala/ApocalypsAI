#!/usr/bin/env python3
"""
Nightly Ansible Playbook Runner

A whimsical-yet-useful utility for running and testing Ansible playbooks
with automated validation and reporting.
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import time
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests


class PlaybookRunner:
    """Main runner class for executing and validating Ansible playbooks."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the runner with optional configuration."""
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
        self.execution_log = []
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from file or use defaults."""
        default_config = {
            'runner': {
                'default_timeout': 600,
                'enable_rollback': True,
                'report_format': 'html',
                'log_level': 'INFO'
            },
            'validation': {
                'check_syntax': True,
                'check_idempotency': True,
                'check_dependencies': True
            },
            'environments': {}
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = yaml.safe_load(f)
                    # Deep merge configs
                    return self._deep_merge(default_config, user_config)
            except Exception as e:
                self.logger.warning(f"Failed to load config from {config_path}: {e}")
                
        return default_config
    
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        logger = logging.getLogger('playbook_runner')
        logger.setLevel(getattr(logging, self.config['runner']['log_level']))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler
        log_file = f"playbook_runner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def validate_playbook(self, playbook_path: str) -> Tuple[bool, List[str]]:
        """Validate playbook syntax and structure."""
        validation_errors = []
        
        if not os.path.exists(playbook_path):
            validation_errors.append(f"Playbook file not found: {playbook_path}")
            return False, validation_errors
        
        # Check YAML syntax
        try:
            with open(playbook_path, 'r') as f:
                yaml.safe_load(f)
        except yaml.YAMLError as e:
            validation_errors.append(f"YAML syntax error in {playbook_path}: {e}")
        
        # Check for required fields
        try:
            with open(playbook_path, 'r') as f:
                playbook_content = yaml.safe_load(f)
                
            if not isinstance(playbook_content, list):
                validation_errors.append(f"Playbook should be a list of plays: {playbook_path}")
                return False, validation_errors
                
            for play in playbook_content:
                if 'hosts' not in play:
                    validation_errors.append(f"Play missing 'hosts' field: {playbook_path}")
                if 'tasks' not in play:
                    validation_errors.append(f"Play missing 'tasks' field: {playbook_path}")
        except Exception as e:
            validation_errors.append(f"Failed to parse playbook: {e}")
        
        return len(validation_errors) == 0, validation_errors
    
    def validate_inventory(self, inventory_path: str) -> Tuple[bool, List[str]]:
        """Validate inventory file."""
        validation_errors = []
        
        if not os.path.exists(inventory_path):
            validation_errors.append(f"Inventory file not found: {inventory_path}")
            return False, validation_errors
        
        # Basic inventory validation
        try:
            with open(inventory_path, 'r') as f:
                content = f.read().strip()
                if not content:
                    validation_errors.append(f"Inventory file is empty: {inventory_path}")
        except Exception as e:
            validation_errors.append(f"Failed to read inventory: {e}")
        
        return len(validation_errors) == 0, validation_errors
    
    def run_playbook(self, playbook_path: str, inventory_path: str, 
                    dry_run: bool = False, timeout: Optional[int] = None) -> Dict:
        """Execute the playbook with optional dry run."""
        if timeout is None:
            timeout = self.config['runner']['default_timeout']
        
        # Build ansible-playbook command
        cmd = ['ansible-playbook', playbook_path, '-i', inventory_path]
        
        if dry_run:
            cmd.append('--check')
            self.logger.info(f"Running playbook in dry-run mode: {playbook_path}")
        else:
            self.logger.info(f"Executing playbook: {playbook_path}")
        
        # Add additional options
        cmd.extend(['-v', '--diff'])
        
        execution_start = datetime.now()
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            execution_end = datetime.now()
            execution_time = (execution_end - execution_start).total_seconds()
            
            execution_record = {
                'playbook': playbook_path,
                'inventory': inventory_path,
                'dry_run': dry_run,
                'execution_time': execution_time,
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
            
            self.execution_log.append(execution_record)
            
            if result.returncode == 0:
                self.logger.info(f"Playbook execution successful: {playbook_path}")
            else:
                self.logger.error(f"Playbook execution failed: {playbook_path}")
                
            return execution_record
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"Playbook execution timed out after {timeout} seconds")
            return {
                'playbook': playbook_path,
                'inventory': inventory_path,
                'dry_run': dry_run,
                'execution_time': timeout,
                'return_code': -1,
                'stdout': '',
                'stderr': f'Timeout after {timeout} seconds',
                'success': False
            }
        except Exception as e:
            self.logger.error(f"Failed to execute playbook: {e}")
            return {
                'playbook': playbook_path,
                'inventory': inventory_path,
                'dry_run': dry_run,
                'execution_time': 0,
                'return_code': -1,
                'stdout': '',
                'stderr': str(e),
                'success': False
            }
    
    def generate_report(self, output_format: str = 'html') -> str:
        """Generate execution report in specified format."""
        if output_format == 'json':
            return self._generate_json_report()
        elif output_format == 'html':
            return self._generate_html_report()
        elif output_format == 'markdown':
            return self._generate_markdown_report()
        elif output_format == 'xml':
            return self._generate_xml_report()
        else:
            raise ValueError(f"Unsupported report format: {output_format}")
    
    def _generate_json_report(self) -> str:
        """Generate JSON report."""
        report = {
            'execution_summary': {
                'total_executions': len(self.execution_log),
                'successful': sum(1 for exec in self.execution_log if exec['success']),
                'failed': sum(1 for exec in self.execution_log if not exec['success']),
                'total_execution_time': sum(exec['execution_time'] for exec in self.execution_log)
            },
            'executions': self.execution_log
        }
        return json.dumps(report, indent=2)
    
    def _generate_html_report(self) -> str:
        """Generate HTML report."""
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Ansible Playbook Runner Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f0f0f0; padding: 20px; border-radius: 5px; }
        .summary { display: flex; gap: 20px; margin: 20px 0; }
        .metric { background: white; padding: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .execution { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
        .success { border-left: 5px solid #28a745; }
        .failure { border-left: 5px solid #dc3545; }
        pre { background: #f8f9fa; padding: 10px; border-radius: 3px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Ansible Playbook Runner Report</h1>
        <p>Generated on {timestamp}</p>
    </div>
    
    <div class="summary">
        <div class="metric">
            <h3>Total Executions</h3>
            <p>{total_executions}</p>
        </div>
        <div class="metric">
            <h3>Successful</h3>
            <p>{successful}</p>
        </div>
        <div class="metric">
            <h3>Failed</h3>
            <p>{failed}</p>
        </div>
        <div class="metric">
            <h3>Total Time</h3>
            <p>{total_time:.2f}s</p>
        </div>
    </div>
    
    <h2>Execution Details</h2>
    {executions_html}
</body>
</html>
"""
        
        executions_html = ""
        for execution in self.execution_log:
            status_class = "success" if execution['success'] else "failure"
            executions_html += f"""
    <div class="execution {status_class}">
        <h3>{execution['playbook']} - {execution['inventory']}</h3>
        <p><strong>Status:</strong> {'Success' if execution['success'] else 'Failed'}</p>
        <p><strong>Execution Time:</strong> {execution['execution_time']:.2f}s</p>
        <p><strong>Return Code:</strong> {execution['return_code']}</p>
        <details>
            <summary>Output</summary>
            <pre>{execution['stdout']}</pre>
            {f'<pre style="color: red;">{execution["stderr"]}</pre>' if execution['stderr'] else ''}
        </details>
    </div>
"""
        
        return html_template.format(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            total_executions=len(self.execution_log),
            successful=sum(1 for exec in self.execution_log if exec['success']),
            failed=sum(1 for exec in self.execution_log if not exec['success']),
            total_time=sum(exec['execution_time'] for exec in self.execution_log),
            executions_html=executions_html
        )
    
    def _generate_markdown_report(self) -> str:
        """Generate Markdown report."""
        md = "# Ansible Playbook Runner Report\n\n"
        md += f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Summary
        total = len(self.execution_log)
        successful = sum(1 for exec in self.execution_log if exec['success'])
        failed = total - successful
        
        md += "## Summary\n\n"
        md += f"- **Total Executions:** {total}\n"
        md += f"- **Successful:** {successful}\n"
        md += f"- **Failed:** {failed}\n"
        md += f"- **Total Time:** {sum(exec['execution_time'] for exec in self.execution_log):.2f}s\n\n"
        
        # Details
        md += "## Execution Details\n\n"
        for i, execution in enumerate(self.execution_log, 1):
            md += f"### Execution {i}\n\n"
            md += f"**Playbook:** {execution['playbook']}\n"
            md += f"**Inventory:** {execution['inventory']}\n"
            md += f"**Status:** {'✅ Success' if execution['success'] else '❌ Failed'}\n"
            md += f"**Execution Time:** {execution['execution_time']:.2f}s\n"
            md += f"**Return Code:** {execution['return_code']}\n\n"
            
            if execution['stdout']:
                md += "**Output:**\n```
"
                md += execution['stdout']
                md += "\n```
\n"
            
            if execution['stderr']:
                md += "**Errors:**\n```
"
                md += execution['stderr']
                md += "\n```
\n"
        
        return md
    
    def _generate_xml_report(self) -> str:
        """Generate XML report (JUnit format)."""
        xml = "<?xml version='1.0' encoding='UTF-8'?>\n"
        xml += "<testsuites>\n"
        
        for execution in self.execution_log:
            test_name = f"{Path(execution['playbook']).name} - {Path(execution['inventory']).name}"
            
            if execution['success']:
                xml += f"  <testcase name='{test_name}' time='{execution['execution_time']:.2f}'/>\n"
            else:
                xml += f"  <testcase name='{test_name}' time='{execution['execution_time']:.2f}'>\n"
                xml += f"    <failure message='Playbook execution failed'>{execution['stderr']}</failure>\n"
                xml += f"  </testcase>\n"
        
        xml += "</testsuites>\n"
        return xml


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Ansible Playbook Runner')
    parser.add_argument('--playbook', required=True, help='Path to playbook file')
    parser.add_argument('--inventory', required=True, help='Path to inventory file')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--dry-run', action='store_true', help='Run in dry-run mode')
    parser.add_argument('--timeout', type=int, help='Execution timeout in seconds')
    parser.add_argument('--report-format', choices=['json', 'html', 'markdown', 'xml'], 
                       help='Report format')
    parser.add_argument('--output', help='Output file for report')
    
    args = parser.parse_args()
    
    # Initialize runner
    runner = PlaybookRunner(args.config)
    
    # Validate inputs
    playbook_valid, playbook_errors = runner.validate_playbook(args.playbook)
    if not playbook_valid:
        for error in playbook_errors:
            runner.logger.error(error)
        sys.exit(1)
    
    inventory_valid, inventory_errors = runner.validate_inventory(args.inventory)
    if not inventory_valid:
        for error in inventory_errors:
            runner.logger.error(error)
        sys.exit(1)
    
    # Run playbook
    result = runner.run_playbook(
        args.playbook, 
        args.inventory, 
        dry_run=args.dry_run, 
        timeout=args.timeout
    )
    
    # Generate report
    report_format = args.report_format or runner.config['runner']['report_format']
    report = runner.generate_report(report_format)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        runner.logger.info(f"Report saved to: {args.output}")
    else:
        print(report)
    
    # Exit with appropriate code
    if not result['success']:
        sys.exit(1)


if __name__ == '__main__':
    main()
