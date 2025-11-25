# Nightly Scavenger Stash Validator

## Overview

In the post-apocalyptic digital wasteland, every byte counts! The `Nightly Scavenger Stash Validator` is a crucial tool for any diligent scavenger looking to maintain an efficient and organized digital 'stash' of salvaged data. This utility helps you identify common issues within a specified directory, such as empty files, excessively large files, and redundant duplicates, ensuring your valuable storage space isn't wasted on digital debris.

## Features

*   **Empty File Detection**: Quickly finds and lists all files that occupy space but contain no data.
*   **Large File Identification**: Flags files that exceed a user-defined size limit, helping you manage storage hogs.
*   **Duplicate Content Discovery**: Identifies files with identical content (using SHA256 hashing), allowing you to consolidate redundant copies.
*   **Comprehensive Report**: Provides a clear summary of all detected issues, making stash maintenance a breeze.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are strictly required beyond the standard library.

1.  Navigate to the `utils/nightly-scavenger-stash-validator` directory.
2.  You can run it directly using `python src/validator.py`.

## Usage

Run the validator from your terminal, specifying the directory to scan and an optional maximum file size (in megabytes).

```bash
python src/validator.py --path /path/to/your/stash --max-size 10
```

### Arguments:

*   `--path <directory>` (required): The path to the directory you want to validate.
*   `--max-size <MB>` (optional): The maximum allowed file size in megabytes. Files larger than this will be flagged. Defaults to 100 MB.

### Example Output:

```
Scanning /path/to/your/stash...

--- Stash Validation Report ---

[!] Found 2 empty files:
    - /path/to/your/stash/empty_log.txt
    - /path/to/your/stash/placeholder.dat

[!] Found 1 large file (exceeds 10 MB):
    - /path/to/your/stash/massive_archive.zip (15.2 MB)

[!] Found 1 set of duplicate files:
    - Group 1 (SHA256: abcdef123...):
        - /path/to/your/stash/important_note.txt
        - /path/to/your/stash/backup/important_note_copy.txt

--- Scan Complete ---
Total files scanned: 10
Total issues found: 4
```

## Development

To run tests, navigate to the utility's root directory and execute:

```bash
python -m unittest tests/test_validator.py
```
