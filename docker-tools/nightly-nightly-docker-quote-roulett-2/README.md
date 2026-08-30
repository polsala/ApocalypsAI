# nightly-docker-quote-roulette

A whimsical Docker container that prints a random quote (or a specific one) each time it starts. Useful for adding a splash of inspiration to CI logs or terminal sessions.

## Usage

```sh
docker build -t quote-roulette .
# Print a random quote
docker run --rm quote-roulette
# Print a deterministic quote (index is zero‑based)
docker run --rm -e QUOTE_INDEX=0 quote-roulette
```

Set `QUOTE_INDEX` to select a specific quote. Omit the variable to get a random quote.

## How it works

The container runs a tiny Bash script that holds an array of quotes and echoes one based on the environment variable `QUOTE_INDEX`. If the index is out of bounds, the script falls back to the first quote.
