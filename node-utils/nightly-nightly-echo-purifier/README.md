# Nightly Digital Echo Purifier

Scans directories for forgotten files (digital echoes) and moves them to a designated archive.

## Overview

In the post-apocalyptic digital landscape, data accumulates like dust in abandoned servers. The Nightly Digital Echo Purifier is a whimsical yet practical utility designed to help you declutter your digital workspace. It identifies files that haven't been touched in a while – your "digital echoes" – and offers to gracefully move them to a designated archive, preventing them from haunting your active directories.

## Features

*   **Echo Detection**: Scans a specified directory (and its subdirectories) for files older than a configurable age threshold.
*   **Whimsical Archiving**: Moves detected "digital echoes" to a structured archive directory, preserving their relative paths.
*   **Cross-Platform**: Built with Node.js, runs on Windows, macOS, and Linux.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-echo-purifier
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```
3.  **Make the CLI executable (optional, for direct execution)**:
    ```bash
    chmod +x src/cli.js
    ```
    Or, for global access:
    ```bash
    npm link # This will symlink the utility to your global node_modules/bin
    ```

## Usage

### Listing Digital Echoes

To simply list files older than 90 days in the current directory:

```bash
# If installed globally:
nightly-echo-purifier

# If running directly:
node src/cli.js
```

To list files older than 180 days in a specific directory:

```bash
nightly-echo-purifier --dir /path/to/your/project --age 180
```

### Archiving Digital Echoes

To move detected echoes to a default archive directory (`_digital_echoes_archive` within the scanned directory):

```bash
nightly-echo-purifier --archive
```

To move echoes to a custom archive path:

```bash
nightly-echo-purifier --dir /path/to/scan --age 365 --archive /path/to/your/void_of_forgotten_bytes
```

### Options

*   `-d, --dir <path>`: Directory to scan (default: current working directory).
*   `-a, --age <days>`: Files older than this many days are considered echoes (default: 90).
*   `-r, --archive [path]`: Move echoes to an archive directory. If `path` is not provided, defaults to `_digital_echoes_archive` within the target directory.
*   `-h, --help`: Show the help message.

## Development

### Running Tests

```bash
npm test
```

## License

This project is licensed under the MIT License.
