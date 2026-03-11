# Nightly Temporal Debris Sweeper

A whimsical yet useful bash utility to identify and optionally sweep away old, temporary files and directories, treating them as digital "temporal debris" that accumulates over time. Keep your digital space sparkling clean and free from the echoes of forgotten data!

## \ud83d\ud broom Features

*   **Temporal Debris Detection**: Scans specified directories for files and directories older than a configurable number of days.
*   **Dry Run by Default**: Safely lists what *would* be swept without making any changes.
*   **Interactive Sweeping**: Prompts for confirmation before actual deletion.
*   **Force Sweeping**: Option to bypass confirmation for automated cleanup (use with caution!).
*   **Flexible Paths & Ages**: Customize the scan path and the age threshold for debris.

## \ud83d\ude80 Usage

### Prerequisites

You need a Unix-like environment with `bash`, `find`, `xargs`, `rm`, and `date` utilities.

### Basic Dry Run (Recommended First Step)

To see what temporal debris is lurking in your `/tmp` directory (default path) that's older than 7 days (default age), simply run:

```bash
./src/temporal_debris_sweeper.sh
```

Or specify a path and age:

```bash
./src/temporal_debris_sweeper.sh --path ~/.cache --age 30
```

This will list all identified debris without deleting anything.

### Performing an Actual Sweep (with Confirmation)

Once you're confident with the dry run results, you can initiate an actual sweep. The script will ask for confirmation before proceeding:

```bash
./src/temporal_debris_sweeper.sh --sweep --path /var/log/old_logs --age 60
```

You can also use `-c` for confirmation:
```bash
./src/temporal_debris_sweeper.sh -p /tmp -a 14 -c
```

### Force Sweeping (No Confirmation - Use with Extreme Caution!)

For automated environments or when you are absolutely sure, you can force the sweep without any confirmation prompt. **Be very careful with this option, as it will permanently delete files.**

```bash
./src/temporal_debris_sweeper.sh --path ~/Downloads --age 90 --force
```

### Full Options

```
Usage: ./src/temporal_debris_sweeper.sh [OPTIONS] [PATH]

Whimsically identifies and optionally sweeps away old, temporary files and directories.
Treats old files as 'temporal debris' that accumulates over time.

Options:
  -p, --path <PATH>     Specify the directory to scan (default: /tmp)
  -a, --age <DAYS>      Files/directories older than <DAYS> will be considered debris (default: 7 days)
  -f, --force           Perform actual deletion without confirmation (USE WITH CAUTION!)
  -c, --confirm         Require confirmation before deletion (overrides -f if both present)
  -s, --sweep           Perform actual deletion (disables dry run, requires confirmation unless -f is used)
  -h, --help            Display this help message

By default, the script runs in dry-run mode, only listing files that would be swept.
Use -s to enable actual sweeping. It will prompt for confirmation unless -f is also used.
```

## \ud83e\uddea Testing

The utility comes with a self-contained test suite written in Bash. These tests are deterministic and use mocks to simulate file operations and user input without affecting your actual filesystem.

To run the tests:

```bash
./tests/test_temporal_debris_sweeper.sh
```

The tests will create temporary directories, populate them with files of specific ages, and then verify the script's behavior in dry-run and sweep modes, including confirmation prompts.
