# Nightly Quote Mixer Docker

A whimsical Docker container that prints a mixed quote when run. It combines an inspirational quote with an apocalyptic twist.

## Usage

```sh
docker run --rm ghcr.io/yourrepo/nightly-quote-mixer
```

You can also specify a specific quote index for reproducible output:

```sh
docker run --rm -e QUOTE_INDEX=2 ghcr.io/yourrepo/nightly-quote-mixer
```

## How it works

The container is based on Alpine Linux and runs a tiny shell script that selects a quote from an embedded list.
