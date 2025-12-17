import os
import requests
from datetime import datetime, timedelta
from rich.console import Console

console = Console()

def get_github_api_url(owner, repo, endpoint):
    return f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"

def get_recent_workflow_runs(owner, repo, github_token):
    url = get_github_api_url(owner, repo, "actions/runs")
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    # Fetch runs from the last 7 days to be safe, adjust as needed
    since = (datetime.now() - timedelta(days=7)).isoformat() + 'Z'
    params = {
        "per_page": 100, # Max per page
        "since": since
    }
    all_runs = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        runs = response.json().get('workflow_runs', [])
        all_runs.extend(runs)
        if 'next' in response.links:
            url = response.links['next']['url']
            params = {}
        else:
            break
    return all_runs

def analyze_workflows(runs, failure_threshold, long_run_threshold_minutes):
    failed_runs = []
    long_running_runs = []
    now = datetime.now(timedelta(0).tzinfo) # Use timezone-aware datetime

    for run in runs:
        status = run.get('status')
        conclusion = run.get('conclusion')
        run_started_at = datetime.fromisoformat(run.get('run_started_at').replace('Z', '+00:00'))
        run_duration = now - run_started_at

        # Check for failures
        if status == 'completed' and conclusion == 'failure':
            failed_runs.append(run)

        # Check for long running workflows (only if not completed)
        if status not in ['completed', 'cancelled'] and run_duration.total_seconds() > long_run_threshold_minutes * 60:
            long_running_runs.append({
                'run': run,
                'duration_minutes': run_duration.total_seconds() / 60
            })

    return failed_runs, long_running_runs

def report_alerts(failed_runs, long_running_runs, failure_threshold, long_run_threshold_minutes):
    alert_count = 0

    if len(failed_runs) > failure_threshold:
        console.print(f"[bold red]🚨 ALERT: Too many recent workflow failures![/bold red]")
        console.print(f"Found {len(failed_runs)} failed runs (threshold: {failure_threshold}).")
        for i, run in enumerate(failed_runs):
            if i >= failure_threshold: break # Only report up to threshold for brevity
            console.print(f"  - Workflow: {run.get('name')} (ID: {run.get('id')}) - Status: {run.get('status')}, Conclusion: {run.get('conclusion')}")
            console.print(f"    URL: {run.get('html_url')}")
        alert_count += 1

    if long_running_runs:
        console.print(f"[bold yellow]⏳ ALERT: Long-running workflows detected![/bold yellow]")
        for run_info in long_running_runs:
            run = run_info['run']
            duration = run_info['duration_minutes']
            console.print(f"  - Workflow: {run.get('name')} (ID: {run.get('id')}) has been running for {duration:.2f} minutes (threshold: {long_run_threshold_minutes} min).")
            console.print(f"    URL: {run.get('html_url')}")
        alert_count += 1

    if alert_count == 0:
        console.print("[bold green]✅ All workflows are healthy![/bold green]")

if __name__ == "__main__":
    repo_owner = os.environ.get('REPO_OWNER')
    repo_name = os.environ.get('REPO_NAME')
    failure_threshold = int(os.environ.get('FAILURE_THRESHOLD', 1))
    long_run_threshold_minutes = int(os.environ.get('LONG_RUN_THRESHOLD_MINUTES', 60))
    github_token = os.environ.get('GITHUB_TOKEN')

    if not all([repo_owner, repo_name, github_token]):
        console.print("[bold red]Error: Missing required environment variables (REPO_OWNER, REPO_NAME, GITHUB_TOKEN).[/bold red]")
        exit(1)

    console.print(f"[cyan]Watching workflows for {repo_owner}/{repo_name}...[/cyan]")
    try:
        all_runs = get_recent_workflow_runs(repo_owner, repo_name, github_token)
        failed_runs, long_running_runs = analyze_workflows(all_runs, failure_threshold, long_run_threshold_minutes)
        report_alerts(failed_runs, long_running_runs, failure_threshold, long_run_threshold_minutes)
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error communicating with GitHub API: {e}[/bold red]")
        exit(1)
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
        exit(1)
