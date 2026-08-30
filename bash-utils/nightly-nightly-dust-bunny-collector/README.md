# Nightly Digital Dust Bunny Collector

The digital realm, much like our physical spaces, accumulates clutter. Over time, old, forgotten files — our "digital dust bunnies" — can hog valuable disk space. The `nightly-dust-bunny-collector` is a whimsical yet powerful utility designed to help you identify and manage these digital remnants, reclaiming precious storage.

It scans specified directories for files older than a certain age and larger than a minimum size, then offers options to report, archive, or delete them.

## Features

*   **Targeted Scanning**: Specify directories to scan.
*   **Age-based Filtering**: Only consider files older than a configurable number of days.
*   **Size-based Filtering**: Focus on larger files to maximize space reclamation.
*   **Flexible Actions**:
    *   **Report**: Simply list the identified dust bunnies.
    *   **Archive**: Compress and move dust bunnies to a specified archive location, then delete the originals.
    *   **Delete**: Permanently remove the dust bunnies.
*   **Whimsical Output**: Enjoy a touch of fun while cleaning your system.

## Usage

```bash
./src/dust_bunny_collector.sh <directory> <age_in_days> <min_size_mb> <action> [archive_dir]
```

### Arguments:

*   `<directory>`: The path to the directory to scan (e.g., `/var/log`, `/tmp`, `~/Downloads`).
*   `<age_in_days>`: Files older than this many days will be considered (e.g., `30` for files older than 30 days).
*   `<min_size_mb>`: Minimum file size in megabytes. Files smaller than this will be ignored (e.g., `100` for files larger than 100MB).
*   `<action>`: The action to perform. Choose one of:
    *   `report`: List the identified files.
    *   `archive`: Archive the files into a `.tar.gz` file and then delete the originals. Requires `[archive_dir]`.
    *   `delete`: Permanently delete the identified files.
*   `[archive_dir]` (Optional, required for `archive` action): The directory where archived dust bunnies will be stored.

## Examples

1.  **Report digital dust bunnies older than 60 days and larger than 50MB in `/var/log`:**
    ```bash
    ./src/dust_bunny_collector.sh /var/log 60 50 report
    ```

2.  **Archive dust bunnies older than 90 days and larger than 200MB from `/tmp` to `~/archives/dust_bunnies`:**
    ```bash
    ./src/dust_bunny_collector.sh /tmp 90 200 archive ~/archives/dust_bunnies
    ```

3.  **Delete dust bunnies older than 7 days and larger than 10MB from `~/Downloads`:**
    ```bash
    ./src/dust_bunny_collector.sh ~/Downloads 7 10 delete
    ```

## Installation

Simply place the `src/dust_bunny_collector.sh` script in your desired location and make it executable:

```bash
chmod +x src/dust_bunny_collector.sh
```

## Contributing

Feel free to sweep in with improvements or new features!
