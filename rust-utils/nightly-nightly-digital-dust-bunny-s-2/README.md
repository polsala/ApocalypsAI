# Nightly Digital Dust Bunny Sweeper

## Overview

The `nightly-digital-dust-bunny-sweeper` is a whimsical yet powerful command-line utility crafted in Rust. It helps you unearth and categorize those long-forgotten, unused files lurking in your file system \u2013 your "digital dust bunnies." By scanning directories and analyzing file access and modification times, it provides playful suggestions for decluttering your digital realm.

Think of it as a tiny, efficient Roomba for your hard drive, but with a sense of humor.

## Features

*   **High Performance:** Built with Rust for speed and efficiency in file system traversal.
*   **Whimsical Categorization:** Files are grouped into fun categories like "Petrified Pixie Dust," "Forgotten Digital Relics," and "Slumbering Data Golems."
*   **Configurable Age Threshold:** Specify how old a file must be to be considered a "dust bunny."
*   **Dry Run Mode:** See what would be swept without actually deleting anything.
*   **Interactive Cleanup (Future):** (Mention as a potential future feature, but not implemented in V1 to keep it simple and focused on detection).

## Installation

### Prerequisites

*   Rust toolchain (rustup recommended)

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Build and Install

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-digital-dust-bunny-sweeper
cargo build --release
cargo install --path .
```

This will install `dust-bunny-sweeper` to your Cargo bin directory, usually `~/.cargo/bin`. Make sure this directory is in your `PATH`.

## Usage

```bash
dust-bunny-sweeper --help
```

```
Nightly Digital Dust Bunny Sweeper

A whimsical yet powerful command-line utility to unearth and categorize old, unused files.

Usage: dust-bunny-sweeper [OPTIONS] --path <PATH>

Options:
  -p, --path <PATH>          The directory to scan for digital dust bunnies
  -a, --age <AGE>            Minimum age for a file to be considered (e.g., "30d", "1y", "2w"). Defaults to 90 days.
  -d, --dry-run              Perform a dry run without suggesting actual deletion commands
  -v, --verbose              Enable verbose output
  -h, --help                 Print help
  -V, --version              Print version
```

### Examples

1.  **Scan your downloads folder for files older than 60 days (dry run):**

    ```bash
dust-bunny-sweeper --path ~/Downloads --age 60d --dry-run
    ```

2.  **Scan a project directory for files older than 1 year:**

    ```bash
dust-bunny-sweeper --path ~/Projects/old-project --age 1y
    ```

3.  **Scan the current directory with default age (90 days):**

    ```bash
dust-bunny-sweeper --path .
    ```

## Whimsical Categories Explained

*   **Petrified Pixie Dust:** Very old, small files (e.g., tiny logs, forgotten config snippets).
*   **Forgotten Digital Relics:** Older, medium-sized files (e.g., old backups, archived documents).
*   **Slumbering Data Golems:** Large, ancient files that haven't been touched in ages (e.g., old ISOs, forgotten video projects).
*   **Vacant Memory Caverns:** Empty directories that serve no purpose.

## Development

To run tests:

```bash
cargo test
```
