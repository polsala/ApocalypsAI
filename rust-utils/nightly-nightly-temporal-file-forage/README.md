# nightly-temporal-file-forager

Unearth the hidden history of your digital landscape! The `nightly-temporal-file-forager` is a whimsical Rust CLI tool that scans specified directories and categorizes files and subdirectories based on their last modification time. It helps you identify "Ancient Relics," "Dusty Tomes," "Blooming Archives," and "Fresh Sprouts" in your file system, guiding you in your digital archaeology efforts.

## Features

*   **Temporal Classification:** Assigns whimsical categories to files/directories based on their age.
*   **Recursive Scanning:** Explores subdirectories to provide a comprehensive overview.
*   **Configurable Depth:** Control how deep the forager digs.
*   **Action Suggestions:** Provides light-hearted suggestions for managing your digital findings.

## Installation

Ensure you have Rust and Cargo installed. If not, visit [rust-lang.org](https://www.rust-lang.org/tools/install).

```bash
cargo install temporal-file-forager
```

## Usage

```bash
temporal-file-forager [OPTIONS] <PATH>
```

### Arguments

*   `<PATH>`: The starting directory to forage.

### Options

*   `-d, --depth <DEPTH>`: Maximum recursion depth. Default is unlimited.
*   `-v, --verbose`: Show more details about each file/directory.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

### Examples

1.  **Forage the current directory with default settings:**
    ```bash
    temporal-file-forager .
    ```

2.  **Forage your documents folder, showing verbose output:**
    ```bash
    temporal-file-forager ~/Documents -v
    ```

3.  **Forage a specific project directory, limiting depth to 2:**
    ```bash
    temporal-file-forager ~/Projects/MyOldProject --depth 2
    ```

## Temporal Categories

The forager uses the following whimsical categories based on the last modification time:

*   **Fresh Sprout (0-7 days old):** Recently touched, actively growing. *Action: Keep nurturing.*
*   **Blooming Archive (7-30 days old):** Still relevant, but settling in. *Action: Review periodically.*
*   **Dusty Tome (30-180 days old):** Gathering a bit of digital dust. *Action: Consider archiving or refactoring.*
*   **Ancient Relic (180-365 days old):** A true artifact from a bygone era. *Action: Archive or evaluate for deletion.*
*   **Forgotten Echo (> 365 days old):** Lost to the sands of time. *Action: Deep archive or purge with care.*

## Development

To build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-temporal-file-forager
cargo build --release
./target/release/temporal-file-forager .
```

To run tests:

```bash
cargo test
```
