import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple

# Regular expression to capture TODO/FIXME comments.
_COMMENT_RE = re.compile(r"(?P<comment>(?:#|//|/\*)\s*(?:TODO|FIXME)[:\s].*)", re.IGNORECASE)


def _extract_from_file(file_path: Path) -> List[Tuple[int, str]]:
    """Return a list of (line_number, comment_text) for each TODO/FIXME in *file_path*.

    The function reads the file as UTF‑8 text; binary files are ignored.
    """
    todos: List[Tuple[int, str]] = []
    try:
        with file_path.open("r", encoding="utf-8") as f:
            for idx, line in enumerate(f, start=1):
                match = _COMMENT_RE.search(line)
                if match:
                    # Strip comment marker and leading whitespace for readability.
                    comment = match.group("comment")
                    comment = re.sub(r"^(?:#|//|/\*)\s*", "", comment, flags=re.IGNORECASE).strip()
                    todos.append((idx, comment))
    except (UnicodeDecodeError, PermissionError):
        # Non‑text or unreadable files are silently skipped.
        pass
    return todos


def extract_todos(root: Path) -> Dict[Path, List[Tuple[int, str]]]:
    """Recursively walk *root* and collect TODO/FIXME comments.

    Returns a mapping of file paths (relative to *root*) to a list of
    ``(line_number, comment)`` tuples.
    """
    result: Dict[Path, List[Tuple[int, str]]] = {}
    for file_path in root.rglob("*"):
        if file_path.is_file():
            todos = _extract_from_file(file_path)
            if todos:
                result[file_path.relative_to(root)] = todos
    return result


def generate_markdown(report: Dict[Path, List[Tuple[int, str]]]) -> str:
    """Convert *report* into a Markdown table string.

    The table has columns: **File**, **Line**, **Comment**.
    """
    if not report:
        return "# TODO Report\n\n_No TODO/FIXME comments found._\n"
    lines = ["# TODO Report", "", "| File | Line | Comment |", "| ---- | ---- | ------- |"]
    for file_path, entries in sorted(report.items()):
        for line_no, comment in entries:
            lines.append(f"| `{file_path}` | {line_no} | {comment} |")
    lines.append("")
    return "\n".join(lines)


def main(argv: List[str] = None) -> int:
    argv = argv or sys.argv[1:]
    if len(argv) != 2:
        print("Usage: python -m src.extractor <source-dir> <output-md>")
        return 1
    src_dir = Path(argv[0])
    out_md = Path(argv[1])
    if not src_dir.is_dir():
        print(f"Error: source directory '{src_dir}' does not exist or is not a directory.")
        return 1
    report = extract_todos(src_dir)
    markdown = generate_markdown(report)
    out_md.write_text(markdown, encoding="utf-8")
    print(f"✅ Report written to {out_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
