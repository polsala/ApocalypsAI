import argparse
import os
import sys
from datetime import datetime, timedelta, timezone
import requests

def get_github_data(url, token):
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status() # Raise an exception for HTTP errors
    return response.json()

def generate_digest(repo_owner, repo_name, github_token, days_back=1):
    # Use UTC for consistent date calculations across environments
    current_utc_time = datetime.now(timezone.utc)
    since_date = (current_utc_time - timedelta(days=days_back)).isoformat(timespec='seconds')

    repo_url = f'https://github.com/{repo_owner}/{repo_name}'
    api_base = f'https://api.github.com/repos/{repo_owner}/{repo_name}'

    digest_output = []
    digest_output.append(f"\n--- The Scroll of Recent Portents ---")
    digest_output.append(f"\nDate: {current_utc_time.strftime('%Y-%m-%d')}")
    digest_output.append(f"Repository: {repo_owner}/{repo_name}\n")

    # --- Issues ---
    digest_output.append("--- New Anomalies Detected (Issues) ---")
    # Filter by `since` parameter to get only recent issues
    issues_url = f'{api_base}/issues?state=all&since={since_date}'
    issues = [issue for issue in get_github_data(issues_url, github_token) if 'pull_request' not in issue]
    if issues:
        for issue in issues:
            title = issue['title']
            number = issue['number']
            state = issue['state']
            html_url = issue['html_url']
            digest_output.append(f"*   [#{number}] {title} ({state}) - {html_url}")
    else:
        digest_output.append("*   No new anomalies detected.")
    digest_output.append("")

    # --- Pull Requests ---
    digest_output.append("--- Convergences Observed (Pull Requests) ---")
    # Filter by `since` parameter to get only recent pull requests
    pulls_url = f'{api_base}/pulls?state=all&since={since_date}'
    pulls = get_github_data(pulls_url, github_token)
    if pulls:
        for pull in pulls:
            title = pull['title']
            number = pull['number']
            state = pull['state']
            html_url = pull['html_url']
            digest_output.append(f"*   [#{number}] {title} ({state}) - {html_url}")
    else:
        digest_output.append("*   No new convergences observed.")
    digest_output.append("")

    # --- Commits ---
    digest_output.append("--- Temporal Fluxes Recorded (Commits) ---")
    # Filter by `since` parameter to get only recent commits
    commits_url = f'{api_base}/commits?since={since_date}'
    commits = get_github_data(commits_url, github_token)
    if commits:
        for commit in commits:
            sha = commit['sha'][:7] # Short SHA
            message = commit['commit']['message'].split('\n')[0] # First line of commit message
            author = commit['commit']['author']['name']
            html_url = commit['html_url']
            digest_output.append(f"*   [{sha}] {message} ({author}) - {html_url}")
    else:
        digest_output.append("*   No new temporal fluxes recorded.")
    digest_output.append("")

    digest_output.append("--- The Oracle has spoken. ---")

    return '\n'.join(digest_output)

def main():
    parser = argparse.ArgumentParser(description='Generate a Nightly Doom Scroll Digest of GitHub repository activity.')
    parser.add_argument('--repo-owner', required=True, help='The owner of the GitHub repository.')
    parser.add_argument('--repo-name', required=True, help='The name of the GitHub repository.')
    parser.add_argument('--github-token', required=True, help='GitHub Personal Access Token.')
    parser.add_argument('--days-back', type=int, default=1, help='Number of days to look back for activity.')

    args = parser.parse_args()

    try:
        digest = generate_digest(
            args.repo_owner,
            args.repo_name,
            args.github_token,
            args.days_back
        )
        print(digest)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
