# nightly-quote-mixer-docker

A whimsical Docker container that mixes a motivational quote with an apocalyptic twist. Each run prints a combined quote. Useful for adding flavor to CI logs or terminal greetings.

## Build

```sh
docker build -t nightly-quote-mixer .
```

## Run

```sh
docker run --rm nightly-quote-mixer [N]
```

Optional `N` selects the N‑th quote pair (default 1). The selection is deterministic.

## How it works

The container includes two small quote lists and a Bash script `quote_mixer.sh` that picks the same‑indexed line from each list and prints them together.
