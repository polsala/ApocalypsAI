# nightly-future-timestamp

A tiny, whimsical yet useful command‑line utility written in Rust.

## What it does

`nightly-future-timestamp` takes a single *duration* argument (e.g. `2d5h30m`) and prints the ISO‑8601 timestamp that will occur after adding that duration to the current UTC time.

The duration syntax supports:

- `d` – days
- `h` – hours
- `m` – minutes
- `s` – seconds

The components can appear in any order and are optional, but at least one must be present. Examples:

```
$ nightly-future-timestamp 1h
2023-09-15T14:23:45Z

$ nightly-future-timestamp 2d5h30m
2023-09-17T19:53:45Z
```

## Installation

```bash
# Clone the repository (or copy the generated folder) and build
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-future-timestamp
cargo build --release
# The binary will be at target/release/nightly-future-timestamp
```

## Usage

```bash
nightly-future-timestamp <duration>
```

If the argument cannot be parsed, the program exits with a non‑zero status and prints an error message.

## Testing

Run the built‑in test suite with:

```bash
cargo test
```

The tests are deterministic and do not depend on the actual current time.
