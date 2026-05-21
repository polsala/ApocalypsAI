# Nightly Digital Dust Bunny Sweeper

## Overview
The `nightly-digital-dust-bunny-sweeper` is a whimsical Bash utility designed to help you tidy up your digital spaces. It identifies files that haven't been accessed in a specified number of days, metaphorically sweeping them away like digital dust bunnies. You can use it to list these forgotten files or move them to a designated archive directory.

## Features
- **Identify Stale Files**: Locates files in a target directory that haven't been accessed for a configurable duration.
- **Dry Run Mode**: Preview which files would be affected without making any changes.
- **Archive Functionality**: Move identified "dust bunnies" to a specified archive directory for later review or deletion.
- **Whimsical Output**: Enjoy charming messages as you clean your digital abode.

## Usage

```bash
./src/dust_bunny_sweeper.sh <target_directory> <days_old> [archive_directory] [--dry-run]
```

### Arguments:
- `<target_directory>`: The directory to scan for digital dust bunnies.
- `<days_old>`: The minimum age (in days) a file must be (based on last access time) to be considered a dust bunny.
- `[archive_directory]` (Optional): If provided, identified files will be moved to this directory. If omitted, the script will only list the files.
- `--dry-run` (Optional): If present, the script will only list files and report what *would* happen, without performing any moves. This is implied if `archive_directory` is not provided.

### Examples:

1. **List all files in `/var/log` not accessed in the last 30 days (dry run by default):**
   ```bash
   ./src/dust_bunny_sweeper.sh /var/log 30
   ```

2. **List all files in `~/Downloads` not accessed in the last 90 days (explicit dry run):**
   ```bash
   ./src/dust_bunny_sweeper.sh ~/Downloads 90 --dry-run
   ```

3. **Move files in `/tmp/old_stuff` not accessed in the last 7 days to `/tmp/archive`:**
   ```bash
   ./src/dust_bunny_sweeper.sh /tmp/old_stuff 7 /tmp/archive
   ```

## Installation
Simply clone the repository and ensure the script has execute permissions:
```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/bash-utils/nightly-digital-dust-bunny-sweeper
chmod +x src/dust_bunny_sweeper.sh
```

## Testing
To run the automated tests:
```bash
./tests/test_dust_bunny_sweeper.sh
```
