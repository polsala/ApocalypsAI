# Nightly Chronicle Keeper Checksum Calculator

## Purpose

In the uncertain times of the ApocalypsAI, ensuring the integrity of your precious digital chronicles is paramount. The Nightly Chronicle Keeper Checksum Calculator is a standalone utility designed to help you generate and verify checksums (MD5 or SHA256) for files within a specified directory. This allows you to detect any accidental corruption, tampering, or changes to your vital data archives.

Keep your history intact, one checksum at a time.

## Usage

### Prerequisites

*   Python 3.6+

### Installation

This utility is self-contained. Simply navigate to its directory.

### Commands

#### 1. Generate a Checksum Manifest

To scan a directory and create a manifest file containing checksums for all its files:

```bash
python src/checksum_keeper.py generate <directory_to_scan> <output_manifest_path> [--algorithm <md5|sha256>]
```

*   `<directory_to_scan>`: The path to the directory whose files you want to checksum.
*   `<output_manifest_path>`: The path where the JSON manifest file will be saved.
*   `--algorithm`: (Optional) The hashing algorithm to use. Defaults to `sha256`. Options: `md5`, `sha256`.

**Example:**
```bash
python src/checksum_keeper.py generate ./my_important_data ./manifest.json --algorithm md5
```

#### 2. Verify Checksums Against a Manifest

To compare the current state of files in a directory against a previously generated manifest:

```bash
python src/checksum_keeper.py verify <directory_to_verify> <input_manifest_path> [--algorithm <md5|sha256>]
```

*   `<directory_to_verify>`: The path to the directory whose files you want to verify.
*   `<input_manifest_path>`: The path to the JSON manifest file.
*   `--algorithm`: (Optional) The hashing algorithm that was used to generate the manifest. Defaults to `sha256`. Options: `md5`, `sha256`.

**Example:**
```bash
python src/checksum_keeper.py verify ./my_important_data ./manifest.json
```

The verification process will report:
*   Files with matching checksums.
*   Files with *mismatched* checksums (indicating modification).
*   Files present in the directory but *not* in the manifest (new files).
*   Files in the manifest but *not* in the directory (missing files).

## Development

### Running Tests

To ensure the Chronicle Keeper is functioning correctly, run the tests:

```bash
python -m unittest discover tests
```
