import subprocess
import sys
import argparse
import re

def run_git_command(command, check=True, capture_output=True, text=True, cwd=None):
    """Helper to run git commands."""
    try:
        result = subprocess.run(
            command,
            check=check,
            capture_output=capture_output,
            text=text,
            cwd=cwd
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {' '.join(command)}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Git is not installed or not in your PATH.", file=sys.stderr)
        sys.exit(1)

def get_current_branch(cwd=None):
    """Get the name of the current Git branch."""
    result = run_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=cwd)
    return result.stdout.strip()

def get_merged_branches(current_branch, cwd=None):
    """Get a list of local branches merged into the specified branch."""
    # Exclude the current branch itself
    result = run_git_command(['git', 'branch', '--merged', current_branch], cwd=cwd)
    branches = [b.strip() for b in result.stdout.splitlines() if b.strip() and not b.startswith('*')]
    return [b for b in branches if b != current_branch]

def get_gone_remote_branches(cwd=None):
    """Get a list of local branches whose remote tracking branch is gone."""
    # First, prune remote to ensure local tracking info is up-to-date
    # Use --dry-run to just see what would be pruned, not actually prune
    run_git_command(['git', 'remote', 'prune', 'origin', '--dry-run'], cwd=cwd)

    result = run_git_command(['git', 'branch', '-vv'], cwd=cwd)
    gone_branches = []
    for line in result.stdout.splitlines():
        match = re.search(r'^\s*(\S+)\s+.*?\[origin/\S+: gone\]', line)
        if match:
            branch_name = match.group(1)
            if not line.strip().startswith('*'): # Exclude current branch if it's gone (unlikely but possible)
                gone_branches.append(branch_name)
    return gone_branches

def identify_stale_branches(current_branch_name=None, cwd=None):
    """Identify all stale branches."""
    if not current_branch_name:
        current_branch_name = get_current_branch(cwd=cwd)

    merged_branches = set(get_merged_branches(current_branch_name, cwd=cwd))
    gone_remote_branches = set(get_gone_remote_branches(cwd=cwd))

    stale_branches = sorted(list(merged_branches.union(gone_remote_branches)))
    return stale_branches

def delete_branches(branches, dry_run=False, cwd=None):
    """Delete a list of branches."""
    if not branches:
        print("No branches to delete.")
        return

    print(f"{'[DRY RUN] ' if dry_run else ''}Attempting to delete the following branches:")
    for branch in branches:
        print(f"  - {branch}")

    if dry_run:
        print("\n(Dry run complete. No changes were made.)")
        return

    print("\nConfirm deletion? (y/N): ", end='')
    confirmation = input().strip().lower()

    if confirmation == 'y':
        for branch in branches:
            print(f"Deleting branch: {branch}...")
            result = run_git_command(['git', 'branch', '-D', branch], check=False, cwd=cwd)
            if result.returncode == 0:
                print(f"Successfully deleted {branch}")
            else:
                print(f"Failed to delete {branch}: {result.stderr.strip()}", file=sys.stderr)
    else:
        print("Deletion cancelled.")

def main():
    parser = argparse.ArgumentParser(
        description="Git Gremlin Groomer: Clean up stale local Git branches."
    )
    parser.add_argument(
        '--list', '-l', action='store_true',
        help="List all identified stale branches (default if no action specified)."
    )
    parser.add_argument(
        '--delete', '-d', action='store_true',
        help="Prompt to delete identified stale branches."
    )
    parser.add_argument(
        '--dry-run', '-n', action='store_true',
        help="Show what *would* be deleted without actually deleting anything."
    )
    parser.add_argument(
        '--current-branch', type=str,
        help="Specify the branch to compare against for 'merged' status (defaults to current HEAD)."
    )

    args = parser.parse_args()

    stale_branches = identify_stale_branches(current_branch_name=args.current_branch)

    if not stale_branches:
        print("No stale branches found. Your repository is pristine! ✨")
        sys.exit(0)

    if args.delete:
        delete_branches(stale_branches, dry_run=args.dry_run)
    elif args.list or not (args.list or args.delete):
        print("Found the following stale branches:")
        for branch in stale_branches:
            print(f"  - {branch}")
        if args.dry_run:
            print("\n(Dry run complete. No changes were made.)")

if __name__ == '__main__':
    main()
