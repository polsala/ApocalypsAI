import yaml
import sys
import os
import argparse

def lint_workflow_file(filepath):
    """Lints a single GitHub Actions workflow YAML file."""
    errors = []
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            # Basic YAML syntax check
            yaml.safe_load(content)

            # Whimsical checks for common patterns or potential issues
            if "jobs:" not in content:
                errors.append(f"'{filepath}': Missing 'jobs:' section.")
            if "runs-on:" not in content and "jobs:" in content:
                # Check if any job explicitly defines 'runs-on'
                jobs_data = yaml.safe_load(content).get('jobs', {})
                if not any('runs-on' in job for job in jobs_data.values()):
                    errors.append(f"'{filepath}': No 'runs-on:' defined for any job. Consider adding it.")
            if "actions/checkout@" not in content:
                errors.append(f"'{filepath}': Consider adding 'actions/checkout@' for code checkout.")
            if "name:" not in content:
                errors.append(f"'{filepath}': Missing 'name:' at the top level. Good practice for clarity.")
            if "on: " not in content:
                errors.append(f"'{filepath}': Missing 'on:' trigger. Workflows need triggers.")

    except yaml.YAMLError as e:
        errors.append(f"'{filepath}': Invalid YAML syntax - {e}")
    except FileNotFoundError:
        errors.append(f"'{filepath}': File not found.")
    except Exception as e:
        errors.append(f"'{filepath}': An unexpected error occurred - {e}")

    return errors

def main():
    parser = argparse.ArgumentParser(description='Lint GitHub Actions workflow YAML files.')
    parser.add_argument('--workflow-path', type=str, default='.github/workflows/',
                        help='Directory containing workflow YAML files.')
    args = parser.parse_args()

    workflow_dir = args.workflow_path
    all_errors = []

    if not os.path.isdir(workflow_dir):
        print(f"Error: Workflow directory '{workflow_dir}' not found.", file=sys.stderr)
        sys.exit(1)

    for filename in os.listdir(workflow_dir):
        if filename.endswith('.yml') or filename.endswith('.yaml'):
            filepath = os.path.join(workflow_dir, filename)
            errors = lint_workflow_file(filepath)
            all_errors.extend(errors)

    if all_errors:
        print("\n--- Nightly GitHub Action Lint Checker Findings ---", file=sys.stderr)
        for error in all_errors:
            print(f"- {error}", file=sys.stderr)
        print("---------------------------------------------------", file=sys.stderr)
        sys.exit(1) # Exit with a non-zero status code to fail the job
    else:
        print("All GitHub Actions workflows passed linting!")
        sys.exit(0)

if __name__ == "__main__":
    main()
