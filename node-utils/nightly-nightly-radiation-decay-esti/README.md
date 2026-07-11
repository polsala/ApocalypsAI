# Nightly Radiation Decay Estimator

A whimsical CLI utility that estimates remaining radioactivity of a given isotope after a certain time, using built‑in half‑life data. Perfect for post‑apocalyptic scavengers who need to know if a glowing barrel is still dangerous.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/index.js <isotope> <initial_activity_Bq> <years_elapsed>
```

Example:

```sh
node src/index.js Cs-137 1000 30.17
# => Remaining activity: 500.00 Bq
```

## Supported isotopes

- I-131 (8 days)
- Cs-137 (30.17 years)
- U-235 (7.04e8 years)

## License

MIT
