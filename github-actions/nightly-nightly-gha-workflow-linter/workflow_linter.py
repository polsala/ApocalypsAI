#!/usr/bin/env python3
"""GitHub Actions workflow linter.

Validates YAML syntax, checks for security anti-patterns,
and enforces best practices across GitHub Actions workflows.
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

import yaml


class WorkflowLinter:
    """Lints GitHub Actions workflow files for syntax and security issues."""

    def __init__(self, workflows_dir: str = ".github/workflows"):
        self.workflows_dir = Path(workflows_dir)
        self.errors: List[Tuple[str, str]] = []
        self.warnings: List[Tuple[str, str]] = []

    def lint_all(self) -> bool:
        """Lint all workflow files and return True if no errors."""
        if not self.workflows_dir.exists():
            print(f"❌ Workflows directory not found: {self.workflows_dir}")
            return False

        workflow_files = list(self.workflows_dir.glob("*.yml")) + list(
            self.workflows_dir.glob("*.yaml")
        )

        if not workflow_files:
            print("⚠️  No workflow files found")
            return True

        print(f"🔍 Found {len(workflow_files)} workflow file(s)")

        for workflow_file in workflow_files:
            self._lint_file(workflow_file)

        self._print_results()
        return len(self.errors) == 0

    def _lint_file(self, file_path: Path) -> None:
        """Lint a single workflow file."""
        print(f"\n📄 Linting {file_path.relative_to(Path.cwd())}...")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip():
                    self.errors.append((str(file_path), "Empty workflow file"))
                    return

                # YAML syntax check
                try:
                    workflow = yaml.safe_load(content)
                except yaml.YAMLError as e:
                    self.errors.append((str(file_path), f"Invalid YAML syntax: {e}"))
                    return

                if not isinstance(workflow, dict):
                    self.errors.append((str(file_path), "Workflow must be a YAML object"))
                    return

                # Security and best practice checks
                self._check_security(file_path, workflow)
                self._check_best_practices(file_path, workflow)

        except Exception as e:
            self.errors.append((str(file_path), f"Failed to read file: {e}"))

    def _check_security(self, file_path: Path, workflow: dict) -> None:
        """Check for security anti-patterns."""
        jobs = workflow.get("jobs", {})
        for job_name, job in jobs.items():
            if not isinstance(job, dict):
                continue
            
            steps = job.get("steps", [])
            for i, step in enumerate(steps):
                if not isinstance(step, dict):
                    continue
                
                # Check for hardcoded secrets
                step_str = str(step)
                if re.search(r"\$\{\{\s*secrets\.\w+\s*\}\}", step_str):
                    # This is actually good practice, skip
                    pass
                
                # Check for curl/wget without --fail
                run_cmd = step.get("run", "")
                if isinstance(run_cmd, str):
                    if re.search(r"\bcurl\b.*-O", run_cmd) and "--fail" not in run_cmd:
                        self.warnings.append((
                            str(file_path),
                            f"Job '{job_name}', step {i+1}: curl without --fail flag"
                        ))
                    
                    # Check for eval/exec of untrusted input
                    if "eval" in run_cmd.lower() or "exec" in run_cmd.lower():
                        self.warnings.append((
                            str(file_path),
                            f"Job '{job_name}', step {i+1}: Potential unsafe eval/exec usage"
                        ))
                    
                    # Check for sudo without justification
                    if "sudo " in run_cmd and "# safe: sudo required" not in run_cmd:
                        self.warnings.append((
                            str(file_path),
                            f"Job '{job_name}', step {i+1}: sudo usage without justification comment"
                        ))
                
                # Check for uses: actions/checkout without token
                if step.get("uses", "").startswith("actions/checkout"):
                    if "token" not in step:
                        self.warnings.append((
                            str(file_path),
                            f"Job '{job_name}', step {i+1}: checkout without explicit token (may have security implications)"
                        ))

    def _check_best_practices(self, file_path: Path, workflow: dict) -> None:
        """Check for best practice violations."""
        # Check for name field
        if "name" not in workflow:
            self.warnings.append((str(file_path), "Missing 'name' field"))
        
        # Check for on field
        if "on" not in workflow:
            self.errors.append((str(file_path), "Missing 'on' field"))
        else:
            on_value = workflow["on"]
            if isinstance(on_value, list) and len(on_value) == 0:
                self.errors.append((str(file_path), "'on' field is empty"))
        
        # Check jobs
        jobs = workflow.get("jobs", {})
        if not jobs:
            self.warnings.append((str(file_path), "No jobs defined"))
        
        for job_name, job in jobs.items():
            if not isinstance(job, dict):
                continue
            
            # Check for runs-on
            if "runs-on" not in job:
                self.errors.append((str(file_path), f"Job '{job_name}' missing 'runs-on'"))
            
            # Check steps
            steps = job.get("steps", [])
            if not steps:
                self.warnings.append((str(file_path), f"Job '{job_name}' has no steps"))
            
            # Check for name on steps
            for i, step in enumerate(steps):
                if isinstance(step, dict) and "name" not in step:
                    self.warnings.append((
                        str(file_path),
                        f"Job '{job_name}', step {i+1}: Missing step name"
                    ))

    def _print_results(self) -> None:
        """Print linting results."""
        print("\n" + "="*60)
        print("LINTING RESULTS")
        print("="*60)
        
        if self.errors:
            print(f"\n❌ {len(self.errors)} ERROR(S):")
            for file_path, error in self.errors:
                print(f"  • {file_path}: {error}")
        else:
            print("\n✅ No errors found!")
        
        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} WARNING(S):")
            for file_path, warning in self.warnings:
                print(f"  • {file_path}: {warning}")
        else:
            print("\n✅ No warnings!")
        
        print("\n" + "="*60)


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Lint GitHub Actions workflows")
    parser.add_argument(
        "--workflows-dir",
        default=".github/workflows",
        help="Path to workflows directory (default: .github/workflows)",
    )
    parser.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Exit with non-zero code if warnings are found",
    )
    
    args = parser.parse_args()
    
    linter = WorkflowLinter(args.workflows_dir)
    success = linter.lint_all()
    
    if not success:
        sys.exit(1)
    
    if args.fail_on_warning and linter.warnings:
        sys.exit(2)


if __name__ == "__main__":
    main()
