# Nightly Data Harmonizer: Untangling the Quantum Duplicates

The universe is full of echoes, and your file system is no exception! The Nightly Data Harmonizer is a whimsical-yet-powerful utility designed to detect and eliminate redundant data, bringing order to the digital chaos. By identifying files with identical content (our "quantum duplicates"), this tool can replace them with efficient hard links, saving precious disk space and harmonizing your data landscape.

Think of it as a cosmic librarian, ensuring every unique piece of information has only one physical manifestation, while all its echoes point back to the original source.

## Features

*   **Content-Based Duplication Detection**: Uses SHA256 hashing to accurately identify files with identical content, regardless of name or location.
*   **Hard Link Harmonization**: Replaces duplicate files with hard links to a single "master" file, freeing up disk space without altering file paths.
*   **Dry Run Mode**: Safely preview changes before committing to any modifications on your file system.
*   **Directory Traversal**: Recursively scans specified directories to find duplicates across your chosen data realms.

## Usage

To invoke the Nightly Data Harmonizer, simply provide one or more directories you wish to scan.

```bash
python src/harmonizer.py <directory1> [directory2 ...] [--dry-run]
```

### Arguments

*   `<directory1> [directory2 ...]`: One or more paths to directories that the harmonizer will scan for duplicate files.
*   `--dry-run`: (Optional) If specified, the utility will only report what changes *would* be made without actually modifying any files. Highly recommended for initial runs!

### Examples

**1. Perform a dry run on your 'documents' and 'backups' folders:**

```bash
python src/harmonizer.py /home/user/documents /mnt/external/backups --dry-run
```

This will show you how much space could be saved and which files would be linked, without touching your data.

**2. Live harmonization of your 'downloads' folder:**

```bash
python src/harmonizer.py /home/user/downloads
```

This will remove duplicate files in `/home/user/downloads` and replace them with hard links, saving disk space. **Use with caution after reviewing a dry run!**

## How it Works

1.  **Scanning**: The harmonizer recursively walks through the specified directories, identifying all regular files.
2.  **Hashing**: For each file, it calculates a SHA256 hash of its content. This hash acts as a unique "quantum signature."
3.  **Grouping**: Files with identical quantum signatures (hashes) are grouped together.
4.  **Linking**: For each group of duplicates, one file is chosen as the "master." All other duplicates in that group are then deleted and replaced with a hard link pointing to the master file. This means they appear as separate files in the file system but share the same underlying data blocks on disk.

## Important Considerations

*   **Hard Links**: Hard links work only within the same file system. If your directories span different partitions or drives, duplicates across those boundaries cannot be hard-linked.
*   **Data Integrity**: While hard links are generally safe, always back up critical data before running any utility that modifies your file system. The `--dry-run` option is your best friend!
*   **Symbolic Links**: The harmonizer explicitly skips symbolic links to prevent infinite loops or unintended modifications of linked targets.
