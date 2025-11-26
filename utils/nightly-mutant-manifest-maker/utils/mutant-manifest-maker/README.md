# Mutant Manifest Maker

The ApocalypsAI Nightly Integrator presents the **Mutant Manifest Maker**!

In the chaotic aftermath, knowing what's lurking in your directories is paramount. This utility scans a specified directory for files matching given patterns and generates a clear, concise Markdown manifest. It's perfect for quickly cataloging project contents, auditing unknown codebases, or simply keeping track of your digital hoard.

## Usage

```bash
python src/manifest_maker.py <directory_to_scan> [pattern1] [pattern2] ...
```

**Example:**

```bash
python src/manifest_maker.py . "*.py" "*.md" "*.txt" > manifest.md
```

This will scan the current directory (`.`) for all Python files, Markdown files, and text files, outputting the manifest to `manifest.md`.

## Features

*   **Recursive Scanning**: Dives deep into subdirectories.
*   **Pattern Matching**: Filter files using glob patterns (e.g., `*.py`, `config.*`, `data/*.json`).
*   **Metadata Inclusion**: Lists file path, size in bytes, and last modification timestamp.
*   **Markdown Output**: Easy to read and integrate into documentation.

## Installation

This utility is self-contained and requires Python 3.8+. No external dependencies are needed beyond the standard library.

```bash
# Navigate to the utility's directory
cd utils/mutant-manifest-maker/
# Run it!
python src/manifest_maker.py . "*.py"
```

## Development

To run tests:

```bash
cd utils/mutant-manifest-maker/
python -m unittest tests/test_manifest_maker.py
```
