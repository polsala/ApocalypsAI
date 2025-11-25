# Nightly Echo Chamber Resonator

## 🎶 Silence the Redundancy, Amplify the Uniqueness 🎶

The **Nightly Echo Chamber Resonator** is a whimsical yet vital utility designed to detect and report duplicate files within a specified directory. In the chaotic aftermath, redundant data can clog precious storage and obscure critical information. This resonator helps you identify those echoing copies, allowing you to silence the noise and amplify the truly unique signals.

### Features

*   **Duplicate Detection**: Scans a target directory and its subdirectories for files with identical content (using SHA256 hashing).
*   **Detailed Reporting**: Provides a clear list of duplicate groups, showing all paths for each set of identical files.
*   **Whimsical Output**: Presents findings with a touch of apocalyptic charm.
*   **Self-Contained**: A single Python script with no external dependencies beyond the standard library.

### Usage

```bash
python src/resonator.py --path /path/to/your/directory
```

#### Arguments

*   `--path <directory_path>`: The root directory to scan for duplicate files. (Required)

### Example Output

```
🎶 Initiating Echo Chamber Resonation in /path/to/your/directory... 🎶

Found 2 groups of echoing files:

--- Group 1 (SHA256: a1b2c3d4e5f6...) ---
  - /path/to/your/directory/data/report_v1.txt
  - /path/to/your/directory/archive/old_report.txt
  - /path/to/your/directory/backup/report_copy.txt

--- Group 2 (SHA256: f6e5d4c3b2a1...) ---
  - /path/to/your/directory/images/logo.png
  - /path/to/your/directory/assets/brand/logo_final.png

🎶 Echo Chamber Resonation complete. Uniqueness amplified! 🎶
```

### Development

The `resonator.py` script uses `hashlib` for SHA256 hashing and `os` for directory traversal. Tests are located in `tests/test_resonator.py` and use `unittest.mock` for deterministic, offline testing.
