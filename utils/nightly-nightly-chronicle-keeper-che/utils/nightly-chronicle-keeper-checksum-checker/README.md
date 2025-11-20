# Chronicle Keeper's Checksum Checker

## 📜 Overview

In the ever-shifting sands of the digital wasteland, data integrity is paramount. The Chronicle Keeper's Checksum Checker is your trusty sentinel, designed to create an immutable record (a 'manifest') of your files' digital fingerprints (checksums). Later, you can use this manifest to verify that no file has been altered, corrupted, or mysteriously vanished since the last check.

Whether you're safeguarding critical configuration files, precious log archives, or the very source code of your survival bunker, the Chronicle Keeper ensures your digital chronicles remain untainted.

## ✨ Features

*   **Generate Manifest**: Scans a specified directory and creates a JSON file containing the checksums of all its files.
*   **Verify Manifest**: Compares the current state of a directory against a previously generated manifest, reporting any missing, modified, or new files.
*   **Customizable Algorithm**: Supports various hashing algorithms (defaulting to SHA256).

## 🚀 Usage

This utility is a Python 3.11 script and can be run directly.

### 1. Generate a Manifest

To create a new manifest for a directory:

```bash
python src/checksum_checker.py generate <directory_to_scan> <output_manifest_file.json> [--algorithm <hash_algo>]
```

**Example:**

```bash
python src/checksum_checker.py generate ./my_bunker_data ./manifests/bunker_data_v1.json
```

This will scan the `./my_bunker_data` directory and save a manifest named `bunker_data_v1.json` in the `./manifests/` folder.

### 2. Verify Against a Manifest

To check the integrity of a directory against an existing manifest:

```bash
python src/checksum_checker.py verify <directory_to_verify> <manifest_file.json> [--algorithm <hash_algo>]
```

**Example:**

```bash
python src/checksum_checker.py verify ./my_bunker_data ./manifests/bunker_data_v1.json
```

This will re-scan `./my_bunker_data` and compare its files against `bunker_data_v1.json`, reporting any discrepancies.

### Supported Algorithms

By default, `sha256` is used. You can specify others like `md5`, `sha1`, `sha512`, etc., using the `--algorithm` flag. Ensure the same algorithm is used for both generation and verification.

## 🧪 Development & Testing

Tests are located in `tests/test_checksum_checker.py` and can be run using `unittest`:

```bash
python -m unittest tests/test_checksum_checker.py
```

All tests are deterministic and use mocks to simulate file system operations and file content, ensuring reliability and speed without touching the actual disk.
