import subprocess
import datetime
import argparse
import sys

def run_git_command(command, cwd=None):
    """Helper to run git commands and return stdout."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {' '.join(command)}", file=sys.stderr)
        print(f"Stderr: {e.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'git' command not found. Please ensure Git is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)

def get_local_branches(cwd=None):
    """Returns a list of local Git branch names."""
    output = run_git_command(['git', 'branch', '--format=%(refname:short)'], cwd=cwd)
    return [branch for branch in output.split('\n') if branch]

def get_last_commit_date(branch_name, cwd=None):
    """Returns the last commit date for a given branch as a datetime object."""
    try:
        # Using --date=iso-strict for consistent parsing
        date_str = run_git_command(['git', 'log', '-1', '--format=%cd', '--date=iso-strict', branch_name], cwd=cwd)
        # Example format: 2023-10-27T10:30:00+02:00
        # Python's datetime.fromisoformat handles this well.
        return datetime.datetime.fromisoformat(date_str)
    except Exception as e:
        print(f"Warning: Could not get last commit date for branch '{branch_name}': {e}", file=sys.stderr)
        return None

def find_stale_branches(branches, days_stale, current_date, cwd=None):
    """Identifies branches older than 'days_stale' days."""
    stale_branches = []
    for branch in branches:
        last_commit_dt = get_last_commit_date(branch, cwd=cwd)
        if last_commit_dt:
            # Compare just the date part, ignoring timezones for staleness calculation.
            # This is sufficient for 'days stale' and avoids timezone complexities.
            if (current_date.date() - last_commit_dt.date()).days > days_stale:
                stale_branches.append((branch, last_commit_dt.date()))
    return stale_branches

def main():
    parser = argparse.ArgumentParser(
        description="Identify and optionally purge stale local Git branches."
    )
    parser.add_argument(
        '--days', 
        type=int, 
        default=30, 
        help="Number of days after which a branch is considered stale (default: 30)."
    )
    parser.add_argument(
        '--suggest-delete', 
        action='store_true', 
        help="Print 'git branch -d <branch>' commands for stale branches instead of just listing them."
    )
    parser.add_argument(
        '--delete', 
        action='store_true', 
        help="Actually delete stale branches. USE WITH CAUTION!"
    )
    parser.add_argument(
        '--cwd', 
        type=str, 
        default=None, 
        help="Working directory to run git commands in (for testing/specific repos)."
    )

    args = parser.parse_args()

    current_date = datetime.datetime.now()

    print(f"\n--- The Great Git Gremlin is at work! ---")
    print(f"Looking for branches older than {args.days} days as of {current_date.strftime('%Y-%m-%d')}.")

    all_branches = get_local_branches(cwd=args.cwd)
    if not all_branches:
        print("No local Git branches found.")
        sys.exit(0)

    stale_branches = find_stale_branches(all_branches, args.days, current_date, cwd=args.cwd)

    if not stale_branches:
        print("No stale branches found. Your repository is spick and span!")
        sys.exit(0)

    print(f"\nFound {len(stale_branches)} stale branch(es):")
    for branch, date in stale_branches:
        print(f"  - {branch} (last commit: {date})")

    if args.delete:
        print("\nAttempting to delete stale branches...")
        for branch, _ in stale_branches:
            try:
                print(f"  Deleting branch: {branch}")
                # -d only deletes if merged. For unmerged, it requires -D (force), which we don't use by default.
                run_git_command(['git', 'branch', '-d', branch], cwd=args.cwd)
                print(f"    Successfully deleted {branch}")
            except Exception as e:
                print(f"    Failed to delete {branch}: {e}", file=sys.stderr)
        print("\nDeletion attempt complete.")
    elif args.suggest_delete:
        print("\nTo delete these branches, run the following commands (use with caution!):")
        for branch, _ in stale_branches:
            print(f"  git branch -d {branch}")
    else:
        print("\nTo delete these branches, run with '--delete' or '--suggest-delete'.")

    sys.exit(0)

if __name__ == '__main__':
    main()
