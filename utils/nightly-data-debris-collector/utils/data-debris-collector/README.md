# Data Debris Collector

## Purpose
In the digital wasteland, old, forgotten files and empty directories accumulate like radioactive dust. The Data Debris Collector is your trusty Geiger counter for identifying this 'digital debris' – files not accessed in ages, or directories that serve no purpose. It helps you reclaim precious storage space and maintain a tidy, efficient data bunker.

## Usage
Run the `collector.py` script with a target path and optional filters:

```bash
python src/collector.py <path> [--age <days>] [--empty] [--min-size <bytes>]
```

### Arguments:
*   `<path>`: The root directory to scan for debris.
*   `--age <days>`: (Optional) Report files not accessed in at least this many days. If neither `--age` nor `--empty` is specified, defaults to 30 days.
*   `--empty`: (Optional) Report empty files and directories.
*   `--min-size <bytes>`: (Optional) Only report files larger than or equal to this size. Useful for ignoring tiny config files.

### Examples:
*   Scan current directory for files older than 90 days:
    ```bash
    python src/collector.py . --age 90
    ```
*   Scan `/var/log` for empty files and directories:
    ```bash
    python src/collector.py /var/log --empty
    ```
*   Scan `/tmp` for files older than 7 days and larger than 1MB:
    ```bash
    python src/collector.py /tmp --age 7 --min-size 1048576
    ```

## Output
The utility will print a list of identified debris, including its path, type (file/directory), size (for files), and last access time.
