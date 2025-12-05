import subprocess
import os
from collections import Counter
from datetime import datetime, timedelta

def _run_git_command(repo_path, command_args):
    """Helper to run git commands."""
    try:
        result = subprocess.run(
            ['git'] + command_args,
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git command failed: {' '.join(command_args)}\n{e.stderr}")
    except FileNotFoundError:
        raise RuntimeError("Git command not found. Is Git installed and in your PATH?")

def get_git_glimpse_summary(repo_path: str, days: int = 7, top_authors: int = 3) -> str:
    """
    Generates a concise summary of recent Git activity for a given repository.

    Args:
        repo_path: The path to the Git repository.
        days: The number of past days to consider for recent activity.
        top_authors: The number of top active authors to list.

    Returns:
        A formatted string summarizing the Git activity.
    """
    if not os.path.isdir(repo_path):
        return f"Error: Repository path '{repo_path}' does not exist."

    try:
        # Check if it's a Git repository
        _run_git_command(repo_path, ['rev-parse', '--is-inside-work-tree'])
    except RuntimeError:
        return f"Error: '{repo_path}' is not a valid Git repository."

    summary_parts = []
    summary_parts.append(f"--- Git Glimpse Report for '{os.path.basename(repo_path)}' ---")

    # Total commits
    try:
        total_commits = _run_git_command(repo_path, ['rev-list', '--count', 'HEAD'])
        summary_parts.append(f"Total Commits: {total_commits}")
    except RuntimeError as e:
        summary_parts.append(f"Total Commits: N/A ({e})")

    # Recent commits
    since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    try:
        recent_commits_output = _run_git_command(repo_path, ['log', '--pretty=format:%h %an %s', f'--since={since_date}'])
        recent_commits = recent_commits_output.split('\n') if recent_commits_output else []
        summary_parts.append(f"Recent Commits (last {days} days): {len(recent_commits)}")
        if recent_commits:
            for commit in recent_commits[:5]: # Show up to 5 recent commits
                summary_parts.append(f"  - {commit}")
            if len(recent_commits) > 5:
                summary_parts.append(f"  ... and {len(recent_commits) - 5} more.")
        else:
            summary_parts.append("  No recent commits.")
    except RuntimeError as e:
        summary_parts.append(f"Recent Commits (last {days} days): N/A ({e})")

    # Top authors
    try:
        authors_output = _run_git_command(repo_path, ['log', '--pretty=format:%an', f'--since={since_date}'])
        authors = [a.strip() for a in authors_output.split('\n') if a.strip()]
        author_counts = Counter(authors)
        summary_parts.append(f"Top Active Authors (last {days} days):")
        if author_counts:
            for author, count in author_counts.most_common(top_authors):
                summary_parts.append(f"  - {author} ({count} commits)")
        else:
            summary_parts.append("  No active authors.")
    except RuntimeError as e:
        summary_parts.append(f"Top Active Authors: N/A ({e})")

    # Active branches
    try:
        branches_output = _run_git_command(repo_path, ['branch', '--list', '--sort=-committerdate', '--format=%(refname:short) (last commit: %(committerdate:relative))'])
        branches = [b.strip() for b in branches_output.split('\n') if b.strip()]
        summary_parts.append("Recently Active Branches:")
        if branches:
            for branch in branches[:3]: # Show up to 3 active branches
                summary_parts.append(f"  - {branch}")
            if len(branches) > 3:
                summary_parts.append(f"  ... and {len(branches) - 3} more.")
        else:
            summary_parts.append("  No branches found.")
    except RuntimeError as e:
        summary_parts.append(f"Recently Active Branches: N/A ({e})")

    summary_parts.append("------------------------------------------")
    return "\n".join(summary_parts)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a concise summary of recent Git activity for a repository."
    )
    parser.add_argument(
        "repo_path",
        type=str,
        help="The path to the Git repository."
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of past days to consider for recent activity (default: 7)."
    )
    parser.add_argument(
        "--top-authors",
        type=int,
        default=3,
        help="Number of top active authors to list (default: 3)."
    )

    args = parser.parse_args()
    print(get_git_glimpse_summary(args.repo_path, args.days, args.top_authors))
