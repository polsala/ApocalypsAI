# Nightly Memory Mender

A Rust CLI tool to detect and mend minor data corruptions in text files, ensuring the integrity of precious post-apocalyptic logs and records. It identifies non-printable control characters and invalid UTF-8 sequences, replacing them with a configurable placeholder.

## Features

*   **Corruption Detection**: Identifies common control characters (e.g., `\x00` to `\x1F` excluding `\n`, `\r`, `\t`) and Unicode replacement characters (`U+FFFD`) which often signify invalid UTF-8.
*   **Automated Mending**: Replaces detected corruptions with a specified placeholder (default: `[MENDED]`).
*   **Dry Run Mode**: Preview changes without modifying the original file.
*   **Backup Creation**: Automatically creates a `.bak` file when overwriting the input file.
*   **Customizable Placeholder**: Define your own text for mended sections.

## Installation

To install `nightly-memory-mender`, you need to have Rust and Cargo installed. If you don't, visit [rustup.rs](https://rustup.rs/).

1.  Clone the ApocalypsAI repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-memory-mender
    ```
2.  Build and install the utility:
    ```bash
    cargo install --path .
    ```
    This will install `nightly-memory-mender` to your Cargo bin directory (usually `~/.cargo/bin`), making it available in your PATH.

## Usage

```bash
nightly-memory-mender --input <FILE_PATH> [--output <OUTPUT_FILE_PATH>] [--placeholder <TEXT>] [--dry-run]
```

### Arguments

*   `-i`, `--input <FILE_PATH>`: **Required**. Path to the input file to mend.
*   `-o`, `--output <OUTPUT_FILE_PATH>`: Optional. Path to the output file. If not specified, the input file will be overwritten, and a backup (`.bak`) will be created.
*   `-p`, `--placeholder <TEXT>`: Optional. Placeholder text to insert where corruption is detected. Defaults to `[MENDED]`.
*   `-d`, `--dry-run`: Optional. Perform a dry run: detect corruptions and report, but do not write any changes to disk.

### Examples

1.  **Mend a file and overwrite it (with backup):**
    ```bash
    echo -e "Important\x00Log\u{FFFD}Entry" > corrupted_log.txt
    nightly-memory-mender --input corrupted_log.txt
    # This will create 'corrupted_log.txt.bak' and update 'corrupted_log.txt'
    cat corrupted_log.txt
    # Output: Important[MENDED]Log[MENDED]Entry
    ```

2.  **Mend a file and save to a new file:**
    ```bash
    echo -e "Secret\x01Plans" > secret_plans.txt
    nightly-memory-mender --input secret_plans.txt --output mended_plans.txt
    cat mended_plans.txt
    # Output: Secret[MENDED]Plans
    ```

3.  **Perform a dry run with a custom placeholder:**
    ```bash
    echo -e "Ancient\x02Scroll\x03Fragment" > ancient_scroll.txt
    nightly-memory-mender --input ancient_scroll.txt --placeholder "[VOID_ECHO]" --dry-run
    # Output will show detected corruptions and a preview, but ancient_scroll.txt remains unchanged.
    ```

4.  **Check a clean file:**
    ```bash
    echo "Pristine data here." > clean_data.txt
    nightly-memory-mender --input clean_data.txt
    # Output: No corruptions detected in "clean_data.txt". All clear!
    ```

## Development

To run tests:
```bash
cargo test
```
