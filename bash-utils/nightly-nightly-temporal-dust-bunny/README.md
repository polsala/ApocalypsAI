# Nightly Temporal Dust Bunny Sweeper

## Overview

The `nightly-temporal-dust-bunny-sweeper` is a whimsical yet practical bash utility designed to help you maintain a pristine digital environment. It identifies and, optionally, sweeps away old, forgotten files – affectionately termed 'temporal dust bunnies' – from your specified directories. Keep your digital wasteland tidy and free from ancient digital detritus!

## Features

*   **Age-based Cleanup**: Target files older than a specified number of days.
*   **Dry Run Mode**: Safely preview which files would be deleted without making any changes.
*   **Verbose Output**: See the full list of detected dust bunnies.
*   **Recursive Search**: Scans subdirectories for hidden digital clutter.

## Usage

```bash
./src/temporal_dust_bunny_sweeper.sh [OPTIONS] <directory>
```

### Arguments

*   `<directory>`: The path to the directory you wish to sweep for temporal dust bunnies. This is a mandatory argument.

### Options

*   `-d <days>`: Specify the age threshold in days. Files older than this many days will be considered temporal dust bunnies. Defaults to `30` days.
*   `-x`: **Execute deletion**. By default, the script runs in dry-run mode, only listing files. Use this option to actually remove the detected files.
*   `-v`: **Verbose output**. Displays the full paths of all detected temporal dust bunnies.
*   `-h`: Display the help message and exit.

## Examples

1.  **Dry run to find files older than 60 days in your home directory:**
    ```bash
    ./src/temporal_dust_bunny_sweeper.sh -d 60 ~/my_project_logs
    ```

2.  **Execute deletion of files older than 7 days in `/tmp`, with verbose output:**
    ```bash
    ./src/temporal_dust_bunny_sweeper.sh -d 7 -x -v /tmp
    ```

3.  **Check for any files older than the default 30 days in the current directory:**
    ```bash
    ./src/temporal_dust_bunny_sweeper.sh .
    ```

## Installation

This utility is a standalone bash script. Simply ensure it's executable:

```bash
chmod +x src/temporal_dust_bunny_sweeper.sh
```

Then, you can run it directly or add it to your system's PATH for easier access.

## Contributing

Feel free to contribute to the ongoing battle against digital clutter! Suggestions for new features, bug reports, or whimsical output messages are always welcome.
