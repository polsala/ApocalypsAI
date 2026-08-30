# Nightly Docker Emoji Survival Tip

A whimsical yet useful utility that prints a random post‑apocalypse survival tip, each prefixed with an appropriate emoji.  The whole thing lives inside a tiny Docker container, so you can run it anywhere Docker is available.

## How it works

* The container is built from Alpine Linux.
* A small Bash script (`src/tip.sh`) holds a list of emojis and matching survival tips.
* When the container starts, the script selects an entry (randomly, or deterministically when the `SEED` environment variable is set) and prints it to stdout.

## Build the image

```bash
docker build -t emoji-survival .
```

## Run the container

```bash
# Random tip (uses Bash's $RANDOM)
docker run --rm emoji-survival

# Deterministic tip – useful for testing or reproducible outputs
docker run --rm -e SEED=42 emoji-survival
```

## Example output

```
🛡️ Keep a spare set of spare parts for your generator.
```

## Testing

The repository includes a Python test (`tests/test_tip.py`) that runs the script directly (bypassing Docker) with a fixed seed and checks that the output matches the expected pattern.

---

*Feel free to pull, tweak the tip list, or embed the container in your own automation pipelines!*
