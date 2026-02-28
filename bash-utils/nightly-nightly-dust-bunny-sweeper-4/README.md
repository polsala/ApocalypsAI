# Nightly Digital Dust Bunny Sweeper

## Summary

The `nightly-dust-bunny-sweeper` is a whimsical-yet-useful bash utility designed to help you declutter your digital workspace by identifying and optionally removing old, large, or temporary files. Think of it as a friendly robot sweeping away the "digital dust bunnies" that accumulate over time.

## Usage

To run the sweeper, simply execute the script. It will scan the current directory by default for files older than 30 days or larger than 100MB.

```bash
./src/dust_bunny_sweeper.sh
```

### Options

- `-d <directory>`: Specify the target directory to sweep. Defaults to the current directory (`.`).
- `-a <days>`: Identify files older than `<days>` (modification time). Defaults to `30`.
- `-s <megabytes>`: Identify files larger than `<megabytes>` (in MB). Defaults to `100`.
- `-p <pattern>`: Identify files matching a specific glob `<pattern>` (e.g., `*.tmp`, `cache/*`). Can be used multiple times.
- `-f`: Force deletion without confirmation. Use with caution!
- `-h`: Display help message.

### Examples

1. **Sweep current directory for default dust bunnies:**
   ```bash
   ./src/dust_bunny_sweeper.sh
   ```

2. **Sweep `/var/log` for files older than 7 days:**
   ```bash
   ./src/dust_bunny_sweeper.sh -d /var/log -a 7
   ```

3. **Find large cache files in your home directory:**
   ```bash
   ./src/dust_bunny_sweeper.sh -d ~/ -s 500 -p "cache/*"
   ```

4. **Force delete all `.tmp` files older than 1 day in `/tmp`:**
   ```bash
   ./src/dust_bunny_sweeper.sh -d /tmp -a 1 -p "*.tmp" -f
   ```

## How it Works

The script uses the `find` command to locate files based on the specified criteria. It then presents a list of these "digital dust bunnies" and, unless `-f` is used, prompts for confirmation before permanently deleting them using `rm`.

## Installation

No special installation is required. Simply ensure the `dust_bunny_sweeper.sh` script is executable:

```bash
chmod +x src/dust_bunny_sweeper.sh
```
