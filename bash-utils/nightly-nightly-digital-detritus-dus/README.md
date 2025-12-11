# Nightly Digital Detritus Duster

## Overview

The `nightly-digital-detritus-duster` is a whimsical Bash utility designed to help you maintain a pristine digital environment in the face of the apocalypse (or just general system clutter). It scans specified directories for 'ancient scrolls' (old files) and 'echoing vaults' (empty directories), providing a report and optionally performing cleanup actions like quarantining or outright deletion.

Keep your systems lean and mean, ready for whatever digital or physical threats lurk in the wasteland!

## Features

*   **Identify Old Files**: Finds files older than a specified number of days.
*   **Identify Empty Directories**: Locates directories that contain no files or subdirectories.
*   **Categorized Reporting**: Presents findings with a whimsical flair.
*   **Optional Cleanup**: Move identified detritus to a quarantine zone or permanently delete it.

## Usage

```bash
./src/detritus_duster.sh [OPTIONS] [PATH...]
```

### Options:

*   `-a <days>` or `--age <days>`: Specify the age threshold in days for 'ancient scrolls'. Files older than this will be flagged. Default is `3` days.
*   `-q` or `--quarantine`: Move identified detritus to a `.digital_detritus_quarantine` subdirectory within its parent directory. This is a safe way to remove items without permanent deletion.
*   `-d` or `--delete`: Permanently delete identified detritus. **Use with extreme caution!**
*   `-h` or `--help`: Display this help message.

### Arguments:

*   `[PATH...]`: One or more directories to scan. If no paths are provided, the current directory (`.`) will be scanned.

### Examples:

1.  **Scan current directory for detritus older than 5 days (report only):**
    ```bash
    ./src/detritus_duster.sh -a 5 .
    ```

2.  **Scan `/var/log` and `/tmp` for detritus and quarantine it:**
    ```bash
    ./src/detritus_duster.sh -q /var/log /tmp
    ```

3.  **Scan `/home/user/downloads` for detritus older than 30 days and delete it (DANGER!):**
    ```bash
    ./src/detritus_duster.sh -a 30 -d /home/user/downloads
    ```

## Installation

This is a standalone Bash script. Simply clone the repository and ensure the script is executable:

```bash
chmod +x src/detritus_duster.sh
```

## Testing

To run the automated tests, navigate to the utility's root directory and execute the test script:

```bash
./tests/test_detritus_duster.sh
```

## Contributing

Feel free to contribute to the ongoing effort of digital hygiene in the post-apocalyptic world! Submit issues or pull requests to the main repository.
