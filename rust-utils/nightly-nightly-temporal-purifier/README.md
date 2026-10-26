# Nightly Temporal Purifier

A high-performance CLI tool to identify and optionally purge files older than a specified duration, framed as "temporal residue cleanup". This utility helps maintain system hygiene by removing digital detritus that accumulates over time, ensuring your storage remains pristine and free from temporal distortions.

## Features

*   **Recursive Scanning**: Scans directories and their subdirectories for files.
*   **Age-Based Filtering**: Identifies files older than a user-defined duration (e.g., 1 day, 3 hours, 45 minutes).
*   **Dry-Run Mode**: Safely preview which files would be purged without making any changes.
*   **Deletion Mode**: Permanently removes identified "temporal residue" files.
*   **Whimsical Narrative**: Adds a touch of ApocalypsAI charm to mundane cleanup tasks.

## Installation

To build and install `nightly-temporal-purifier`, you need Rust and Cargo installed.

1.  Clone the repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-temporal-purifier
    ```
2.  Build the utility:
    ```bash
    cargo build --release
    ```
3.  The executable will be located at `target/release/nightly-temporal-purifier`. You can move it to your system's PATH for easier access.

## Usage

```bash
nightly-temporal-purifier --help
```

### Examples

**1. List files older than 7 days in the current directory (dry-run, default):**

```bash
nightly-temporal-purifier . --duration 7d
```

**2. List files older than 3 hours in a specific log directory:**

```bash
nightly-temporal-purifier /var/log/app --duration 3h
```

**3. Permanently purge files older than 30 minutes in a temporary directory:**

```bash
nightly-temporal-purifier /tmp/cache --duration 30m --delete
```

**4. List files older than 1 month in your downloads folder:**

```bash
nightly-temporal-purifier ~/Downloads --duration 1M
```

## Duration Format

The `--duration` argument accepts a number followed by a unit:
*   `s`: seconds (e.g., `60s`)
*   `m`: minutes (e.g., `30m`)
*   `h`: hours (e.g., `24h`)
*   `d`: days (e.g., `7d`)
*   `w`: weeks (e.g., `2w`)
*   `M`: months (approx. 30 days, e.g., `1M`) - *Note: Months are approximate for simplicity.*
*   `y`: years (approx. 365 days, e.g., `1y`) - *Note: Years are approximate for simplicity.*

## Contributing

Feel free to contribute to the temporal purification efforts!
