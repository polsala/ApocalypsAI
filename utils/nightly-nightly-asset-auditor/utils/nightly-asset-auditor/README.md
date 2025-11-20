# Nightly Asset Auditor

## Overview

The Nightly Asset Auditor is a whimsical-yet-useful utility designed to help you make sense of your digital landscape after a 'cataclysmic event' – or just a regular day of coding. It scans a specified directory and all its subdirectories, providing a concise summary of your files.

Ever wondered how many `.py` files you have, or how much space your `.json` logs are taking up? This tool gives you a quick overview of your digital 'rubble' and 'assets', categorized by file extension, count, and total size.

## Features

*   **Directory Scanning**: Recursively scans all subdirectories.
*   **File Type Categorization**: Groups files by their extension.
*   **Size Calculation**: Reports total size for each file type and overall.
*   **Exclusion List**: Ignores common development and system directories (`.git`, `node_modules`, `__pycache__`, etc.) to focus on relevant assets.
*   **Human-Readable Output**: Presents results in a clear, formatted table.

## Usage

To run the auditor, simply execute the `auditor.py` script with the path to the directory you wish to audit:

```bash
python src/auditor.py /path/to/your/project
```

### Example Output

```
Apocalypse Asset Audit Report for: /path/to/your/project
---------------------------------------------------

Total Files Scanned: 15
Total Size: 1.25 MB

File Type Summary:

| Extension | Count | Total Size |
| :-------- | :---- | :--------- |
| .py       | 5     | 500 KB     |
| .md       | 3     | 200 KB     |
| .json     | 4     | 400 KB     |
| .txt      | 2     | 100 KB     |
| (no ext)  | 1     | 50 KB      |
---------------------------------------------------
Audit Complete. May your digital assets be ever in your favor.
```

## Development

### Requirements

*   Python 3.6+

### Running Tests

Navigate to the `utils/nightly-asset-auditor` directory and run:

```bash
python -m unittest tests/test_auditor.py
```
