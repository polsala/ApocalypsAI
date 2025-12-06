import re
import sys
from typing import List

def sanitize_branch(name: str) -> str:
    """
    Convert an arbitrary string into a Git‑compatible branch name.

    Rules applied:
    * lower‑case
    * spaces, underscores, and any non‑alphanumeric separator become hyphens
    * only keep alphanumerics, hyphens, slashes, and periods
    * collapse consecutive hyphens
    * strip leading/trailing hyphens
    """
    # Lowercase
    s = name.lower()
    # Replace spaces and underscores with hyphens
    s = re.sub(r"[\s_]+", "-", s)
    # Remove disallowed characters (keep alnum, hyphen, slash, period)
    s = re.sub(r"[^a-z0-9\-/.]+", "", s)
    # Collapse multiple hyphens
    s = re.sub(r"-{2,}", "-", s)
    # Strip leading/trailing hyphens
    s = s.strip("-")
    return s

def main(argv: List[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: python -m utils.git-branch-sanitizer.src.sanitizer <branch-name>", file=sys.stderr)
        return 1
    input_name = " ".join(argv)
    print(sanitize_branch(input_name))
    return 0

if __name__ == "__main__":
    sys.exit(main())
