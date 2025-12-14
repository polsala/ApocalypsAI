# Nightly Relic Sorter

A high-performance CLI tool to categorize and organize scavenged files into whimsical "relic" types based on their content and metadata. This utility helps survivors quickly make sense of the digital detritus found in the wasteland, providing a structured overview of their digital treasures.

## Usage

To use the `nightly-relic-sorter`, navigate to its directory and run it with `cargo run -- [OPTIONS] <PATH>`. For a release build, use `cargo install` or `cargo build --release` and run the executable directly.

```bash
# Scan a directory and print a summary
nightly-relic-sorter --path /path/to/your/scavenged/data

# Scan a directory with verbose output (shows each file's classification)
nightly-relic-sorter -p /path/to/your/scavenged/data -v

# Get help
nightly-relic-sorter --help
```

### Arguments

*   `-p`, `--path <PATH>`: The directory to scan for relics. This is a required argument.
*   `-v`, `--verbose`: Be verbose, showing each file's path and its detected relic type during the scan.

## Relic Categories

Files are classified into the following whimsical categories:

*   **Ancient Scrolls (Text)**: Text files, documents, logs, markdown.
*   **Visual Glyphs (Image)**: Image files (JPG, PNG, GIF, etc.).
*   **Sonic Echoes (Audio)**: Audio files (MP3, WAV, FLAC, etc.).
*   **Moving Illusions (Video)**: Video files (MP4, AVI, MOV, etc.).
*   **Bundled Secrets (Archive)**: Compressed archives (ZIP, TAR, GZ, RAR, 7Z).
*   **Forbidden Runes (Executable/Script)**: Executables, scripts, and source code files.
*   **Digital Artifacts (Data/Code)**: Structured data files (JSON, XML, CSV, YAML, TOML, SQL) and other code-related files.
*   **Unidentified Relic**: Files that couldn't be classified by content or extension.

## Development

This utility is written in Rust.

### Building

```bash
cargo build --release
```

The executable will be found in `target/release/nightly-relic-sorter`.

### Running Tests

```bash
cargo test
```
