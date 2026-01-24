# nightly-echo-echo

A whimsical Rust CLI that echoes input reversed and reports its length.

## Usage

```bash
cargo run -- <text>
```

Example:

```bash
$ cargo run -- hello
olleh (5 chars)
```

The utility is useful for quick string manipulation and debugging.

## Build

```bash
cargo build --release
```

The binary will be at `target/release/nightly-echo-echo`.

## Tests

Run `cargo test` to execute the unit tests.
