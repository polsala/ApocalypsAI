# Nightly Digital Debris Scavenger

The digital wasteland is vast, and forgotten files accumulate like radioactive dust. The `nightly-digital-debris-scavenger` is your trusty companion for sifting through the detritus of your file systems, identifying and quarantining the digital junk that no longer serves a purpose. Keep your directories lean and mean, ready for the next survival challenge!

## Features

*   **Debris Detection**: Scans specified directories for files older than a configurable age.
*   **Whimsical Reporting**: Clearly lists all detected "digital debris."
*   **Quarantine Protocol**: Optionally moves identified debris to a temporary, isolated "quarantine zone" for later review or permanent disposal.
*   **Simple & Efficient**: A lightweight Bash script, perfect for integrating into your nightly maintenance routines.

## Usage

### Prerequisites

*   Bash shell
*   `find` utility
*   `mktemp` utility
*   `mv` utility
*   `date` utility (for `touch -t` in tests, standard on most Linux/macOS)

### Running the Scavenger

Navigate to the utility's directory and run the `scavenge.sh` script.

```bash
./src/scavenge.sh -d /path/to/your/wasteland [-a <age_in_days>] [-q]
```

#### Arguments:

*   `-d <directory>` (Required): The root directory where the scavenger will begin its search for digital debris.
*   `-a <age_in_days>` (Optional): Specifies the age threshold in days. Any file last modified *more than* this many days ago will be considered debris. Defaults to `30` days if not specified.
*   `-q` (Optional): Activates "quarantine mode." Instead of just listing the debris, the scavenger will move the detected files into a newly created, temporary quarantine directory within the target directory (e.g., `/path/to/your/wasteland/.scavenger_quarantine_XXXXXX`).

#### Examples:

1.  **Just list debris older than 60 days in your home directory:**
    ```bash
    ./src/scavenge.sh -d ~/my_project_files -a 60
    ```

2.  **Quarantine all files older than the default 30 days in a specific data directory:**
    ```bash
    ./src/scavenge.sh -d /var/log/old_archives -q
    ```

3.  **List all files older than 7 days in a temporary directory:**
    ```bash
    ./src/scavenge.sh -d /tmp/downloads -a 7
    ```

## Testing

To ensure the scavenger is functioning correctly and ready for deployment in your post-apocalyptic infrastructure, run the provided test suite:

```bash
./tests/test_scavenge.sh
```

The tests will create temporary directories and files, simulate various scenarios (no debris, debris found, debris quarantined, invalid inputs), and verify the script's behavior. All test files are cleaned up automatically.

## Contribution

Got an idea for a new scavenging tool or a better way to handle digital detritus? Contributions are welcome! Just remember to keep it whimsical and useful.
