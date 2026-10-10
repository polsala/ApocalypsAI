# nightly-decay-calculator

A whimsical Node.js CLI that calculates the remaining activity of a radioactive material after a given elapsed time using its half‑life. Perfect for scavengers, scientists, and anyone curious about how long the glow will last in the wasteland.

## Installation

```sh
npm install -g nightly-decay-calculator
```

## Usage

```sh
decay <initial_activity> <half_life> <elapsed_time>
```

- `initial_activity` – initial activity in becquerels (Bq)
- `half_life` – half‑life of the isotope in years
- `elapsed_time` – time elapsed in years

Example:

```sh
decay 1000 30 90
```

Outputs:

```
After 90 years, activity drops from 1000 Bq to 125.00 Bq.
The wasteland is still mildly glowing.
```

## How it works

Uses the exponential decay formula:

```
A = A0 * (0.5)^(t / T½)
```

## License

MIT
