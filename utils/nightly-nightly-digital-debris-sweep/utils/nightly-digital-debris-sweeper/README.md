# Nightly Digital Debris Sweeper

"Sweeping away the digital dust bunnies before they clog the gears of progress."

The Nightly Digital Debris Sweeper is a whimsical-yet-useful utility designed to help maintain a clean and efficient development environment by identifying and optionally removing old, common cache and build artifact directories. Over time, projects accumulate `__pycache__`, `node_modules`, `target/` (Rust), `dist/` (Python/JS), and other temporary files that consume valuable disk space and can sometimes lead to stale build issues.

This tool scans a specified root directory for these common "debris" patterns and, based on a configurable age threshold, lists or deletes them.

## Features

*   **Identifies Common Debris**: Detects directories like `__pycache__`, `.pytest_cache`, `node_modules`, `target`, `dist`, `build`, `.mypy_cache`, `.venv`, and `venv`.
*   **Age-Based Filtering**: Only considers directories for removal if their last modification time is older than a specified number of days.
*   **Safe Operation**: By default, it only lists potential debris. Deletion requires an explicit `--delete` flag.
*   **Self-Contained**: Written in Python 3.11 with only standard library dependencies.

## Usage

```bash
python src/sweeper.py <root_directory> [--age <days>] [--delete]
```

### Arguments

*   `<root_directory>`: The absolute or relative path to the directory you want to scan. The sweeper will recursively search within this directory.
*   `--age <days>`: (Optional) The age threshold in days. Directories whose last modification time is older than this many days will be considered debris. Defaults to `30` days.
*   `--delete`: (Optional) If this flag is present, the identified debris directories will actually be removed from the filesystem. **Use with caution!** Without this flag, the tool will only list the directories it would delete.

### Examples

1.  **List old debris in the current directory (default 30 days age):**
    ```bash
    python src/sweeper.py .
    ```

2.  **List debris older than 7 days in a specific project directory:**
    ```bash
    python src/sweeper.py /path/to/my/project --age 7
    ```

3.  **Delete all identified debris older than 60 days in your home directory:**
    ```bash
    python src/sweeper.py ~/ --age 60 --delete
    ```

## Development

### Running Tests

To ensure the sweeper is functioning correctly and safely, run the provided unit tests.

```bash
python -m unittest tests/test_sweeper.py
```

The tests use mocks to simulate filesystem operations and time, ensuring they are deterministic and do not modify your actual files.
