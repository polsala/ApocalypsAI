import os
import yaml
import re
import sys

def check_workflow_file(filepath):
    issues = []
    try:
        with open(filepath, 'r') as f:
            workflow = yaml.safe_load(f)
        if not workflow:
            issues.append("WARNING: Workflow file is empty or invalid YAML.")
            return issues

        # 1. Check for 'on' trigger
        if 'on' not in workflow:
            issues.append("WARNING: Workflow is missing an 'on' trigger.")

        # 2. Check jobs
        if 'jobs' in workflow and isinstance(workflow['jobs'], dict):
            for job_name, job_config in workflow['jobs'].items():
                if not isinstance(job_config, dict):
                    issues.append(f"WARNING: Job '{job_name}' has an invalid configuration.")
                    continue

                # Check for 'runs-on'
                if 'runs-on' not in job_config:
                    issues.append(f"WARNING: Job '{job_name}' is missing 'runs-on'.")

                # Check for steps
                if 'steps' in job_config and isinstance(job_config['steps'], list):
                    for i, step in enumerate(job_config['steps']):
                        if not isinstance(step, dict):
                            issues.append(f"WARNING: Step {i+1} in job '{job_name}' has an invalid configuration.")
                            continue
                        if 'uses' not in step and 'run' not in step:
                            issues.append(f"WARNING: Step '{step.get('name', f'#{i+1}')}' in job '{job_name}' is missing 'uses' or 'run'.")

                        # Check for ::set-output
                        if 'run' in step and '::set-output' in step['run']:
                            issues.append(f"DEPRECATION: Found '::set-output' in step '{step.get('name', f'#{i+1}')}' in job '{job_name}'. Consider using job outputs or environment files.")

                        # Basic hardcoded secret detection (whimsical) in step env
                        if 'env' in step and isinstance(step['env'], dict):
                            for env_var, env_val in step['env'].items():
                                if isinstance(env_val, str) and ('KEY' in env_var.upper() or 'TOKEN' in env_var.upper()):
                                    # Simple heuristic: long alphanumeric string
                                    if len(env_val) > 16 and re.match(r'^[a-zA-Z0-9_-]+$', env_val):
                                        issues.append(f"WHIMSICAL WARNING: Potential hardcoded secret '{env_var}' found in step '{step.get('name', f'#{i+1}')}' in job '{job_name}' env. Consider using GitHub Secrets.")

                # Basic hardcoded secret detection in job env (whimsical)
                if 'env' in job_config and isinstance(job_config['env'], dict):
                    for env_var, env_val in job_config['env'].items():
                        if isinstance(env_val, str) and ('KEY' in env_var.upper() or 'TOKEN' in env_var.upper()):
                            if len(env_val) > 16 and re.match(r'^[a-zA-Z0-9_-]+$', env_val):
                                issues.append(f"WHIMSICAL WARNING: Potential hardcoded secret '{env_var}' found in job '{job_name}' env. Consider using GitHub Secrets.")

    except yaml.YAMLError as e:
        issues.append(f"ERROR: Invalid YAML syntax: {e}")
    except Exception as e:
        issues.append(f"ERROR: An unexpected error occurred: {e}")
    return issues

def main(workflows_dir):
    if not os.path.isdir(workflows_dir):
        print(f"Error: Directory '{workflows_dir}' not found.")
        sys.exit(1)

    print(f"Scanning workflows in {workflows_dir}...")
    all_issues = {}
    for root, _, files in os.walk(workflows_dir):
        for file in files:
            if file.endswith(('.yml', '.yaml')):
                filepath = os.path.join(root, file)
                issues = check_workflow_file(filepath)
                if issues:
                    all_issues[filepath] = issues

    print("\n--- Workflow Wellness Report ---")
    if not all_issues:
        print("All workflows are in peak wellness! No issues found.")
    else:
        for filepath, issues in all_issues.items():
            print(f"\nFile: {filepath}")
            for issue in issues:
                print(f"  - {issue}")
    print("\nAll workflows scanned. May your automation be ever well!")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python oracle.py <path_to_workflows_dir>")
        sys.exit(1)
    main(sys.argv[1])
