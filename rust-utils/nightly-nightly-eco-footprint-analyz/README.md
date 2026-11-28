# Eco Footprint Analyzer

Estimates CO₂ emissions from a CSV file.

## Usage

```sh
eco-footprint-analyzer path/to/activities.csv
```

CSV format: `activity,co2_kg` (header required). Example:

```
activity,co2_kg

driving,2.5

eating_beef,3.0
```

The tool prints the total CO₂ in kilograms.

## Build

```sh
cargo build --release
```

## Test

```sh
cargo test
```
