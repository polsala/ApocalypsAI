# Nightly Digital Dust Sweeper

A whimsical Node.js utility designed to help you declutter your digital spaces by identifying and managing "dusty" (old and forgotten) files. Sweep them into a designated "digital attic" or receive playful suggestions for their fate!

## Features

*   **Find Dusty Files**: Scans a specified directory for files older than a given age threshold.
*   **Recursive Scanning**: Optionally delves into subdirectories to uncover hidden digital dust bunnies.
*   **Digital Attic**: Move identified dusty files to a specified archive directory.
*   **Whimsical Suggestions**: For files not moved, receive fun, imaginative suggestions on what to do with them.
*   **Dry Run Mode**: Preview actions before committing to any file operations.

## Installation

1.  **Node.js**: Ensure you have Node.js (v14 or higher recommended) installed on your system.
2.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-digital-dust-sweeper
    ```
3.  No external `npm` dependencies are required for this utility.

## Usage

Run the utility using `node src/index.js` followed by options.

```bash
node src/index.js [options]
```

### Options

*   `-d, --dir <path>`: **Directory to scan** (default: current directory `.`).
*   `-a, --age <days>`: **Minimum age in days** for a file to be considered 'dusty' (default: `30`).
*   `-r, --recursive`: **Scan directories recursively**.
*   `-t, --attic <path>`: **Move dusty files to this 'digital attic' directory.** Implies `--execute`.
*   `-e, --execute`: **Execute file operations** (move to attic or suggest actions). By default, the utility runs in dry-run mode.
*   `-h, --help`: Display this help message.

### Examples

1.  **Find dusty files (older than 30 days) in the current directory (dry run):**
    ```bash
    node src/index.js
    ```

2.  **Find dusty files (older than 60 days) in a specific directory, recursively (dry run):**
    ```bash
    node src/index.js --dir /path/to/my/documents --age 60 --recursive
    ```

3.  **Move dusty files (older than 90 days) from a project folder to a 'digital_attic' folder:**
    ```bash
    node src/index.js -d /path/to/my/project -a 90 -t /path/to/my/digital_attic
    ```
    *(Note: `--attic` automatically enables execution mode)*

4.  **Get whimsical suggestions for dusty files (older than 14 days) in a specific folder, executing the suggestions (not moving):**
    ```bash
    node src/index.js --dir /path/to/downloads -a 14 --execute
    ```

## Development & Testing

To run the automated tests, navigate to the utility's directory and execute the test script:

```bash
cd node-utils/nightly-digital-dust-sweeper
node tests/index.test.js
```

The tests use a custom mock file system to ensure they are deterministic and do not interact with your actual file system.
