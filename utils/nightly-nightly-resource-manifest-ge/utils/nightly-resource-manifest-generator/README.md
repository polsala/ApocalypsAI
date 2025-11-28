# Nightly Resource Manifest Generator

## 📜 Overview

In the post-apocalyptic digital wasteland, knowing what data "resources" you possess is paramount. The **Nightly Resource Manifest Generator** is a whimsical-yet-useful utility designed to scan a specified directory and compile a comprehensive manifest of its contents. It provides a quick inventory of files, their sizes, and last modification times, helping you keep track of your precious digital hoard.

Think of it as a digital scavenger's logbook, automatically updated nightly, detailing every scrap of data you've managed to salvage.

## ✨ Features

*   **Directory Scanning**: Recursively scans a target directory for all files.
*   **Metadata Collection**: Gathers file name, size, and last modification timestamp.
*   **Manifest Generation**: Outputs a structured JSON report summarizing the findings.
*   **Whimsical Naming**: Because even in the apocalypse, a little charm goes a long way.

## 🚀 Usage

To run the manifest generator, execute the `manifest_generator.py` script with the target directory as an argument.

```bash
python src/manifest_generator.py --path /path/to/your/digital/hoard
```

The output will be printed to `stdout` in JSON format. You can redirect it to a file:

```bash
python src/manifest_generator.py --path /path/to/your/digital/hoard > manifest_report.json
```

### Example Output

```json
{
  "scan_path": "/path/to/your/digital/hoard",
  "scan_timestamp": "2023-10-27T04:42:00Z",
  "total_files": 3,
  "total_size_bytes": 12345,
  "files": [
    {
      "name": "data_fragment_alpha.txt",
      "path": "/path/to/your/digital/hoard/data_fragment_alpha.txt",
      "size_bytes": 123,
      "last_modified": "2023-10-26T10:00:00Z"
    },
    {
      "name": "archive/old_logs.zip",
      "path": "/path/to/your/digital/hoard/archive/old_logs.zip",
      "size_bytes": 12000,
      "last_modified": "2023-09-15T14:30:00Z"
    },
    {
      "name": "config.json",
      "path": "/path/to/your/digital/hoard/config.json",
      "size_bytes": 22,
      "last_modified": "2023-10-27T04:00:00Z"
    }
  ]
}
```

## 🛠️ Development

### Requirements

*   Python 3.11+

### Running Tests

Navigate to the `utils/nightly-resource-manifest-generator` directory and run:

```bash
python -m unittest tests/test_manifest_generator.py
```
