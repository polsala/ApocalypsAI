# Nightly Barter Price Estimator

A tiny Rust command‑line utility that gives you a deterministic "barter price" (in caps) for common post‑apocalypse items.  The price is calculated from a hard‑coded base value plus a deterministic modifier derived from the item name, so the same input always yields the same output – perfect for offline testing and fun role‑playing.

## Build
```bash
# Requires Rust toolchain (rustc, cargo)
cargo build --release
```

The binary will be placed at `target/release/nightly-barter-price-estimator`.

## Usage
```bash
nightly-barter-price-estimator <item-name>
```
Example:
```bash
$ nightly-barter-price-estimator water
Estimated barter price for 'water' is 12 caps
```

### Known items
- `water`
- `canned-food`
- `medicine`
- `ammo`
- `fuel`
- `scrap-metal`

If an unknown item is supplied, the program exits with an error and lists the known items.

## Testing
```bash
cargo test
```
All tests are deterministic and run offline.
