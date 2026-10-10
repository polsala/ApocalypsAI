# Nightly Digital Dust Sweeper

A whimsical yet practical bash utility to help you tidy up your digital workspace by sweeping away "digital dust" – old, unused files that accumulate over time. It's like a tiny, automated Roomba for your file system, but with a healthy dose of caution!

## Features

- **Age-based Cleanup**: Deletes files older than a specified number of days.
- **Dry Run Mode (Default)**: Safely preview which files *would* be deleted without actually removing them.
- **Safety First**: Prevents accidental deletion from critical system directories and requires explicit `--sweep` flag for live operations.
- **Minimum Age Threshold**: Ensures no files younger than 7 days are ever considered for deletion, regardless of input.

## Usage

```bash
./src/dust_sweeper.sh [OPTIONS] <directory> <age_in_days>
```

### Arguments

- `<directory>`: The path to the directory you want to clean. **Crucially, this cannot be a critical system directory like `/`, `/bin`, `/etc`, etc.**
- `<age_in_days>`: Files older than this many days will be targeted. Must be 7 or greater.

### Options

- `--sweep`: **REQUIRED to actually delete files.** Without this flag, the script will only perform a dry run and list files.
- `--help`: Display this help message.

## Examples

1. **Dry run**: See what files in `/home/user/downloads` older than 30 days would be deleted:
   ```bash
   ./src/dust_sweeper.sh /home/user/downloads 30
   ```

2. **Live sweep**: Actually delete files in `/tmp/old_logs` older than 7 days:
   ```bash
   ./src/dust_sweeper.sh --sweep /tmp/old_logs 7
   ```

3. **Display help**:
   ```bash
   ./src/dust_sweeper.sh --help
   ```

## Safety Precautions

- **Always start with a dry run!** Review the output carefully before using `--sweep`.
- The script explicitly forbids cleaning critical system directories. Attempts to do so will result in an error.
- A minimum age of 7 days is enforced to prevent accidental deletion of recently used files.
- Only regular files are targeted for deletion, not directories.

## Installation

This is a standalone bash script. Simply ensure it's executable:
```bash
chmod +x src/dust_sweeper.sh
```
