# Nightly Dust Bunny Sweeper

## Overview

The `nightly-dust-bunny-sweeper` is a whimsical yet practical utility designed to help you declutter your digital spaces. It scans a specified directory for old, unused files – affectionately termed 'digital dust bunnies' – and provides options to either sweep them away (delete) or tuck them into a cozy 'archive' folder.

Say goodbye to digital clutter and reclaim your disk space with a touch of apocalyptic charm!

## Features

*   **Digital Dust Bunny Detection**: Scans a target directory for files older than a specified number of days.
*   **Fluffiness Rating**: Displays file sizes (fluffiness) for easy prioritization.
*   **Interactive Cleanup**: Prompts the user to delete or archive detected dust bunnies.
*   **Cross-Platform**: Built with Node.js, it runs on Windows, macOS, and Linux.

## Installation

1.  **Ensure Node.js is installed**: If you don't have Node.js, download it from [nodejs.org](https://nodejs.org/).
2.  **Navigate to the utility directory**:
    ```bash
    cd nightly-dust-bunny-sweeper
    ```
3.  **Install dependencies**: (Currently none, but good practice)
    ```bash
    npm install
    ```

## Usage

Run the utility from your terminal. You'll need to specify the directory to scan and the age threshold in days.

```bash
node src/index.js <directory_to_scan> [options]
```

### Arguments

*   `<directory_to_scan>`: The absolute or relative path to the directory you want to scan for dust bunnies.

### Options

*   `-a, --age <days>`: Minimum age in days for a file to be considered a 'dust bunny'. Defaults to `30` days.
*   `-m, --mode <mode>`: Operation mode. Can be `report` (default), `delete`, or `archive`. In `report` mode, it only lists files. In `delete` or `archive` mode, it prompts for confirmation.
*   `-o, --output <path>`: (Only for `archive` mode) The path to the archive directory. Defaults to `./archive_dust_bunnies` within the scanned directory.
*   `-y, --yes`: Skip confirmation prompts and proceed with the chosen action (`delete` or `archive`). Use with caution!
*   `-h, --help`: Display help for command.

### Examples

1.  **Report dust bunnies older than 60 days in your Downloads folder:**
    ```bash
    node src/index.js ~/Downloads --age 60
    ```

2.  **Interactively delete dust bunnies older than 90 days in a project folder:**
    ```bash
    node src/index.js /path/to/my/project --age 90 --mode delete
    ```

3.  **Archive dust bunnies older than 30 days from a temp folder to a specific archive location, without prompting:**
    ```bash
    node src/index.js /var/tmp --age 30 --mode archive --output ~/DigitalArchives/TempDust --yes
    ```

## Development & Testing

To run tests:

```bash
node tests/index.test.js
```
