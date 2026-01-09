#!/usr/bin/env python3
"""
Ansible Playbook Linter Reporter

Generates formatted reports from linting results.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


class Reporter:
    def __init__(self, results_file: str):
        self.results_file = Path(results_file)
        self.results = self._load_results()
    
    def _load_results(self) -> Dict[str, Any]:
        """Load results from JSON file"""
        try:
            with open(self.results_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading results: {e}", file=sys.stderr)
            sys.exit(1)
    
    def generate_summary(self) -> str:
        """Generate a summary report"""
        summary = self.results["summary"]
        violations = self.results["violations"]
        
        report = []
        report.append("# Ansible Playbook Linting Summary")
        report.append("")
        report.append(f"**Files processed:** {summary['files_processed']}")
        report.append(f"**Total violations:** {summary['violations_found']}")
        report.append(f"**Errors:** {summary['errors']}")
        report.append(f"**Warnings:** {summary['warnings']}")
        report.append(f"**Info:** {summary['info']}")
        report.append("")
        
        if summary['violations_found'] > 0:
            report.append("## Violations by Severity")
            report.append("")
            
            # Group violations by severity
            by_severity = {"error": [], "warning": [], "info": []}
            for violation in violations:
                by_severity[violation['severity']].append(violation)
            
            for severity in ["error", "warning", "info"]:
                count = len(by_severity[severity])
                if count > 0:
                    report.append(f"### {severity.upper()} ({count})")
                    report.append("")
                    for violation in by_severity[severity]:
                        report.append(f"- **{violation['rule_id']}**: {violation['message']}")
                        report.append(f"  File: {violation['file_path']}")
                        if violation.get('line'):
                            report.append(f"  Line: {violation['line']}")
                        if violation.get('suggestion'):
                            report.append(f"  Suggestion: {violation['suggestion']}")
                        report.append("")
        
        return "\n".join(report)
    
    def generate_detailed_report(self) -> str:
        """Generate a detailed report with all violations"""
        violations = self.results["violations"]
        
        report = []
        report.append("# Detailed Ansible Playbook Linting Report")
        report.append("")
        
        if not violations:
            report.append("No violations found! 🎉")
            return "\n".join(report)
        
        # Group by file
        by_file = {}
        for violation in violations:
            file_path = violation['file_path']
            if file_path not in by_file:
                by_file[file_path] = []
            by_file[file_path].append(violation)
        
        for file_path, file_violations in by_file.items():
            report.append(f"## {file_path}")
            report.append("")
            
            for violation in file_violations:
                severity_emoji = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(violation['severity'], "")
                report.append(f"### {severity_emoji} {violation['severity'].upper()}: {violation['rule_id']}")
                report.append("")
                report.append(f"**Message:** {violation['message']}")
                if violation.get('line'):
                    report.append(f"**Line:** {violation['line']}")
                if violation.get('suggestion'):
                    report.append(f"**Suggestion:** {violation['suggestion']}")
                report.append("")
        
        return "\n".join(report)
    
    def generate_security_report(self) -> str:
        """Generate a security-focused report"""
        violations = self.results["violations"]
        
        # Filter security-related violations
        security_rules = ["no-hardcoded-secrets", "sudo-usage", "file-permissions"]
        security_violations = [v for v in violations if v['rule_id'] in security_rules]
        
        if not security_violations:
            return "# Security Report\n\nNo security issues found! 🛡️"
        
        report = []
        report.append("# Security Issues Report")
        report.append("")
        report.append(f"**Security violations found:** {len(security_violations)}")
        report.append("")
        
        for violation in security_violations:
            report.append(f"## {violation['rule_id']}")
            report.append("")
            report.append(f"**Severity:** {violation['severity'].upper()}")
            report.append(f"**Message:** {violation['message']}")
            report.append(f"**File:** {violation['file_path']}")
            if violation.get('line'):
                report.append(f"**Line:** {violation['line']}")
            if violation.get('suggestion'):
                report.append(f"**Recommendation:** {violation['suggestion']}")
            report.append("")
        
        return "\n".join(report)
    
    def save_report(self, output_file: str, report_type: str = "summary") -> None:
        """Save report to file"""
        if report_type == "summary":
            content = self.generate_summary()
        elif report_type == "detailed":
            content = self.generate_detailed_report()
        elif report_type == "security":
            content = self.generate_security_report()
        else:
            raise ValueError(f"Unknown report type: {report_type}")
        
        with open(output_file, 'w') as f:
            f.write(content)
    
    def print_summary(self) -> None:
        """Print summary to stdout"""
        print(self.generate_summary())
    
    def print_detailed(self) -> None:
        """Print detailed report to stdout"""
        print(self.generate_detailed_report())
    
    def print_security(self) -> None:
        """Print security report to stdout"""
        print(self.generate_security_report())


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate reports from Ansible linter results")
    parser.add_argument("results_file", help="Path to JSON results file")
    parser.add_argument("--output", help="Output file for report")
    parser.add_argument("--type", choices=["summary", "detailed", "security"], 
                       default="summary", help="Type of report to generate")
    parser.add_argument("--format", choices=["markdown", "text"], default="markdown",
                       help="Output format")
    
    args = parser.parse_args()
    
    reporter = Reporter(args.results_file)
    
    if args.output:
        reporter.save_report(args.output, args.type)
        print(f"Report saved to {args.output}")
    else:
        if args.type == "summary":
            reporter.print_summary()
        elif args.type == "detailed":
            reporter.print_detailed()
        elif args.type == "security":
            reporter.print_security()


if __name__ == "__main__":
    main()
