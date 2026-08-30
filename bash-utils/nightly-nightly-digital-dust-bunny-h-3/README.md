# Nightly Digital Dust Bunny Hunt

## Summary
The `nightly-digital-dust-bunny-hunt` utility helps you discover forgotten files and directories (our "digital dust bunnies") that haven't been modified in a specified number of days. It's a whimsical way to identify old cruft that might be cluttering your storage.

## Usage

```bash
./src/dust_bunny_hunt.sh [-p <path>] [-a <age_days>] [-t <type>] [-h]
```

### Options
*   `-p <path>`: The starting directory to search. Defaults to the current directory (`.`).
*   `-a <age_days>`: The minimum age in days. Files/directories modified *before* this many days ago will be reported. Defaults to `30` days.
*   `-t <type>`: The type of digital dust bunny to hunt.
    *   `f`: Hunt for files only (default).
    *   `d`: Hunt for directories only.
    *   `a`: Hunt for all (files and directories).
*   `-h`: Display the help message and exit.

## Examples

1.  **Find all files older than 60 days in the current directory:**
    ```bash
    ./src/dust_bunny_hunt.sh -a 60
    ```

2.  **Find directories older than 90 days in your home directory:**
    ```bash
    ```bash
    ./src/dust_bunny_hunt.sh -p ~/ -a 90 -t d
    ```

3.  **Find all files and directories older than 7 days in a specific project folder:**
    ```bash
    ./src/dust_bunny_hunt.sh -p /var/log/old_archives -a 7 -t a
    ```

4.  **Display help message:**
    ```bash
    ./src/dust_bunny_hunt.sh -h
    ```

## How it Works
The script uses the `find` command with the `-mtime` (modification time) option to locate items older than the specified age. It then prints a whimsical message for each "dust bunny" found.

## Deterministic Tests
The `tests/test_dust_bunny_hunt.sh` script creates a temporary directory and populates it with files and directories whose modification times are precisely controlled using `touch -d`. This ensures that the `find` command, when run by the main utility, produces consistent and predictable results, making the tests deterministic and reliable regardless of the execution environment or current date.
