import os
import requests
from datetime import datetime

REPO_OWNER = "polsala"
REPO_NAME = "ApocalypsAI"
GITHUB_API_BASE = "https://api.github.com"

def get_workflow_runs(token: str, owner: str, repo: str) -> dict:
    """Fetches the latest workflow runs for a given repository."""
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not set.")

    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/actions/runs"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching workflow runs: {e}")
        return {}

def analyze_workflows(workflow_data: dict) -> str:
    """Analyzes workflow data and returns a whimsical status report."""
    if not workflow_data or not workflow_data.get('workflow_runs'):
        return "The void stares back. No workflow activity detected. Is this the calm before the storm, or have we already fallen?"

    latest_runs = {}
    # GitHub API returns runs ordered by creation date descending by default.
    # So, the first run encountered for a workflow_id is the latest.
    for run in workflow_data['workflow_runs']:
        workflow_id = run['workflow_id']
        if workflow_id not in latest_runs:
            latest_runs[workflow_id] = run

    all_successful = True
    failing_workflows = []

    for run in latest_runs.values():
        # 'conclusion' is the final state, 'status' is the current state (e.g., 'in_progress', 'completed')
        # We care about 'completed' runs and their 'conclusion'
        if run['status'] == 'completed' and run['conclusion'] != 'success':
            all_successful = False
            run_time_str = run['updated_at'] # updated_at is usually closer to the conclusion time
            run_time = datetime.strptime(run_time_str, "%Y-%m-%dT%H:%M:%SZ")
            failing_workflows.append(
                f"-   {run['name']} ({run['conclusion'].capitalize()} {run_time.strftime('%Y-%m-%d %H:%M:%S')})"
            )

    if all_successful:
        return "The gears of fate grind smoothly. ApocalypsAI operations are nominal. All systems green!"
    else:
        report = "A tremor in the timeline! Critical systems are faltering. Immediate intervention required to avert digital doom!\n\n"
        report += "Failing Workflows:\n"
        report += "\n".join(failing_workflows)
        return report


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set. Please set it to a valid GitHub PAT.")
        exit(1)

    workflow_data = get_workflow_runs(token, REPO_OWNER, REPO_NAME)
    if workflow_data:
        print(analyze_workflows(workflow_data))
    else:
        print("Could not retrieve workflow data. Check your token and network connection.")
        exit(1)


if __name__ == "__main__":
    main()
