# Nightly Digital Dust Bunny Sweeper

A whimsical-yet-useful Node.js CLI tool that helps you identify and optionally remove common temporary files, build artifacts, and cache directories from your projects. Think of them as "digital dust bunnies" cluttering your disk space – this tool helps you sweep them away!

## Features

-   **Scans for common clutter**: Identifies `node_modules`, `dist`, `build`, `.cache`, `.log` files, `.DS_Store`, and many more by default.
-   **Customizable patterns**: Define your own "dust bunny" patterns to search for.
-   **Interactive confirmation**: Review what will be deleted before it's swept away (unless forced).
-   **Cross-platform**: Works wherever Node.js runs.

## Installation

1.  **Ensure Node.js is installed**: You need Node.js (v14 or higher recommended) to run this utility.
    You can download it from [nodejs.org](https://nodejs.org/).

2.  **Install globally (recommended for CLI tools):**

    ```bash
    npm install -g nightly-dust-bunny-sweeper
    ```

    Or, if you prefer to run it directly from the repository:

    ```bash
    # Clone the repository (if not already part of ApocalypsAI)
    # git clone https://github.com/polsala/ApocalypsAI.git
    # cd ApocalypsAI/node-utils/nightly-dust-bunny-sweeper

    npm install
    npm link # To make it available as a global command
    ```

## Usage

Run the `nightly-dust-bunny-sweeper` command from your terminal.

```bash
nightly-dust-bunny-sweeper [directory] [options]
```

### Arguments

-   `[directory]` (optional): The path to the directory you want to scan. If not provided, it defaults to the current working directory (`.`).

### Options

-   `-f, --force`: Skip the interactive confirmation and immediately delete all found dust bunnies. Use with caution!
-   `-p, --patterns <patterns...>`: Provide a comma-separated list of custom patterns to search for. This will *override* the default patterns.
    -   Example: `-p "temp,logs,*.bak"`
    -   Simple glob patterns like `*.log` are supported for files. Directory names are matched exactly.

### Examples

1.  **Scan current directory and confirm deletion:**

    ```bash
    nightly-dust-bunny-sweeper
    ```

2.  **Scan a specific project directory and force delete:**

    ```bash
    nightly-dust-bunny-sweeper ~/my-old-project --force
    ```

3.  **Scan with custom patterns:**

    ```bash
    nightly-dust-bunny-sweeper . -p "cache,old-builds,*.tmp"
    ```

4.  **Scan a parent directory:**

    ```bash
    nightly-dust-bunny-sweeper ..
    ```

## Default Dust Bunny Patterns

By default, the sweeper looks for directories and files matching these patterns:

-   `node_modules`
-   `dist`
-   `build`
-   `target`
-   `.cache`
-   `.tmp`
-   `tmp`
-   `.DS_Store`
-   `Thumbs.db`
-   `*.log`
-   `*.bak`
-   `*.swp`
-   `coverage`
-   `.nyc_output`

## Development & Testing

To run tests:

```bash
npm test
```

The tests use `jest` and mock the file system operations to ensure determinism and avoid actual file deletions during testing.
