# Nightly Chronicle Keeper Checksum Calculator

## 📜 Preserve Your Digital Legacies

In the face of digital entropy and cosmic ray interference, the integrity of your most vital files is paramount. The `Nightly Chronicle Keeper Checksum Calculator` is your trusty guardian, meticulously cataloging the unique digital fingerprint of each file. Use it to ensure that your data remains pristine, untampered, and exactly as you left it, even after the apocalypse.

## ✨ Features

*   **Checksum Generation**: Calculate SHA256 checksums for individual files or entire directories.
*   **Integrity Verification**: Compare current file checksums against a previously saved manifest to detect any changes.
*   **Simple CLI**: Easy-to-use command-line interface for quick operations.

## 🚀 Usage

### Prerequisites

*   Python 3.6+

### Installation (for standalone use)

This utility is self-contained. Simply navigate into its directory.

```bash
cd utils/nightly-chronicle-keeper-checksum-calculator
```

### Calculate Checksums for a Directory

To calculate checksums for all files in a specified directory and save them to a JSON manifest:

```bash
python src/checksum_calculator.py calculate --directory /path/to/your/chronicles --output checksums.json
```

*   `--directory`: The path to the directory containing the files you wish to checksum.
*   `--output`: The filename for the JSON manifest where checksums will be saved.

### Verify Checksums Against a Manifest

To verify the current state of files in a directory against a previously generated checksum manifest:

```bash
python src/checksum_calculator.py verify --directory /path/to/your/chronicles --manifest checksums.json
```

*   `--directory`: The path to the directory containing the files to verify.
*   `--manifest`: The path to the JSON manifest file containing the saved checksums.

The verification process will report:
*   Files with changed content.
*   Files that are present in the directory but not in the manifest.
*   Files that are in the manifest but missing from the directory.
*   Files that are unchanged.

## 🛠️ Development

To run tests:

```bash
python -m unittest tests/test_checksum_calculator.py
```

## License

This utility is provided under the [MIT License](LICENSE) of the ApocalypsAI project.
