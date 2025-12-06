# Digital Dust Bunny Collector

## 🧹 Your Digital Wasteland Cleanup Crew 🧹

In the vast, ever-expanding digital landscape, forgotten files accumulate like dust bunnies under a server rack. The `digital-dust-bunny-collector` is your trusty utility for identifying these digital relics – files that haven't been touched in ages – helping you reclaim precious disk space and bring order to your data chaos.

Whether you're preparing for the next data apocalypse or just tidying up, this tool helps you pinpoint those long-lost files that are just taking up space.

## Features

*   **Scan Directories**: Recursively scans specified directories for files.
*   **Age-Based Filtering**: Identifies files older than a configurable number of days (e.g., 90 days, 180 days).
*   **Exclusion Rules**: Ignore specific file extensions (e.g., `.log`, `.tmp`) or entire directories.
*   **Report Generation**: Outputs a list of identified "dust bunnies" for review.

## Usage

### Prerequisites

*   Python 3.8+

### Running the Collector

1.  Navigate to the `utils/digital-dust-bunny-collector/` directory.
2.  Run the `collector.py` script with the desired path and options:

    ```bash
    python src/collector.py /path/to/scan --min-age-days 180 --exclude-ext .log .tmp --exclude-dir node_modules .git
    ```

### Command-Line Arguments

*   `<path>` (positional): The root directory to start scanning from.
*   `--min-age-days <int>`: Minimum age in days for a file to be considered a "dust bunny" (default: 90).
*   `--exclude-ext <ext1> [<ext2> ...]`: Space-separated list of file extensions to ignore (e.g., `.log`, `.bak`).
*   `--exclude-dir <dir1> [<dir2> ...]`: Space-separated list of directory names to ignore (e.g., `node_modules`, `.git`).

### Example Output

```
Scanning '/path/to/scan' for digital dust bunnies older than 90 days...
Excluding extensions: .log, .tmp
Excluding directories: node_modules, .git

Found 3 digital dust bunnies older than 90 days in '/path/to/scan':
- /path/to/scan/old_project/legacy_code.py (Last modified: 2023-01-15)
- /path/to/scan/downloads/unopened_archive.zip (Last modified: 2022-11-01)
- /path/to/scan/documents/forgotten_memo.txt (Last modified: 2023-02-28)
```

## Development

### Running Tests

To ensure the dust bunnies are properly identified (and not just imaginary), run the tests:

```bash
python -m unittest tests/test_collector.py
```
