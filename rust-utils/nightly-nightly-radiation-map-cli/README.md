# Radiation Map CLI

A tiny Rust command‑line tool that reads a CSV file of locations and radiation levels and prints a colored summary table. Useful for post‑apocalypse scavengers to quickly assess safe zones.

## Usage

```sh
radiomap <path-to-csv>
```

CSV format: `location,level` where level is a floating point number (µSv/h).

Example:

```csv
Vault,0.02
Wasteland,3.5
Radiated City,12.7
```

The tool will display each location with a color: green (≤1), yellow (1‑5), red (>5).

## Installation

```sh
cargo install --path .
```

## License

MIT
