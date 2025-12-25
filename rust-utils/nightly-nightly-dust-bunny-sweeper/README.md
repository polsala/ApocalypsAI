# Nightly Dust Bunny Sweeper

"Don't let your digital space get cluttered with forgotten echoes of the past!"

The `nightly-dust-bunny-sweeper` is a whimsical yet powerful command-line utility written in Rust, designed to help you identify and manage stale, unused files on your filesystem. It metaphorically sweeps through your directories, finding "digital dust bunnies" – files that haven't been modified in a specified number of days – and reports them, helping you reclaim precious digital real estate.

## Features

*   **High Performance**: Built with Rust for blazing-fast directory traversal and file metadata inspection.
*   **Configurable Age Threshold**: Define what constitutes a "dust bunny" by specifying the age in days.
*   **Recursive Scanning**: Scans directories and all their subdirectories.
*   **Dry Run Mode**: Preview which files would be reported without making any changes.
*   **Clear Reporting**: Outputs the path and last modification time of each identified dust bunny.

## Installation

To install `nightly-dust-bunny-sweeper`, you'll need [Rust and Cargo](https://www.rust-lang.org/tools/install) installed on your system.

1.  **Clone the repository (or navigate to the utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-dust-bunny-sweeper
    ```
2.  **Build the project:**
    ```bash
    cargo build --release
    ```
3.  **The executable will be located at `target/release/nightly-dust-bunny-sweeper`. You can move it to a directory in your system's PATH for easier access (e.g., `/usr/local/bin`).**

    ```bash
    sudo cp target/release/nightly-dust-bunny-sweeper /usr/local/bin/
    ```

## Usage

Run the `nightly-dust-bunny-sweeper` from your terminal.

```bash
nightly-dust-bunny-sweeper [OPTIONS]
```

### Options

*   `-p, --path <PATH>`: The directory to sweep for digital dust bunnies. Defaults to the current directory (`.`).
*   `-a, --age-days <DAYS>`: The age in days after which a file is considered a dust bunny. Defaults to `90` days.
*   `-d, --dry-run`: Perform a dry run without actually deleting or archiving files. This is the default behavior for this version, as it only reports.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

### Examples

1.  **Scan the current directory for files older than 90 days (default):**
    ```bash
    nightly-dust-bunny-sweeper
    ```

2.  **Scan a specific directory (`/var/log/old_archives`) for files older than 365 days:**
    ```bash
    nightly-dust-bunny-sweeper --path /var/log/old_archives --age-days 365
    ```

3.  **Scan your home directory for files older than 30 days (dry run is implicit as no deletion is implemented yet):**
    ```bash
    nightly-dust-bunny-sweeper -p ~/ -a 30 --dry-run
    ```

## Development

To run tests:

```bash
cargo test
```

## Contributing

Feel free to contribute to sweeping more digital dust bunnies! Open issues or pull requests on the main ApocalypsAI repository.
