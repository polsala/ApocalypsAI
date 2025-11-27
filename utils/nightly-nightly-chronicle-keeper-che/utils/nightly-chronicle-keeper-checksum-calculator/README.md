# Nightly Chronicle Keeper Checksum Calculator

## Overview

In the uncertain times of the ApocalypsAI, preserving the integrity of our digital chronicles is paramount. The Chronicle Keeper Checksum Calculator is a standalone utility designed to generate and verify SHA256 checksums for all files within a specified directory. This ensures that your precious data remains untainted by cosmic rays, rogue AI, or accidental deletions.

It creates a `checksum_manifest.json` file, a digital ledger of your files' pristine state, allowing for future verification.

## Usage

### Generate a Checksum Manifest

To generate a `checksum_manifest.json` for a directory:

```bash
python src/checksum_calculator.py generate <path_to_directory> [output_manifest_path]
```

- `<path_to_directory>`: The directory to scan.
- `[output_manifest_path]`: (Optional) The path where the `checksum_manifest.json` will be saved. If not provided, it defaults to `checksum_manifest.json` in the current working directory.

Example:
```bash
python src/checksum_calculator.py generate ./my_important_data
```

This will create `checksum_manifest.json` listing all files and their SHA256 hashes within `./my_important_data`.

### Verify Files Against a Manifest

To verify the integrity of files in a directory against an existing `checksum_manifest.json`:

```bash
python src/checksum_calculator.py verify <path_to_directory> <path_to_manifest>
```

- `<path_to_directory>`: The directory containing the files to verify.
- `<path_to_manifest>`: The path to the `checksum_manifest.json` file.

Example:
```bash
python src/checksum_calculator.py verify ./my_important_data checksum_manifest.json
```

The utility will report any missing files, new files, or files with altered checksums.

## Development

The utility is written in Python 3.x and requires no external dependencies beyond the standard library.

### Running Tests

```bash
python -m unittest tests/test_checksum_calculator.py
```
