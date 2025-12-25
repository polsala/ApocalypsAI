# nightly-ghost-buster

A whimsical Rust CLI that hunts down hidden files (ghosts) in a directory and optionally deletes them.

## Usage

```bash
# List hidden files
cargo run -- --path /path/to/dir

# Delete hidden files
cargo run -- --path /path/to/dir --delete
```

## Features

- Scans recursively for files starting with a dot.
- Prints each ghost with a spooky message.
- Optional `--delete` flag to remove them.
