# Nightly Temporal Debris Sweeper

## Overview

The `nightly-temporal-debris-sweep` is a whimsical yet practical utility designed to help you maintain a clean filesystem by identifying and optionally purging "temporal debris" – files and logs that have overstayed their welcome. Think of it as a digital broom for your timelines, ensuring your directories remain free of unnecessary clutter.

## Features

- **Configurable Target Directory**: Specify which directory to scan for old files.
- **Adjustable Age Threshold**: Define how old a file must be to be considered "temporal debris" (in days).
- **Dry Run Mode (Default)**: Safely preview which files would be swept without actually deleting anything.
- **Commit Mode**: Execute the purge and remove the identified temporal debris.
- **Whimsical Messaging**: Enjoy a touch of ApocalypsAI charm with messages about temporal anomalies and timeline clarity.

## Usage

To run the Temporal Debris Sweeper, navigate to its directory and execute the script. It accepts several command-line options:

```bash
bash src/temporal_debris_sweep.sh [OPTIONS]
```

### Options:

- `-d <directory>`: Specifies the target directory to scan. Defaults to the current directory (`.`).
- `-a <age_days>`: Sets the age threshold in days. Files older than this will be flagged as temporal debris. Defaults to `7` days.
- `-c`: **Commit to sweeping**. This flag will cause the script to actually delete the identified files. **Use with caution!** By default, the script runs in dry-run mode, only listing files.
- `-h`: Displays the help message and exits.

### Examples:

1. **Dry run in the current directory for files older than 7 days (default behavior):**
   ```bash
bash src/temporal_debris_sweep.sh
   ```

2. **Dry run in `/var/log` for files older than 30 days:**
   ```bash
bash src/temporal_debris_sweep.sh -d /var/log -a 30
   ```

3. **Commit to sweeping files older than 14 days in `/tmp`:**
   ```bash
bash src/temporal_debris_sweep.sh -d /tmp -a 14 -c
   ```

4. **Display help message:**
   ```bash
bash src/temporal_debris_sweep.sh -h
   ```

## How it Works

The script uses the `find` command to locate regular files (`-type f`) within the specified directory that have a modification time (`-mtime`) older than the given age threshold. It then either lists these files (dry run) or pipes them to `rm -f` for deletion (commit mode). Filenames are handled safely using `find -print0` and `xargs -0`.

## Installation

This utility is a standalone Bash script. No special installation is required beyond having Bash available on your system. Simply clone the repository and run the script.

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/bash-utils/nightly-temporal-debris-sweep
bash src/temporal_debris_sweep.sh -h
```

## Contributing

Feel free to contribute to the ApocalypsAI project! If you have ideas for improving the Temporal Debris Sweeper or other utilities, please open an issue or submit a pull request.
