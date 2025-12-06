# nightly-markdown-table-to-csv

## Overview

`markdown-table-to-csv` is a lightweight, zero‑dependency Python utility that reads a markdown file (or standard input) and converts the **first** markdown table it finds into CSV format.

## Why?

- Quickly turn documentation tables into data you can feed to spreadsheets or scripts.
- No external libraries – works out‑of‑the‑box with Python 3.11.
- Ideal for CI pipelines, GitHub Actions, or ad‑hoc terminal use.

## Installation

```bash
# Clone the repository (or copy the folder) and install the utility in a venv
python -m venv .venv && source .venv/bin/activate
pip install -e utils/nightly-markdown-table-to-csv
```

The package is pure Python; no additional dependencies are required.

## Usage

```bash
# Convert a file
python -m nightly_markdown_table_to_csv src/example.md > output.csv

# Pipe from stdin
cat src/example.md | python -m nightly_markdown_table_to_csv > output.csv
```

If the input contains no markdown table, the utility prints nothing and exits with code 0.

## Development & Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-markdown-table-to-csv/tests
```

## License

MIT – see the root LICENSE file.
