# Nightly Digital Dust Bunny Sweeper

## 🧹 Overview

The `nightly-digital-dust-bunny-sweeper` is a whimsical-yet-useful Bash script designed to help you keep your digital environment tidy. It scans specified directories for "digital dust bunnies" – old, unused files that accumulate over time – and offers to sweep them away, freeing up valuable disk space. Think of it as a friendly janitor for your filesystem!

## ✨ Features

*   **Customizable Scan Paths**: Define which directories the sweeper should examine.
*   **Adjustable Age Threshold**: Specify how old a file needs to be to qualify as a "dust bunny."
*   **Dry Run Mode**: Preview which files would be deleted without actually removing them.
*   **Interactive Confirmation**: Get a report on found dust bunnies and confirm before sweeping.
*   **Automated Sweeping**: Use the `--yes` flag for non-interactive cleanup, perfect for cron jobs.

## 🚀 Usage

### Prerequisites

*   Bash (usually pre-installed on Linux/macOS)
*   `find` utility
*   `du` utility
*   `rm` utility

### Running the Sweeper

1.  **Make the script executable:**
    ```bash
    chmod +x src/dust_bunny_sweeper.sh
    ```

2.  **Run with default settings:**
    By default, the script scans common clutter locations (`~/Downloads`, `~/.cache`, `/tmp`, `/var/log`) for files older than 30 days.
    ```bash
    ./src/dust_bunny_sweeper.sh
    ```

3.  **Specify custom paths and age:**
    You can add specific directories to scan using `-p` or `--path` (can be used multiple times) and set a custom age threshold with `-a` or `--age`.
    ```bash
    ./src/dust_bunny_sweeper.sh -p /var/tmp -p ~/Documents/old_projects -a 60
    ```
    *Note: If you specify custom paths, the default paths will NOT be scanned unless you explicitly add them.*

4.  **Perform a dry run:**
    See what would be swept without actually deleting anything.
    ```bash
    ./src/dust_bunny_sweeper.sh --dry-run
    ```

5.  **Automated sweeping (non-interactive):**
    Use the `--yes` flag to automatically confirm deletion. Be cautious with this option, especially when combined with custom paths.
    ```bash
    ./src/dust_bunny_sweeper.sh -y -p /path/to/my/logs -a 90
    ```

6.  **Get help:**
    ```bash
    ./src/dust_bunny_sweeper.sh --help
    ```

## ⚙️ Configuration

The script uses internal defaults for scan paths and age. You can override these via command-line arguments.

**Default Scan Paths:**
*   `$HOME/Downloads`
*   `$HOME/.cache`
*   `/tmp`
*   `/var/log`

**Default Age Threshold:**
*   `30` days

## 🧪 Testing

To run the automated tests for this utility:

1.  Navigate to the utility's root directory:
    ```bash
    cd nightly-digital-dust-bunny-sweep
    ```
2.  Execute the test script:
    ```bash
    ./tests/test_sweeper.sh
    ```

The tests use mock functions for `find`, `du`, `rm`, and `read` to ensure they are deterministic and do not interact with your actual filesystem. This allows for safe and repeatable testing of the script's logic.
