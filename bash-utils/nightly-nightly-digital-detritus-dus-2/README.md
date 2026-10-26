# Nightly Digital Detritus Duster

## Summary
The `nightly-digital-detritus-duster` is a whimsical Bash utility designed to help you tidy up your digital workspace by identifying and optionally "dusting" (moving to a quarantine directory) old or temporary files. Think of it as a friendly digital Roomba, sweeping away the forgotten bits and bytes that accumulate over time.

## Features
- **Targeted Cleaning**: Specify directories to scan for digital detritus.
- **Age-based Filtering**: Only considers files older than a configurable number of days.
- **Safe "Dusting"**: Instead of immediate deletion, files are moved to a designated "Digital Quarantine Zone" for review.
- **Dry Run Mode**: See what files would be "dusted" without actually moving anything.
- **Exclusion Patterns**: Ignore specific file types or patterns.

## Usage

```bash
./src/nightly-digital-detritus-duster.sh [OPTIONS] <DIRECTORY1> [DIRECTORY2...]
```

### Options
- `-a <days>`: Files older than `<days>` will be considered detritus. Default is 30 days.
- `-q <path>`: Specify the "Digital Quarantine Zone" directory. Default is `~/DigitalQuarantineZone`.
- `-d`: Dry run mode. Show what would be dusted without moving files.
- `-e <pattern>`: Exclude files matching this pattern (e.g., `*.log`, `temp_dir/*`). Can be used multiple times.
- `-h`: Display this help message.

### Examples

1. **Dry run in your Downloads folder for files older than 60 days:**
   ```bash
   ./src/nightly-digital-detritus-duster.sh -d -a 60 ~/Downloads
   ```

2. **Dust old temporary files in `/tmp` and `~/temp` to a custom quarantine path:**
   ```bash
   ./src/nightly-digital-detritus-duster.sh -q /var/digital_compost -a 7 /tmp ~/temp
   ```

3. **Dust files in a project's `dist/` directory, excluding `.gitkeep` files:**
   ```bash
   ./src/nightly-digital-detritus-duster.sh -a 90 -e "*.gitkeep" ~/my_project/dist
   ```

## Installation
Simply clone the repository and make the script executable:
```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/bash-utils/nightly-digital-detritus-duster
chmod +x src/nightly-digital-detritus-duster.sh
```

## Tests
To run the tests, navigate to the utility's directory and execute the test script:
```bash
cd bash-utils/nightly-digital-detritus-duster
./tests/test_detritus_duster.sh
```
