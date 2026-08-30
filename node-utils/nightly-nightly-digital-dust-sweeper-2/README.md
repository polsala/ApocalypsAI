# Nightly Digital Dust Bunny Sweeper

## Summary
The Nightly Digital Dust Bunny Sweeper is a whimsical-yet-useful command-line utility designed to help you identify and manage old, unused files lurking in your directories. Think of these as "digital dust bunnies" – forgotten files accumulating over time, consuming precious storage and mental bandwidth. This tool helps you sweep them away, either by listing them for review or moving them to a designated "quarantine zone."

## Features
- **Scan for Ancient Files**: Recursively scans a specified directory for files older than a given number of days.
- **List Findings**: Outputs a clear list of identified "dust bunnies" with their paths and age.
- **Quarantine Option**: Safely moves identified files to a specified quarantine directory, rather than immediately deleting them. This allows for review before permanent removal.
- **Cross-Platform**: Built with Node.js, it runs on Windows, macOS, and Linux.

## Installation

1.  **Prerequisites**: Ensure you have Node.js (v14 or higher) installed.
2.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-digital-dust-sweeper
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    ```

## Usage

The utility can be run directly using `node` or via its `bin` alias `dust-sweeper` after `npm link` (or `npx`).

```bash
# To list files older than 90 days in the current directory:
node src/index.js scan . --age 90

# To list files older than 365 days in a specific directory:
node src/index.js scan /path/to/my/old/files --age 365

# To quarantine files older than 180 days from '/data/archive' to '/data/quarantine':
node src/index.js quarantine /data/archive --age 180 --output /data/quarantine

# Get help:
node src/index.js --help
```

### Commands

-   `scan <directory>`: Scans the specified directory and lists files older than `--age` days.
-   `quarantine <directory>`: Scans the specified directory and moves files older than `--age` days to the `--output` directory.

### Options

-   `-a, --age <days>`: **Required**. The minimum age in days for a file to be considered a "dust bunny".
-   `-o, --output <path>`: **Required for `quarantine` command**. The directory where identified files will be moved.
-   `-v, --verbose`: Display more detailed output during scanning.

## Development & Testing

To run the automated tests:

```bash
npm test
```

The tests use mocks for file system operations to ensure determinism and avoid actual file manipulation during testing.
