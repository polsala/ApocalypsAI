# Nightly Chronicle Keeper Checksum Checker

## Overview
In the ever-shifting sands of the post-apocalyptic digital landscape, data integrity is paramount. The "Nightly Chronicle Keeper Checksum Checker" is a vigilant utility designed to safeguard your precious files. It generates a manifest of SHA256 checksums for all files within a specified directory, acting as a digital ledger. Later, you can use this manifest to verify that no file has been altered, corrupted, or gone missing since the last chronicle was kept.

Think of it as a digital archivist, ensuring your historical records, critical blueprints, or even your favorite meme collection remains pristine against the ravages of time and unexpected bit-flips.

## Features
- **Generate Manifest**: Scans a directory and creates a JSON file containing the SHA256 checksum for each file.
- **Verify Integrity**: Compares the current state of files in a directory against a previously generated manifest, reporting any discrepancies (missing files, changed content, new files).
- **Recursive Scan**: Works on entire directory trees.

## Usage

### Prerequisites
- Python 3.8+ (tested with 3.11)

### Installation
This utility is self-contained. Simply navigate to its directory.

### Commands

#### 1. Generate a checksum manifest
To create a new manifest file for a directory:

```bash
python src/checksum_checker.py generate --path /path/to/your/data --output manifest.json
```

- `--path`: The directory to scan (e.g., `/path/to/your/data`).
- `--output`: The name of the JSON file to save the manifest to (e.g., `manifest.json`).

Example:
```bash
# Create some dummy files
mkdir -p my_chronicles
echo "Hello World" > my_chronicles/file1.txt
echo "Apocalypse Now" > my_chronicles/file2.txt
mkdir -p my_chronicles/sub_dir
echo "Secret plans" > my_chronicles/sub_dir/secret.txt

# Generate manifest
python src/checksum_checker.py generate --path my_chronicles --output my_chronicles_manifest.json
```

The `my_chronicles_manifest.json` file will contain entries like:
```json
{
    "file1.txt": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b27796ac9d051d",
    "file2.txt": "979212001c90587784157774783307521a221f5822b39912066d213981297621",
    "sub_dir/secret.txt": "2c19989d9701168925501865a95441a13e54117820610f6018151478170c502b"
}
```
(Note: Paths in the manifest are relative to the `--path` argument.)

#### 2. Verify file integrity
To check if files in a directory match a previously generated manifest:

```bash
python src/checksum_checker.py verify --path /path/to/your/data --manifest manifest.json
```

- `--path`: The directory to verify (e.g., `/path/to/your/data`).
- `--manifest`: The path to the manifest JSON file (e.g., `manifest.json`).

Example:
```bash
# Verify against the manifest
python src/checksum_checker.py verify --path my_chronicles --manifest my_chronicles_manifest.json

# Expected output (if no changes):
# Verification successful. All 3 files match the manifest.

# Now, let's tamper with a file
echo "Tampered!" > my_chronicles/file1.txt
python src/checksum_checker.py verify --path my_chronicles --manifest my_chronicles_manifest.json

# Expected output:
# Verification found discrepancies:
# - CHANGED: file1.txt (Expected: a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b27796ac9d051d, Found: 53f1947b539a6152433012971271612445c91456578a8707122822119042978d)
# Verification FAILED.
```

## Development
To run tests:
```bash
python -m unittest tests/test_checksum_checker.py
```
