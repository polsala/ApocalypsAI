# nightly-digital-dust-sweeper

A whimsical Bash script to find and suggest cleaning up digital 'dust bunnies' – old, unused files and empty directories – from your system. It helps declutter your digital space by identifying forgotten files and vacant directories, offering a "dry run" for review or a "sweep" mode to move them to a designated "digital compost heap."

## Features

*   **Find Ancient Scrolls**: Identifies files older than a specified age threshold.
*   **Locate Forgotten Chambers**: Discovers empty directories.
*   **Dry Run Mode (Default)**: Safely lists potential dust bunnies without making any changes.
*   **Sweep Mode**: Moves identified old files to a configurable "digital compost heap" and removes empty directories.
*   **Configurable**: Set target directory, age threshold, and compost heap location.

## Usage

### Prerequisites

*   Bash shell
*   `find` utility
*   `mv` utility (for sweep mode)
*   `rmdir` utility (for sweep mode)
*   `mkdir` utility
*   `grep` utility

### Running the Sweeper

Navigate to the utility's directory or call the script directly:

```bash
./src/dust_sweeper.sh [OPTIONS]
```

**Options:**

*   `-d, --directory <path>`: Target directory to scan (default: current directory `.` ).
*   `-a, --age <days>`: Files older than this many days are considered dust bunnies (default: `90`).
*   `-c, --compost <path>`: Directory to move dust bunnies to when sweeping (default: `./digital_compost_heap`).
*   `-s, --sweep`: **DANGER!** Actually move files to the compost heap and remove empty directories. **Use with caution!** (Default: dry run).
*   `-h, --help`: Display the help message.

### Examples

**1. Dry run in the current directory, finding files older than 90 days (default):**

```bash
./src/dust_sweeper.sh
```

**2. Dry run in `/var/log`, looking for files older than 180 days:**

```bash
./src/dust_sweeper.sh --directory /var/log --age 180
```

**3. Perform a sweep in `/tmp/my_app_data`, moving files older than 30 days to `/archive/compost`:**

```bash
./src/dust_sweeper.sh --directory /tmp/my_app_data --age 30 --sweep --compost /archive/compost
```

## Development and Testing

### Running Tests

The tests are self-contained and create a temporary environment to simulate file system changes.

```bash
./tests/test_dust_sweeper.sh
```

**Note on `date` command:** The test script uses `date -d "X days ago"` for setting file modification times, which is common on GNU/Linux systems. If you are on a macOS/BSD system, you might need to adjust the `touch` commands in `tests/test_dust_sweeper.sh` to use `date -v -Xd` syntax (e.g., `touch -t $(date -v -91d +%Y%m%d%H%M.%S)`). The main script itself relies on `find -mtime` which is standard.

## Contributing

Feel free to suggest improvements or new features!
