# Nightly Docker Quote Mixer

A whimsical Dockerized Go CLI that blends a quote about ambition with a quote about chaos, producing a mash‑up each run.

## Build

```sh
docker build -t nightly-quote-mixer .
```

## Run

```sh
docker run --rm nightly-quote-mixer
```

Example output:

```
Fortune favors the bold. — All that glitters is not gold.
```

## How it works

The image contains a tiny Go program that reads two quote files, picks the second line from each (deterministic), and prints them joined by an em dash.
