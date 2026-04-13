# nightly-rust-sys-info

A whimsical yet useful standalone utility built with Rust. This CLI tool provides a quick and efficient way to display essential system information.

## Features

*   Displays CPU information (cores, architecture).
*   Shows RAM usage (total, available, used).
*   Lists disk usage for mounted filesystems.
*   Provides network interface details.

## Installation

Ensure you have Rust and Cargo installed.

1.  Clone this repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```

2.  Navigate to the utility's directory:
    ```bash
    cd rust-utils/nightly-rust-sys-info
    ```

3.  Build the project:
    ```bash
    cargo build --release
    ```

4.  The executable will be located at `target/release/nightly-rust-sys-info`.

## Usage

Run the tool from your terminal:

```bash
./target/release/nightly-rust-sys-info
```

## Example Output

```
System Information:
-------------------
CPU:
  Cores: 8
  Architecture: x86_64

Memory:
  Total: 16.00 GiB
  Available: 12.50 GiB
  Used: 3.50 GiB

Disk Usage:
  /: 100.50 GiB / 250.00 GiB (40.2%)
  /home: 50.20 GiB / 100.00 GiB (50.2%)

Network Interfaces:
  eth0: UP, 192.168.1.100/24
  lo: UP, 127.0.0.1/8
-------------------
```

## Testing

Run the tests using Cargo:

```bash
cargo test
```
