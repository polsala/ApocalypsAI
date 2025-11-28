# Nightly Asset Auditor

## "Rummaging Through the Digital Rubble"

This utility, the `Nightly Asset Auditor`, is designed to help you take stock of your digital assets. Whether you're recovering from a catastrophic data event, performing a routine cleanup, or just curious about the composition of your directories, this tool will scan a specified path, categorize files by their extensions, and provide a comprehensive report on counts, total sizes, and even highlight the largest files.

It's like a digital archaeologist, sifting through the layers of your file system to reveal what truly remains.

## Features

*   **Directory Scanning**: Recursively scans a target directory.
*   **File Categorization**: Groups files by their extensions (e.g., `.py`, `.txt`, `.jpg`).
*   **Size Aggregation**: Calculates the total size for each file type.
*   **Largest Files**: Identifies and lists the top 10 largest files found by default.
*   **Human-Readable Report**: Presents the findings in a clear, concise format.

## Usage

To run the auditor, simply execute the `auditor.py` script with the path you wish to audit:

```bash
python3 src/auditor.py /path/to/your/directory
```

### Example Output

```
Asset Audit Report for: /path/to/your/directory
------------------------------------------------

Total Files Scanned: 150
Total Size Scanned: 1.2 GB

File Type Summary:
------------------
.py   : 50 files (25.5 MB)
.txt  : 30 files (1.2 MB)
.jpg  : 20 files (800.0 MB)
.png  : 15 files (150.0 MB)
.md   : 35 files (0.5 MB)

Top Largest Files:
---------------------
1.  /path/to/your/directory/images/large_photo.jpg (250.0 MB)
2.  /path/to/your/directory/data/archive.zip (180.0 MB)
3.  /path/to/your/directory/videos/clip.mp4 (100.0 MB)
...
```

## Development

### Running Tests

To ensure the auditor is working correctly, run the provided tests:

```bash
python3 -m unittest tests/test_auditor.py
```
