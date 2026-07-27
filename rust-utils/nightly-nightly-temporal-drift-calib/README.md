# Nightly Temporal Drift Calibrator

## Overview
In the ever-shifting currents of the digital realm, even file modification timestamps can fall prey to subtle 'temporal drift'. The `nightly-temporal-drift-calibrator` is your trusty Rust-powered CLI tool designed to detect these micro-anomalies and, if you dare, realign them with the present moment.

Think of it as a chronometer for your file system, ensuring that your digital artifacts are always in sync with the true flow of time. Useful for identifying files with incorrect timestamps that might disrupt build systems, caching, or backup integrity.

## Features
*   **Drift Detection**: Scans a specified directory (or the current one) for files whose modification times deviate significantly from the current system time.
*   **Configurable Threshold**: Set how much drift (in seconds) is considered an anomaly.
*   **Optional Recalibration**: With the `--fix` flag, it can reset drifted file modification times to the current system time.
*   **High Performance**: Written in Rust for blazing-fast file system traversal and time calculations.

## Installation

To install `nightly-temporal-drift-calibrator`, you'll need Rust and Cargo installed.

```bash
cargo install nightly-temporal-drift-calibrator
```

Alternatively, clone the repository and build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-temporal-drift-calibrator
cargo build --release
# The executable will be found at target/release/tdc
```

## Usage

```bash
tdc [OPTIONS] [PATH]
```

### Arguments
*   `<PATH>`: The directory to scan for temporal drift. Defaults to the current directory if not specified.

### Options
*   `-t, --threshold <SECONDS>`: The maximum allowed temporal drift in seconds. Files with modification times deviating more than this from the current system time will be reported. Defaults to `60` seconds.
*   `-f, --fix`: If present, detected drifted files will have their modification times updated to the current system time.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

### Examples

1.  **Scan the current directory for drifts greater than 300 seconds (5 minutes):**
    ```bash
tdc --threshold 300
    ```

2.  **Scan a specific directory and fix any drifts exceeding 120 seconds:**
    ```bash
tdc /path/to/your/data --threshold 120 --fix
    ```

3.  **Just check for any drift in a project folder (default threshold of 60s):**
    ```bash
tdc my_project_folder
    ```

## Whimsical Context

In the grand tapestry of existence, even the smallest digital threads can fray, leading to 'temporal echoes' and 'reality desynchronization'. The Nightly Temporal Drift Calibrator acts as a digital chrononaut, meticulously scanning for these subtle shifts. By realigning your file system's temporal signatures, you ensure that your local reality remains stable, preventing cascading causality errors and ensuring your backups don't accidentally retrieve a version of your cat from a parallel dimension where it's a sentient toaster.
