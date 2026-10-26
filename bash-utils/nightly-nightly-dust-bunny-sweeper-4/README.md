# Nightly Digital Dust Bunny Sweeper

## Summary

The `nightly-dust-bunny-sweeper` is a whimsical yet practical bash utility designed to help you keep your digital environment tidy. It scans specified directories for files that haven't been accessed or modified in a long time, affectionately calling them 'digital dust bunnies'. You can use it to simply list these forgotten files or, with caution, sweep them away into the void.

In a post-apocalyptic world where every byte of storage and every CPU cycle counts, managing digital clutter is crucial. This tool helps reclaim precious resources by identifying and removing stale data.

## Usage

```bash
./src/dust-bunny-sweeper.sh [OPTIONS] <directory>
```

### Arguments

*   `<directory>`: The path to the directory you want to scan for digital dust bunnies. This is a mandatory argument.

### Options

*   `-a <days>`, `--age <days>`: Specifies the age threshold in days. Files older than this many days will be considered digital dust bunnies. Defaults to `30` days.
*   `-d`, `--delete`: Activates deletion mode. The script will prompt for confirmation before removing files unless `--force` is also used. **USE WITH EXTREME CAUTION!**
*   `-f`, `--force`: Forces deletion without any confirmation prompt. This option *must* be used in conjunction with `--delete`. **USE WITH EXTREME CAUTION!**
*   `-h`, `--help`: Displays the usage information and exits.

### Examples

1.  **List dust bunnies older than 60 days in `/var/log`:**
    ```bash
    ./src/dust-bunny-sweeper.sh --age 60 /var/log
    ```

2.  **Delete dust bunnies older than 90 days in `/tmp/old_cache` (with confirmation):**
    ```bash
    ./src/dust-bunny-sweeper.sh --age 90 --delete /tmp/old_cache
    ```

3.  **Force delete dust bunnies older than 7 days in `~/downloads` (NO CONFIRMATION!):**
    ```bash
    ./src/dust-bunny-sweeper.sh -a 7 -d -f ~/downloads
    ```

## Installation

This is a standalone bash script. Simply place `dust-bunny-sweeper.sh` in your desired location, ensure it has execute permissions, and run it.

```bash
chmod +x src/dust-bunny-sweeper.sh
```

## Testing

To run the automated tests, navigate to the utility's root directory and execute the test script:

```bash
./tests/test_dust-bunny-sweeper.sh
```
