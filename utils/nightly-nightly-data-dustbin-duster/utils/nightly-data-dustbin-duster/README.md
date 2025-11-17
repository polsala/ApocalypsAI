# Nightly Data Dustbin Duster

## Overview

In the chaotic aftermath, digital clutter can be as overwhelming as physical rubble. The "Nightly Data Dustbin Duster" is a whimsical-yet-useful utility designed to help you maintain a lean and efficient digital footprint by identifying and optionally removing duplicate files across your directories. Keep your precious storage space clear for more vital survival data!

## Features

*   **Duplicate Detection**: Scans a specified directory (and its subdirectories) to find files with identical content using SHA256 hashing.
*   **Dry Run Mode**: Lists all identified duplicates without deleting anything, allowing you to review before committing to removal.
*   **Safe Removal**: Optionally deletes duplicate files, always preserving one instance of each unique file.

## Usage

### Prerequisites

*   Python 3.8+ (tested with 3.11)

### Running the Duster

1.  Navigate to the `utils/nightly-data-dustbin-duster` directory.
2.  Run the `duster.py` script from your terminal.

    ```bash
    python src/duster.py <directory_to_scan> [options]
    ```

### Examples

**1. Find duplicates (dry run - default):**

This command will scan `/path/to/your/data` and its subdirectories, then print a list of all duplicate files found without deleting anything.

```bash
python src/duster.py /path/to/your/data
```

**2. Find and delete duplicates:**

This command will scan `/path/to/your/data`, identify duplicates, and then proceed to delete all but one instance of each duplicate file. **Use with caution!**

```bash
python src/duster.py /path/to/your/data --delete
```

## How it Works

The Duster uses SHA256 cryptographic hashing to determine if files are identical. It reads files in blocks to efficiently calculate hashes, even for very large files. Files with the same hash are considered duplicates. When deleting, it keeps the first encountered instance of a file and removes subsequent ones.

## Development & Testing

### Running Tests

To ensure the Duster is functioning correctly and won't accidentally delete your precious cat memes, run the included tests:

1.  Navigate to the `utils/nightly-data-dustbin-duster` directory.
2.  Run the test script:

    ```bash
    python -m unittest tests/test_duster.py
    ```

The tests use `unittest.mock` to simulate file system operations and file content, ensuring they are deterministic and do not interact with your actual file system.
