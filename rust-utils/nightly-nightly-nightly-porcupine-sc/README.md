Nightly Porcupine Port Scan
=========================
A whimsical yet useful concurrent port scanner written in Rust. It scans a range of TCP ports on a given host and reports which ports are open.

Usage
-----
```bash
cargo run --release -- 127.0.0.1 8000 8010
```
The program will output a list of open ports in the specified range.

Features
--------
- Concurrent scanning with a configurable concurrency limit.
- Simple command‑line interface.
- No external dependencies.

Installation
------------
```bash
cargo install nightly-nightly-porcupine-scan
```

Testing
-------
Run the test suite with `cargo test`.
