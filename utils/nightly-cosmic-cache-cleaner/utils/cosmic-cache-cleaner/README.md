# Cosmic Cache Cleaner

## Overview

The `Cosmic Cache Cleaner` is your trusty companion in the relentless battle against digital entropy. As the universe expands and contracts, so too do our project directories, often accumulating vast amounts of temporary files, build artifacts, and cache data that serve no purpose beyond hogging precious disk space. This utility helps you identify and purge these digital remnants, ensuring your development environment remains lean, mean, and ready for whatever cosmic anomalies come your way.

## Features

*   **Configurable Scan Paths**: Specify which directories to scan for digital debris.
*   **Intelligent Pattern Matching**: Use glob patterns to target common cache directories (`__pycache__`, `node_modules`, `.venv`, `target`, `build`, etc.) and exclude important files.
*   **Dry Run Mode**: Preview what would be deleted and how much space would be reclaimed without actually touching your files.
*   **Execute Mode**: Confidently purge the identified caches and temporary files.
*   **Space Reclamation Report**: Get a summary of the space saved.

## Usage

```bash
python3 src/cleaner.py --help
```

### Example: Dry Run

To see what files would be cleaned in your current directory and its subdirectories, without making any changes:

```bash
python3 src/cleaner.py --path . --dry-run
```

### Example: Execute Clean

To actually clean the identified files and directories:

```bash
python3 src/cleaner.py --path . --execute
```

### Example: Custom Patterns

To clean only `__pycache__` and `node_modules` directories, ignoring `.git`:

```bash
python3 src/cleaner.py --path . --execute \
  --include "**/__pycache__" "**/node_modules" \
  --exclude "**/.git/**"
```

## Configuration

The cleaner uses a set of default patterns for common cache and build directories across various languages and tools. You can override or extend these using `--include` and `--exclude` arguments.

**Default Include Patterns:**
*   `**/__pycache__`
*   `**/.pytest_cache`
*   `**/.mypy_cache`
*   `**/.venv`
*   `**/env`
*   `**/node_modules`
*   `**/target` (Rust, Maven)
*   `**/build` (C++, Java, Go)
*   `**/dist` (Python, JS)
*   `**/out`
*   `**/*.tmp`

**Default Exclude Patterns:**
*   `**/.git/**`
*   `**/.svn/**`
*   `**/.hg/**`
*   `**/.vscode/**`
*   `**/.idea/**`

## Development

To run tests:

```bash
python3 -m unittest tests/test_cleaner.py
```
