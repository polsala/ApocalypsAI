# nightly-fallout-time-cli

Convert ISO 8601 timestamps into a whimsical Fallout‑style calendar format.

## Usage

```sh
cargo run --release -- <ISO8601-timestamp>
```

Example:

```sh
$ cargo run -- 2023-08-15T14:23:00Z
Day 19684, 14:23 after the fallout
```

## Build

```sh
cargo build --release
```

## Testing

```sh
cargo test
```
