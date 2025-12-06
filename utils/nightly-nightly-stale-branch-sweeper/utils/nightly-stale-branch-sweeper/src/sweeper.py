import argparse
import os
import requests
from datetime import datetime, timedelta, timezone

def get_stale_branches(repo_owner: str, repo_name: str, stale_days: int) -> list[dict]:
    """
    Identifies stale branches in a GitHub repository.

    Args:
        repo_owner (str): The owner of the repository.
        repo_name (str): The name of the repository.
        stale_days (int): The number of days after which a branch is considered stale.

    Returns:
        list[dict]: A list of dictionaries, each representing a stale branch
                    with its name and last commit date.
    """
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable not set.")

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    stale_threshold = datetime.now(timezone.utc) - timedelta(days=stale_days)
    stale_branches = []

    # Fetch all branches
    branches_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/branches"
    page = 1
    while True:
        response = requests.get(branches_url, headers=headers, params={'per_page': 100, 'page': page})
        response.raise_for_status() # Raise an exception for HTTP errors
        branches_data = response.json()

        if not branches_data:
            break

        for branch in branches_data:
            branch_name = branch['name']
            commit_sha = branch['commit']['sha']

            # Fetch commit details to get the commit date
            commit_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{commit_sha}"
            commit_response = requests.get(commit_url, headers=headers)
            commit_response.raise_for_status()
            commit_data = commit_response.json()

            commit_date_str = commit_data['commit']['author']['date']
            commit_date = datetime.fromisoformat(commit_date_str.replace('Z', '+00:00'))

            if commit_date < stale_threshold:
                stale_branches.append({
                    'name': branch_name,
                    'last_commit_date': commit_date.isoformat()
                })
        page += 1
    return stale_branches

def main():
    parser = argparse.ArgumentParser(description="Identify stale branches in a GitHub repository.")
    parser.add_argument('--repo', required=True, help="Repository in 'owner/name' format.")
    parser.add_argument('--stale-days', type=int, default=90, help="Number of days after which a branch is considered stale.")

    args = parser.parse_args()
    repo_owner, repo_name = args.repo.split('/')

    try:
        stale_branches = get_stale_branches(repo_owner, repo_name, args.stale_days)

        if stale_branches:
            print(f"\n--- Stale Branches in {args.repo} (older than {args.stale_days} days) ---")
            for branch in stale_branches:
                print(f"- Branch: {branch['name']}, Last Commit: {branch['last_commit_date']}")
            print("\nConsider reviewing and potentially archiving/deleting these branches.")
        else:
            print(f"No stale branches found in {args.repo} older than {args.stale_days} days. Keep up the good work!")

    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Network or API error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == '__main__':
    main()
