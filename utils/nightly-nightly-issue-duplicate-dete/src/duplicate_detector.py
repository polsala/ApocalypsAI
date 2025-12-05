#!/usr/bin/env python3
"""Duplicate Issue Detector

Detects duplicate issue titles based on a similarity ratio.
"""

import argparse
import json
import sys
from difflib import SequenceMatcher
from pathlib import Path
from typing import List, Dict


def similarity(a: str, b: str) -> float:
    """Return a similarity ratio between two strings.

    The ratio is computed using :class:`difflib.SequenceMatcher` and is
    case‑insensitive.
    """
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_duplicates(titles: List[str], threshold: float = 0.8) -> List[List[int]]:
    """Group indices of titles that are similar.

    Parameters
    ----------
    titles:
        List of issue titles.
    threshold:
        Similarity ratio threshold (0‑1). Titles with a ratio >= threshold
        are considered duplicates.

    Returns
    -------
    List[List[int]]
        Each inner list contains indices of titles that belong to the same
        duplicate group.
    """
    groups: List[List[int]] = []
    used: set[int] = set()
    for i, title_i in enumerate(titles):
        if i in used:
            continue
        group = [i]
        for j in range(i + 1, len(titles)):
            if j in used:
                continue
            if similarity(title_i, titles[j]) >= threshold:
                group.append(j)
                used.add(j)
        if len(group) > 1:
            groups.append(group)
            used.update(group)
    return groups


def load_issues(file_path: Path) -> List[Dict]:
    """Load a JSON file containing a list of issue objects.

    The JSON must be a list; each element should be a mapping with at least a
    ``title`` key.
    """
    with file_path.open() as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("JSON must be a list of issue objects")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect duplicate issue titles.")
    parser.add_argument(
        "--issues-file",
        type=Path,
        required=True,
        help="Path to JSON file containing list of issue objects with a 'title' field.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.8,
        help="Similarity threshold (0-1).",
    )
    args = parser.parse_args()

    issues = load_issues(args.issues_file)
    titles = [issue.get("title", "") for issue in issues]
    groups = find_duplicates(titles, args.threshold)

    if not groups:
        print("No duplicate groups found.")
        sys.exit(0)

    print("Duplicate groups:")
    for group in groups:
        print(f"Group {group[0] + 1}:")
        for idx in group:
            print(f"  [{idx}] {titles[idx]}")
    sys.exit(0)


if __name__ == "__main__":
    main()
