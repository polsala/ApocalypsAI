# Nightly Cosmic Dust Collector

The apocalypse leaves behind a lot of digital debris. The Nightly Cosmic Dust Collector is here to help you sweep away the accumulated "cosmic dust" – old log files, temporary data, and other forgotten detritus – keeping your systems lean and efficient.

This utility scans specified directories for files matching defined patterns and removes them if they are older than a configured age threshold.

## Features

*   **Targeted Cleaning**: Specify directories and file patterns (regex) to clean.
*   **Age-Based Removal**: Only removes files older than a set number of days.
*   **Dry Run Mode**: Preview what would be removed without actually deleting anything.
*   **Configurable**: Easy to adapt to different cleaning needs.

## Usage

```bash
python src/dust_collector.py --dir /var/log --pattern ".*\\.log\\.\\d+" --age 7 --dir /tmp --pattern ".*\\.tmp" --age 3 --dry-run
```

### Arguments

*   `--dir <path>`: (Required, can be repeated) Directory to scan for dust.
*   `--pattern <regex>`: (Required, can be repeated) Regular expression pattern for files to consider. Must be paired with a `--dir`.
*   `--age <days>`: (Required, can be repeated) Minimum age in days for a file to be considered "dust". Must be paired with a `--dir`.
*   `--dry-run`: (Optional) If present, the utility will only report what *would* be removed, without actually deleting files.
*   `--verbose`: (Optional) Print more detailed output about files being considered.

**Note**: Each `--dir`, `--pattern`, and `--age` argument forms a cleaning rule. Ensure they are provided in sets. For example, `--dir /a --pattern "a.log" --age 7 --dir /b --pattern "b.tmp" --age 3`.

## Examples

1.  **Clean `.log.gz` files older than 30 days in `/var/log`**:
    ```bash
    python src/dust_collector.py --dir /var/log --pattern ".*\\.log\\.gz$" --age 30
    ```

2.  **Dry run to see what `.tmp` files older than 7 days would be removed from `/tmp`**:
    ```bash
    python src/dust_collector.py --dir /tmp --pattern ".*\\.tmp$" --age 7 --dry-run
    ```

3.  **Clean multiple types of files in different locations**:
    ```bash
    python src/dust_collector.py \
        --dir /var/log --pattern ".*\\.old$" --age 14 \
        --dir /home/user/cache --pattern ".*\\.cache$" --age 7 \
        --verbose
    ```

## Development

To run tests:

```bash
python -m unittest tests/test_dust_collector.py
```
