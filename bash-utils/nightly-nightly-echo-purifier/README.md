# Nightly Echo Purifier

## Summary

The `nightly-echo-purifier` is a whimsical-yet-useful utility designed to detect and report duplicate files across one or more specified directories. In the ApocalypsAI lore, these redundant files are referred to as 'temporal echoes' that clutter the 'echo chambers' of your system. By identifying and listing these duplicates, the utility helps you maintain a clean and efficient data landscape, preventing unnecessary storage consumption and potential confusion.

## Usage

To run the Echo Purifier, simply provide one or more directory paths as arguments:

```bash
./src/echo_purifier.sh <directory1> [directory2 ...]
```

**Example:**

```bash
./src/echo_purifier.sh /path/to/my/data /path/to/my/backups
```

The script will scan all regular files within the specified directories (and their subdirectories), calculate their MD5 checksums, and then group and report any files that share identical checksums.

### Output Format

The output will list groups of duplicate files, each preceded by the shared MD5 checksum:

```
Duplicate Group (Checksum: <md5_checksum>):
  - /path/to/first/duplicate/file.txt
  - /path/to/second/duplicate/file_copy.txt
  - /path/to/another/duplicate/file.bak

Duplicate Group (Checksum: <another_md5_checksum>):
  - /path/to/yet/another/file.log
  - /path/to/archive/old_file.log
```

## Requirements

- Bash (version 4.0 or higher recommended)
- `find` utility
- `md5sum` utility (or `shasum -a 256` if `md5sum` is not available, though `md5sum` is preferred for consistency)
- `sort` utility
- `awk` utility

## How it Works

1.  **File Discovery**: Uses `find` to locate all regular files within the provided directories.
2.  **Checksum Calculation**: For each file, it computes an MD5 checksum using `md5sum`.
3.  **Grouping**: It then groups files by their checksums.
4.  **Reporting**: Finally, it identifies and prints groups where more than one file shares the same checksum, indicating a duplicate.

This utility is read-only and will not modify or delete any files. It only reports the detected duplicates.
