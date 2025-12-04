# Nightly Scavenger Manifest Generator

## Overview
In the desolate digital wasteland, valuable data can be scattered and forgotten. The `Nightly Scavenger Manifest Generator` is your trusty companion for cataloging these digital artifacts. It scans a specified directory for files matching your criteria and compiles a neat Markdown manifest, detailing their paths, sizes, and even a peek into their contents.

Think of it as your personal data archaeologist, creating an inventory of your most precious (or just present) files.

## Usage

```bash
python src/manifest_generator.py --directory <path_to_scan> --output <output_manifest.md> [--patterns <pattern1> <pattern2> ...] [--snippet-length <int>]
```

### Arguments:
*   `--directory` (required): The root directory to start scanning from.
*   `--output` (required): The path to the output Markdown manifest file.
*   `--patterns` (optional): One or more glob-style patterns (e.g., `*.txt`, `report_*.log`) to filter files. If not provided, all files are included.
*   `--snippet-length` (optional): The number of characters to include as a content snippet for each file. Defaults to `0` (no snippet).

## Examples

1.  **Generate a manifest of all `.log` and `.txt` files in the current directory, with no snippets:**
    ```bash
    python src/manifest_generator.py --directory . --output manifest.md --patterns "*.log" "*.txt"
    ```

2.  **Generate a manifest of all files in `/var/log`, including a 100-character snippet from each, outputting to `~/log_manifest.md`:**
    ```bash
    python src/manifest_generator.py --directory /var/log --output ~/log_manifest.md --snippet-length 100
    ```

3.  **Generate a manifest of all files in a specific project folder, without any pattern filtering:**
    ```bash
    python src/manifest_generator.py --directory ./my_project --output project_files.md
    ```
