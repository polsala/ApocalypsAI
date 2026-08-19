# nightly-moon-phase-notifier

A whimsical Bash utility that tells you the current (or specified) moon phase with a cute ASCII illustration. Perfect for terminal enthusiasts who want a touch of lunar magic in their workflow.

## Usage

```sh
# Use the system date (default)
./src/moon_notifier.sh

# Or specify a date (YYYY-MM-DD) via MOON_DATE environment variable
MOON_DATE=2023-09-29 ./src/moon_notifier.sh
```

The script outputs the phase name and an ASCII art representation.

## How it works

- Calculates days since a known new‑moon reference (2000‑01‑06).
- Uses the average lunar month (29.53 days) to determine the phase.
- Maps the phase to one of eight common names and corresponding ASCII art.

## Testing

Run the test suite:

```sh
./tests/test_moon_notifier.sh
```
