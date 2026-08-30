# Nightly Starlight Synchronizer

Align your digital artifacts with the celestial rhythm! The `nightly-starlight-sync` utility helps you harmonize file modification times, either by setting them to a precise cosmic epoch or by scattering them across a temporal nebula for a touch of digital stardust.

## ✨ Features

*   **Precise Alignment**: Set all files and directories within a specified path to a single, exact modification timestamp.
*   **Temporal Nebula**: Randomize modification timestamps within a defined range (e.g., last 24 hours, last 7 days) for a whimsical, yet organized, digital scattering.
*   **Recursive Operation**: Processes all files and subdirectories within the target path.
*   **Cross-Platform**: Built with Node.js, works wherever Node.js runs.

## 🚀 Usage

```bash
node src/index.js <path> [--date <YYYY-MM-DDTHH:MM:SSZ>] [--random-range <duration>] [--dry-run]
```

### Arguments:

*   `<path>`: The target directory whose files and subdirectories will have their modification times synchronized. **Required.**

### Options:

*   `--date <YYYY-MM-DDTHH:MM:SSZ>`: Sets all modification times to this specific date and time. Must be a valid ISO 8601 string (e.g., `2023-10-27T10:00:00Z`). If omitted, the current time will be used as the base.
*   `--random-range <duration>`: Randomizes modification times within the specified duration *before* the base time (either `--date` or current time).
    *   Examples: `24h` (24 hours), `7d` (7 days), `30m` (30 minutes).
    *   If `--date` is provided, `--random-range` will randomize *before* that date. If `--date` is omitted, it randomizes *before* the current time.
*   `--dry-run`: Simulate the synchronization without actually modifying any files. Prints what *would* be done.

### Examples:

1.  **Align with current cosmic epoch:**
    ```bash
    node src/index.js ./my-project
    ```
    (Sets all files in `./my-project` to the current timestamp)

2.  **Align with a specific historical event:**
    ```bash
    node src/index.js ./old-logs --date 2022-01-15T12:30:00Z
    ```
    (Sets all files in `./old-logs` to January 15, 2022, 12:30:00 UTC)

3.  **Scatter across a temporal nebula (last 48 hours):**
    ```bash
    node src/index.js ./stardust-archive --random-range 48h
    ```
    (Randomizes timestamps for files in `./stardust-archive` within the last 48 hours from now)

4.  **Dry run to see the cosmic plan:**
    ```bash
    node src/index.js ./my-project --date 2023-01-01T00:00:00Z --dry-run
    ```
    (Shows which files in `./my-project` would be set to Jan 1, 2023, without actually changing them)

## 🛠️ Development

1.  Clone the repository.
2.  Navigate to `node-utils/nightly-starlight-sync`.
3.  Run tests: `node tests/index.test.js` (requires `sinon` for mocking, install with `npm install sinon` if not globally available)
