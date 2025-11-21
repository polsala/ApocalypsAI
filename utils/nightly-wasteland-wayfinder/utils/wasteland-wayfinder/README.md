# Wasteland Wayfinder

A command-line utility for the discerning digital scavenger. Navigate the desolate landscapes of your file system and uncover "points of interest" – recently modified files, valuable large caches, or specific data fragments – with ease.

## Features

*   **Scavenge by Recency**: Find files modified within a specified number of days (`--recent`).
*   **Unearth Large Caches**: Pinpoint files exceeding a certain size (`--large`).
*   **Filter Data Fragments**: Focus on specific file types by extension (`--ext`).
*   **Control Exploration Depth**: Limit how deep into the digital ruins you venture (`--depth`).

## Installation

This utility is self-contained and requires Python 3.8+.

1.  Navigate to the `utils/wasteland-wayfinder/` directory.
2.  Run directly: `python src/wayfinder.py --help`

## Usage

```bash
python src/wayfinder.py --path <directory> [OPTIONS]
```

### Options

*   `--path <directory>`: The starting directory for your scavenging expedition. Defaults to the current directory.
*   `--recent <days>`: Highlight files modified in the last `N` days.
*   `--large <size_kb>`: Highlight files larger than `N` kilobytes.
*   `--ext <ext1,ext2,...>`: Comma-separated list of file extensions to include (e.g., `py,md,txt`).
*   `--depth <int>`: Maximum recursion depth for directory traversal. Default is unlimited.
*   `--help`: Show this help message and exit.

## Examples

**Find all Python files modified in the last 7 days in the current directory:**
```bash
python src/wayfinder.py --recent 7 --ext py
```

**Discover large markdown files (over 100KB) in the 'docs' folder:**
```bash
python src/wayfinder.py --path docs --large 100 --ext md
```

**List all files in the current directory, but only 2 levels deep:**
```bash
python src/wayfinder.py --depth 2
```
