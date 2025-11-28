# Nightly Checksum Guardian

## Overview

The Nightly Checksum Guardian is a vigilant utility designed to monitor the integrity of your critical files. It works by computing cryptographic checksums (SHA256) for files within a specified directory and storing them in a manifest. On subsequent runs, it re-computes these checksums and compares them against the stored manifest, reporting any additions, removals, or modifications.

This helps detect unauthorized changes, accidental corruption, or even subtle tampering that might otherwise go unnoticed.

## Usage

```bash
python3 src/guardian.py --path <directory_to_monitor> --manifest <path_to_manifest_file>
```

### First Run (Generate Manifest)

When run for the first time with a non-existent manifest file, the Guardian will scan the specified directory, compute checksums for all files, and save them to the manifest.

```bash
python3 src/guardian.py --path /path/to/my/important/data --manifest /path/to/.checksum_manifest
```

### Subsequent Runs (Verify Integrity)

On subsequent runs, if the manifest file exists, the Guardian will compare the current state of the files against the stored checksums. It will then print a report detailing any changes.

```bash
python3 src/guardian.py --path /path/to/my/important/data --manifest /path/to/.checksum_manifest
```

## Example Output (Verification)

```
--- Checksum Guardian Report ---

Files Added:
  - /path/to/my/important/data/new_report.txt

Files Removed:
  - /path/to/my/important/data/old_log.txt

Files Modified:
  - /path/to/my/important/data/config.ini (Old: abc...123, New: def...456)

Files Unchanged: 23

--- Report End ---
Integrity check completed with detected changes.
```

## Development

To run tests:

```bash
python3 -m unittest tests/test_guardian.py
```
