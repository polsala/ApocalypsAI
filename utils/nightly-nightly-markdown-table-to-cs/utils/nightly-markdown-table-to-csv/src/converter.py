import sys
import csv
import re
from typing import List


def _split_pipe_row(row: str) -> List[str]:
    """Split a markdown table row on pipes, stripping surrounding whitespace.

    Empty cells (e.g., leading/trailing pipes) are ignored.
    """
    # Remove leading/trailing pipe if present, then split
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [cell.strip() for cell in row.split("|")]


def _extract_first_table(lines: List[str]) -> List[List[str]]:
    """Return a list of rows (as list of cells) for the first markdown table.

    The function stops parsing once a blank line or a non‑table line is encountered
    after the table has started.
    """
    table_started = False
    table_rows: List[List[str]] = []
    for line in lines:
        if re.match(r"^\s*\|.*\|\s*$", line):
            # This line looks like a table row
            if not table_started:
                table_started = True
            # Skip the separator row (---|---) if present
            if re.match(r"^\s*\|?\s*[-:]+\s*(\|\s*[-:]+\s*)*\|?\s*$", line):
                continue
            table_rows.append(_split_pipe_row(line))
        elif table_started:
            # Table ended
            break
    return table_rows


def markdown_table_to_csv(markdown: str) -> str:
    """Convert the first markdown table in *markdown* to a CSV string.

    If no table is found, returns an empty string.
    """
    lines = markdown.splitlines()
    rows = _extract_first_table(lines)
    if not rows:
        return ""
    output = []
    for row in rows:
        output.append(",".join([csv_escape(cell) for cell in row]))
    return "\n".join(output) + "\n"


def csv_escape(cell: str) -> str:
    """Escape a cell for CSV output according to RFC 4180.

    Cells containing commas, quotes, or newlines are wrapped in double quotes,
    and internal quotes are doubled.
    """
    if any(ch in cell for ch in [',', '"', '\n']):
        cell = cell.replace('"', '""')
        return f'"{cell}"'
    return cell


def main() -> None:
    """Entry‑point for the CLI.

    Reads from a file path passed as the first argument or from stdin when no
    argument is given, converts the first markdown table to CSV, and writes the
    result to stdout.
    """
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        with open(input_path, "r", encoding="utf-8") as f:
            markdown = f.read()
    else:
        markdown = sys.stdin.read()
    csv_output = markdown_table_to_csv(markdown)
    if csv_output:
        sys.stdout.write(csv_output)
    # No output (and no error) when no table is present.


if __name__ == "__main__":
    main()
