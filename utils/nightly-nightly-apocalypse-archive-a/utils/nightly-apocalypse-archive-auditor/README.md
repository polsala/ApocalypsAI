# Nightly Apocalypse Archive Auditor

## Overview

In the grim future of ApocalypsAI, even digital archives need auditing. The "Nightly Apocalypse Archive Auditor" is a whimsical yet practical utility designed to help you make sense of your digital hoard. It scans a specified directory, recursively identifying all files, categorizing them by extension, and providing a summary of file counts and total sizes for each type.

Whether you're cataloging salvaged data drives or just tidying up your pre-apocalypse backups, this tool offers a quick overview of your digital assets.

## Features

*   **Recursive Scanning**: Explores all subdirectories from the given path.
*   **File Type Categorization**: Groups files by their extensions (e.g., `.txt`, `.jpg`, `.py`).
*   **Count & Size Summary**: Provides a total count and cumulative size for each file type.
*   **Human-Readable Output**: Presents results in a clear, easy-to-read format.

## Usage

1.  **Navigate**: Change into the `src` directory:
    ```bash
    cd utils/nightly-apocalypse-archive-auditor/src
    ```
2.  **Run**: Execute the `auditor.py` script, providing the path to the directory you wish to audit.
    ```bash
    python auditor.py /path/to/your/archive
    ```
    Replace `/path/to/your/archive` with the actual directory you want to scan.

### Example Output

```
Apocalypse Archive Audit Report for: /path/to/your/archive
------------------------------------------------------------

.txt  | Count:     10 | Size:   1.2 MB
.jpg  | Count:     50 | Size:  25.5 MB
.py   | Count:      5 | Size: 150.0 KB
.log  | Count:      3 | Size:   5.0 MB
(No Ext) | Count:     2 | Size: 200.0 KB

------------------------------------------------------------
Total Files: 70
Total Size: 32.0 MB
------------------------------------------------------------
```

## Development

The `auditor.py` script is written in Python 3.11 and uses only standard library modules (`os`, `sys`).

## Testing

To run the tests, navigate to the `tests` directory and execute `pytest` (ensure `pytest` is installed: `pip install pytest`):

```bash
cd utils/nightly-apocalypse-archive-auditor/tests
pytest
```
