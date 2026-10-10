# nightly-chrono-delta-humanizer

Utility that takes two ISO8601 timestamps and prints the human‑readable difference (days, hours, minutes, seconds).

## Usage

```bash
cargo run -- <START_ISO> <END_ISO>
```

Example:

```bash
cargo run -- 2023-01-01T00:00:00Z 2023-01-02T03:04:05Z
```

Output:
```
1 day, 3 hours, 4 minutes, 5 seconds
```

## Building

```bash
cargo build --release
```

## Testing

```bash
cargo test
```
