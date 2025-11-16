# Nightly Chrono-Scan

## Overview

The `nightly-chrono-scan` utility acts as a vigilant sentinel for your file system. It performs a "chrono-scan" of a specified directory, comparing its current state against a previously recorded snapshot. Any new, modified, or deleted files are detected and reported in a concise, human-readable summary.

This tool is invaluable for:

*   **Detecting unexpected changes**: Catching rogue processes or manual alterations that shouldn't have occurred.
*   **Monitoring build outputs**: Ensuring that build artifacts are consistent and no unintended files are created or removed.
*   **Integrity checks**: Verifying that critical directories remain stable over time.

## Usage

```bash
python3 src/ticker.py --path /path/to/monitor --state-file /path/to/state.json
```

*   `--path`: The directory to scan for changes.
*   `--state-file`: The JSON file where the utility will store its last known state (file paths and modification times). This file will be created if it doesn't exist.

### Example Workflow

1.  **First Run (Initialize State)**:
    ```bash
    python3 src/ticker.py --path /my/project/dist --state-file /tmp/dist_state.json
    ```
    (This will scan the directory and save its state. No changes will be reported on the first run as there's no previous state to compare against, only an initialization message.)

2.  **Subsequent Runs (Detect Changes)**:
    ```bash
    # After some operations on /my/project/dist
    python3 src/ticker.py --path /my/project/dist --state-file /tmp/dist_state.json
    ```
    (This will report any differences found since the last run and update the state file.)

## Output

The utility will print a summary to `stdout` detailing:

*   New files detected.
*   Modified files detected.
*   Deleted files detected.

If no changes are found, it will report "No significant temporal tears detected."

## Development

To run tests:

```bash
python3 -m unittest tests/test_ticker.py
```
