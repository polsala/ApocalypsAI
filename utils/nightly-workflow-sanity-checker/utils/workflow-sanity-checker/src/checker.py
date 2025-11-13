import os
import yaml
import sys

class WorkflowSanityChecker:
    def __init__(self, base_path="."):
        self.base_path = base_path
        self.workflow_dir = os.path.join(self.base_path, ".github", "workflows")
        self.issues = []

    def _add_issue(self, level, file_path, message):
        self.issues.append(f"[{level}] {file_path}: {message}")

    def _find_workflow_files(self):
        if not os.path.isdir(self.workflow_dir):
            return []
        workflow_files = []
        for root, _, files in os.walk(self.workflow_dir):
            for file in files:
                if file.endswith(('.yml', '.yaml')):
                    workflow_files.append(os.path.join(root, file))
        return workflow_files

    def _check_workflow(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            workflow = yaml.safe_load(content)
            if not isinstance(workflow, dict):
                self._add_issue("ERROR", file_path, "Workflow file is not a valid YAML dictionary.")
                return

            # Check 1: Presence of 'on:' trigger
            if 'on' not in workflow:
                self._add_issue("ERROR", file_path, "Missing 'on:' trigger.")

            # Check 2: Presence of 'jobs:' section
            if 'jobs' not in workflow:
                self._add_issue("ERROR", file_path, "Missing 'jobs:' section.")
                return # Cannot proceed with job-specific checks without 'jobs'

            # Check 3 & 4: Job structure and action versioning
            for job_name, job_config in workflow['jobs'].items():
                if not isinstance(job_config, dict):
                    self._add_issue("ERROR", file_path, f"Job '{job_name}' is not a valid dictionary.")
                    continue

                if 'runs-on' not in job_config:
                    self._add_issue("ERROR", file_path, f"Job '{job_name}': Missing 'runs-on' key.")
                if 'steps' not in job_config:
                    self._add_issue("ERROR", file_path, f"Job '{job_name}': Missing 'steps' key.")
                    continue

                for i, step in enumerate(job_config['steps']):
                    if isinstance(step, dict) and 'uses' in step:
                        action_path = step['uses']
                        if '@' not in action_path:
                            step_name = step.get('name', f"Step {i+1}")
                            self._add_issue("WARNING", file_path,
                                             f"Job '{job_name}': Step '{step_name}': Action '{action_path}' should specify a version (e.g., '{action_path}@v3').")

            # Check 5: Permissions block recommendation
            if 'permissions' not in workflow:
                self._add_issue("INFO", file_path, "Consider adding an explicit 'permissions' block for better security.")

        except yaml.YAMLError as e:
            self._add_issue("ERROR", file_path, f"Invalid YAML syntax: {e}")
        except Exception as e:
            self._add_issue("ERROR", file_path, f"An unexpected error occurred: {e}")

    def run_checks(self):
        print(f"Scanning workflows in {self.workflow_dir}...")
        workflow_files = self._find_workflow_files()

        if not workflow_files:
            print("No workflow files found. Ensure you are in the repository root and .github/workflows exists.")
            return False

        for file_path in workflow_files:
            self._check_workflow(file_path)

        if self.issues:
            for issue in self.issues:
                print(issue)
            print(f"\nFound {len(self.issues)} issues. Please review.")
            return False
        else:
            print("[SUCCESS] All workflows appear sane. The apocalypse can wait... for now.")
            return True

if __name__ == "__main__":
    # Allow running from any directory, but assume .github/workflows is relative to current
    # For testing, we might pass a different base_path
    checker = WorkflowSanityChecker()
    if not checker.run_checks():
        sys.exit(1) # Exit with non-zero code if issues found
