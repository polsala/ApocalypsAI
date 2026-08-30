# Nightly Digital Echo Scrubber

A high-performance CLI tool crafted in Rust to help you identify and suggest the removal of stale, unused files, metaphorically scrubbing digital echoes from your filesystem.

## The Whispers of Forgotten Data

Over time, our digital landscapes accumulate forgotten files – temporary relics, old downloads, abandoned projects. These "digital echoes" linger, consuming precious space and contributing to system clutter. The Digital Echo Scrubber helps you find these spectral files, allowing you to decide which echoes to silence forever.

## Features

*   **Blazing Fast:** Written in Rust for optimal performance when traversing large filesystems.
*   **Configurable Age:** Specify how old a file must be to be considered an "echo."
*   **Dry Run Mode:** Preview which files would be affected before making any changes.
*   **Simple CLI:** Easy to integrate into your nightly maintenance routines.

## Installation

Ensure you have Rust and Cargo installed. If not, follow the instructions at [rust-lang.org](https://www.rust-lang.org/tools/install).

```bash
cargo install nightly-digital-echo-scrubber
```

## Usage

```bash
nightly-digital-echo-scrubber [OPTIONS] <PATH>
```

### Arguments

*   `<PATH>`: The directory to scan for digital echoes.

### Options

*   `-a, --age <DAYS>`: Files older than this many days will be considered digital echoes. Defaults to `30` days.
*   `-d, --dry-run`: Perform a dry run. Only print what *would* be scrubbed, without deleting anything. (Recommended for first use!)
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

## Examples

1.  **Scan your current directory for files older than 60 days (dry run):**
    ```bash
    nightly-digital-echo-scrubber . --age 60 --dry-run
    ```

2.  **Scan a specific directory (`~/Downloads`) for files older than 90 days, and actually scrub them (use with caution!):**
    ```bash
    nightly-digital-echo-scrubber ~/Downloads --age 90
    ```

3.  **Just see the default (30 days) echoes in your home directory (dry run):**
    ```bash
    nightly-digital-echo-scrubber ~ --dry-run
    ```

## How it Works

The scrubber examines the "last modified" timestamp of each file. If a file's last modified time is older than the specified `--age` threshold, it's flagged as a digital echo. In dry-run mode, it simply reports these files. Without dry-run, it will attempt to delete them.

**Always use `--dry-run` first to understand the impact!**
