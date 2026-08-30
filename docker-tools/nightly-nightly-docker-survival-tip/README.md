# nightly-docker-survival-tip

## Overview
A minimal Docker image that prints a whimsical survival tip when run. Useful for a quick morale boost in terminal sessions.

## Usage
```sh
docker run --rm ghcr.io/your-repo/nightly-docker-survival-tip
```
You can select a specific tip with the `TIP_INDEX` environment variable (0‑based):
```sh
docker run --rm -e TIP_INDEX=2 ghcr.io/your-repo/nightly-docker-survival-tip
```

## Tips
- Always carry a rubber duck for debugging; it listens better than humans.
- When in doubt, add more coffee. It fuels both code and courage.
- A well‑placed meme can defuse even the most critical merge conflict.
- Never underestimate the power of a well‑timed break; it resets the apocalypse clock.
- If all else fails, blame the build server – it loves the attention.

## Building locally
```sh
docker build -t nightly-docker-survival-tip .
```
