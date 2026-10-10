# Nightly Digital Debris Disperser

## 🧹 The Whispering Winds of Digital Tidiness 🧹

In the vast, ever-expanding cosmos of your digital realm, forgotten files and directories accumulate like cosmic dust bunnies. They linger, silent and unseen, until their temporal echoes begin to weigh down your system. Fear not, for the Nightly Digital Debris Disperser is here to help you gently sweep away these digital remnants!

This whimsical Bash utility scans specified directories for files and empty folders that have long since been touched, offering to either list them for your contemplation or gracefully relocate them to a designated 'temporal attic'.

## ✨ Features

*   **Temporal Foraging**: Identifies files and empty directories older than a specified number of days (based on modification time).
*   **List Mode**: Presents a serene list of all detected digital debris, allowing you to ponder their fate.
*   **Move Mode**: Carefully relocates qualifying files and removes empty directories, tidying your digital landscape without permanent deletion.
*   **Customizable**: Specify target paths and age thresholds.

## 🚀 Usage

To invoke the Digital Debris Disperser, simply run the script with your desired options.

```bash
bash src/debris_disperser.sh [OPTIONS]
```

### Options:

*   `-p <path>`: The target directory to scan. Defaults to the current directory (`.`).
*   `-a <age_days>`: The age threshold in days. Files/directories older than this will be considered debris. Defaults to `90` days.
*   `-m <mode>`: The action mode. Can be `list` (default) or `move`.
    *   `list`: Displays the detected debris without making any changes.
    *   `move`: Relocates qualifying files to a `.digital_debris_archive` directory within the target path and removes qualifying empty directories.
*   `-h`: Display the help message.

### Examples:

1.  **List all digital debris older than 180 days in your home directory:**
    ```bash
bash src/debris_disperser.sh -p ~/ -a 180 -m list
    ```

2.  **Relocate files older than 30 days in the current directory to the temporal attic:**
    ```bash
bash src/debris_disperser.sh -a 30 -m move
    ```

3.  **Simply see what's considered debris with default settings (90 days, current dir):**
    ```bash
bash src/debris_disperser.sh
    ```

## 📦 Installation

This utility is a standalone Bash script. Simply place `debris_disperser.sh` in your desired location, ensure it's executable (`chmod +x src/debris_disperser.sh`), and run it.

## 🧪 Testing

To ensure the Digital Debris Disperser functions as intended, run the provided test script:

```bash
bash tests/test_debris_disperser.sh
```

The tests use mocking to simulate file system states and `find` command outputs, ensuring deterministic and safe validation without altering your actual files.
