# nightly-digital-dust-bunny-sweeper

A whimsical-yet-useful utility to help you declutter your digital wasteland! The `nightly-digital-dust-bunny-sweeper` scans a specified directory for stale, unused files and empty directories, reporting them so you can decide what to sweep away. Keep your digital environment sparkling clean and free up valuable space.

## Features

*   **Stale File Detection**: Identifies files that haven't been modified for a configurable period (default: 1 year).
*   **Empty Directory Discovery**: Pinpoints directories that contain no files or subdirectories.
*   **Recursive Scanning**: Traverses subdirectories to find hidden dust bunnies.
*   **Cross-Platform**: Built with Node.js, it runs on Windows, macOS, and Linux.

## Usage

### Prerequisites

Ensure you have Node.js (v16.x or higher recommended) installed on your system.

### Running the Sweeper

1.  Navigate to the utility's directory:
    ```bash
    cd nightly-digital-dust-bunny-sweeper
    ```
2.  Run the script, optionally providing a target path and an age threshold in days.

    **Scan current directory with default 1-year threshold:**
    ```bash
    node src/index.js
    ```

    **Scan a specific directory (e.g., `/path/to/my/documents`) with default 1-year threshold:**
    ```bash
    node src/index.js /path/to/my/documents
    ```

    **Scan a specific directory with a custom age threshold (e.g., 180 days):**
    ```bash
    node src/index.js /path/to/my/old_projects 180
    ```

### Example Output

```
🔍 Sweeping for digital dust bunnies in: /home/user/my_projects
⏳ Considering files untouched for over 365 days.

--- Digital Dust Bunnies Report ---

👻 Stale Files (2):
  - /home/user/my_projects/old_report.pdf (Last modified: 2022-01-15T10:30:00.000Z)
  - /home/user/my_projects/legacy_code/temp_script.js (Last modified: 2021-11-20T14:00:00.000Z)

🗑️ Empty Directories (1):
  - /home/user/my_projects/empty_folder

🧹 Time to grab your digital broom and sweep these away!
```

## Development

### Running Tests

To ensure the sweeper is working correctly, you can run the provided tests:

```bash
node --test tests/index.test.js
```

The tests use Node.js's built-in `node:test` module and mock the file system operations to ensure deterministic and offline execution.
