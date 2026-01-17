# nightly-digital-decay-detect

The ApocalypsAI Nightly Integrator presents the `nightly-digital-decay-detect` utility! In the ever-shifting sands of the digital wasteland, files and directories can become forgotten relics, accumulating "digital decay" and consuming precious storage. This whimsical-yet-useful Bash script helps you identify these stale fragments of the past, allowing for informed cleanup or archiving.

## Purpose

This utility scans a specified directory for files and subdirectories that haven't been modified for a given number of days. It categorizes these as "Forgotten Tomes" (files) and "Ancient Relics" (directories), providing a report to help maintain system hygiene and reclaim digital space.

## Usage

```bash
./src/detect_decay.sh [-p <path>] [-d <days>] [-t <type>] [-h]
```

### Arguments

*   `-p <path>`: The target directory to scan. Defaults to the current directory (`.`).
*   `-d <days>`: The threshold in days. Files/directories not modified for this many days or more will be flagged as digital decay. Must be a positive integer. Defaults to `90`.
*   `-t <type>`: The report type.
    *   `summary` (default): Provides counts of decayed files and directories.
    *   `detailed`: Lists all identified decayed files and directories.
*   `-h`: Display the help message and exit.

## Examples

1.  **Scan the current directory for items older than 90 days (default summary report):**
    ```bash
    ./src/detect_decay.sh
    ```

2.  **Scan `/var/log` for items older than 365 days, with a detailed list:**
    ```bash
    ./src/detect_decay.sh -p /var/log -d 365 -t detailed
    ```

3.  **Scan your home directory for items older than 30 days (summary report):**
    ```bash
    ./src/detect_decay.sh -p ~/ -d 30
    ```

## Example Output (Summary)

```
--- Digital Decay Detector Report ---
Scanning: /home/user/my_project
Threshold: 90 days of inactivity
Report Type: summary
-------------------------------------

--- Decay Analysis ---
Files showing signs of 'Forgotten Tomes' (12 found):
Directories resembling 'Ancient Relics' (3 found):

Total 'Digital Decay' items: 15
Consider archiving or cleansing these forgotten fragments of the past.
-------------------------------------
```

## Example Output (Detailed)

```
--- Digital Decay Detector Report ---
Scanning: /home/user/my_project
Threshold: 90 days of inactivity
Report Type: detailed
-------------------------------------

--- Decay Analysis ---
Files showing signs of 'Forgotten Tomes' (2 found):
  - /home/user/my_project/old_report.pdf
  - /home/user/my_project/archive/legacy_data.zip
Directories resembling 'Ancient Relics' (1 found):
  - /home/user/my_project/old_backup_dir

Total 'Digital Decay' items: 3
Consider archiving or cleansing these forgotten fragments of the past.
-------------------------------------
```
