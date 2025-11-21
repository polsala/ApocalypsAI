# Nightly Digital Echo Recorder

## 🌌 Overview

In the ever-shifting landscape of the digital realm, sometimes you just need a reliable echo of the past. The "Nightly Digital Echo Recorder" is a whimsical-yet-useful utility designed to capture a precise snapshot of your chosen directories. Think of it as a digital time capsule, meticulously cataloging every file's path, size, last modification time, and a unique cryptographic hash.

Whether you're tracking unauthorized changes, ensuring data integrity, or simply documenting the evolution of a project, the Echo Recorder provides a deterministic record. Run it nightly to keep a vigilant eye on your critical data, ensuring that even in the most chaotic digital apocalypse, you have a clear memory of what once was.

## ✨ Features

*   **Directory Snapshotting**: Recursively scans a target directory and its subdirectories.
*   **File Integrity Hashing**: Calculates SHA256 hashes for all files, providing a robust fingerprint.
*   **Metadata Capture**: Records file size and last modification timestamp.
*   **JSON Output**: Stores the snapshot data in a human-readable and machine-parseable JSON format.
*   **Self-Contained**: A single Python script with minimal dependencies, easy to integrate and run.

## 🚀 Usage

### Prerequisites

*   Python 3.6+ (tested with 3.11)

### Running the Recorder

1.  Navigate to the `src` directory:
    ```bash
    cd utils/nightly-digital-echo-recorder/src
    ```
2.  Run the script, providing the target directory to snapshot and the desired output JSON file:
    ```bash
    python echo_recorder.py /path/to/your/important/data /path/to/save/snapshot.json
    ```

    **Example:**
    ```bash
    python echo_recorder.py ~/my_project_repo ./my_project_snapshot.json
    ```

    This will create `my_project_snapshot.json` containing the detailed snapshot.

### Example Output (`my_project_snapshot.json`)

```json
{
  "timestamp": "2023-10-27T10:00:00",
  "target_directory": "/home/user/my_project_repo",
  "files": [
    {
      "path": "README.md",
      "hash": "a1b2c3d4e5f6...",
      "size": 1024,
      "mtime": "2023-09-15T08:30:00"
    },
    {
      "path": "src/main.py",
      "hash": "f6e5d4c3b2a1...",
      "size": 4096,
      "mtime": "2023-10-26T14:15:22"
    },
    {
      "path": "data/config.yaml",
      "hash": "1a2b3c4d5e6f...",
      "size": 512,
      "mtime": "2023-10-01T10:00:00"
    }
  ]
}
```

## 🧪 Testing

To run the automated tests for the Nightly Digital Echo Recorder:

1.  Navigate to the utility's root directory:
    ```bash
    cd utils/nightly-digital-echo-recorder
    ```
2.  Run the Python `unittest` module:
    ```bash
    python -m unittest tests/test_echo_recorder.py
    ```

    All tests should pass, confirming the utility's functionality and robust error handling.
