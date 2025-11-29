import subprocess
import datetime
import argparse
import os
import sys
from typing import List, Dict

def _run_git_command(repo_path: str, command_args: List[str]) -> str:
    """Helper to run a git command and return its stdout."""
    try:
        result = subprocess.run(
            ['git', '-C', repo_path] + command_args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {' '.join(e.cmd)}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        raise
    except FileNotFoundError:
        print("Error: 'git' command not found. Please ensure Git is installed and in your PATH.", file=sys.stderr)
        raise

def get_all_local_branches(repo_path: str) -> List[str]:
    """Returns a list of all local branch names."""
    output = _run_git_command(repo_path, ['branch', '--format=%(refname:short)'])
    return [branch.strip() for branch in output.split('\n') if branch.strip()]

def get_last_commit_date(repo_path: str, branch_name: str) -> datetime.datetime:
    """Returns the last commit date for a given branch."""
    # Use --date=iso-strict for consistent parsing, which includes timezone info.
    output = _run_git_command(repo_path, ['log', '-1', '--format=%cd', '--date=iso-strict', branch_name])
    # Example format: 2023-10-27T10:30:00+02:00
    # datetime.fromisoformat handles this well, creating a timezone-aware datetime object.
    return datetime.datetime.fromisoformat(output)

def find_stale_branches(repo_path: str, days_threshold: int) -> Dict[str, datetime.datetime]:
    """
    Finds branches that have not been committed to within the last `days_threshold`.

    Args:
        repo_path (str): The path to the Git repository.
        days_threshold (int): The number of days after which a branch is considered stale.

    Returns:
        Dict[str, datetime.datetime]: A dictionary of stale branch names and their last commit dates.
    """
    # Check if the path is a directory and contains a .git directory
    if not os.path.isdir(repo_path) or not os.path.isdir(os.path.join(repo_path, '.git')):
        raise ValueError(f"'{repo_path}' is not a valid Git repository.")

    stale_branches = {}
    current_time = datetime.datetime.now(datetime.timezone.utc) # Use UTC for consistency
    threshold_date = current_time - datetime.timedelta(days=days_threshold)

    branches = get_all_local_branches(repo_path)

    for branch in branches:
        try:
            last_commit_date = get_last_commit_date(repo_path, branch)
            # git log --date=iso-strict provides timezone-aware dates, so direct comparison with current_time (UTC) is fine.
            if last_commit_date < threshold_date:
                stale_branches[branch] = last_commit_date
        except Exception as e:
            # This could happen if a branch is somehow malformed or git log fails for it.
            print(f"Warning: Could not get last commit date for branch '{branch}': {e}", file=sys.stderr)
            continue # Skip this branch if there's an error

    return stale_branches

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Stardust Sweeper: Identifies stale Git branches."
    )
    parser.add_argument(
        '--repo',
        type=str,
        default='.',
        help="Path to the Git repository (default: current directory)."
    )
    parser.add_argument(
        '--days',
        type=int,
        default=90,
        help="Number of days after which a branch is considered stale (default: 90)."
    )
    args = parser.parse_args()

    try:
        stale_branches = find_stale_branches(args.repo, args.days)

        if stale_branches:
            print(f"\n🌌 Stardust Sweeper Report 🌌")
            print(f"The following branches in '{os.path.abspath(args.repo)}' are older than {args.days} days:")
            for branch, date in stale_branches.items():
                print(f"  - {branch} (Last commit: {date.strftime('%Y-%m-%d %H:%M:%S %Z')})")
            print("\nConsider reviewing these branches for potential cleanup.")
        else:
            print(f"\n✨ Repository '{os.path.abspath(args.repo)}' is sparkling clean! No stale branches found older than {args.days} days.")
        
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
