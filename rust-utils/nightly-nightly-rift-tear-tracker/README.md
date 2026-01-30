# nightly-rift-tear-tracker

A blazingly fast CLI utility written in Rust to track and log temporal rift anomalies. Designed for performance-critical environments where every millisecond counts.

## Features
- Tracks temporal rift events with high precision
- Outputs structured logs for downstream analysis
- Zero-copy parsing and minimal allocations

## Usage

```bash
$ rift-tracker --log-level info
```

## Installation

```bash
$ cargo build --release
$ ./target/release/rift-tracker
```

## Tests

Run tests with:

```bash
$ cargo test
```
