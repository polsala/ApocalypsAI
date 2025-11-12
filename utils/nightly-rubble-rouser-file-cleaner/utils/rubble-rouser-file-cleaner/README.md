# Rubble-Rouser File Cleaner

## Clear the Digital Wasteland!

The digital world, much like a post-apocalyptic landscape, can accumulate a lot of forgotten "rubble." The Rubble-Rouser File Cleaner is your trusty companion for tidying up your file system, identifying forgotten empty directories and pesky duplicate files that hog precious storage.

### Features

*   **Empty Directory Detection**: Scans a specified path for subdirectories that contain no files or subdirectories.
*   **Duplicate File Identification**: Finds files with identical content (using MD5 hashing) across your chosen path, helping you reclaim disk space.
*   **Safe Reporting**: Provides a clear report of findings before any action is taken. (Deletion functionality is planned for future iterations, currently it only reports.)

### Installation

This utility is self-contained. Simply copy the `rubble-rouser-file-cleaner` directory to your desired location.

### Usage

Run the `rubble_rouser.py` script from your terminal.

```bash
python src/rubble_rouser.py --path /path/to/scan
```

**Arguments:**

*   `--path <directory>`: The root directory to start scanning from. **Required.**
*   `--find-empty-dirs`: Enable scanning for empty directories.
*   `--find-duplicates`: Enable scanning for duplicate files.
*   `--verbose`: Print more detailed output during scanning.

**Example:**

To find empty directories and duplicate files in your `~/documents` folder:

```bash
python src/rubble_rouser.py --path ~/documents --find-empty-dirs --find-duplicates
```

### Why use Rubble-Rouser?

Even in the most organized digital shelters, clutter accumulates. This tool helps you:
*   **Reclaim Disk Space**: Identify and remove unnecessary duplicates.
*   **Improve Navigation**: Get rid of empty folders that make browsing cumbersome.
*   **Maintain Sanity**: A clean file system is a happy file system, even after the apocalypse.
