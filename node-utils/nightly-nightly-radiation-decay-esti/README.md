# Nightly Radiation Decay Estimator

A tiny, self‑contained Node.js utility that tells you how much of a radioactive isotope is left after a given number of years.

## Features
- Built‑in half‑life data for a few classic isotopes (C‑14, U‑238, I‑131).
- Simple CLI: `node src/main.js --isotope C-14 --years 5730`
- Exported `computeDecay(isotope, years)` function for programmatic use and testing.

## Installation
No external dependencies are required. Just clone the repository and run the script with Node ≥12.

```bash
node src/main.js --isotope C-14 --years 5730
```

## Example Output
```
Remaining activity of C-14 after 5730 years: 0.5
```

## Testing
Run the bundled tests with:
```bash
node tests/test_main.js
```
All tests should pass and print `All tests passed`.

## Extending
Add new isotopes by editing the `HALF_LIVES` object in `src/main.js`.
