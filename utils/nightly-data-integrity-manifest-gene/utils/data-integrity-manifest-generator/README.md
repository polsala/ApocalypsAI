# Data Integrity Manifest Generator

## 📜 Overview

In the face of digital entropy and the looming byte-rot, the `data-integrity-manifest-generator` is your trusty companion for cataloging and verifying your precious data. This utility scans a specified directory, calculates SHA256 hashes for each file, and compiles a comprehensive JSON manifest. Think of it as a digital time capsule's inventory list, ensuring that when the dust settles, you can confirm your files are exactly as you left them.

## ✨ Features

*   **Directory Scanning**: Recursively traverses a specified directory.
*   **SHA256 Hashing**: Generates robust cryptographic hashes for each file.
*   **JSON Manifest**: Outputs a human-readable and machine-parseable manifest.
*   **Self-Contained**: Pure Python, no external dependencies beyond the standard library.

## 🚀 Usage

To generate a manifest for a directory, simply run the script with the `--path` argument:

```bash
python src/manifest_generator.py --path /path/to/your/important/data --output manifest.json
```

### Arguments:

*   `--path <directory>`: The root directory to scan. (Required)
*   `--output <filename>`: The output JSON file name. (Optional, defaults to `manifest.json` in the current directory)

## 📦 Example Output

```json
{
  "timestamp": "2023-10-27T10:00:00Z",
  "root_path": "/path/to/your/important/data",
  "files": [
    {
      "path": "file1.txt",
      "size": 1234,
      "sha256": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2"
    },
    {
      "path": "subdir/image.jpg",
      "size": 56789,
      "sha256": "b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3"
    }
  ]
}
```
