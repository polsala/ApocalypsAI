# Apocalypse Prep Packager

## Overview

The `apocalypse-prep-packager` is a whimsical-yet-useful command-line utility designed to help you quickly package critical files and directories into a timestamped ZIP archive. Think of it as your last-minute digital survival kit, ensuring your most important data is consolidated and ready for any unforeseen digital disruptions.

It's perfect for creating quick backups of configuration files, essential documents, or any data you wouldn't want to lose if the digital world suddenly went sideways.

## Features

*   **Timestamped Archives**: Each package is named with a precise timestamp, making it easy to track when your 'prep' was done.
*   **Recursive Packaging**: Easily include entire directories, and the utility will handle all subdirectories and files.
*   **Self-Contained**: Written in Python, it uses only standard library modules, ensuring it runs anywhere Python 3.6+ is available.

## Installation

This utility is self-contained. Simply copy the `apocalypse-prep-packager` folder into your `utils/` directory.

## Usage

Run the `packager.py` script directly from your terminal.

```bash
python3 utils/apocalypse-prep-packager/src/packager.py --source <path_to_file_or_dir_1> [--source <path_to_file_or_dir_2> ...] --output <path_to_output_directory>
```

### Arguments:

*   `--source <path>`: One or more paths to files or directories you want to include in the package. You can specify this argument multiple times.
*   `--output <path>`: The directory where the timestamped ZIP archive will be created.

### Examples:

1.  **Package a single file:**
    ```bash
    python3 utils/apocalypse-prep-packager/src/packager.py --source ~/my_important_doc.txt --output ~/apocalypse_backups
    ```

2.  **Package an entire directory:**
    ```bash
    python3 utils/apocalypse-prep-packager/src/packager.py --source ~/my_config_folder --output ~/apocalypse_backups
    ```

3.  **Package multiple files and directories:**
    ```bash
    python3 utils/apocalypse-prep-packager/src/packager.py --source ~/my_doc.txt --source ~/project_data --output ~/apocalypse_backups
    ```

Upon successful execution, a file named `apocalypse_prep_YYYYMMDD_HHMMSS.zip` (e.g., `apocalypse_prep_20231027_143000.zip`) will be created in your specified output directory.
