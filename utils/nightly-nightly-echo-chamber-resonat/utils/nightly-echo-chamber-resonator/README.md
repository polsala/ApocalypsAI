# Nightly Echo Chamber Resonator

## 🎶 Resonate with Clarity: Find Your Duplicates! 🎶

The digital world can be a messy place, filled with echoes of the same data. The `Nightly Echo Chamber Resonator` is here to bring clarity to your file system, identifying and reporting duplicate files that are silently consuming your precious storage.

This utility scans one or more specified directories, calculates a unique cryptographic hash for each file's content, and then groups together files that share the exact same content. It's like listening for the same note played twice in an echo chamber – once you hear it, you can't un-hear it!

## Features

*   **Content-Based Duplication**: Identifies duplicates by comparing file content hashes (SHA256), not just names or sizes.
*   **Recursive Scanning**: Traverses subdirectories to find all potential echoes.
*   **Clear Reporting**: Outputs a list of duplicate groups, showing all paths for each set of identical files.
*   **Lightweight & Self-Contained**: Written in Python, with no external dependencies beyond the standard library.

## Usage

To run the Echo Chamber Resonator, simply provide one or more paths (directories or specific files) to scan:

```bash
python src/resonator.py --path /path/to/your/documents --path /path/to/your/downloads
```

### Arguments

*   `--path <path>`: One or more paths to directories or files to scan for duplicates. This argument can be specified multiple times.

### Example Output

```
Found 2 groups of duplicate files:

Group 1 (SHA256: a1b2c3d4e5f6...):
  - /path/to/your/documents/report_v1.pdf
  - /path/to/your/downloads/old_report.pdf

Group 2 (SHA256: f6e5d4c3b2a1...):
  - /path/to/your/photos/IMG_0001_copy.jpg
  - /path/to/your/photos/IMG_0001.jpg
  - /path/to/your/backup/IMG_0001.jpg
```

## Installation

No special installation is required. Just ensure you have Python 3.6+ installed. Clone the repository, navigate to the `utils/nightly-echo-chamber-resonator` directory, and run the `resonator.py` script directly.

## Contributing

Feel free to contribute to the clarity of the digital soundscape! Open issues or pull requests on the main ApocalypsAI repository.
