# nightly-void-chronometer

A blazingly fast CLI chronometer utility for precise time measurement, built with Rust.

## Features

- Start/stop stopwatch with sub-millisecond precision
- Set countdown timers with custom durations
- Colorized terminal output
- Cross-platform support

## Installation

Ensure you have Rust installed. Then run:

```bash
cargo build --release
```

The binary will be located at `target/release/void-chronometer`.

## Usage

### Stopwatch Mode

```bash
void-chronometer stopwatch
```

Press `Enter` to start/stop the stopwatch.

### Timer Mode

```bash
void-chronometer timer 5s
```

Supported time units: `ms`, `s`, `m`, `h`.

## Example

```bash
$ void-chronometer timer 1.5s
[Timer] Starting countdown for 1.5s...
[Timer] Time's up!
```
