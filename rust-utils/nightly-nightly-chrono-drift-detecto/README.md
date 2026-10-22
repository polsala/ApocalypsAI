# Nightly Chrono-Drift Detector

## Overview

The Nightly Chrono-Drift Detector is a high-performance Rust CLI tool designed to monitor the subtle (and sometimes not-so-subtle) temporal anomalies affecting your system's internal chronometer. In the post-apocalyptic landscape, precise timekeeping is paramount, whether for coordinating scavenger runs, synchronizing defense protocols, or simply knowing when the next temporal echo might ripple through reality.

This utility queries a designated Network Time Protocol (NTP) server, compares its cosmic chronometer reading with your local chrono-oscillator, and reports any detected temporal drift. It then offers whimsical insights into the stability of the spacetime fabric and suggests recalibration protocols to keep your system perfectly aligned with the universal pulse.

## Features

*   **Precise Drift Detection**: Utilizes NTP to accurately measure the offset between local and network time.
*   **Whimsical Reporting**: Provides status updates on the 'fabric of spacetime' and 'chronal currents'.
*   **Recalibration Suggestions**: Offers guidance on how to correct significant temporal anomalies.
*   **High Performance**: Built with Rust for speed and reliability, ensuring your temporal diagnostics are swift and accurate.

## Installation & Usage

### Prerequisites

*   Rust toolchain (latest stable recommended)

### Build from Source

1.  Clone the ApocalypsAI repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```
2.  Navigate to the utility directory:
    ```bash
    cd rust-utils/nightly-chrono-drift-detector
    ```
3.  Build the project:
    ```bash
    cargo build --release
    ```
4.  The executable will be located at `target/release/nightly-chrono-drift-detector`.

### Run the Detector

```bash
./target/release/nightly-chrono-drift-detector [OPTIONS]
```

**Options:**

*   `-s, --server <NTP_SERVER>`: Specify the NTP server to query (default: `pool.ntp.org`).
*   `-t, --timeout <SECONDS>`: Set the timeout for the NTP query in seconds (default: `5`).

**Examples:**

*   **Default check:**
    ```bash
    ./target/release/nightly-chrono-drift-detector
    ```
*   **Check against a specific server with a longer timeout:**
    ```bash
    ./target/release/nightly-chrono-drift-detector --server time.google.com --timeout 10
    ```

## Recalibration Protocol

If significant drift is detected, consider using your system's time synchronization tools. Common commands include:

*   **Linux (using `ntpdate` - may need to install):**
    ```bash
    sudo ntpdate -s pool.ntp.org
    ```
*   **Linux (using `timedatectl` for systemd-based systems):**
    ```bash
    sudo timedatectl set-ntp true
    sudo timedatectl status
    ```
*   **Windows (from an elevated command prompt):**
    ```cmd
    w32tm /config /syncfromflags:manual /manualpeerlist:pool.ntp.org
    w32tm /config /update
    w32tm /resync
    ```

Always exercise caution when modifying system time settings.

## Contributing

Temporal stability is a collective effort! Feel free to contribute to the Nightly Chrono-Drift Detector by submitting issues or pull requests.
