import os
import yaml
import glob
from typing import List, Dict, Any

# Mock rationale: These are static checks, no external services needed.


def find_workflow_files() -> List[str]:
    """Finds all YAML workflow files in the .github/workflows directory."""
    return glob.glob(".github/workflows/*.yml")

def validate_workflow(filepath: str) -> List[str]:
    """Validates a single GitHub Actions workflow file."""
    errors = []
    try:
        with open(filepath, 'r') as f:
            workflow_data = yaml.safe_load(f)
    except Exception as e:
        errors.append(f"Could not parse YAML file: {e}")
        return errors

    if not workflow_data:
        errors.append("Workflow file is empty.")
        return errors

    # Check for overly broad permissions
    permissions = workflow_data.get('jobs', {}).get('runs-on', {}).get('permissions')
    if permissions:
        for job_name, job_details in workflow_data.get('jobs', {}).items():
            job_permissions = job_details.get('permissions')
            if job_permissions:
                if 'contents' in job_permissions and job_permissions['contents'] == 'write':
                    errors.append(f"`{filepath}`: Job '{job_name}' grants `write` permissions to `contents`. Consider using more granular permissions.")
                if 'secrets' in job_permissions and job_permissions['secrets'] == 'write':
                    errors.append(f"`{filepath}`: Job '{job_name}' grants `write` permissions to `secrets`. Consider using more granular permissions.")
                if 'packages' in job_permissions and job_permissions['packages'] == 'write':
                    errors.append(f"`{filepath}`: Job '{job_name}' grants `write` permissions to `packages`. Consider using more granular permissions.")
                if 'id-token' in job_permissions and job_permissions['id-token'] == 'write':
                    errors.append(f"`{filepath}`: Job '{job_name}' grants `write` permissions to `id-token`. Consider using more granular permissions.")

    # Check for common secrets usage that might be too broad
    # This is a simplified check; a more robust solution would involve AST parsing
    # For now, we'll look for common patterns in the run steps
    for job_name, job_details in workflow_data.get('jobs', {}).items():
        steps = job_details.get('steps', [])
        for step in steps:
            if 'run' in step:
                run_script = step['run']
                if "secrets.ANY_SECRET" in run_script or "secrets.GITHUB_TOKEN" in run_script:
                    # This is a very basic check. A real-world scenario might need more context.
                    # For demonstration, we'll flag any use of secrets.ANY_SECRET
                    if "secrets.ANY_SECRET" in run_script:
                        errors.append(f"`{filepath}`: Job '{job_name}' uses `secrets.ANY_SECRET`. This is generally discouraged. Consider using specific secrets.")

    return errors

def main():
    workflow_files = find_workflow_files()
    all_errors: List[str] = []

    if not workflow_files:
        print(":warning: No workflow files found in `.github/workflows/`.")
        exit(0)

    for wf_file in workflow_files:
        errors = validate_workflow(wf_file)
        all_errors.extend(errors)

    if all_errors:
        print("validation_status=failed", flush=True)
        for error in all_errors:
            print(error, flush=True)
    else:
        print("validation_status=success", flush=True)

if __name__ == "__main__":
    main()
