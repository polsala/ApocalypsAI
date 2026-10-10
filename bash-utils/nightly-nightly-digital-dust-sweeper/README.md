# Nightly Digital Dust Sweeper

## Summary
The `nightly-digital-dust-sweeper` is a whimsical bash utility designed to help you tidy up your digital spaces. It scans specified directories for files and folders that haven't been accessed or modified in a long time, presenting them as "digital dust bunnies" ready for a good sweep. It's a gentle reminder to declutter and reclaim precious disk space.

## Usage
```bash
./src/dust_sweeper.sh <path> [age_in_days]
```

- `<path>`: The directory to start sweeping for digital dust. This is a mandatory argument.
- `[age_in_days]`: (Optional) The minimum age in days for files/directories to be considered "dust bunnies". Defaults to 90 days if not specified.

The script will output a list of files and directories that meet the criteria. It *does not* delete anything; it only reports. You can then review the list and decide what to do with your digital dust.

## Examples

1. **Sweep the current directory for items older than 90 days (default):**
   ```bash
   ./src/dust_sweeper.sh .
   ```

2. **Sweep your home directory for items older than 180 days:**
   ```bash
   ./src/dust_sweeper.sh ~/ 180
   ```

3. **Sweep a specific project directory for items older than 30 days:**
   ```bash
   ./src/dust_sweeper.sh /var/log/old_archives 30
   ```

## How it Works
The script uses the `find` command to locate files and directories based on their last modification time (`-mtime`). It then formats the output to be easily readable, showing the approximate age and last modification date of each digital dust bunny.

## Installation
Simply place the `src/dust_sweeper.sh` file in your desired location and make it executable:
```bash
chmod +x src/dust_sweeper.sh
```
