# nightly-path-purifier

A high-performance Rust CLI tool to clean and optimize your system's `PATH` environment variable by removing duplicate and non-existent entries. Keep your command-line environment pristine and efficient!

## Features

*   **Duplicate Removal**: Automatically identifies and removes redundant entries from your `PATH`.
*   **Non-Existent Path Pruning**: Scans for and removes directories that no longer exist on your filesystem.
*   **Cross-Platform**: Works on Linux, macOS, and Windows, respecting platform-specific path delimiters.
*   **Dry Run Mode**: Preview changes before applying them, ensuring no surprises.
*   **Interactive Mode**: Review each proposed change and decide whether to keep or remove it.

## Installation

To install `nightly-path-purifier`, you'll need Rust and Cargo installed. If you don't have them, visit [rust-lang.org](https://www.rust-lang.org/tools/install) for instructions.

```bash
cargo install nightly-path-purifier
```

## Usage

The `path-purifier` command provides several options for cleaning your `PATH`.

### Dry Run (Recommended First Step)

To see what changes would be made without actually modifying your `PATH`, use the `--dry-run` flag:

```bash
path-purifier --dry-run
```

This will print the proposed clean `PATH` to standard output and list any removed entries.

### Apply Changes

To apply the changes and print the new `PATH` to standard output (which you can then use to set your environment variable, e.g., `export PATH=$(path-purifier --apply)`):

```bash
path-purifier --apply
```

**Note**: This command prints the new PATH to stdout. You'll typically want to capture this output and set your `PATH` variable in your shell's configuration file (e.g., `.bashrc`, `.zshrc`, `config.fish`, or Windows environment variables) or directly in your current session.

Example for Bash/Zsh:
```bash
export PATH="$(path-purifier --apply)"
```

Example for Fish:
```fish
set -gx PATH (path-purifier --apply)
```

### Interactive Mode

For fine-grained control, use the `--interactive` flag. This will prompt you for each duplicate or non-existent path, allowing you to decide whether to keep or remove it.

```bash
path-purifier --interactive
```

### Options

```
path-purifier 0.1.0
A high-performance Rust CLI tool to clean and optimize your system's PATH environment variable.

USAGE:
    path-purifier [OPTIONS]

OPTIONS:
    -a, --apply          Apply the changes and print the new PATH to stdout
    -d, --dry-run        Perform a dry run and show what changes would be made
    -h, --help           Print help information
    -i, --interactive    Interactively choose which paths to keep or remove
    -V, --version        Print version information
```

## Development

To build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-path-purifier
cargo build --release
```

The executable will be located at `target/release/path-purifier`.

## Tests

To run the tests:

```bash
cargo test
```
