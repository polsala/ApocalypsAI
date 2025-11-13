#!/usr/bin/env python3
"""
git-branch-namer: generate a git branch name from a ticket ID and title.
"""

import argparse
import re
import sys


def slugify(text: str) -> str:
    """Convert text to a URL‑friendly slug.

    * Lowercase
    * Replace non‑alphanumeric characters with hyphens
    * Collapse multiple hyphens
    * Strip leading/trailing hyphens
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-{2,}', '-', text)
    return text.strip('-')


def generate_branch_name(
    ticket: str,
    title: str,
    prefix: str = "feature",
    max_len: int = 50,
) -> str:
    """Build a branch name like `feature/ABC-123-add-login-page`.

    Parameters
    ----------
    ticket: str
        Ticket identifier (e.g., "ABC-123").
    title: str
        Human‑readable title.
    prefix: str, optional
        Branch prefix (feature, bugfix, hotfix, etc.).
    max_len: int, optional
        Maximum total length; title part will be truncated if needed.

    Returns
    -------
    str
        The formatted branch name.
    """
    base = f"{prefix}/{ticket}"
    slug = slugify(title)
    # Ensure total length does not exceed max_len
    allowed_slug_len = max_len - len(base) - 1  # minus the separating slash
    if allowed_slug_len < 1:
        # Mock rationale: if prefix+ticket already exceed max_len, we truncate ticket.
        truncated = (prefix + '/' + ticket)[:max_len]
        return truncated.rstrip('/')
    if len(slug) > allowed_slug_len:
        slug = slug[:allowed_slug_len].rstrip('-')
    return f"{base}/{slug}"


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Generate a git branch name.")
    parser.add_argument("--ticket", required=True, help="Ticket identifier (e.g., ABC-123)")
    parser.add_argument("--title", required=True, help="Title of the work")
    parser.add_argument("--prefix", default="feature", help="Branch prefix")
    parser.add_argument("--max-len", type=int, default=50, help="Maximum branch name length")
    return parser.parse_args(argv)


def main():
    args = parse_args()
    branch = generate_branch_name(args.ticket, args.title, args.prefix, args.max_len)
    print(branch)
    return 0

if __name__ == "__main__":
    sys.exit(main())
