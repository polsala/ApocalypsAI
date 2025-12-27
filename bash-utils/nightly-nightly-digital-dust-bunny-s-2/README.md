# Nightly Digital Dust Bunny Sweeper

The digital realm, much like our physical spaces, accumulates its fair share of forgotten detritus. Files left behind, growing silently, consuming precious storage, and slowing down the cosmic flow of information. Fear not, for the **Nightly Digital Dust Bunny Sweeper** is here to bring order to the digital chaos!

This whimsical-yet-useful Bash utility helps you identify and optionally archive those pesky "digital dust bunnies" – old or excessively large files that have overstayed their welcome in your specified directories.

## Features

*   **Targeted Sweeping**: Scan any directory for digital clutter.
*   **Age-Based Detection**: Find files older than a specified number of days.
*   **Size-Based Detection**: Pinpoint files larger than a given megabyte threshold.
*   **Void Archiving**: Safely move identified dust bunnies to a designated "Void Archive" directory, rather than outright deletion.
*   **Interactive or Forceful**: Confirm each sweep or let the sweeper do its work without interruption.
*   **Whimsical Output**: Enjoy a touch of cosmic charm as you cleanse your digital space.

## Installation

This is a standalone Bash script. No special installation is required beyond having Bash available on your system (which is standard on most Linux/macOS environments).

1.  Clone the `polsala/ApocalypsAI` repository (if you haven't already):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```
2.  Navigate to the utility's directory:
    ```bash
    cd bash-utils/nightly-digital-dust-bunny-sweeper
    ```
3.  Make the script executable:
    ```bash
    chmod +x src/dust_bunny_sweeper.sh
    ```

## Usage

Run the `dust_bunny_sweeper.sh` script with the required target directory and at least one criterion (age or size).

```bash
./src/dust_bunny_sweeper.sh -d <directory> [-a <days> | -s <size_mb>] [-o <archive_dir>] [-f] [-h]
```

### Options

*   `-d <directory>`: **(Required)** The target directory to scan for digital dust bunnies.
*   `-a <days>`: Find files older than `N` days.
*   `-s <size_mb>`: Find files larger than `N` megabytes.
*   `-o <archive_dir>`: **(Optional)** Directory to move found files to. If not specified, files are only listed. The script will attempt to create this directory if it doesn't exist.
*   `-f`: **(Optional)** Force sweep. Do not ask for confirmation before archiving.
*   `-h`: Display the help message and exit.

### Examples

1.  **List all files in `/var/log` older than 30 days:**
    ```bash
    ./src/dust_bunny_sweeper.sh -d /var/log -a 30
    ```

2.  **Move files in `~/Downloads` larger than 100MB to `~/VoidArchive` (with confirmation):**
    ```bash
    ./src/dust_bunny_sweeper.sh -d ~/Downloads -s 100 -o ~/VoidArchive
    ```

3.  **Forcefully move files in `/tmp` older than 7 days to `/tmp/quarantine`:**
    ```bash
    ./src/dust_bunny_sweeper.sh -d /tmp -a 7 -o /tmp/quarantine -f
    ```

4.  **Find files in `/home/user/documents` that are either older than 365 days OR larger than 50MB (listing only):**
    ```bash
    ./src/dust_bunny_sweeper.sh -d /home/user/documents -a 365 -s 50
    ```
    *(Note: When both `-a` and `-s` are used, files matching either criterion will be identified.)*

## Development & Testing

To run the automated tests:

```bash
cd bash-utils/nightly-digital-dust-bunny-sweeper
./tests/test_dust_bunny_sweeper.sh
```

The tests create temporary directories and files to simulate various scenarios, ensuring the sweeper functions correctly without affecting your actual filesystem.
