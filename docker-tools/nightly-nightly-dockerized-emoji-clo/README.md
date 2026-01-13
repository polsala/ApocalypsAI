# Nightly Dockerized Emoji Clock

A whimsical utility that prints the current time as an emoji clock face.

## Features
- Prints a single emoji representing the current hour (12‑hour clock).
- Override the time with the `TIME` environment variable in `HH:MM` 24‑hour format (useful for testing).
- Packaged as a minimal Docker image (Python 3.11 slim).

## Usage
```bash
# Build the image
docker build -t emoji-clock .

# Run – prints the emoji for the current system time
docker run --rm emoji-clock

# Run with a custom time (e.g., 14:30)
docker run --rm -e TIME=14:30 emoji-clock
```

The above command will output `🕑` (2 o’clock).

## Implementation Details
- The core logic lives in `src/emoji_clock.py`.
- The Dockerfile uses the official `python:3.11-slim` base image, copies the script, and sets it as the entrypoint.

## Testing
Run the unit tests locally (no Docker required):
```bash
python -m unittest discover -s tests
```

The tests cover the hour‑to‑emoji mapping and the `TIME` environment variable handling.
