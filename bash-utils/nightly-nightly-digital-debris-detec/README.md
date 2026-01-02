# Nightly Digital Debris Detector

The digital world, much like the physical, accumulates its fair share of detritus. Over time, forgotten logs, temporary files, and abandoned data fragments can pile up, consuming precious storage and obscuring vital information. The Nightly Digital Debris Detector is your automated sentinel against this digital clutter, designed to identify and manage the aged remnants of your system's past.

## 🌌 What it Does

This whimsical-yet-useful utility scans a specified directory for files that haven't been touched in a while, classifying them as "digital debris." Once identified, you have the power to:

*   **Report:** Simply list the detected debris, giving you an overview of what's lurking.
*   **Archive:** Gently move the debris into a designated `.digital_debris_vault` subdirectory, preserving it for potential future archeology without cluttering the main pathways.
*   **Vaporize:** Permanently erase the debris from existence, freeing up space and ensuring a pristine digital landscape.

## 🚀 Usage

### Prerequisites

*   A Bash-compatible shell (e.g., Bash, Zsh).
*   Standard Unix utilities: `find`, `mv`, `rm`, `mkdir`, `wc`, `xargs`, `date`.

### Installation

1.  Save the script `digital_debris_detector.sh` to a convenient location (e.g., `~/bin/`).
2.  Make it executable: `chmod +x digital_debris_detector.sh`

### Running the Detector

```bash
./digital_debris_detector.sh [OPTIONS] <directory>
```

**Arguments:**

*   `<directory>`: The path to the directory you wish to scan for debris. This is a mandatory argument.

**Options:**

*   `-d <N>`, `--days <N>`: Specifies that files older than `N` days should be considered debris. `N` must be a positive integer. (Default: `30` days)
*   `-r`, `--report`: (Default action) Lists all detected debris files to standard output.
*   `-a`, `--archive`: Moves detected debris files into a `.digital_debris_vault` subdirectory within the scanned directory. If the vault doesn't exist, it will be created.
*   `-v`, `--vaporize`: Permanently deletes all detected debris files. **Use with caution!**
*   `-h`, `--help`: Displays the usage information and exits.

### Examples

**1. Report debris older than 60 days in your home directory:**

```bash
./digital_debris_detector.sh --days 60 --report ~/
```

**2. Archive debris older than 90 days in `/var/log`:**

```bash
./digital_debris_detector.sh -d 90 -a /var/log
```

**3. Vaporize all debris older than 7 days in your temporary files directory:**

```bash
./digital_debris_detector.sh --days 7 --vaporize /tmp
```

## 🛡️ Safety & Whimsy

*   **Archive First!** Before vaporizing, consider archiving files to the `.digital_debris_vault`. This provides a safety net, allowing you to review or recover files if needed.
*   **No Recursive Vaults:** The `.digital_debris_vault` is always created directly within the target directory, not recursively within subdirectories.
*   **Whimsical Output:** Enjoy the themed messages as your detector goes about its nightly duties!

May your digital realms remain ever clean and efficient!
