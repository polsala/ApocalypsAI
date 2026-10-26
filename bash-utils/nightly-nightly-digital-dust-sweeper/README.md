# 🌌 Nightly Digital Dust Bunny Sweeper 🌌

A whimsical utility to help you maintain a pristine digital environment by identifying and sweeping away 'digital dust bunnies' – those old, unused, or temporary files that accumulate over time.

## ✨ What it Does

This script scans a specified directory for files that meet certain criteria:

1.  **Ancient Artifacts**: Files older than a configurable number of days.
2.  **Ephemeral Remnants**: Files matching common temporary patterns (e.g., `.tmp`, `~`, `#*#`, `.DS_Store`, `.bak`, `.log`).

Once identified, you can either get a report of these digital dust bunnies or choose to sweep them away by moving them to a 'digital dustbin' (quarantine directory) or permanently deleting them.

## 🧹 Usage

```bash
digital-dust-bunny-sweeper.sh [OPTIONS]
```

### Options:

*   `--dir <path>`: Specify the directory to sweep. Defaults to the current directory (`.`).
*   `--age <days>`: Files older than this many days are considered ancient artifacts. Defaults to `30` days.
*   `--report`: (Default) Only report findings, do not perform any actions. This is highly recommended for a first run!
*   `--sweep`: Activate sweep mode. This will perform actions on the identified files. Requires either `--delete` or `--dustbin`.
*   `--delete`: When `--sweep` is active, permanently delete identified files. **Use with extreme caution!**
*   `--dustbin <path>`: When `--sweep` is active, move identified files to this 'digital dustbin' directory. If `--dustbin` is not specified with `--sweep`, `--delete` is implied.
*   `--help`: Display the help message and exit.

### Examples:

1.  **Just a Report (Recommended First Step):**
    ```bash
    ./src/digital-dust-bunny-sweeper.sh --dir /var/log --age 7 --report
    ```
    _This will show you all log files in `/var/log` older than 7 days, and any temporary files, without touching them._

2.  **Quarantine Dust Bunnies:**
    ```bash
    ./src/digital-dust-bunny-sweeper.sh --dir ~/Downloads --sweep --dustbin ~/DigitalDustbin
    ```
    _Moves all identified dust bunnies from `~/Downloads` into `~/DigitalDustbin`._

3.  **Vanquish Ephemeral Remnants (Use with Caution!):**
    ```bash
    ./src/digital-dust-bunny-sweeper.sh --dir /tmp --age 1 --sweep --delete
    ```
    _Permanently deletes files in `/tmp` older than 1 day or matching temporary patterns._

4.  **Sweep Current Directory (Default Age, Move to Default Dustbin):**
    ```bash
    ./src/digital-dust-bunny-sweeper.sh --sweep --dustbin ./quarantine
    ```
    _Scans the current directory for files older than 30 days or temporary, moving them to `./quarantine`._

## ⚠️ Important Considerations

*   **Always run with `--report` first** to see what files would be affected before performing any sweep actions.
*   Be mindful of the directory you target and the age you set. Deleting critical system files or recent work can lead to unexpected issues.
*   The script uses `find`, `rm`, and `mv` commands. Ensure you have appropriate permissions in the target and dustbin directories.

May your digital realm remain pristine!
