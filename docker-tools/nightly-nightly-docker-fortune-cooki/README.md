# nightly-docker-fortune-cookie

A whimsical Docker utility that prints a random fortune cookie message each time it runs. Perfect for a quick morale boost in the apocalypse.

## Build

```sh
docker build -t fortune-cookie .
```

## Run

```sh
docker run --rm fortune-cookie
```

Will output one of several pre‑written fortunes.

## How it works

The container is based on Alpine Linux and runs a tiny Bash script that selects a random line from an internal list.

## Testing

Run the test suite with:

```sh
bash tests/test_fortune.sh
```
