# Moon Phase Predictor

**Utility name:** `nightly-moon-phase-predictor`

## What it does

`moon-phase-predictor` computes the lunar phase (e.g., *New Moon*, *First Quarter*, *Full Moon*, *Last Quarter*, etc.) for a supplied date. It is completely offline, deterministic, and requires only the Python standard library.

## Usage

```bash
# Install (no extra dependencies needed)
python -m venv .venv && source .venv/bin/activate
pip install -e utils/nightly-moon-phase-predictor

# Run the CLI (defaults to today)
python -m moon_phase_predictor

# Specify a date (ISO format)
python -m moon_phase_predictor 2023-02-05
```

The script prints a human‑readable description, e.g.:
```
2023-02-05 → Full Moon
```

## How it works

The implementation uses a simple version of Conway’s algorithm to approximate the Moon’s age in days and maps that age to one of eight named phases.

## Testing

Run the test suite with:
```bash
python -m pytest utils/nightly-moon-phase-predictor/utils/moon-phase-predictor/tests
```
All tests are deterministic and offline.
