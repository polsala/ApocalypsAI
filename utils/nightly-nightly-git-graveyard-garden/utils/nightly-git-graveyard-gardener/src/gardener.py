import subprocess
import argparse
from datetime import datetime, timedelta
import sys

def run_git_command(command, cwd=None):
    """Runs a git command and returns its stdout, or raises an error."""
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
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'git' command not found. Is Git installed and in your PATH?", file=sys.stderr)
        sys.exit(1)

def get_local_branches(cwd=None):
    """Returns a list of all local branch names."""
    output = run_git_command(['git', 'branch', '--format=%(refname:short)'], cwd=cwd)
    return [branch for branch in output.split('\n') if branch]

def get_merged_branches(current_branch, cwd=None):
    """Returns a list of local branches merged into the specified current_branch."""
    output = run_git_command(['git', 'branch', '--merged', '--format=%(refname:short)'], cwd=cwd)
    merged_branches = [branch for branch in output.split('\n') if branch]
    # Exclude the current branch itself if it appears in the merged list
    return [b for b in merged_branches if b != current_branch]

def get_current_branch(cwd=None):
    """Returns the name of the current active branch."""
    try:
        return run_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=cwd)
    except SystemExit:
        # Handle cases where HEAD is detached (e.g., during rebase or specific CI environments)
        return "HEAD" # Indicate detached HEAD, which should not be deleted

def get_last_commit_date(branch_name, cwd=None):
    """Returns the last commit date of a branch as a datetime object."""
    # %at: author date as UNIX timestamp
    timestamp_str = run_git_command(['git', 'log', branch_name, '-1', '--format=%at'], cwd=cwd)
    return datetime.fromtimestamp(int(timestamp_str))

def delete_branch(branch_name, force=False, cwd=None):
    """Deletes a local branch."""
    command = ['git', 'branch', '-d', branch_name]
    if force:
        command = ['git', 'branch', '-D', branch_name]
    print(f"Deleting branch: {branch_name}")
    run_git_command(command, cwd=cwd)

def main():
    parser = argparse.ArgumentParser(
        description="Prune your local Git branches. Identifies and optionally deletes stale or merged branches."
    )
    parser.add_argument(
        '--merged',
        action='store_true',
        help="Include branches that are already merged into the current HEAD."
    )
    parser.add_argument(
        '--days',
        type=int,
        help="Include branches whose last commit is older than N days."
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Show what would be deleted without actually deleting anything."
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help="Delete branches without asking for confirmation. Use with extreme caution!"
    )
    parser.add_argument(
        '--current-branch',
        type=str,
        help=argparse.SUPPRESS # Hidden argument for testing/specific scenarios
    )

    args = parser.parse_args()

    cwd = '.' # Assume current working directory is the repo root

    current_branch = args.current_branch if args.current_branch else get_current_branch(cwd=cwd)
    all_local_branches = get_local_branches(cwd=cwd)
    
    branches_to_consider = set(all_local_branches)
    
    # Always exclude the current branch from deletion consideration
    if current_branch in branches_to_consider:
        branches_to_consider.remove(current_branch)

    deletable_branches = set()

    if args.merged:
        merged_branches = get_merged_branches(current_branch, cwd=cwd)
        deletable_branches.update(b for b in merged_branches if b in branches_to_consider)

    if args.days is not None:
        now = datetime.now()
        stale_threshold = now - timedelta(days=args.days)
        
        for branch in list(branches_to_consider): # Iterate over a copy to allow modification if needed, though not strictly necessary here
            if branch in deletable_branches: # Already marked for deletion by --merged, no need to re-check date
                continue
            try:
                last_commit_date = get_last_commit_date(branch, cwd=cwd)
                if last_commit_date < stale_threshold:
                    deletable_branches.add(branch)
            except SystemExit:
                # Handle cases where branch might not exist or git log fails for some reason
                print(f"Warning: Could not get commit date for branch '{branch}'. Skipping.", file=sys.stderr)
                pass

    if not deletable_branches:
        print("No deletable branches found based on the criteria.")
        sys.exit(0)

    print("\n--- Branches identified for pruning ---")
    for branch in sorted(list(deletable_branches)):
        print(f"- {branch}")
    print("-------------------------------------\n")

    if args.dry_run:
        print("Dry run complete. No branches were deleted.")
        sys.exit(0)

    if not args.force:
        confirmation = input("Proceed with deletion? (y/N): ").strip().lower()
        if confirmation != 'y':
            print("Deletion cancelled.")
            sys.exit(0)

    for branch in sorted(list(deletable_branches)):
        delete_branch(branch, force=args.force, cwd=cwd)
    
    print("\nPruning complete. Your Git graveyard is now a little tidier! 🌿")

if __name__ == '__main__':
    main()
