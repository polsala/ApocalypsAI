# nightly-docker-survival-tip

A whimsical Docker container that prints a random post‑apocalyptic survival tip each time it runs. Useful for a quick morale boost in terminal sessions.

## Usage

```sh
docker build -t survival-tip .
docker run --rm survival-tip          # prints a random tip
docker run --rm survival-tip 2        # prints the tip with index 2 (deterministic)
```

## How it works

The container is based on Alpine Linux and runs a small Bash script that stores a handful of tongue‑in‑cheek tips. If an argument is supplied, the script prints the tip at that index, making testing deterministic.

## Adding tips

Edit `src/tip.sh` and append new entries to the `tips` array.
