# nightly-carbon-footprint-cli

Estimate CO2 emissions for a travel leg.

## Usage

```sh
node src/main.js <distance_km> <mode>
```

- `<distance_km>`: distance in kilometers (non‑negative number)
- `<mode>`: one of `car`, `bus`, `train`, `plane`

The script prints the estimated CO2 emission in kilograms.

### Example

```sh
$ node src/main.js 100 car
Estimated CO2 emission: 21.0 kg
```

## How it works

A simple table of emission factors (kg CO₂ per km) is used:

- `car`: 0.21
- `bus`: 0.105
- `train`: 0.041
- `plane`: 0.254

The emission is calculated as `distance * factor` and rounded to one decimal place.

## Tests

Run the test suite with:

```sh
node tests/test_main.js
```

All tests should pass, confirming correct calculations and error handling.
