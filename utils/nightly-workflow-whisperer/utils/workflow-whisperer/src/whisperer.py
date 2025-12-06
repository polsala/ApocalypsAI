import os
import yaml
import re

def lint_workflow_file(filepath):
    """Lints a single GitHub Actions workflow file and returns a list of issues/suggestions."""
    issues = []
    try:
        with open(filepath, 'r') as f:
            workflow_content = f.read()
        
        if not workflow_content.strip():
            issues.append(f"[ERROR] File '{os.path.basename(filepath)}' is empty.")
            return issues

        workflow = yaml.safe_load(workflow_content)

        if not isinstance(workflow, dict):
            issues.append(f"[ERROR] File '{os.path.basename(filepath)}' is not a valid YAML dictionary.")
            return issues

        # Rule 1: Missing Workflow Name
        if 'name' not in workflow:
            issues.append(f"[WARNING] Workflow '{os.path.basename(filepath)}' is missing a top-level 'name'. Consider adding one for clarity.")

        jobs = workflow.get('jobs', {})
        if not jobs:
            issues.append(f"[WARNING] Workflow '{os.path.basename(filepath)}' has no jobs defined.")

        for job_id, job_config in jobs.items():
            if not isinstance(job_config, dict):
                issues.append(f"[ERROR] Job '{job_id}' in '{os.path.basename(filepath)}' is not a valid dictionary.")
                continue

            # Rule 2: Missing Job Name
            if 'name' not in job_config:
                issues.append(f"[WARNING] Job '{job_id}' is missing a 'name'. Consider adding one for better readability in the GitHub UI.")

            # Rule 3: Missing runs-on
            if 'runs-on' not in job_config:
                issues.append(f"[WARNING] Job '{job_id}' is missing 'runs-on'. This job will not run.")

            # Rule 4: Outdated actions/checkout
            steps = job_config.get('steps', [])
            if isinstance(steps, list):
                for step in steps:
                    if isinstance(step, dict) and 'uses' in step:
                        uses_action = step['uses']
                        if re.match(r'actions/checkout@v[12]', uses_action):
                            issues.append(f"[SUGGESTION] Job '{job_id}' uses '{uses_action}'. Consider upgrading to 'actions/checkout@v3' or 'v4' for better security and features.")
            else:
                issues.append(f"[ERROR] Steps for job '{job_id}' in '{os.path.basename(filepath)}' is not a valid list.")

        # Rule 5: Unfiltered on: push / on: pull_request
        on_triggers = workflow.get('on', {})
        if isinstance(on_triggers, list):
            if 'push' in on_triggers or 'pull_request' in on_triggers:
                issues.append(f"[SUGGESTION] Workflow '{os.path.basename(filepath)}' triggers on 'push' or 'pull_request' without 'branches' or 'paths'. This can lead to excessive runs. Consider filtering.")
        elif isinstance(on_triggers, dict):
            if 'push' in on_triggers and not (on_triggers['push'] and (on_triggers['push'].get('branches') or on_triggers['push'].get('paths'))):
                issues.append(f"[SUGGESTION] Workflow '{os.path.basename(filepath)}' triggers on 'push' without 'branches' or 'paths'. This can lead to excessive runs. Consider filtering.")
            if 'pull_request' in on_triggers and not (on_triggers['pull_request'] and (on_triggers['pull_request'].get('branches') or on_triggers['pull_request'].get('paths'))):
                issues.append(f"[SUGGESTION] Workflow '{os.path.basename(filepath)}' triggers on 'pull_request' without 'branches' or 'paths'. This can lead to excessive runs. Consider filtering.")

        # Rule 6: Missing concurrency for multiple jobs
        if len(jobs) > 1 and 'concurrency' not in workflow:
            issues.append(f"[SUGGESTION] Workflow '{os.path.basename(filepath)}' has multiple jobs but no 'concurrency' key. Consider adding 'concurrency' to manage parallel runs.")

    except yaml.YAMLError as e:
        issues.append(f"[ERROR] YAML parsing error in '{os.path.basename(filepath)}': {e}")
    except Exception as e:
        issues.append(f"[ERROR] An unexpected error occurred while processing '{os.path.basename(filepath)}': {e}")

    return issues

def find_workflow_files(root_dir):
    """Finds all .yml files in .github/workflows/ within the given root_dir."""
    workflow_dir = os.path.join(root_dir, '.github', 'workflows')
    if not os.path.isdir(workflow_dir):
        return []

    workflow_files = []
    for filename in os.listdir(workflow_dir):
        if filename.endswith(('.yml', '.yaml')):
            workflow_files.append(os.path.join(workflow_dir, filename))
    return workflow_files


def main():
    root_dir = os.getcwd()
    workflow_files = find_workflow_files(root_dir)

    if not workflow_files:
        print(f"No GitHub Actions workflow files found in '{os.path.join(root_dir, '.github', 'workflows')}'")
        return

    all_issues_found = False
    for filepath in workflow_files:
        print(f"Scanning workflow: {filepath}")
        issues = lint_workflow_file(filepath)
        if issues:
            all_issues_found = True
            for issue in issues:
                print(f"  {issue}")
        else:
            print(f"  No issues found.")
    
    if not all_issues_found:
        print("\nAll workflows appear to be in good shape according to the Workflow Whisperer!")


if __name__ == '__main__':
    main()
