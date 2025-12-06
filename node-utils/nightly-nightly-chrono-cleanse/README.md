# Nightly Chrono-Cleanse

A Node.js CLI utility designed to help you manage digital temporal residue by identifying and optionally archiving or deleting files older than a specified duration. Keep your digital wasteland tidy!

## Features

*   **Temporal Scan**: Scans a specified directory for files older than a given age.
*   **Flexible Actions**: Choose to merely list the "temporal echoes," archive them to a designated "temporal archive" directory, or permanently "cleanse" them from existence.
*   **Whimsical Output**: Provides clear, slightly dramatic output about the cleansing process.

## Installation

1.  Navigate to the `node-utils/nightly-chrono-cleanse` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  (Optional) Link the CLI tool globally:
    ```bash
    npm link
    ```
    Or run directly using `node src/main.js`.

## Usage

```bash
chrono-cleanse <command> [options]
```

### Commands

*   `list <directory>`: Lists files older than the specified age.
*   `archive <directory>`: Moves files older than the specified age to an archive directory.
*   `delete <directory>`: Deletes files older than the specified age.

### Options

*   `-a, --age <duration>`: **Required**. The age threshold for files. Format: `Nd` for N days, `Nh` for N hours, `Nm` for N minutes, `Ns` for N seconds. (e.g., `7d`, `24h`, `30m`, `60s`).
*   `-o, --output <path>`: **Required for `archive` command**. The path to the temporal archive directory.
*   `-v, --verbose`: Show more detailed output.

### Examples

1.  **List files in `/tmp/logs` older than 30 days:**
    ```bash
    chrono-cleanse list /tmp/logs --age 30d
    ```

2.  **Archive files in `/var/cache` older than 7 days to `/tmp/archive`:**
    ```bash
    chrono-cleanse archive /var/cache --age 7d --output /tmp/archive
    ```

3.  **Delete files in `~/downloads` older than 1 hour:**
    ```bash
    chrono-cleanse delete ~/downloads --age 1h
    ```

## Development

To run tests:

```bash
npm test
```
