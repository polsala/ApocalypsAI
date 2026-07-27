# Nightly Cosmic Dustifier

🌌 ApocalypsAI Nightly Cosmic Dustifier 🌌

This whimsical-yet-useful command-line interface (CLI) tool helps you manage digital clutter by identifying and optionally 'dustifying' (archiving or deleting) files that have exceeded their cosmic decay threshold.

Think of it as a celestial janitor for your file system, ensuring that only the most vibrant and recently touched data remains, while older, less-used files gracefully transition into cosmic dust.

## Features

*   **Scan**: Identify files in a specified directory that are older than a configurable number of days.
*   **List**: Display identified 'cosmic dust' files without making any changes (default action).
*   **Archive**: Move old files to a designated 'void archive' directory.
*   **Delete**: Permanently remove old files from existence.
*   **Dry Run**: Simulate any action to see what would happen before committing to changes.
*   **Type-Safe**: Built with TypeScript for robust and predictable operation.

## Installation

To use the Cosmic Dustifier, you need Node.js (v14 or higher) and npm/yarn installed.

1.  **Clone the repository (if not already part of ApocalypsAI):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-cosmic-dustifier
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    # or yarn install
    ```
3.  **Build the project:**
    ```bash
    npm run build
    # or yarn build
    ```
4.  **Run directly or link globally:**
    To run directly:
    ```bash
    node dist/index.js <path> [options]
    ```
    To link globally (recommended for CLI tools):
    ```bash
    npm link
    # or yarn link
    ```
    Now you can run `cosmic-dustifier` from anywhere.

## Usage

```bash
cosmic-dustifier <path> [options]
```

### Arguments

*   `<path>`: The cosmic directory to scan for ancient files.

### Options

*   `-t, --threshold <days>`: Files older than this many days will be considered cosmic dust. (Default: `30`)
*   `-a, --action <type>`: Action to perform: `list` (default), `archive`, or `delete`. (Default: `list`)
*   `-d, --archive-dir <directory>`: Directory to move archived files to. Required for the `archive` action.
*   `-n, --dry-run`: Simulate the dustification process without making any actual changes.
*   `-h, --help`: Display help for command.
*   `-V, --version`: Output the version number.

## Examples

1.  **List files older than 60 days in the current directory (dry run):**
    ```bash
    cosmic-dustifier . --threshold 60 --dry-run
    ```

2.  **Archive files older than 90 days from `/var/log` to `/tmp/cosmic-archive`:**
    ```bash
    cosmic-dustifier /var/log --threshold 90 --action archive --archive-dir /tmp/cosmic-archive
    ```

3.  **Delete files older than 7 days from `~/Downloads` (after a dry run):**
    ```bash
    # First, a dry run to be safe
    cosmic-dustifier ~/Downloads --threshold 7 --action delete --dry-run
    # If satisfied, run for real
    cosmic-dustifier ~/Downloads --threshold 7 --action delete
    ```

4.  **List files older than the default 30 days in a specific project folder:**
    ```bash
    cosmic-dustifier ~/projects/old-project
    ```

## Development

To run tests:

```bash
npm test
# or yarn test
```

## Contributing

Feel free to contribute to the cosmic order! Open issues or pull requests on the main ApocalypsAI repository.
