import os
import yaml
import glob
from rich.console import Console

console = Console()

def get_workflow_files():
    """Finds all workflow YAML files in the .github/workflows directory."""
    return glob.glob('.github/workflows/*.yml')

def analyze_workflow(filepath):
    """Analyzes a single workflow file for potential issues."""
    findings = []
    try:
        with open(filepath, 'r') as f:
            workflow_data = yaml.safe_load(f)

        workflow_name = os.path.basename(filepath)

        # Check for missing 'runs-on' in jobs
        if 'jobs' in workflow_data:
            for job_name, job_details in workflow_data['jobs'].items():
                if 'runs-on' not in job_details:
                    findings.append(f"- Job '{job_name}' in '{workflow_name}' is missing a 'runs-on' key. It might wander aimlessly!")

        # Check for overly broad cron schedules (e.g., every minute)
        if 'on' in workflow_data and 'schedule' in workflow_data['on']:
            for schedule in workflow_data['on']['schedule']:
                if schedule == '* * * * *':
                    findings.append(f"- Workflow '{workflow_name}' has a very frequent cron schedule ('* * * * *'). Is it trying to outrun the apocalypse? Consider a less frantic pace.")

        # Check for missing permissions (basic check)
        if 'jobs' in workflow_data:
            for job_name, job_details in workflow_data['jobs'].items():
                if 'permissions' not in job_details and 'uses' not in job_details and 'run' not in job_details:
                    findings.append(f"- Job '{job_name}' in '{workflow_name}' might benefit from explicit 'permissions' to ensure it has the necessary access.")

    except yaml.YAMLError as e:
        findings.append(f"- Could not parse '{workflow_name}': {e}. Perhaps it's speaking an ancient dialect?")
    except Exception as e:
        findings.append(f"- An unexpected error occurred while analyzing '{workflow_name}': {e}. The digital ether is unpredictable!")

    return findings

def main():
    """Main function to orchestrate the workflow analysis."""
    all_findings = []
    workflow_files = get_workflow_files()

    if not workflow_files:
        console.print("No workflow files found in .github/workflows/. The guardian angel is resting.")
        return

    console.print(f"[bold green]Guardian Angel is surveying your workflows...[/bold green]")

    for wf_file in workflow_files:
        workflow_findings = analyze_workflow(wf_file)
        if workflow_findings:
            all_findings.extend(workflow_findings)

    if all_findings:
        report_body = "Greetings, fellow traveler of the digital wasteland! Your friendly Workflow Guardian Angel has surveyed your automated paths. Here are a few observations to ponder:\n\n" + "\n".join(all_findings) + "\n\nKeep up the good work in navigating the chaos!"
        print(f"::set-output name=findings::{report_body}")
        console.print(f"[bold yellow]Guardian Angel found some points of interest![/bold yellow]")
    else:
        console.print("[bold green]All workflows appear to be in good spirits! The Guardian Angel is pleased.[/bold green]")

if __name__ == "__main__":
    main()
