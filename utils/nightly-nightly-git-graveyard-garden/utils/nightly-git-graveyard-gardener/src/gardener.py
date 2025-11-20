import subprocess
import sys
import os
import argparse

def _run_git_command(command, check=True, capture_output=True, text=True):
    """Helper to run git commands."""
    try:
        result = subprocess.run(
            ['git'] + command,
            check=check,
            capture_output=capture_output,
            text=text,
            cwd=os.getcwd() # Ensure command runs in current directory
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {' '.join(['git'] + command)}", file=sys.stderr)
        print(f"Stdout: {e.stdout}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'git' command not found. Please ensure Git is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)

def is_git_repo():
    """Checks if the current directory is a Git repository."""
    result = _run_git_command(['rev-parse', '--is-inside-work-tree'], check=False, capture_output=True)
    return result.returncode == 0 and 'true' in result.stdout

def get_current_branch():
    """Gets the name of the current active branch."""
    result = _run_git_command(['rev-parse', '--abbrev-ref', 'HEAD'])
    return result.stdout.strip()

def fetch_remote():
    """Fetches from the remote and prunes stale remote-tracking branches."""
    print("\nFetching from remote and pruning stale remote-tracking branches...")
    _run_git_command(['fetch', '--prune'], check=False) # fetch --prune can fail if no remote, but that's fine
    print("Fetch complete.")

def get_local_branches():
    """Returns a list of all local branch names, excluding the current one."""
    current_branch = get_current_branch()
    result = _run_git_command(['branch', '--format=%(refname:short)'])
    branches = [b.strip() for b in result.stdout.splitlines() if b.strip() and b.strip() != current_branch]
    return branches

def get_merged_branches(current_branch):
    """Returns a list of local branches that have been merged into the current branch."""
    result = _run_git_command(['branch', '--merged', current_branch, '--format=%(refname:short)'])
    merged_branches = [b.strip() for b in result.stdout.splitlines() if b.strip() and b.strip() != current_branch]
    return merged_branches

def get_remote_deleted_branches():
    """Returns a list of local branches that no longer exist on the remote."""
    # Get all local branches
    local_branches = set(get_local_branches())

    # Get all remote branches (e.g., origin/main, origin/feature)
    result = _run_git_command(['branch', '-r', '--format=%(refname:short)'])
    remote_branches_full = [b.strip() for b in result.stdout.splitlines() if b.strip()]

    # Extract just the branch names from remote branches (e.g., 'main' from 'origin/main')
    # Assuming 'origin' as the default remote, but could be generalized.
    remote_branch_names = set()
    for rb in remote_branches_full:
        if '/' in rb:
            remote_branch_names.add(rb.split('/', 1)[1])

    deleted_branches = []
    for lb in local_branches:
        if lb not in remote_branch_names:
            deleted_branches.append(lb)
    return deleted_branches

def delete_branches(branches, dry_run, force):
    """Deletes the specified local branches."""
    if not branches:
        print("No branches to delete.")
        return

    print("\nBranches to be deleted:")
    for branch in branches:
        print(f"  - {branch}")

    if dry_run:
        print("\n(Dry run) No branches were actually deleted.")
        return

    if not force:
        confirmation = input("\nProceed with deletion? (y/N): ").lower()
        if confirmation != 'y':
            print("Deletion cancelled.")
            return

    print("\nDeleting branches...")
    for branch in branches:
        print(f"  Deleting branch: {branch}")
        _run_git_command(['branch', '-D', branch])
    print("Branches deleted successfully.")

def prune_remote_tracking_branches(dry_run):
    """Prunes remote-tracking branches that no longer exist on the remote."""
    print("\nPruning stale remote-tracking branches (e.g., origin/feature-x if feature-x is gone from remote)...")
    if dry_run:
        print("(Dry run) Remote-tracking branches would have been pruned.")
        return
    
    # git remote prune origin will show what it's doing
    _run_git_command(['remote', 'prune', 'origin'], check=False) 
    print("Remote-tracking branches pruned.")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Git Graveyard Gardener: Prune stale local Git branches."
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help="Show what would be deleted without performing any actions."
    )
    parser.add_argument(
        '--force', action='store_true',
        help="Delete branches without asking for confirmation."
    )
    parser.add_argument(
        '--no-prune-remote', action='store_true',
        help="Skip pruning remote-tracking branches."
    )
    args = parser.parse_args()

    if not is_git_repo():
        print("Error: Not inside a Git repository.", file=sys.stderr)
        sys.exit(1)

    fetch_remote()

    current_branch = get_current_branch()
    print(f"Current branch: {current_branch}")

    # Identify merged branches
    merged_branches = get_merged_branches(current_branch)
    print(f"\nFound {len(merged_branches)} local branches merged into '{current_branch}':")
    for branch in merged_branches:
        print(f"  - {branch}")

    # Identify local branches whose remote counterparts have been deleted
    remote_deleted_branches = get_remote_deleted_branches()
    print(f"\nFound {len(remote_deleted_branches)} local branches whose remote counterparts are gone:")
    for branch in remote_deleted_branches:
        print(f"  - {branch}")

    branches_to_delete = sorted(list(set(merged_branches + remote_deleted_branches)))

    delete_branches(branches_to_delete, args.dry_run, args.force)

    if not args.no_prune_remote:
        prune_remote_tracking_branches(args.dry_run)

    print("\nGit Graveyard Gardening complete! Your repository is now tidier.")

if __name__ == '__main__':
    main()
