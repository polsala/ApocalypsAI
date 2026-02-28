# nightly-chaos-monkey-rust

A blazingly fast chaos engineering CLI tool written in Rust. It randomly kills processes to simulate failures and test system robustness.

## Features

- Kill random processes by name or PID
- Configurable intensity and duration
- Dry-run mode for safety
- Colored terminal output

## Usage

```bash
# Kill random 'node' processes every 5 seconds for 60s
chaos-monkey --target node --interval 5 --duration 60

# Dry run to preview targets
chaos-monkey --target nginx --dry-run
```

## Installation

```bash
cargo build --release
sudo cp target/release/chaos-monkey /usr/local/bin/
```

## Safety

⚠️ This tool can terminate processes. Always use `--dry-run` first and run with caution in production environments.
