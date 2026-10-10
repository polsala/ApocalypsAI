# Nightly Temporal Dust Bunny Sweeper

## 🧹 Overview

The `nightly-temporal-dust-bunny-sweeper` is a whimsical-yet-useful utility designed to help you keep your digital realms tidy. It scans specified directories for "temporal dust bunnies" – files and directories that haven't been touched in an age, accumulating digital clutter. Whether you want to merely observe these ancient artifacts, sweep them into the void, or archive them for future archaeological expeditions, this tool has you covered.

Think of it as a digital broom for the forgotten corners of your filesystem, ensuring that only the freshest temporal matter remains.

## ✨ Features

*   **Age-based Scanning**: Identify files and directories older than a specified number of days.
*   **Dry Run Mode**: Safely preview what would be swept or archived without making any changes.
*   **Temporal Sweep**: Permanently delete detected temporal dust bunnies, freeing up precious digital space.
*   **Archive to the Void**: Move old files and directories to a designated archive location, preserving them for posterity (or until you decide to truly sweep them).
*   **Multiple Target Directories**: Scan several locations at once.
*   **Logging**: Records all sweep/archive actions to a log file for audit.

## 🚀 Usage

### Prerequisites

*   A Bash-compatible shell (e.g., Bash, Zsh).
*   Standard Unix utilities: `find`, `rm`, `mv`, `mkdir`, `date`, `grep`.

### Running the Sweeper

```bash
./src/temporal_dust_bunny_sweeper.sh [OPTIONS] <DIRECTORY...>
```

### Options

*   `-a, --age <DAYS>`: Specify the age threshold in days. Files/directories modified *more than* this many days ago will be considered temporal dust bunnies. Default is `90` days.
*   `-d, --dry-run`: Perform a dry run. The script will list all detected dust bunnies but will not delete or move any files. This is the default action if no `--sweep` or `--archive` option is provided.
*   `-s, --sweep`: Permanently delete the detected temporal dust bunnies. **Use with caution!** This action is irreversible.
*   `-r, --archive <DIR>`: Move the detected temporal dust bunnies to the specified archive directory. If the directory does not exist, the script will attempt to create it.
*   `-h, --help`: Display the usage information and exit.

### Examples

**1. Dry Run: See what's lurking in `/var/log` and `/tmp` older than 60 days:**

```bash
./src/temporal_dust_bunny_sweeper.sh --age 60 --dry-run /var/log /tmp
```

**2. Sweep: Permanently delete files in `/old_backups` older than 30 days:**

```bash
./src/temporal_dust_bunny_sweeper.sh --age 30 --sweep /old_backups
```

**3. Archive: Move old downloads from `/home/user/downloads` to `/temporal_void_archive`:**

```bash
./src/temporal_dust_bunny_sweeper.sh --archive /temporal_void_archive /home/user/downloads
```

**4. Default Dry Run (90 days):**

```bash
./src/temporal_dust_bunny_sweeper.sh /home/user/documents /var/cache
```

## 📝 Logging

All actual sweep or archive operations are logged to `/tmp/temporal_dust_bunny_sweeper.log`. This log file records the timestamp of the action and the path of the item that was processed, providing an audit trail of your temporal tidying efforts.

## ⚠️ Important Notes

*   **Permissions**: Ensure the script has appropriate read/write/delete permissions in the target directories and the archive directory.
*   **Root/Sudo**: For system directories (e.g., `/var/log`), you might need to run the script with `sudo`.
*   **Irreversible Actions**: The `--sweep` option performs permanent deletion. Always use `--dry-run` first to confirm the intended actions.
*   **Symlinks**: `find` typically follows symlinks. Be aware of this behavior when scanning directories that contain them.

## 🧪 Testing

To run the automated tests for the `Nightly Temporal Dust Bunny Sweeper`, navigate to the utility's root directory and execute:

```bash
./tests/test_sweeper.sh
```

The tests create temporary files and directories with specific modification times to simulate different scenarios (old files, recent files, dry runs, sweeps, archives) and verify the script's behavior.
