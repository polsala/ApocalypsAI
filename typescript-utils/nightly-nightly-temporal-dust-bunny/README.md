# Nightly Temporal Dust Bunny Collector

## Summary
A whimsical-yet-useful TypeScript CLI utility designed to help you tidy up your digital timelines by finding and reporting old or temporary files – affectionately known as 'temporal dust bunnies' – in specified directories.

## Features
*   **Recursive Scanning**: Dive deep into directory structures to uncover hidden digital detritus.
*   **Age-Based Filtering**: Identify files older than a specified number of days.
*   **Pattern Matching**: Pinpoint files by name using regular expressions (e.g., `.bak`, `temp_`, `~`).
*   **Dry Run (Default)**: Safely preview which files would be affected without making any changes.
*   **Type-Safe**: Built with TypeScript for robust and maintainable code.

## Installation
To use the Temporal Dust Bunny Collector, you'll need Node.js (v18 or higher) and npm installed.

1.  Navigate to the `nightly-temporal-dust-bunny-collector` directory.
2.  Install dependencies and build the project:
    ```bash
    npm install
    npm run build
    ```
3.  (Optional) Link the utility globally for easy access:
    ```bash
    npm link
    ```
    Now you can run `temporal-dust-bunny-collector` from any directory.

## Usage
```bash
temporal-dust-bunny-collector <path> [options]
```

### Arguments
*   `<path>`: The root directory to start scanning for temporal dust bunnies.

### Options
*   `-a, --age-days <days>`: Files older than this many days are considered dust bunnies. Defaults to `30` days.
*   `-p, --patterns <patterns...>`: One or more file name patterns (regular expressions) to consider as dust bunnies. For example, `".*\\.bak"` or `"temp_.*"`. Defaults to no specific patterns.
*   `-r, --recursive`: Scan directories recursively. By default, only the top-level directory is scanned.
*   `-d, --dry-run`: Perform a dry run without making any changes. This is `true` by default for safety. To disable, use `--no-dry-run` (though actual cleanup functionality is not yet implemented).

### Examples

1.  **Find all files older than 60 days in the current directory (non-recursive, dry run):**
    ```bash
    temporal-dust-bunny-collector . --age-days 60
    ```

2.  **Recursively find all `.bak` or `~` files in your home directory:**
    ```bash
    temporal-dust-bunny-collector ~/ --recursive --patterns ".*\\.bak" ".*~$"
    ```

3.  **Find files older than 7 days OR matching `temp_` pattern in `/var/log` (recursive):**
    ```bash
    temporal-dust-bunny-collector /var/log --age-days 7 --patterns "temp_.*" --recursive
    ```

## Development

### Running Tests
```bash
npm test
```

### Building
```bash
npm run build
```

## Contributing
This utility is currently a reporting tool. Future enhancements could include actual cleanup (move to archive, delete) with proper safety mechanisms. Feel free to contribute to evolve this temporal tidiness agent!
