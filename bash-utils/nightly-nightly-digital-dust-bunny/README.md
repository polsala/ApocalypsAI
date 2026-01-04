# Nightly Digital Dust Bunny Collector

## Summary

This whimsical Bash utility helps you keep your digital environment tidy by identifying and archiving old, unused files – affectionately termed "digital dust bunnies" – into a designated "void archive". It's perfect for cleaning up temporary files, old logs, or forgotten project remnants that are cluttering your system.

## Usage

```bash
./src/dust_bunny_collector.sh <target_directory> <archive_directory> <age_in_days>
```

- `<target_directory>`: The directory to scan for digital dust bunnies.
- `<archive_directory>`: The directory where identified dust bunnies will be moved. The original directory structure relative to `target_directory` will be preserved within the archive.
- `<age_in_days>`: Files older than this many days will be considered dust bunnies.

### Example

To clean up files older than 90 days in `/var/log/old_logs` and move them to `/mnt/archive/dust_bunnies`:

```bash
mkdir -p /mnt/archive/dust_bunnies
./src/dust_bunny_collector.sh /var/log/old_logs /mnt/archive/dust_bunnies 90
```

## Output

The script will print a report to standard output, detailing which files were identified as dust bunnies and where they were moved. If no dust bunnies are found, it will report that your digital space is sparkling clean!

## Requirements

- Bash (version 4.0+ recommended)
- `find` utility
- `mkdir` utility
- `mv` utility
- `realpath` utility (commonly available on most Linux distributions; for macOS, install `coreutils` via Homebrew for `grealpath` or use a simpler path resolution if `realpath` is not present).

## How it Works

1. It scans the `target_directory` for regular files (`-type f`) that haven't been modified in `age_in_days` (`-mtime +<age>`).
2. For each identified file, it determines its relative path from the `target_directory`.
3. It creates the necessary subdirectories in the `archive_directory` to maintain the original file structure.
4. It moves the file from its original location to the corresponding path within the `archive_directory`.
5. A summary report is generated at the end.
