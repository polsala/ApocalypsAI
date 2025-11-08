# JSON Pretty Printer

A lightweight, zero‑dependency Python utility that reads JSON from a file or STDIN and prints a nicely formatted, sorted, and optionally color‑highlighted version.

## Features

- **Sorted keys** for deterministic output.
- **Indentation** (default 2 spaces) for readability.
- **Optional color** using ANSI escape codes (no external libraries).
- Works offline – no network calls.

## Installation

Copy the `src/pretty_print.py` script into your `$PATH` or run it via `python -m utils.json-pretty-printer.src.pretty_print`.

```bash
pip install .   # if you turn this folder into a package later
```

## Usage

```bash
# From a file
python -m utils.json-pretty-printer.src.pretty_print path/to/file.json

# From stdin
cat data.json | python -m utils.json-pretty-printer.src.pretty_print

# Enable color output
python -m utils.json-pretty-printer.src.pretty_print --color path/to/file.json
```

## Options

| Flag | Description |
|------|-------------|
| `--color` | Enable ANSI color highlighting for keys and values. |
| `-h`, `--help` | Show help message. |

## Testing

Run the bundled tests with:

```bash
python -m pytest utils/json-pretty-printer/tests
```
