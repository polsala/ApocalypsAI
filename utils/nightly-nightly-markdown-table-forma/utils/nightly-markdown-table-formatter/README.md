# Markdown Table Formatter

This utility provides a single function `csv_to_markdown` that takes a CSV string and returns a Markdown table.

## Usage

```python
from markdown_table_formatter.src.formatter import csv_to_markdown

csv_data = """name,age,city
Alice,30,New York
Bob,25,Los Angeles"""
print(csv_to_markdown(csv_data))
```

Output:

```
| name  | age | city        |
|-------|-----|-------------|
| Alice | 30  | New York    |
| Bob   | 25  | Los Angeles |
```

## Installation

No external dependencies are required beyond the Python standard library.

## Tests

Run `pytest` in the `tests/` directory to verify functionality.
