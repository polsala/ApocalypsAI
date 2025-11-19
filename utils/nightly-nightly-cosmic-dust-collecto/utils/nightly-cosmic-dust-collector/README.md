# Nightly Cosmic Dust Collector

The digital universe is vast, and sometimes, tiny, forgotten files accumulate like cosmic dust, cluttering your project directories. The Nightly Cosmic Dust Collector is here to help! This utility scans specified directories for files that are either empty, exceedingly small, or haven't been touched in ages, offering to list them for your review or gracefully move them to a designated quarantine zone.

Keep your digital space clean and your projects light, ready for the next cosmic event!

## Features

*   **Scan for Empty Files**: Identifies files with zero bytes.
*   **Scan for Small Files**: Finds files below a configurable size threshold.
*   **Scan for Old Files**: Locates files not modified within a configurable age threshold.
*   **List or Quarantine**: Choose to simply list the identified "dust" or move it to a specified quarantine directory.
*   **Exclusions**: Ignore specific directories or file patterns.

## Usage

```bash
python src/dust_collector.py --help
```

### Examples

1.  **List all "dust" (empty, <1KB, or >30 days old) in the current directory:**
    ```bash
    python src/dust_collector.py .
    ```

2.  **Quarantine files older than 60 days and smaller than 500 bytes in `/my/project` to `/tmp/quarantine_dust`:**
    ```bash
    python src/dust_collector.py /my/project --action quarantine --quarantine-path /tmp/quarantine_dust --max-size 500 --min-age 60
    ```

3.  **List only empty files in a specific directory, excluding `node_modules`:**
    ```bash
    python src/dust_collector.py /path/to/scan --max-size 0 --exclude node_modules
    ```

## Installation

This utility is self-contained and requires Python 3.8+ (compatible with 3.11). No external dependencies are needed.

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/utils/nightly-cosmic-dust-collector

# Run directly
python src/dust_collector.py .
```

## Configuration

| Argument            | Description                                                                 | Default      |
| :------------------ | :-------------------------------------------------------------------------- | :----------- |
| `paths`             | One or more directories to scan.                                            | `.`          |
| `--action`          | Action to perform: `list` or `quarantine`.                                  | `list`       |
| `--quarantine-path` | Directory to move files to if `action` is `quarantine`.                     | `./dust_quarantine` |
| `--max-size`        | Maximum file size in bytes to consider as dust. Set to 0 for empty files only. | `1024` (1KB) |
| `--min-age`         | Minimum age in days for a file to be considered old dust.                   | `30`         |
| `--exclude`         | Comma-separated list of directory names to exclude from scanning.           | `.git,node_modules,venv,env` |
| `--verbose`         | Print detailed information about scanned files.                             | `False`      |
