# Nightly Cosmic Dust Collector

## Summary

The `nightly-cosmic-dust-collect` utility helps you tidy up your digital cosmos by identifying and managing 'cosmic dust' – stale, old, or empty files lurking in your directories. It provides options to list, archive, or delete these files, ensuring your systems remain pristine and efficient.

## Usage

```bash
bash src/cosmic_dust_collect.sh [OPTIONS] <DIRECTORY>
```

### Arguments

*   `<DIRECTORY>`: The path to the directory to scan for cosmic dust.

### Options

*   `-a, --age <DAYS>`: Files older than `<DAYS>` will be considered cosmic dust. (e.g., `--age 30` for files older than 30 days).
*   `-e, --empty`: Include zero-byte files in the cosmic dust collection.
*   `-d, --dry-run`: (Default) Show what would be done without making any changes.
*   `-r, --archive <ARCHIVE_DIR>`: Archive identified files into a tarball in the specified `<ARCHIVE_DIR>` instead of deleting them. Files will be removed after successful archiving.
*   `-D, --delete`: Permanently delete identified files. **Use with caution!**
*   `-h, --help`: Display this help message.

### Examples

*   **Find files older than 90 days in `/var/log` (dry run):**
    ```bash
    bash src/cosmic_dust_collect.sh --age 90 /var/log
    ```

*   **Archive empty files in `~/downloads` to `~/archives`:**
    ```bash
    bash src/cosmic_dust_collect.sh --empty --archive ~/archives ~/downloads
    ```

*   **Delete files older than 7 days in `/tmp` (DANGEROUS!):**
    ```bash
    bash src/cosmic_dust_collect.sh --age 7 --delete /tmp
    ```

## Installation

This is a standalone Bash script. Simply place `src/cosmic_dust_collect.sh` in your desired location and make it executable:

```bash
chmod +x src/cosmic_dust_collect.sh
```

Then run it using `bash src/cosmic_dust_collect.sh` or `./src/cosmic_dust_collect.sh` if it's in your PATH or current directory.
