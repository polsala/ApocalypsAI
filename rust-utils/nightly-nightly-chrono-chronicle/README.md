# nightly-chrono-chronicle

**nightly-chrono-chronicle** is a tiny Rust CLI that takes a date (YYYY‑MM‑DD) and spits out a deterministic, whimsical apocalyptic event for that day.  The output is based on a simple hash of the date, so the same date always yields the same event.

## Usage
```bash
# Build the binary (requires Rust toolchain)
cargo build --release

# Run the tool with a date argument
./target/release/chrono-chronicle 2023-01-01
```

The program will print a single line, e.g.:
```
Radioactive rain sang lullabies
```

## How it works
1. The date string is summed byte‑wise.
2. The sum modulo the number of predefined events selects an entry.
3. The selected event is printed.

Because the algorithm is deterministic, you can rely on the same date always producing the same event, which makes testing straightforward.

## Adding new events
Edit the `EVENTS` array in `src/main.rs` and re‑compile.
