# Nightly Digital Detritus Duster

## 🧹 Whimsical Utility: Digital Detritus Duster 🧹

In the post-apocalyptic digital landscape, every byte counts. The `nightly-digital-duster` is your trusty companion for keeping your digital spaces clean and efficient. It metaphorically sweeps away the "digital dust bunnies" – old, forgotten files and empty directories that accumulate over time, consuming precious storage and mental bandwidth.

This whimsical Bash script helps you identify and optionally remove these digital remnants, ensuring your systems remain nimble and your data organized, even when the world outside is anything but.

## ✨ Features

*   **Scans for Old Files:** Identifies files modified beyond a specified age.
*   **Finds Empty Directories:** Locates directories that have been left empty and untouched for too long.
*   **Dry Run Mode:** Preview what would be removed without making any actual changes.
*   **Interactive Confirmation:** Asks for your explicit permission before sweeping away any detritus.
*   **Whimsical Output:** Enjoy a touch of humor while tidying up your digital realm.

## 🚀 Usage

1.  **Make the script executable:**
    ```bash
    chmod +x src/digital_duster.sh
    ```

2.  **Run the duster:**
    ```bash
    ./src/digital_duster.sh [OPTIONS] [DIRECTORY]
    ```

### Options:

*   `-a, --age DAYS`: Specify the age in days. Files and empty directories older than this will be considered "dust bunnies." (Default: `30` days)
*   `-d, --dry-run`: Perform a simulated sweep. The script will list what *would* be removed but won't delete anything.
*   `-h, --help`: Display the help message.

### Arguments:

*   `DIRECTORY`: The path to the directory you want to scan. If not specified, the current directory (`.`) will be used.

### Examples:

*   **Scan the current directory for items older than 30 days (default) and ask for confirmation:**
    ```bash
    ./src/digital_duster.sh
    ```

*   **Scan `/var/log` for files older than 60 days, but only show what would be removed (dry run):**
    ```bash
    ./src/digital_duster.sh -a 60 --dry-run /var/log
    ```

*   **Clean up your `~/Downloads` folder, removing items older than 7 days:**
    ```bash
    ./src/digital_duster.sh --age 7 ~/Downloads
    ```

*   **Display help:**
    ```bash
    ./src/digital_duster.sh -h
    ```

## 🧪 Testing

To run the automated tests for the `nightly-digital-duster`:

1.  **Make the test script executable:**
    ```bash
    chmod +x tests/test_duster.sh
    ```
2.  **Execute the test suite:**
    ```bash
    ./tests/test_duster.sh
    ```

The tests will create temporary directories and files, run the duster script against them, and verify its behavior (e.g., correct identification of old files, proper deletion in interactive mode, no deletion in dry-run mode, error handling). All tests are self-contained and clean up after themselves.
