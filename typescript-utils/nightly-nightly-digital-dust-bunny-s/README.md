# Nightly Digital Dust Bunny Sweeper

A whimsical-yet-useful TypeScript CLI tool designed to help you identify and manage digital clutter. It scans specified directories for files that resemble "digital dust bunnies" – old, large, or infrequently accessed files – and presents them for your review, suggesting archiving or deletion. Keep your digital spaces tidy and efficient!

## Features

*   **Directory Scanning**: Recursively scans a target directory.
*   **Age-based Filtering**: Identifies files older than a specified number of days.
*   **Size-based Filtering**: Flags files larger than a given size (in MB).
*   **Dry Run Mode**: Preview suggested "dust bunnies" without taking any action. (This utility always operates in dry-run mode for safety).
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.

## Installation

1.  **Prerequisites**: Ensure you have Node.js (which includes npm) and `ts-node` installed.
    ```bash
    node -v
    npm -v
    npm install -g ts-node typescript # If you don't have them
    ```
2.  **Clone the repository (or navigate to the utility's directory)**:
    ```bash
    # Assuming you are in the root of the ApocalypsAI repository
    cd typescript-utils/nightly-digital-dust-bunny-sweeper
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    ```

## Usage

Run the utility using `ts-node` followed by the path to the `index.ts` file and your desired arguments.

```bash
ts-node src/index.ts <directory_to_scan> [--age <days>] [--size <MB>]
```

### Arguments:

*   `<directory_to_scan>` (required): The path to the directory you want to scan for digital dust bunnies.
*   `--age <days>` (optional): Files older than this many days will be flagged. Default: 365 (1 year).
*   `--size <MB>` (optional): Files larger than this many megabytes will be flagged. Default: 100 (100 MB).

### Examples:

1.  **Scan your `Documents` folder for files older than 2 years (730 days) or larger than 500MB:**
    ```bash
    ts-node src/index.ts ~/Documents --age 730 --size 500
    ```
2.  **Scan a project directory for any files older than 90 days, using default size (100MB):**
    ```bash
    ts-node src/index.ts ./my-old-project --age 90
    ```
3.  **Scan a specific folder for large files (over 1GB) regardless of age:**
    ```bash
    ts-node src/index.ts /var/log --size 1024
    ```

## Development & Testing

To build the TypeScript code:
```bash
npm run build
```

To run tests:
```bash
npm test
```
