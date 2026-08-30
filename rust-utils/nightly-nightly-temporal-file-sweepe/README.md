# Nightly Temporal File Sweeper

## "Cleanse your digital realm of temporal dust bunnies!"

`nightly-temporal-file-sweeper` is a whimsical yet powerful command-line utility written in Rust. It helps you identify and manage old, forgotten files in your filesystem, which we affectionately call "temporal dust bunnies." These are files that haven't been modified or accessed in a long time, cluttering your digital space and consuming precious storage.

Whether you want to simply list them, move them to a designated "void archive," or permanently delete them, this tool provides a fast and efficient way to keep your directories tidy.

## Features

*   **High Performance**: Built with Rust for speed and efficiency in scanning large directories.
*   **Age-Based Filtering**: Specify a minimum age (e.g., 30 days, 1 week, 6 months, 1 year) to define what constitutes a "temporal dust bunny."
*   **Flexible Actions**: Choose to `list`, `move`, or `delete` identified files.
*   **Recursive Scanning**: Option to scan subdirectories or just the top-level directory.
*   **Dry Run Mode**: Preview changes before committing to any actions.
*   **Verbose Output**: Get more details about the scanning process and actions taken.

## Installation

To install `nightly-temporal-file-sweeper`, you need to have Rust and Cargo installed. If you don't, visit [rust-lang.org](https://www.rust-lang.org/tools/install).

```bash
cargo install nightly-temporal-file-sweeper
```

This will compile and install the `nightly-temporal-file-sweeper` executable to your Cargo bin directory (usually `~/.cargo/bin`). Make sure this directory is in your system's PATH.

## Usage

```bash
nightly-temporal-file-sweeper --help
```

```
Nightly Temporal File Sweeper: Cleanse your digital realm of temporal dust bunnies!

Usage: nightly-temporal-file-sweeper [OPTIONS] --path <PATH> --age <AGE_STRING>

Options:
  -p, --path <PATH>
          The root directory to scan for temporal dust bunnies.

  -a, --age <AGE_STRING>
          Minimum age for a file to be considered a temporal dust bunny (e.g., "30d", "1w", "6m", "1y").

  -s, --action <ACTION>
          Action to perform: 'list' (default), 'move', or 'delete'.

  -A, --archive-dir <ARCHIVE_PATH>
          Directory to move files to if action is 'move'.

  -r, --recursive
          Scan subdirectories recursively.

  -d, --dry-run
          Perform a dry run (don't make any changes).

  -v, --verbose
          Be verbose, print more details.

  -h, --help
          Print help (see a summary with '-h')

  -V, --version
          Print version
```

### Examples

1.  **List all files older than 90 days in your documents directory (dry run):**

    ```bash
    nightly-temporal-file-sweeper -p ~/Documents -a 90d --dry-run -v
    ```

2.  **Move files older than 6 months in your downloads to an archive:**

    ```bash
    nightly-temporal-file-sweeper -p ~/Downloads -a 6m --action move --archive-dir ~/VoidArchive -v
    ```

3.  **Recursively delete files older than 1 year in a project directory (use with caution!):**

    ```bash
    nightly-temporal-file-sweeper -p ~/Projects/OldProject -a 1y --action delete -r
    ```

    *Note: Deletion is permanent. Always use `--dry-run` first!*

4.  **List files older than 2 weeks in the current directory, non-recursively:**

    ```bash
    nightly-temporal-file-sweeper -p . -a 2w
    ```

## Contributing

Feel free to contribute to the Nightly Temporal File Sweeper! Report bugs, suggest features, or submit pull requests. Let's keep the digital realm clean together!
