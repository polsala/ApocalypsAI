# Nightly Temporal File Sweeper

The digital realm, much like the cosmos, accumulates echoes of the past. The `nightly-temporal-file-sweeper` is your whimsical guide to identifying these "temporal echoes" – files long forgotten, lingering from projects past, or simply awaiting their next cosmic alignment. This utility helps you discover them and offers playful suggestions for their fate, without actually performing the actions itself. You are the ultimate arbiter of your digital destiny!

## Features

*   **Echo Detection**: Scans a specified directory for files older than a given number of days.
*   **Whimsical Fates**: For each detected echo, suggests options like "Archive to the Chrono-Vault," "Vanish into the Aether," or "Re-energize for the Present."
*   **Safe Suggestions**: Outputs actionable commands for you to review and execute, ensuring you remain in control.

## Usage

```bash
./src/temporal_sweeper.sh <directory_to_scan> <age_in_days>
```

### Arguments:

*   `<directory_to_scan>`: The path to the directory you wish to scan for temporal echoes.
*   `<age_in_days>`: The minimum age (in days) for a file to be considered a "temporal echo."

### Examples:

Scan the current directory for files older than 90 days:
```bash
./src/temporal_sweeper.sh . 90
```

Scan your `~/Documents/OldProjects` directory for files older than 365 days:
```bash
./src/temporal_sweeper.sh ~/Documents/OldProjects 365
```

## Output Example

```
🌌 Initiating Temporal Echo Scan in '/tmp/my_project' for files older than 30 days...

⏳ Temporal Echo Detected: "/tmp/my_project/old_report.pdf" (Last modified: 2023-01-15)
   Suggested Fates:
     1. Archive to the Chrono-Vault: mkdir -p "/tmp/my_project/chrono_vault" && mv "/tmp/my_project/old_report.pdf" "/tmp/my_project/chrono_vault/"
     2. Vanish into the Aether: rm "/tmp/my_project/old_report.pdf"
     3. Re-energize for the Present: touch "/tmp/my_project/old_report.pdf"

⏳ Temporal Echo Detected: "/tmp/my_project/forgotten_script.sh" (Last modified: 2023-03-20)
   Suggested Fates:
     1. Archive to the Chrono-Vault: mkdir -p "/tmp/my_project/chrono_vault" && mv "/tmp/my_project/forgotten_script.sh" "/tmp/my_project/chrono_vault/"
     2. Vanish into the Aether: rm "/tmp/my_project/forgotten_script.sh"
     3. Re-energize for the Present: touch "/tmp/my_project/forgotten_script.sh"

✨ Temporal Echo Scan Complete! May your digital space be ever harmonious.
```

## Installation

Simply clone the repository and navigate to the `bash-utils/nightly-temporal-file-sweeper` directory. The script is self-contained.

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/bash-utils/nightly-temporal-file-sweeper
chmod +x src/temporal_sweeper.sh
```
