# nightly‑battery‑life‑estimator

A tiny, self‑contained Rust command‑line tool that calculates how many hours a battery will last given its capacity (mAh) and the device's average draw (mA).  For a bit of fun it also offers an *apocalypse mode* that applies a random‑looking degradation factor (deterministic for testing).

## Build & Run

```bash
# Build the binary (requires Rust toolchain)
cargo build --release

# Run the tool
./target/release/nightly-battery-life-estimator <capacity_mAh> <draw_mA> [--apocalypse]
```

### Example

```bash
$ ./target/release/nightly-battery-life-estimator 5000 250
Estimated runtime: 20.00 hours
```

With apocalypse mode:

```bash
$ ./target/release/nightly-battery-life-estimator 5000 250 --apocalypse
Estimated runtime (apocalypse mode): 15.00 hours
```

## How It Works

The tool simply computes:

```
hours = capacity_mAh / draw_mA
```

If `--apocalypse` is supplied, the result is multiplied by a deterministic factor of `0.75` to simulate harsh conditions.

## Testing

Run the test suite with:

```bash
cargo test
```

All tests are deterministic and require no external resources.
