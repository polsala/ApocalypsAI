# Whimsical Quote of the Day

A lightweight, zero‑dependency utility that prints a fun, deterministic quote for the current day. The quote is chosen from a short, curated list and is **deterministic** – the same date always yields the same quote, making it perfect for scripts, dashboards, or just a daily smile.

## Features

- **Deterministic**: Uses ISO week number and weekday to select a quote, so the output is repeatable for any given date.
- **Offline**: No network access; all data lives in the repository.
- **CLI**: Simple command‑line interface with optional `--date` override for testing.
- **Tested**: Includes deterministic unit tests that mock dates.

## Installation

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI

# Navigate to the utility
cd utils/whimsical-quote-of-the-day

# (Optional) Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Run the utility
python -m src.quote
```

## Usage

```bash
# Print today's quote
python -m src.quote

# Override the date (useful for scripting or testing)
python -m src.quote --date 2023-01-02
```

## Development & Testing

```bash
# Run the test suite
python -m unittest discover -s tests
```

The tests are deterministic and do not require any external resources.
