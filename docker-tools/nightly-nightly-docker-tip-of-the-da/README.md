# nightly-docker-tip-of-the-day

A tiny Docker container that prints a whimsical post‑apocalyptic tip of the day.

## Usage

```sh
docker build -t tip .
 docker run --rm tip
```

Each run prints a random tip such as "Remember to ration your canned beans.".

## How it works

The container is based on Python 3.11 Alpine, copies `src/tip.py` and sets it as the entrypoint.
