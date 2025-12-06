import os
import yaml
import argparse
from typing import List, Dict, Any, Optional

class WorkflowHardener:
    def __init__(self):
        self.findings: Dict[str, List[str]] = {}

    def _add_finding(self, workflow_path: str, message: str):
        if workflow_path not in self.findings:
            self.findings[workflow_path] = []
        self.findings[workflow_path].append(message)

    def _check_concurrency(self, workflow_path: str, workflow_data: Dict[str, Any]):
        """
        Rule: Suggest adding concurrency for pull_request or push triggers.
        """
        on_triggers = workflow_data.get('on', {})
        if isinstance(on_triggers, list):
            has_pr_or_push = 'pull_request' in on_triggers or 'push' in on_triggers
        elif isinstance(on_triggers, dict):
            has_pr_or_push = 'pull_request' in on_triggers or 'push' in on_triggers
        else:
            has_pr_or_push = False

        if has_pr_or_push and 'concurrency' not in workflow_data:
            self._add_finding(
                workflow_path,
                "[WARNING] Workflow triggered by 'pull_request' or 'push' could benefit from 'concurrency'.\n"
                "          Consider adding:\n"
                "          concurrency:\n"
                "            group: ${{ github.workflow }}-${{ github.ref }}\n"
                "            cancel-in-progress: true"
            )

    def _check_checkout_version(self, workflow_path: str, workflow_data: Dict[str, Any]):
        """
        Rule: Recommend actions/checkout@v3 or later.
        """
        jobs = workflow_data.get('jobs', {})
        for job_name, job_data in jobs.items():
            steps = job_data.get('steps', [])
            for step in steps:
                uses = step.get('uses')
                if uses and uses.startswith('actions/checkout@'):
                    version_str = uses.split('@')[1]
                    try:
                        version_num = int(version_str.split('.')[0])
                        if version_num < 3:
                            self._add_finding(
                                workflow_path,
                                f"[WARNING] Job '{job_name}' uses '{uses}'. Consider updating to 'v3' or later for security."
                            )
                    except ValueError:
                        # Handle non-numeric versions like 'main' or 'latest' if needed,
                        # but for now, focus on explicit v1/v2.
                        pass

    def _check_explicit_permissions(self, workflow_path: str, workflow_data: Dict[str, Any]):
        """
        Rule: Suggest adding explicit permissions block for pull_request triggered workflows.
        """
        on_triggers = workflow_data.get('on', {})
        if isinstance(on_triggers, list):
            is_pr_triggered = 'pull_request' in on_triggers
        elif isinstance(on_triggers, dict):
            is_pr_triggered = 'pull_request' in on_triggers
        else:
            is_pr_triggered = False

        if is_pr_triggered and 'permissions' not in workflow_data:
            self._add_finding(
                workflow_path,
                "[WARNING] Workflow triggered by 'pull_request' lacks an explicit 'permissions' block.\n"
                "          Consider adding:\n"
                "          permissions:\n"
                "            contents: read\n"
                "            pull-requests: write # Or other minimal permissions required"
            )


    def harden_workflow(self, workflow_path: str):
        """
        Analyzes a single workflow file for hardening opportunities.
        """
        try:
            with open(workflow_path, 'r') as f:
                workflow_data = yaml.safe_load(f)
            if not isinstance(workflow_data, dict):
                self._add_finding(workflow_path, "[ERROR] Workflow file is not a valid YAML dictionary.")
                return

            self._check_concurrency(workflow_path, workflow_data)
            self._check_checkout_version(workflow_path, workflow_data)
            self._check_explicit_permissions(workflow_path, workflow_data)

        except yaml.YAMLError as e:
            self._add_finding(workflow_path, f"[ERROR] Invalid YAML syntax: {e}")
        except Exception as e:
            self._add_finding(workflow_path, f"[ERROR] An unexpected error occurred: {e}")

    def scan_workflow_directory(self, workflow_dir: str) -> Dict[str, List[str]]:
        """
        Scans all YAML files in the specified directory for hardening opportunities.
        """
        if not os.path.isdir(workflow_dir):
            print(f"Error: Directory '{workflow_dir}' not found.")
            return {}

        print(f"Scanning workflows in {workflow_dir}\n")
        for filename in os.listdir(workflow_dir):
            if filename.endswith(('.yml', '.yaml')):
                workflow_path = os.path.join(workflow_dir, filename)
                self.harden_workflow(workflow_path)

        for path, messages in self.findings.items():
            print(f"--- Findings for {path} ---")
            for msg in messages:
                print(msg)
            print()
        
        if not self.findings:
            print("No hardening opportunities found. Your workflows are resilient!")

        return self.findings

def main():
    parser = argparse.ArgumentParser(
        description="Apocalypse-Proof Your GitHub Actions Workflows!",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--workflow-dir',
        type=str,
        required=True,
        help="Path to the directory containing GitHub Actions workflow files (e.g., .github/workflows/)"
    )
    args = parser.parse_args()

    hardener = WorkflowHardener()
    hardener.scan_workflow_directory(args.workflow_dir)

if __name__ == '__main__':
    main()
