# Nightly Digital Dust Bunny Sweeper

## Overview

In the post-apocalyptic digital wasteland, data accumulates like dust. The `nightly-digital-dust-bunny-sweeper` is a whimsical-yet-useful utility designed to help you identify and manage these "digital dust bunnies" – old, forgotten files that clutter your storage. It scans a specified directory (and optionally its subdirectories) for files older than a given threshold and generates a report, helping you decide what to clean up, archive, or repurpose.

Think of it as a friendly robot vacuum for your file system, but instead of sucking up physical dust, it highlights digital detritus.

## Features

*   **Directory Scanning**: Recursively scans a target directory.
*   **Age-based Filtering**: Identifies files older than a configurable number of days.
*   **Detailed Reporting**: Outputs a list of "dusty" files, their size, and their age.
*   **Whimsical Output**: Presents findings in a charming, easy-to-read format.

## Installation

1.  Navigate to the `node-utils/nightly-digital-dust-bunny-sweeper` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

Run the utility from the command line:

```bash
node src/index.js <directory_path> [options]
```

### Arguments

*   `<directory_path>`: The path to the directory you want to scan. This is a required argument.

### Options

*   `-a, --age <days>`: The minimum age in days for a file to be considered a "dust bunny". Files older than this will be reported. Defaults to `90` days.
*   `-r, --recursive`: Scan subdirectories recursively. By default, only the top-level directory is scanned.
*   `-o, --output <file_path>`: Output the report to a specified file instead of the console.
*   `-h, --help`: Display help information.

### Examples

Scan the current directory for files older than 180 days, recursively:

```bash
node src/index.js . --age 180 --recursive
```

Scan a specific directory and output the report to a file:

```bash
node src/index.js /path/to/my/old/files -o dust_report.txt
```

## Development & Testing

To run the tests:

```bash
npm test
```

The tests use Jest and mock the file system operations to ensure deterministic and fast execution without touching actual files.
