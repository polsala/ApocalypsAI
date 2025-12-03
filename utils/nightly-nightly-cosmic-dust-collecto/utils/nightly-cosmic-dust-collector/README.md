# Nightly Cosmic Dust Collector

The universe of your repository can accumulate a lot of "cosmic dust" – tiny, forgotten, or ancient files that clutter your digital space. The Nightly Cosmic Dust Collector is here to help you identify and manage these digital specks, keeping your repository clean and efficient.

This utility scans a specified directory for files that meet certain criteria (e.g., empty, very small, or very old) and provides options to list them or, if you're brave, delete them.

## Features

*   **Scan for Empty Files**: Easily find files with zero bytes.
*   **Scan for Small Files**: Identify files below a configurable size threshold.
*   **Scan for Old Files**: Pinpoint files not modified for a configurable number of days.
*   **List or Delete**: Safely list identified "dust" files, or proceed with deletion.

## Usage

```bash
python src/dust_collector.py --path <directory_to_scan> [OPTIONS]
```

### Arguments

*   `--path <directory>`: **Required**. The root directory to start scanning for cosmic dust.
*   `--min-age-days <days>`: Optional. Files older than this many days (based on last modification time) will be considered dust. Default: `30`.
*   `--max-size-kb <kb>`: Optional. Files smaller than this many kilobytes will be considered dust. Default: `1` (1KB).
*   `--delete`: Optional. If provided, the identified dust files will be permanently deleted. **Use with caution!**
*   `--exclude <pattern>`: Optional. A comma-separated list of glob patterns to exclude files or directories. E.g., `*.log,temp_dir/*`.

### Examples

1.  **List all dust files in the current directory (empty, <1KB, >30 days old):**
    ```bash
    python src/dust_collector.py --path .
    ```

2.  **Find files older than 90 days or smaller than 5KB in `my_project/data`:**
    ```bash
    python src/dust_collector.py --path my_project/data --min-age-days 90 --max-size-kb 5
    ```

3.  **Delete all identified dust files in `temp_logs` (use with extreme care!):**
    ```bash
    python src/dust_collector.py --path temp_logs --delete
    ```

4.  **List dust files, excluding `.git` directory and `*.tmp` files:**
    ```bash
    python src/dust_collector.py --path . --exclude ".git/*,*.tmp"
    ```

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are needed beyond standard library modules.

1.  Navigate to the `utils/nightly-cosmic-dust-collector` directory.
2.  Run the script as shown in the Usage section.
