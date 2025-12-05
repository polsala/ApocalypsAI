# Nightly Chronicle Keeper Checksum Checker

## Overview

In the face of impending digital decay or cosmic ray corruption, the Nightly Chronicle Keeper Checksum Checker is your steadfast guardian of data integrity. This utility allows you to generate SHA256 checksums for all files within a specified directory, creating a "chronicle manifest." Later, you can use this manifest to verify that your precious data remains untampered and perfectly preserved, just as you left it.

Whether it's your last will and testament, the blueprints for a self-sustaining bunker, or simply your cat photos, ensure their digital essence is immutable.

## Features

*   **Generate Manifest**: Scans a directory and creates a JSON manifest containing SHA256 checksums for each file.
*   **Verify Integrity**: Compares current file checksums against a previously generated manifest, reporting any discrepancies.
*   **Recursive Scan**: Processes files in subdirectories.
*   **Self-contained**: Pure Python, no external dependencies.

## Usage

### Prerequisites

*   Python 3.8+ (tested with 3.11)

### Installation

This utility is self-contained. Simply place the `nightly-chronicle-keeper-checksum-checker` folder in your desired location.

### Running the Utility

Navigate to the `src` directory within the utility folder.

#### 1. Generate a Checksum Manifest

To create a manifest file (`chronicle.json`) for all files in your `my_archive` directory:

```bash
python checksum_checker.py generate --directory /path/to/my_archive --output chronicle.json
```

This will produce a `chronicle.json` file (or whatever you name it) in the current working directory, looking something like this:

```json
{
    "file1.txt": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
    "subdir/file2.jpg": "b5a920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
    "...": "..."
}
```

#### 2. Verify File Integrity

To check if the files in `/path/to/my_archive` still match the checksums recorded in `chronicle.json`:

```bash
python checksum_checker.py verify --directory /path/to/my_archive --manifest chronicle.json
```

The utility will report:
*   `[OK]` for files that match.
*   `[MODIFIED]` for files whose checksums have changed.
*   `[MISSING]` for files present in the manifest but not found in the directory.
*   `[NEW]` for files found in the directory but not in the manifest.

A summary will be provided at the end.

## Development & Testing

To run the tests, navigate to the `tests` directory and execute:

```bash
python -m unittest test_checksum_checker.py
```
