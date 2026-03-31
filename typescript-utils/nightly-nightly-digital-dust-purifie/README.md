# Nightly Digital Dust Purifier

## Summary
`nightly-digital-dust-purifier` is a whimsical-yet-useful TypeScript CLI tool designed to help you identify and manage "digital dust bunnies" – old, unused, or excessively large files cluttering your digital space. It scans a specified directory, flags files based on configurable criteria (age, size), and suggests actions like archiving them to a dedicated "dust bunnies archive" directory.

## Features
- **Configurable Scan**: Define what constitutes a "dust bunny" by setting minimum age (days) and minimum size (bytes).
- **Exclusion Patterns**: Ignore specific directories or files (e.g., `node_modules`, `.git`).
- **Dry Run Mode**: Preview the files that would be affected without making any changes.
- **Archiving**: Move identified dust bunnies to a specified archive directory.
- **Type-Safe**: Built with TypeScript for robust and maintainable code.

## Installation
1.  Navigate to the `nightly-digital-dust-purifier` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Build the TypeScript project:
    ```bash
    npm run build
    ```

## Usage
Run the utility from your terminal. The basic command is:

```bash
node dist/index.js [target_path] [options]
```

### Arguments
-   `target_path`: The directory to scan for digital dust bunnies. Defaults to the current directory (`.`).

### Options
-   `--age <days>`: Flag files older than this many days. (e.g., `--age 90` for files older than 90 days).
-   `--size <bytes>`: Flag files larger than this many bytes. (e.g., `--size 10485760` for files larger than 10MB).
-   `--exclude <pattern1,pattern2,...>`: Comma-separated list of patterns (substrings or simple regex) to exclude files or directories. Overrides default exclusions.
-   `--dry-run`: (Default) Perform a scan and report findings without moving or deleting any files.
-   `--archive-dir <path>`: Specify a directory where identified dust bunnies will be moved. **Only effective when `--dry-run` is NOT used.**

### Examples

1.  **Scan current directory for files older than 90 days (dry run):**
    ```bash
    node dist/index.js . --age 90 --dry-run
    ```

2.  **Scan a specific directory for files larger than 5MB and older than 180 days (dry run):**
    ```bash
    node dist/index.js /path/to/my/data --size 5242880 --age 180 --dry-run
    ```

3.  **Archive files older than 365 days to a 'digital_archive' folder (use with caution!):**
    ```bash
    node dist/index.js . --age 365 --archive-dir ./digital_archive
    ```
    *Note: `--dry-run` is omitted here, so actual file movements will occur.*

4.  **Scan, excluding 'temp' directories and '.log' files:**
    ```bash
    node dist/index.js . --age 60 --exclude temp,.log --dry-run
    ```

## Configuration File (Optional)
You can create a `dust-purifier.config.json` file in your project root to define default settings:

```json
{
  "minAgeDays": 120,
  "minSizeBytes": 20971520, // 20 MB
  "excludePatterns": [".cache", "logs", "*.bak"],
  "dryRun": true,
  "archiveDir": "./purified_dust"
}
```

CLI arguments will override settings from the configuration file.

## Development & Testing
To run the automated tests:
```bash
npm test
```

## License
MIT
