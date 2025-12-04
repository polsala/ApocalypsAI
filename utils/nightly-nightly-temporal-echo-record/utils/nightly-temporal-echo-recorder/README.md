# Nightly Temporal Echo Recorder

## Overview

The Nightly Temporal Echo Recorder is a whimsical-yet-useful utility designed to help the ApocalypsAI community track changes in files and directories over time. In a world of constant flux and digital decay, sometimes you just need to know what shifted. This tool allows you to capture "snapshots" of your file system's state (specifically, the SHA256 hashes of files) and then compare these snapshots to identify new, deleted, or modified files.

Think of it as a digital archaeologist's tool, recording the "echoes" of past states to understand the present.

## Features

*   **Snapshot Capture**: Recursively scans a given directory or a single file, calculating SHA256 hashes for all files and storing them in a JSON-formatted snapshot.
*   **Snapshot Comparison**: Compares two previously captured snapshots to report:
    *   `new_files`: Files present in the new snapshot but not the old.
    *   `deleted_files`: Files present in the old snapshot but not the new.
    *   `modified_files`: Files present in both, but with different hashes.
    *   `unchanged_files`: Files present in both with identical hashes.
*   **Self-contained**: Written in Python 3.11, with minimal standard library dependencies.

## Usage

The utility can be run from the command line.

### Taking a Snapshot

To capture the current state of a directory or file:

```bash
python src/echo_recorder.py snapshot --path /path/to/monitor --output snapshot_v1.json
```

*   `--path`: The target file or directory to snapshot.
*   `--output`: The JSON file where the snapshot data will be saved.

Example:
```bash
# Create some dummy files for demonstration
mkdir -p my_project/src
echo "print('hello')" > my_project/src/main.py
echo "config_value=1" > my_project/config.ini

# Take an initial snapshot
python src/echo_recorder.py snapshot --path my_project --output snapshot_v1.json
```

The `snapshot_v1.json` file will contain entries like:
```json
{
  "config.ini": "a1b2c3d4...",
  "src/main.py": "e5f6g7h8..."
}
```

### Comparing Snapshots

To compare two previously saved snapshots:

```bash
python src/echo_recorder.py compare --old-snapshot snapshot_v1.json --new-snapshot snapshot_v2.json
```

*   `--old-snapshot`: Path to the JSON file of the older snapshot.
*   `--new-snapshot`: Path to the JSON file of the newer snapshot.

Example:
```bash
# Modify a file and add a new one
echo "print('hello world')" > my_project/src/main.py # Modified
echo "utility_script.sh" > my_project/scripts/setup.sh # New file (create scripts dir first)
mkdir -p my_project/scripts
echo "#!/bin/bash" > my_project/scripts/setup.sh

# Take a second snapshot
python src/echo_recorder.py snapshot --path my_project --output snapshot_v2.json

# Compare the two snapshots
python src/echo_recorder.py compare --old-snapshot snapshot_v1.json --new-snapshot snapshot_v2.json
```

Expected output for the comparison:
```
--- Snapshot Comparison Report ---

New Files:
  - scripts/setup.sh

Modified Files:
  - src/main.py

Deleted Files:
  - (None in this example)

Unchanged Files:
  - config.ini
----------------------------------
```

## Development

### Requirements

*   Python 3.11+

### Running Tests

To run the automated tests, navigate to the utility's root directory and execute:

```bash
python -m unittest tests/test_echo_recorder.py
```

All tests are designed to be deterministic and run offline using mocks for file system operations.
