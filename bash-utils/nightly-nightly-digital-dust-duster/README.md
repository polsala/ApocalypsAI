# Nightly Digital Dust Duster

The digital wasteland can accumulate forgotten relics – old files, unused logs, and cached detritus. The Nightly Digital Dust Duster is your trusty bash utility to scour specified directories, identify these digital "dust bunnies," and report on them, helping you reclaim precious storage and maintain a tidy system.

## Features

*   **Scavenge by Age:** Find files older than a specified number of days.
*   **Filter by Size:** Optionally narrow down the search to files larger than a certain size.
*   **Clear Reporting:** Outputs a list of identified files with their size and last modification date.

## Usage

```bash
./src/dust_duster.sh <directory> <age_in_days> [min_size_in_kb]
```

*   `<directory>`: The path to the directory you want to scour.
*   `<age_in_days>`: Files older than this many days will be reported.
*   `[min_size_in_kb]`: (Optional) Only report files larger than this size in kilobytes.

### Examples

1.  **Find all files in `/var/log` older than 90 days:**
    ```bash
    ./src/dust_duster.sh /var/log 90
    ```

2.  **Find all files in your home directory older than 365 days and larger than 10MB (10240 KB):**
    ```bash
    ./src/dust_duster.sh ~/ 365 10240
    ```

## How it Works

The script uses the `find` command to efficiently locate files based on their modification time (`-mtime`) and size (`-size`). It then pipes the results to `awk` for formatting, converting byte sizes to kilobytes and presenting modification dates clearly.

## Tests

To run the tests, navigate to the utility's root directory and execute:

```bash
./tests/test_dust_duster.sh
```

The tests create a temporary directory structure with various files and verify that the `dust_duster.sh` script correctly identifies and reports files based on different age and size criteria.
