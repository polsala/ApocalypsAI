# Nightly Digital Echo Sweeper

## Overview

The `nightly-digital-echo-sweeper` is a whimsical-yet-useful utility designed to help you manage your digital clutter. It scans specified directories for "digital echoes" – files that haven't been modified in a long time – and offers to move them to a designated "temporal stasis" archive folder. Keep your active directories pristine and let the echoes rest in peace.

## Features

*   **Scan for Digital Echoes**: Recursively searches a source directory for files older than a specified age.
*   **Suggest Rehoming**: Lists detected digital echoes and their last modification dates.
*   **Temporal Stasis**: Optionally moves identified echoes to a target archive directory.
*   **Cross-Platform**: Built with Node.js, runs on Windows, macOS, and Linux.

## Installation

1.  **Prerequisites**: Ensure you have Node.js (v14 or higher) and npm installed.
2.  **Clone the repository (or download the utility folder)**:

    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-digital-echo-sweeper
    ```

3.  **Install dependencies**:

    ```bash
    npm install
    ```

## Usage

Run the utility from its directory using `npm start` or directly with `node src/index.js`.

```bash
node src/index.js [options]
```

### Options

*   `-s, --source <path>`: Source directory to scan for digital echoes. Defaults to the current working directory (`.`).
*   `-a, --age <days>`: Minimum age in days for a file to be considered an echo. Defaults to `30` days.
*   `-t, --target <path>`: Target directory for temporal stasis (archiving). Defaults to `./temporal_stasis_archive`.
*   `-m, --move`: **Execute the rehoming (move files)** instead of just listing suggestions. **Use with caution!**
*   `-h, --help`: Display help for command.

### Examples

1.  **Scan current directory for echoes older than 60 days (suggestion mode)**:

    ```bash
    node src/index.js --age 60
    ```

2.  **Scan a specific 'downloads' folder and suggest moving echoes older than 90 days to a custom archive**:

    ```bash
    node src/index.js --source /path/to/your/downloads --age 90 --target /path/to/my/archive/void
    ```

3.  **Execute the rehoming for echoes older than 7 days in a 'temp' folder**:

    ```bash
    node src/index.js --source /var/tmp --age 7 --move
    ```

## Development & Testing

To run the automated tests:

```bash
npm test
```

This will execute the Jest test suite, which uses mocks to simulate file system operations, ensuring deterministic and offline testing.
