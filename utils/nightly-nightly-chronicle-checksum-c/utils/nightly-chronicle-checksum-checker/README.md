# Nightly Chronicle Checksum Checker

## 📜 Overview

In the tumultuous aftermath, preserving the integrity of our precious chronicles, data fragments, and survival manifests is paramount. The "Nightly Chronicle Checksum Checker" is a humble yet vital utility designed to ensure that your most critical files remain untainted by cosmic rays, digital decay, or mischievous gremlins.

It generates and verifies SHA256 checksums, providing a digital fingerprint for your data. If a single byte shifts, this checker will sound the alarm!

## ✨ Features

*   **Generate Checksum**: Create a `.sha256` file for any given file, containing its unique cryptographic hash.
*   **Verify Checksum**: Compare a file against its corresponding `.sha256` file to detect any alterations.
*   **Simple CLI**: Easy to use from your terminal.

## 🚀 Usage

### Prerequisites

*   Python 3.6+ (standard library only)

### Installation

No installation needed! Just place the `checksum_checker.py` script in your path or run it directly.

### Generating a Checksum

To generate a checksum for a file named `my_important_chronicle.txt`:

```bash
python src/checksum_checker.py generate my_important_chronicle.txt
```

This will create a file named `my_important_chronicle.txt.sha256` in the same directory, containing the SHA256 hash and the original filename.

### Verifying a Checksum

To verify `my_important_chronicle.txt` against its checksum file:

```bash
python src/checksum_checker.py verify my_important_chronicle.txt
```

The utility will report whether the file's integrity is intact or if corruption has been detected.

## 🛠️ Development

The `checksum_checker.py` script is self-contained and uses only standard Python libraries.

### Running Tests

To ensure the checker is functioning correctly, navigate to the `utils/nightly-chronicle-checksum-checker` directory and run:

```bash
python -m unittest tests/test_checksum_checker.py
```

## License

This utility is released under the MIT License. See the main repository's `LICENSE` file for details.
