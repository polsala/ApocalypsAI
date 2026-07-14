# Nightly Temporal Echo Diff (nightly-temporal-echo-diff)

A Rust CLI tool to create and diff files against their 'temporal echoes' (snapshots) for quick change detection without a full version control system.

## Overview

`nightly-temporal-echo-diff` allows you to take a snapshot (an "echo") of a file at a specific moment. Later, you can compare the current state of that file against its stored echo to quickly identify changes. This is particularly useful for configuration files, temporary scripts, or data files where you need to track minor, ad-hoc modifications without the overhead of a full Git repository.

## Features

*   **Create Echo**: Store a snapshot of a file.
*   **Diff Echo**: Compare a file's current content against its last stored echo.
*   **List Echoes**: See which files currently have echoes.
*   **Clean Echo**: Remove a specific file's echo.
*   **Clean All Echoes**: Remove all stored echoes.

## Installation

To install `nightly-temporal-echo-diff`, you need Rust and Cargo installed.

```bash
cargo install --path .
```

This will install the `echo-diff` executable to your Cargo bin directory.

## Usage

The primary executable is `echo-diff`.

```bash
echo-diff --help
```

### Commands:

*   **`echo-diff create <FILE_PATH>`**
    Takes a snapshot of the specified file. If an echo already exists, it will be overwritten.
    ```bash
    echo-diff create /path/to/my_config.txt
    ```

*   **`echo-diff diff <FILE_PATH>`**
    Compares the current content of the specified file against its stored echo. Outputs a line-by-line diff.
    ```bash
    echo-diff diff /path/to/my_config.txt
    ```

*   **`echo-diff list`**
    Lists all files for which echoes are currently stored. Note: Currently, it lists the internal hash-based names of the echo files, not their original paths.
    ```bash
    echo-diff list
    ```

*   **`echo-diff clean <FILE_PATH>`**
    Removes the echo for the specified file.
    ```bash
    echo-diff clean /path/to/my_config.txt
    ```

*   **`echo-diff clean --all`**
    Removes all stored echoes from the system.
    ```bash
    echo-diff clean --all
    ```

## Echo Storage

Echoes are stored in a hidden directory, typically `~/.temporal_echoes/`, where `~` is your user's home directory. Each echo file is named based on a SHA256 hash of the original file's absolute path to ensure uniqueness and avoid conflicts.

## Development

To run tests:

```bash
cargo test
```

To build:

```bash
cargo build
```
