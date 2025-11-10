"""
git-branch-namer utility
Generates a clean git branch name from an issue title.
"""

import re
import sys
from typing import List

_STOPWORDS: List[str] = [
    "the", "a", "an", "and", "or", "but", "for", "with", "to", "of", "in", "on", "at",
    "by", "from", "up", "out", "as", "is", "it", "this", "that"
]

def _slugify(text: str) -> str:
    """
    Convert text to a slug:
    * lower‑case
    * replace non‑alphanumeric characters with spaces
    * split into words
    * filter out stop‑words
    * join with hyphens
    * truncate to 50 characters
    """
    # Lower‑case
    text = text.lower()
    # Replace non‑alphanumeric with space
    text = re.sub(r"[^a-z0-9]+", " ", text)
    words = [w for w in text.split() if w and w not in _STOPWORDS]
    slug = "-".join(words)
    # Truncate to 50 characters, avoiding trailing hyphen
    return slug[:50].rstrip("-")

def suggest_branch_name(issue_title: str) -> str:
    """
    Public API: given an issue title, return a git‑compatible branch name.
    """
    return _slugify(issue_title)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m src.branch_namer \"Issue title here\"")
        sys.exit(1)
    print(suggest_branch_name(sys.argv[1]))
