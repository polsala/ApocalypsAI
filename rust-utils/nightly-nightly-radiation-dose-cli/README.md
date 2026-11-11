# nightly-radiation-dose-cli

A whimsical CLI tool that estimates radiation dose based on distance, exposure time, and source strength. Useful for post‑apocalyptic scavengers who want to know if a glowing barrel is safe.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
nightly-radiation-dose-cli <distance_m> <time_min> <source_sieverts_per_hr_at_1m>
```

Example:

```sh
nightly-radiation-dose-cli 2.0 30 0.5
```

Outputs estimated dose in sieverts.

## How it works

Uses inverse‑square law: dose_rate = source_strength / distance² (Sv/h). Dose = dose_rate × (time_min / 60).
