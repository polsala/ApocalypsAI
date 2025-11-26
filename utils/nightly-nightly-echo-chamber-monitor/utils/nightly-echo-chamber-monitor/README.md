# Nightly Echo Chamber Monitor

The Nightly Echo Chamber Monitor is a whimsical yet essential utility designed to detect and report duplicate files within a specified directory. In the post-apocalyptic landscape, every byte of storage and every shred of information integrity counts. This tool helps you identify redundant data, declutter your file systems, and ensure that your precious digital artifacts aren't just echoes of themselves.

## Features

*   **Duplicate Detection**: Scans a target directory (and its subdirectories) for files with identical content using SHA256 hashing.
*   **Detailed Reporting**: Provides a clear list of all duplicate sets, showing the original file and all its copies.
*   **Whimsical Naming**: Because even in the apocalypse, a little humor goes a long way.

## Usage

To run the Echo Chamber Monitor, simply provide the path to the directory you wish to scan:

```bash
python src/echo_monitor.py /path/to/your/directory
```

### Example Output

```
Scanning '/path/to/your/directory' for duplicate files...

Found 2 sets of duplicate files:

--- Set 1 (Hash: 5d41402a...) ---
Original: /path/to/your/directory/documents/report_v1.txt
Duplicates:
  - /path/to/your/directory/archives/old_report.txt
  - /path/to/your/directory/backups/report_copy.txt

--- Set 2 (Hash: 8d969eef...) ---
Original: /path/to/your/directory/images/logo.png
Duplicates:
  - /path/to/your/directory/assets/logo_small.png
```

## Development

The utility is written in Python 3.11 and is self-contained.

### Running Tests

```bash
python -m unittest tests/test_echo_monitor.py
```
