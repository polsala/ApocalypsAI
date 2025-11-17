# Nightly Data Debris Duster

## 🧹 Purpose

In the post-apocalyptic digital landscape, old, forgotten files accumulate like radioactive dust. The **Nightly Data Debris Duster** is your trusty tool to identify and manage these digital relics. It helps you clear out the "data debris" – files that haven't been touched in ages – keeping your storage lean and your systems nimble for whatever comes next.

## ✨ Features

*   **Age-based Scanning**: Find files older than a specified number of days.
*   **Recursive Search**: Scans directories and their subdirectories for hidden digital detritus.
*   **List Mode**: Safely preview files marked for dusting without making any changes.
*   **Quarantine Mode**: Move identified files to a designated "quarantine zone" for later review or permanent disposal.
*   **Whimsical Output**: Embrace the theme with themed messages.

## 🚀 Usage

### Prerequisites

*   Python 3.6+ (tested with 3.11)

### Running the Duster

```bash
python src/duster.py --path /path/to/scan --age 90 --mode list
```

**Arguments:**

*   `--path <directory>` (required): The root directory to start scanning for debris.
*   `--age <days>` (required): The minimum age in days for a file to be considered "debris" (e.g., `90` for files older than 90 days).
*   `--mode <list|quarantine>` (required):
    *   `list`: Only print the files that would be affected. No changes are made.
    *   `quarantine`: Move the identified files to a new `_quarantined_debris_` subdirectory within their original parent directory.
*   `--quarantine-dir-name <name>` (optional, default: `_quarantined_debris_`): Custom name for the quarantine subdirectory.

### Examples

1.  **List files older than 180 days in your `documents` folder:**
    ```bash
    python src/duster.py --path ~/documents --age 180 --mode list
    ```

2.  **Quarantine files older than 30 days in your `downloads` folder:**
    ```bash
    python src/duster.py --path ~/downloads --age 30 --mode quarantine
    ```

3.  **Quarantine files older than 60 days in your `archive` folder, using a custom quarantine name:**
    ```bash
    python src/duster.py --path /mnt/archive --age 60 --mode quarantine --quarantine-dir-name "digital_vault_overflow"
    ```

## 🧪 Testing

To run the tests, navigate to the `utils/nightly-data-debris-duster/` directory and execute:

```bash
python -m unittest tests/test_duster.py
```
