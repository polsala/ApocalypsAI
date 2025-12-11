# nightly-fallout-distance-estimator

A tiny Rust CLI that helps post‑apocalypse survivors (or curious scientists) calculate the **minimum safe distance** from a nuclear fallout source after a given amount of time.

## What it does

- Takes an initial radiation level at 1 km (in Sv/h).
- Applies the inverse‑square law to model how radiation drops with distance.
- Applies exponential decay based on the isotope’s half‑life.
- Returns the smallest distance (in km) where the radiation falls below a user‑defined safety threshold (default 0.001 Sv/h).

## Installation

```bash
# Clone the repository (or copy the generated folder) and build
git clone https://github.com/polsala/ApocalypsAI.git
cd rust-utils/nightly-fallout-distance-estimator
cargo build --release
```

The binary will be at `target/release/fallout-distance-estimator`.

## Usage

```bash
fallout-distance-estimator \
    --initial 5.0        # initial Sv/h at 1 km
    --half-life 8.0      # half‑life in hours
    --time 24            # hours elapsed since the event
    --threshold 0.001    # safety threshold (Sv/h) – optional
```

The program prints something like:

```
Safe distance: 3.42 km (radiation = 0.001 Sv/h)
```

## How it works

Radiation at distance `d` after time `t` is approximated by:

```
R(d, t) = R0 * (1 / d²) * 0.5^(t / half_life)
```

where `R0` is the initial radiation at 1 km. The tool solves for `d` such that `R(d, t) <= threshold`.

## Testing

Run the test suite with:

```bash
cargo test
```

All tests are deterministic and do not require external resources.

## License

MIT © ApocalypsAI community
