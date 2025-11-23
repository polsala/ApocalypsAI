# Nightly Scavenger Manifest Generator

## Overview

The `nightly-scavenger-manifest-generator` is a utility designed to help you inventory your digital 'scavenged' resources. It scans a specified directory, recursively listing all files and subdirectories, calculating their sizes, and generating SHA256 hashes for each file. The output is a clean, readable Markdown file, perfect for keeping track of your data hoard.

## Features

*   **Recursive Scanning**: Traverses all subdirectories from the starting path.
*   **Detailed Information**: Lists file paths, sizes (in human-readable format), and SHA256 hashes.
*   **Markdown Output**: Generates a `.md` file, easy to integrate into documentation or reports.
*   **Self-Contained**: No external dependencies beyond standard Python libraries.

## Usage

To generate a manifest, run the `manifest_generator.py` script with the target directory and an optional output file path:

```bash
python src/manifest_generator.py --path /path/to/your/scavenged/data --output manifest.md
```

### Arguments:

*   `--path <directory>` (required): The root directory to scan.
*   `--output <file.md>` (optional): The output Markdown file path. Defaults to `manifest.md` in the current working directory.

## Example Output

```markdown
# Scavenger Manifest for /path/to/your/scavenged/data

| Type | Path | Size | SHA256 Hash |
|---|---|---|---|
| Directory | /path/to/your/scavenged/data/docs | - | - |
| File | /path/to/your/scavenged/data/docs/notes.txt | 1.2 KB | a1b2c3d4e5f6...
| Directory | /path/to/your/scavenged/data/images | - | - |
| File | /path/to/your/scavenged/data/images/logo.png | 23.5 KB | f6e5d4c3b2a1...
| Directory | /path/to/your/scavenged/data/src | - | - |
| File | /path/to/your/scavenged/data/src/main.py | 5.8 KB | 1a2b3c4d5e6f...
```
