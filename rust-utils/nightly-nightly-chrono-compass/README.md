# Nightly Chrono-Compass

A high-performance CLI tool crafted in Rust to help survivors maintain their temporal alignment in a chaotic world. It displays the current local time and your system's uptime, translating the latter into a whimsical 'temporal drift' status.

## Features

*   **Current Time Display**: Always know the present moment.
*   **System Uptime**: Track how long your system has been running.
*   **Temporal Drift Status**: Get a whimsical assessment of your system's temporal stability based on its uptime.
*   **Performance**: Built with Rust for speed and efficiency.

## Installation

To install `nightly-chrono-compass`, you need to have Rust and Cargo installed. If you don't, visit [rustup.rs](https://rustup.rs/) for instructions.

1.  **Clone the repository (if not already done):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-chrono-compass
    ```
2.  **Build and install:**
    ```bash
    cargo install --path .
    ```
    This will install the `chrono-compass` executable to your Cargo bin directory (usually `~/.cargo/bin`), making it available globally.

## Usage

Simply run the `chrono-compass` command in your terminal:

```bash
chrono-compass
```

### Example Output

```
--- Nightly Chrono-Compass ---
Current Local Time: 2023-10-27 23:01:42
Uptime: 15h 45m 30s
Temporal Status: Slightly Drifting, but within acceptable parameters.
----------------------------
```

If running on a non-Linux system or if `/proc/uptime` is not accessible, the uptime and temporal status will be reported as unknown:

```
--- Nightly Chrono-Compass ---
Current Local Time: 2023-10-27 23:01:42
Failed to retrieve system uptime. Is this a Linux system?
Temporal Status: Unknown (Chrono-Compass offline)
----------------------------
```

## Temporal Status Guide

*   **Perfectly Aligned with the Chrono-Flow.** (Uptime < 1 hour)
*   **Slightly Drifting, but within acceptable parameters.** (1 hour <= Uptime < 24 hours)
*   **Temporal Anomaly Detected! Consider a system reboot for realignment.** (24 hours <= Uptime < 72 hours)
*   **Critical Temporal Instability! Seek immediate system recalibration!** (Uptime >= 72 hours)

## Development

To run tests:

```bash
cargo test
```

To run the utility directly from the source:

```bash
cargo run
```
