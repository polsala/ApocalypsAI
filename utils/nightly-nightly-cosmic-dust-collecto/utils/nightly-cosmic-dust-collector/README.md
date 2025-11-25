# Nightly Cosmic Dust Collector

A whimsical utility to sweep away digital "cosmic dust" – old, forgotten files – from your directories, keeping your repository pristine and light-speed efficient. Just as cosmic dust accumulates in the vastness of space, digital detritus can clutter your file systems, slowing down operations and obscuring important data. This tool helps you identify and manage it.

## Features

*   **Scan for Old Files**: Recursively searches a specified directory for files older than a given age.
*   **Pattern Matching**: Filter files by glob-style patterns (e.g., `*.log`, `temp_*`).
*   **Multiple Actions**:
    *   `report`: Simply lists the identified "dust" files.
    *   `delete`: Permanently removes the "dust" files.
    *   `move`: Relocates the "dust" files to a specified archive directory.
*   **Self-contained**: Written in Python, requiring only standard library modules.

## Usage

Run the `dust_collector.py` script from the `src/` directory.

```bash
python3 src/dust_collector.py <path> [--age <days>] [--action <report|delete|move>] [--destination <archive_path>] [--patterns <pattern1> <pattern2> ...]
```

### Arguments

*   `<path>`: **Required**. The root directory to scan for cosmic dust.
*   `--age <days>`: Optional. Files older than this many days will be considered cosmic dust. Defaults to `30`.
*   `--action <report|delete|move>`: Optional. The action to perform. Defaults to `report`.
    *   `report`: Lists the files identified as dust.
    *   `delete`: Deletes the identified files. **Use with caution!**
    *   `move`: Moves the identified files to a specified destination.
*   `--destination <archive_path>`: **Required if `--action` is `move`**. The directory where files will be moved.
*   `--patterns <pattern1> <pattern2> ...`: Optional. One or more glob-style file patterns (e.g., `*.log`, `temp_*`). Only files matching these patterns will be considered.

### Examples

1.  **Report all files older than 60 days in the current directory:**
    ```bash
    python3 src/dust_collector.py . --age 60 --action report
    ```

2.  **Delete `.log` and `.tmp` files older than 7 days in a specific project directory:**
    ```bash
    python3 src/dust_collector.py /path/to/my/project --age 7 --action delete --patterns "*.log" "*.tmp"
    ```

3.  **Move all files older than 90 days from `/var/logs` to an archive folder:**
    ```bash
    python3 src/dust_collector.py /var/logs --age 90 --action move --destination /var/logs/archive
    ```

## Development & Testing

The utility is self-contained and uses standard Python libraries. Tests are located in `tests/test_dust_collector.py` and can be run using `unittest`.

```bash
python3 -m unittest tests/test_dust_collector.py
```
