# Nightly Chrono-Sync File Aligner

## Summary
The `nightly-chrono-sync-aligner` is a whimsical-yet-useful Bash utility designed to help you maintain temporal consistency across your scavenged data caches. It compares the modification timestamps of files in two specified directories, reporting any 'temporal misalignments' (different modification times) or 'dimensional shifts' (files missing in one directory).

In the chaotic post-apocalyptic landscape, ensuring your data is in sync is paramount. This tool acts as your digital chronometer, highlighting files that have drifted out of alignment.

## Usage
```bash
./src/chrono_sync_aligner.sh <source_directory> <target_directory>
```

**Arguments:**
*   `<source_directory>`: The path to the primary directory you want to compare from.
*   `<target_directory>`: The path to the secondary directory you want to compare against.

## Example Output
```
[ALIGNED] data/report.txt (Source: 1672567200, Target: 1672567200)
[MISALIGNED] logs/server.log (Source: 1672567200, Target: 1672570800)
[MISSING_TARGET] config/settings.ini (Source: 1672567200)
[MISSING_SOURCE] backups/old_data.zip (Target: 1672567200)
```

## Status Meanings
*   `[ALIGNED]`: The file exists in both directories and has the exact same modification timestamp.
*   `[MISALIGNED]`: The file exists in both directories but their modification timestamps differ.
*   `[MISSING_TARGET]`: The file exists in the source directory but is not found in the target directory.
*   `[MISSING_SOURCE]`: The file exists in the target directory but is not found in the source directory.

## Requirements
*   Bash shell (version 4.0 or higher for associative arrays)
*   `stat` command (GNU coreutils version is assumed for epoch timestamp output, e.g., `stat -c %Y`. On macOS/BSD, `stat -f %m` would be needed, but this script currently relies on GNU `stat`.)
*   `find` command
*   `realpath` command (typically part of GNU coreutils)
