"""
markdown-toc-generator

Provides a function to generate a Markdown Table of Contents from a string
containing Markdown content. Also offers a simple CLI for file‑based usage.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


def _slugify(text: str) -> str:
    """
    Convert heading text to a GitHub‑compatible slug.
    """
    # Lowercase, replace spaces with hyphens, remove non‑alphanum except hyphens
    slug = re.sub(r"[^\w\- ]+", "", text).strip().lower()
    slug = re.sub(r"\s+", "-", slug)
    return slug


def _extract_headings(md: str) -> List[Tuple[int, str]]:
    """
    Return a list of (level, title) tuples for ATX headings.
    """
    headings: List[Tuple[int, str]] = []
    for line in md.splitlines():
        match = re.match(r"^(#{1,6})\s+(.*)", line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            headings.append((level, title))
    return headings


def generate_toc(md: str) -> str:
    """
    Generate a Markdown TOC from the given markdown text.

    Example
    -------
    >>> md = "# Title\n## Section\n"
    >>> print(generate_toc(md))
    - [Title](#title)
      - [Section](#section)
    """
    headings = _extract_headings(md)
    if not headings:
        return ""

    toc_lines: List[str] = []
    for level, title in headings:
        indent = "  " * (level - 1)
        slug = _slugify(title)
        toc_lines.append(f"{indent}- [{title}](#{slug})")
    return "\n".join(toc_lines)


def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m utils.markdown-toc-generator.src.generator <markdown-file>")
        sys.exit(1)
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"File not found: {path}")
        sys.exit(1)
    md = path.read_text(encoding="utf-8")
    toc = generate_toc(md)
    print(toc)

if __name__ == "__main__":
    _cli()
