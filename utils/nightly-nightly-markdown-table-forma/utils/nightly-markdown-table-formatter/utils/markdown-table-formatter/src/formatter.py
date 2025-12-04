import csv
from typing import List


def _format_row(row: List[str]) -> str:
    """Return a Markdown table row from a list of cell values."""
    return "| " + " | ".join(cell.strip() for cell in row) + " |"


def csv_to_markdown(csv_text: str) -> str:
    """Convert a CSV string into a Markdown table.

    Parameters
    ----------
    csv_text: str
        CSV data as a string. The first line is treated as the header.

    Returns
    -------
    str
        Markdown table representation.
    """
    reader = csv.reader(csv_text.splitlines())
    rows = list(reader)
    if not rows:
        return ""

    header = rows[0]
    data_rows = rows[1:]

    # Build separator row based on header length
    separator = ["---" for _ in header]

    md_lines = [
        _format_row(header),
        _format_row(separator),
    ]
    md_lines.extend(_format_row(row) for row in data_rows)
    return "\n".join(md_lines)
