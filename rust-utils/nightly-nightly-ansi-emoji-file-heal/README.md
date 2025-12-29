# nightly-ansi-emoji-file-health

A whimsical Rust CLI that scans a directory and reports the "health" of each file using emojis. Healthy files are small (<1 MB) and short (<1000 lines). Unhealthy files get a red cross.

## Usage

```bash
cargo run --quiet -- <directory>
```

or build and run:

```bash
cargo build --release
./target/release/nightly-ansi-emoji-file-health <directory>
```

## Example

```bash
$ ./nightly-ansi-emoji-file-health .
📁 ./example.txt | 1.2 KB | 42 lines | ✅
📁 ./large.rs | 2.3 MB | 1500 lines | ❌
```

## Features

- Recursively walks directories.
- Counts lines and file size.
- Uses emojis for quick visual feedback.
- Written in Rust for speed and safety.
