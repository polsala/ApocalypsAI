# Digital Dust Bunny Sweeper

## Overview

The Digital Dust Bunny Sweeper is a whimsical-yet-useful Python CLI utility designed to help you maintain a clean and lean repository or project directory. It scans a specified path for 'digital dust bunnies' – common culprits of digital clutter like empty directories, old log files, and temporary build artifacts – and provides a list of suggested items for deletion.

Think of it as a tiny, automated janitor for your codebase, ensuring that only the essential files remain, ready for the next cosmic alignment or apocalyptic event.

## Features

*   **Empty Directory Detection**: Identifies and lists directories that contain no files or subdirectories.
*   **Log & Temp File Identification**: Finds files with common log (`.log`), temporary (`.tmp`), or backup (`.bak`, `.swp`, `.temp`) extensions.
*   **Build Artifact Spotting**: Locates common build output directories (`__pycache__`, `build`, `dist`, `target`, `.venv`, `env`) and OS-specific junk files (`.DS_Store`, `Thumbs.db`).
*   **Safe Suggestions**: By default, it only suggests items for deletion, allowing you to review before taking action.

## Installation

This utility is self-contained. You can run it directly with Python 3.11+.

```bash
cd utils/digital-dust-bunny-sweeper
python3 src/sweeper.py --help
```

## Usage

To scan your current directory for dust bunnies:

```bash
python3 src/sweeper.py .
```

To scan a specific directory (e.g., your project's `temp` folder):

```bash
python3 src/sweeper.py /path/to/your/project/temp
```

### Arguments

*   `<path>` (required): The directory to scan.

## Example Output

```
Scanning /path/to/your/project for digital dust bunnies...

Found 5 digital dust bunnies:

- [EMPTY DIR] /path/to/your/project/empty_folder
- [LOG/TEMP FILE] /path/to/your/project/logs/app.log
- [LOG/TEMP FILE] /path/to/your/project/temp/temp_data.tmp
- [BUILD ARTIFACT DIR] /path/to/your/project/__pycache__
- [BUILD ARTIFACT] /path/to/your/project/.DS_Store

Review the list above. To remove them, you would typically use 'rm -rf' or similar commands manually.
```

## Development

To run tests:

```bash
cd utils/digital-dust-bunny-sweeper
python3 -m unittest tests/test_sweeper.py
```
