# Nightly Data Scavenger's Manifest

In the post-apocalyptic digital wasteland, every byte of data is precious. The `nightly-data-scavenger-manifest` utility helps you catalog your findings, identifying 'valuable data fragments' based on file type and assigning them a whimsical-yet-critical 'integrity score'.

## Purpose

This utility scans a specified directory (and its subdirectories) for files matching a list of desired extensions. For each matching file, it reports its path, size, and a simulated 'data integrity score' – a crucial metric for determining if your scavenged data is still coherent enough to be useful.

## Installation

1.  Navigate to the utility's directory:
    ```bash
    cd node-utils/nightly-data-scavenger-manifest
    ```
2.  Install dependencies (none, but `package.json` is present for Node.js project structure):
    ```bash
    npm install
    ```

## Usage

Run the utility from the command line, providing the target directory and a list of file extensions you're interested in. Extensions can be provided with or without a leading dot.

```bash
node src/index.js <directory_path> <extension1> [extension2 ...]
```

### Arguments:

*   `<directory_path>`: The path to the directory you want to scan.
*   `<extension1> [extension2 ...]`: One or more file extensions (e.g., `txt`, `json`, `md`, `.log`) to include in the manifest.

### Examples:

Scan the current directory for `.txt` and `.json` files:

```bash
node src/index.js . txt json
```

Scan a specific data archive for `.log` and `.md` files:

```bash
node src/index.js /var/data/archive log md
```

### Example Output:

```
--- Nightly Data Scavenger's Manifest ---
Path: /var/data/archive/logs/server.log
  Size: 12345 bytes
  Integrity Score: 85/100
-----------------------------------------
Path: /var/data/archive/docs/notes.md
  Size: 567 bytes
  Integrity Score: 92/100
-----------------------------------------
Total valuable fragments found: 2
```

## Development & Testing

To run the automated tests:

```bash
npm test
```

The tests use mocks for file system operations and the integrity score generation to ensure deterministic and offline execution.
