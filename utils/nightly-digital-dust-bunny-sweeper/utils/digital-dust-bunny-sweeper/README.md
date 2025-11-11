# Digital Dust Bunny Sweeper

## Overview

Are your digital spaces feeling cluttered? The ApocalypsAI Nightly Integrator presents the **Digital Dust Bunny Sweeper**! This whimsical utility helps you tidy up your filesystem by identifying empty directories and files that haven't been touched in ages, much like sweeping dust bunnies from under the couch.

It's designed to be a gentle reminder of forgotten corners of your storage, helping you reclaim space and mental clarity without actually deleting anything (it only reports).

## Features

*   **Empty Directory Detection**: Finds all directories that contain no files or subdirectories within a specified path.
*   **Ancient File Finder**: Locates files that haven't been modified for a specified number of days within a specified path.

## How to Use

1.  Navigate to the `utils/digital-dust-bunny-sweeper/` directory.
2.  Run the `dust_bunny_sweeper.py` script from your terminal.

### Examples:

*   **Scan your current directory for empty folders and files older than 365 days:**
    ```bash
    python src/dust_bunny_sweeper.py --path . --old-files 365
    ```

*   **Scan a specific directory (`/path/to/my/docs`) for only empty folders:**
    ```bash
    python src/dust_bunny-sweeper.py --path /path/to/my/docs --empty-dirs
    ```

*   **Scan your home directory for files older than 90 days (recursive by default):**
    ```bash
    python src/dust_bunny_sweeper.py --path ~/ --old-files 90
    ```

## Output

The utility will print a clear report to your console, listing the detected 'dust bunnies' in categories. No files or directories are modified or deleted by this tool; it's purely for reporting.
