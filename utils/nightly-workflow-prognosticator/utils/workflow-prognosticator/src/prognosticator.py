import os
import argparse
import requests
import json
from typing import Optional, Dict, Any, List, Tuple

# ANSI escape codes for terminal colors
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_RED = '\033[91m'
COLOR_BLUE = '\033[94m'
COLOR_RESET = '\033[0m'

GITHUB_API_BASE = "https://api.github.com"

def get_github_token() -> str:
    """Retrieves the GitHub token from environment variables."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable is not set.")
    return token

def fetch_github_api(url: str, token: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """Helper to make authenticated GET requests to the GitHub API."""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from GitHub API ({url}): {e}")
        return None

def fetch_workflow_runs(
    owner: str,
    repo: str,
    workflow_id_or_name: Optional[str],
    token: str,
    per_page: int = 10
) -> List[Dict[str, Any]]:
    """Fetches recent workflow runs for a given repository and optional workflow."""
    if workflow_id_or_name:
        # First, try to get workflow by name to resolve its ID
        workflows_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/actions/workflows"
        workflows_data = fetch_github_api(workflows_url, token)
        workflow_id = None
        if workflows_data and 'workflows' in workflows_data:
            for wf in workflows_data['workflows']:
                if str(wf['id']) == workflow_id_or_name or wf['name'] == workflow_id_or_name:
                    workflow_id = wf['id']
                    break
        
        if not workflow_id:
            # If it's not a name or a valid ID, assume it's an ID directly
            try:
                workflow_id = int(workflow_id_or_name)
            except ValueError:
                print(f"Warning: Workflow '{workflow_id_or_name}' not found by name or invalid ID format. Skipping.")
                return []

        runs_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs"
    else:
        runs_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/actions/runs"

    params = {"per_page": per_page}
    data = fetch_github_api(runs_url, token, params)
    return data.get('workflow_runs', []) if data else []

def fetch_all_workflows(owner: str, repo: str, token: str) -> List[Dict[str, Any]]:
    """Fetches all active workflows for a given repository."""
    workflows_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/actions/workflows"
    data = fetch_github_api(workflows_url, token)
    return data.get('workflows', []) if data else []

def analyze_runs(runs: List[Dict[str, Any]]) -> Tuple[int, int, int, str, str]:
    """Analyzes a list of workflow runs and provides a prognosis."""
    total_runs = len(runs)
    successful_runs = 0
    failed_runs = 0

    if total_runs == 0:
        return 0, 0, 0, f"{COLOR_BLUE}No recent activity.{COLOR_RESET} No recent runs detected. Is it hibernating for the end times?", "NO_ACTIVITY"

    for run in runs:
        # 'conclusion' is the final state, 'status' is the current state
        if run.get('conclusion') == 'success':
            successful_runs += 1
        elif run.get('conclusion') in ['failure', 'cancelled', 'timed_out', 'stale']:
            failed_runs += 1

    success_rate = (successful_runs / total_runs) * 100 if total_runs > 0 else 0

    prognosis_message = ""
    prognosis_level = ""
    color = COLOR_RESET

    if success_rate == 100:
        prognosis_message = "Excellent! This workflow is a beacon of stability, ready to weather any digital apocalypse!"
        prognosis_level = "EXCELLENT"
        color = COLOR_GREEN
    elif success_rate >= 70:
        prognosis_message = "Stable with minor hiccups. A few glitches in the matrix, but mostly resilient. Keep an eye on it."
        prognosis_level = "STABLE_HICCUPS"
        color = COLOR_YELLOW
    elif success_rate >= 30:
        prognosis_message = "Unstable. This workflow is showing signs of digital fatigue. Intervention might be required."
        prognosis_level = "UNSTABLE"
        color = COLOR_RED
    else:
        prognosis_message = "Critical! Warning! This workflow is in critical condition. Immediate attention is paramount for survival!"
        prognosis_level = "CRITICAL"
        color = COLOR_RED

    return total_runs, successful_runs, failed_runs, f"{color}{prognosis_message}{COLOR_RESET}", prognosis_level

def main():
    parser = argparse.ArgumentParser(
        description="Diagnose GitHub Actions workflow health with a whimsical prognosis."
    )
    parser.add_argument("--repo", required=True, help="The GitHub repository (e.g., octocat/Spoon-Knife).")
    parser.add_argument("--workflow", help="Optional: The name or ID of a specific workflow to analyze.")

    args = parser.parse_args()

    try:
        token = get_github_token()
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

    owner, repo_name = args.repo.split('/')

    if args.workflow:
        print(f"Analyzing workflow '{args.workflow}' in {args.repo}...")
        runs = fetch_workflow_runs(owner, repo_name, args.workflow, token)
        total, success, failed, prognosis, _ = analyze_runs(runs)
        print(f"\n--- Workflow: {args.workflow} ---")
        print(f"  Recent Runs: {total} total, {success} successful, {failed} failed")
        print(f"  Prognosis: {prognosis}")
    else:
        print(f"Analyzing all active workflows in {args.repo}...")
        workflows = fetch_all_workflows(owner, repo_name, token)
        if not workflows:
            print("No active workflows found or unable to fetch workflows.")
            exit(0)

        for wf in workflows:
            print(f"\n--- Workflow: {wf['name']} (ID: {wf['id']}) ---")
            runs = fetch_workflow_runs(owner, repo_name, str(wf['id']), token)
            total, success, failed, prognosis, _ = analyze_runs(runs)
            print(f"  Recent Runs: {total} total, {success} successful, {failed} failed")
            print(f"  Prognosis: {prognosis}")

if __name__ == "__main__":
    main()
