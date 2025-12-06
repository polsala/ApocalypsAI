import argparse
import subprocess
import sys
from pathlib import Path
from typing import List


def _run_git(args: List[str]) -> subprocess.CompletedProcess:
    """Execute a git command and return the CompletedProcess.

    This wrapper exists so tests can monkey‑patch it easily.
    """
    return subprocess.run(["git", *args], capture_output=True, text=True, check=False)


def get_default_branch() -> str:
    """Return the repository's default branch (usually 'main' or 'master').

    It first tries `git symbolic-ref refs/remotes/origin/HEAD` which yields something like
    `refs/remotes/origin/main`. If that fails, it falls back to 'main'.
    """
    result = _run_git(["symbolic-ref", "refs/remotes/origin/HEAD"])
    if result.returncode == 0:
        ref = result.stdout.strip()
        # ref format: refs/remotes/origin/<branch>
        return ref.split('/')[-1]
    # Fallback – common default
    return "main"


def list_merged_branches(default_branch: str) -> List[str]:
    """Return a list of local branches that have been merged into *default_branch*.

    The `git branch --merged <branch>` command lists merged branches, with the current
    branch prefixed by `*`. We strip that marker and filter out the default branch itself.
    """
    result = _run_git(["branch", "--merged", default_branch])
    if result.returncode != 0:
        raise RuntimeError(f"Git error while listing merged branches: {result.stderr.strip()}")
    branches = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("*"):
            line = line[1:].strip()
        if line and line != default_branch:
            branches.append(line)
    return branches


def delete_branches(branches: List[str]) -> None:
    """Delete each branch in *branches* using `git branch -d`.

    Errors are printed but do not abort the whole process – this mirrors the behaviour
    of the interactive `git branch -d` command.
    """
    for branch in branches:
        result = _run_git(["branch", "-d", branch])
        if result.returncode == 0:
            print(f"Deleted branch {branch}")
        else:
            print(f"Failed to delete {branch}: {result.stderr.strip()}", file=sys.stderr)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="List (and optionally delete) local branches merged into the default branch."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Actually delete the merged branches (dry‑run by default).",
    )
    args = parser.parse_args(argv)

    # Ensure we are inside a git repository
    if not Path('.git').exists():
        print("Error: .git directory not found – run inside a Git repository.", file=sys.stderr)
        return 1

    default_branch = get_default_branch()
    try:
        merged = list_merged_branches(default_branch)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 1

    if not merged:
        print("No merged branches found.")
        return 0

    print("Merged branches (excluding default branch):")
    for b in merged:
        print(f"  {b}")

    if args.delete:
        delete_branches(merged)
    else:
        print("(dry‑run) Use --delete to remove these branches.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
