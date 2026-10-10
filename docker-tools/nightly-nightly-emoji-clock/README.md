# nightly-emoji-clock

A Docker container that prints a random whimsical post‑apocalyptic emoji‑filled message each time it runs.

## Usage

```sh
docker build -t nightly-emoji-clock .
Docker run --rm nightly-emoji-clock
```

Each execution will output one of several quirky messages, perfect for a quick morale boost in the wasteland.

## How it works

The container is based on Alpine Linux and runs a tiny shell script (`entrypoint.sh`) that selects a random message from a hard‑coded list and prints it.

## Testing

Run the unit tests with:

```sh
python -m unittest discover -s tests
```

The tests mock Docker commands to verify that the build and run steps succeed and that the output matches one of the expected messages.
