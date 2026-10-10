# nightly-rust-sys-info

A whimsical yet useful standalone utility built with Rust. This command-line tool provides a quick and efficient way to gather and display essential system information.

## Features

*   **CPU Information**: Displays CPU model, cores, and frequency.
*   **Memory Usage**: Shows total, free, and used RAM.
*   **Disk Usage**: Lists mounted filesystems, their total size, used space, and mount points.
*   **OS Information**: Provides the operating system name and version.

## Installation

To install, you'll need Rust and Cargo. If you don't have them, install from [rustup.rs](https://rustup.rs/).

```bash
cargo install --git https://github.com/polsala/ApocalypsAI.git --branch main rust-utils/nightly-rust-sys-info
```

Alternatively, you can build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-rust-sys-info
cargo build --release
./target/release/nightly-rust-sys-info
```

## Usage

Run the tool from your terminal:

```bash
nightly-rust-sys-info
```

## Example Output

```
--- System Information ---

OS: Linux 5.15.0-76-generic

CPU:
  Model: Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz
  Cores: 12
  Frequency: 3700 MHz

Memory:
  Total: 32 GB
  Free:  28 GB
  Used:  4 GB

Disk:
  Filesystem: /dev/sda1
  Size:       500 GB
  Used:       150 GB
  Mounted on: /

  Filesystem: tmpfs
  Size:       16 GB
  Used:       0 GB
  Mounted on: /dev/shm

------------------------
```

## Contributing

Contributions are welcome! Please refer to the main ApocalypsAI repository for contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
