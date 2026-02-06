# Nightly Digital Tremor Scan

`nightly-digital-tremor-scan` is a high-performance command-line utility written in Rust, designed to detect subtle, non-content-altering changes in your file system. Think of it as a digital seismograph for your directories, identifying "tremors" like metadata alterations, permission shifts, or the mysterious appearance/disappearance of files.

This tool is ideal for security monitoring, compliance auditing, or simply understanding the dynamic behavior of critical system directories where content might remain static but underlying attributes change.

## Features

*   **Snapshot Creation**: Generate a baseline JSON snapshot of a directory's file system metadata (file type, size, modification/access times, permissions).
*   **Tremor Detection**: Compare the current state of a directory against a previously saved snapshot to identify:
    *   New files or directories.
    *   Missing files or directories.
    *   Changes in file size.
    *   Changes in modification or access timestamps.
    *   Changes in file permissions (Unix-like systems).
*   **Performance**: Built with Rust for speed and efficiency, suitable for scanning large directory structures.

## Installation

To install `nightly-digital-tremor-scan`, you'll need [Rust and Cargo](https://www.rust-lang.org/tools/install) installed on your system.

```bash
cargo install nightly-digital-tremor-scan
```

Alternatively, you can clone the repository and build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-digital-tremor-scan
cargo build --release
# The executable will be found at target/release/nightly-digital-tremor-scan
```

## Usage

The utility has two main commands: `snapshot` and `detect`.

### 1. Create a Snapshot

First, create a baseline snapshot of the directory you wish to monitor. This will record the current state of all files and subdirectories.

```bash
nightly-digital-tremor-scan snapshot --path /path/to/monitor --output my_baseline_snapshot.json
```

*   `--path <DIRECTORY>`: The directory to scan and create a snapshot of.
*   `--output <FILE>`: The file path where the JSON snapshot will be saved.

Example:

```bash
$ nightly-digital-tremor-scan snapshot --path ./my_app_config --output config_v1.json
Creating snapshot of './my_app_config'...
Snapshot saved to 'config_v1.json'.
```

### 2. Detect Tremors

Later, you can run the `detect` command to compare the current state of the directory against your saved snapshot.

```bash
nightly-digital-tremor-scan detect --path /path/to/monitor --snapshot my_baseline_snapshot.json
```

*   `--path <DIRECTORY>`: The directory to scan for current tremors.
*   `--snapshot <FILE>`: The path to the previously saved JSON snapshot file.

Example (no changes):

```bash
$ nightly-digital-tremor-scan detect --path ./my_app_config --snapshot config_v1.json
Loading snapshot from 'config_v1.json'...
Detecting tremors in './my_app_config'...
No tremors detected. The digital landscape is calm.
```

Example (with changes):

Let's say `my_app_config/settings.conf` had its permissions changed from `644` to `755`, and a new file `my_app_config/new_log.txt` appeared.

```bash
$ nightly-digital-tremor-scan detect --path ./my_app_config --snapshot config_v1.json
Loading snapshot from 'config_v1.json'...
Detecting tremors in './my_app_config'...
--- DIGITAL TREMORS DETECTED! ---
  [CHANGE] 'settings.conf': Field 'permissions' changed from '644' to '755'
  [NEW]    'new_log.txt'
---------------------------------
```

## Development

To build and run tests locally:

```bash
cargo test
```

## Limitations

*   Permission detection for non-Unix systems (e.g., Windows) is currently a placeholder and will not report changes.
*   Does not compare file *content*, only metadata. For content integrity, consider checksumming tools.

## Contributing

Feel free to open issues or submit pull requests to enhance the digital tremor detection capabilities!
