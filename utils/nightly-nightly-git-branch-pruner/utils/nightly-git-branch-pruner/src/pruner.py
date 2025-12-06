#!/usr/bin/env python3
"""git‑branch‑pruner – list (and optionally delete) local branches merged into a base.

The script is deliberately dependency‑light: only the standard library and the optional
`rich` package for colourful output. All external interactions are performed via
`subprocess.run` which is mocked in the test suite, keeping the utility fully offline
for CI.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Set

# Optional pretty printing – fall back to plain text if Rich is unavailable.
try:
    from rich.console import Console
    from rich.table import Table
    console = Console()
except Exception:  # pragma: no cover – Rich is optional.
    console = None


def run_git(args: List[str]) -> subprocess.CompletedProcess:
    """Execute a git command and return the CompletedProcess.

    All calls are routed through this helper so that tests can patch it easily.
    """
    return subprocess.run(["git"] + args, capture_output=True, text=True, check=False)


def get_merged_branches(base: str) -> Set[str]:
    """Return a set of local branch names that are merged into *base*.

    The function runs `git branch --merged <base>` and parses the output.
    """
    result = run_git(["branch", "--merged", base])
    if result.returncode != 0:
        raise RuntimeError(f"Git error while listing merged branches: {result.stderr.strip()}")
    branches = set()
    for line in result.stdout.splitlines():
        # Output format: "  branch-name" or "* current-branch"
        name = line.strip().lstrip("* ")
        if name:
            branches.add(name)
    return branches


def filter_protected(branches: Set[str], protect: Set[str]) -> Set[str]:
    """Remove protected branch names from the set.

    `protect` may contain the base branch itself and any other branches the user
    wants to keep untouched.
    """
    return {b for b in branches if b not in protect}


def delete_branches(branches: Set[str]) -> None:
    """Delete each branch in *branches* using `git branch -d`.

    The function prompts the user for confirmation before proceeding. In a CI
    environment you can pass `--delete` and pipe `yes` to auto‑confirm.
    """
    if not branches:
        return
    if console:
        console.print(f"[bold red]Deleting {len(branches)} merged branch(es):[/bold red]")
        for b in sorted(branches):
            console.print(f"  - {b}")
    else:
        print(f"Deleting {len(branches)} merged branch(es):")
        for b in sorted(branches):
            print(f"  - {b}")
    confirm = input("Proceed? (y/N): ")
    if confirm.lower() != "y":
        print("Aborted by user.")
        return
    for branch in branches:
        result = run_git(["branch", "-d", branch])
        if result.returncode != 0:
            # If -d fails (e.g., branch not fully merged), try -D force delete.
            result = run_git(["branch", "-D", branch])
        if console:
            console.print(result.stdout.strip() or result.stderr.strip())
        else:
            print(result.stdout.strip() or result.stderr.strip())


def pretty_print(branches: Set[str]) -> None:
    """Display the list of branches in a nice table (Rich) or plain text."""
    if not branches:
        msg = "No merged branches to prune."
        if console:
            console.print(f"[green]{msg}[/green]")
        else:
            print(msg)
        return
    if console:
        table = Table(title="Merged Branches Ready for Pruning")
        table.add_column("Branch", style="cyan")
        for b in sorted(branches):
            table.add_row(b)
        console.print(table)
    else:
        print("Merged branches ready for pruning:")
        for b in sorted(branches):
            print(f"  - {b}")


def parse_protect(arg: str) -> Set[str]:
    return {p.strip() for p in arg.split(",") if p.strip()}


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="List (and optionally delete) local branches merged into a base branch.")
    parser.add_argument("--base", default="main", help="Base branch to compare against (default: main)")
    parser.add_argument("--delete", action="store_true", help="Delete the merged branches after confirmation")
    parser.add_argument("--protect", default="", help="Comma‑separated list of branches never to delete (e.g., develop,staging)")
    args = parser.parse_args(argv)

    protect_set = {args.base} | parse_protect(args.protect)
    try:
        merged = get_merged_branches(args.base)
    except RuntimeError as e:
        print(e, file=sys.stderr)
        return 1
    to_prune = filter_protected(merged, protect_set)
    pretty_print(to_prune)
    if args.delete:
        delete_branches(to_prune)
    return 0


if __name__ == "__main__":
    sys.exit(main())
