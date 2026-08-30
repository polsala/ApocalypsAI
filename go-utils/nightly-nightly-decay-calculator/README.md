# Nightly Decay Calculator

**Utility name:** `nightly-decay-calculator`

## Overview

`nightly-decay-calculator` is a small, self‑contained Go command‑line tool that calculates how much of a radioactive material remains after a certain amount of time, based on its half‑life. It is useful for anyone who wants a quick, offline estimate of radioactive decay without pulling in heavy scientific libraries.

## Installation

```bash
# Clone the repository (or copy the utility folder into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/go-utils/nightly-decay-calculator

# Build the binary
go build -o decaycalc ./src/main.go
```

The binary `decaycalc` will be created in the current directory.

## Usage

```bash
./decaycalc -initial <initial_amount> -half-life <half_life> -time <elapsed_time>
```

- `-initial`   : Initial amount of the substance (any unit, e.g., grams).
- `-half-life` : Half‑life of the substance in the same time unit you will use for `-time`.
- `-time`      : Elapsed time since the start of the decay.

### Example

```bash
# 100 grams of a material with a half‑life of 30 years, after 90 years:
./decaycalc -initial 100 -half-life 30 -time 90
```

Output:
```
Remaining amount after 90.00 units of time: 12.50 (same unit as initial)
```

## How it works

The tool uses the classic exponential decay formula:

```
remaining = initial * 0.5^(time / half_life)
```

All calculations are performed with `float64` precision.

## Testing

Run the unit tests with:

```bash
go test ./tests
```

The test suite covers a few typical scenarios and edge cases.

## License

This utility is released under the MIT License.
