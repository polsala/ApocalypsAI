# nightly-dockerfile-size-estimator

Utility that estimates the size of a Docker image based on its Dockerfile without building it. It uses simple heuristics: each `RUN` instruction adds ~50 MB, each `COPY` or `ADD` adds ~5 MB per file, and the base image size is approximated from a tiny lookup table (e.g., `python:3.11-slim` → 30 MB). The tool runs inside a lightweight Docker container.

## Usage

```sh
# Build the estimator image
docker build -t dsize .

# Run the estimator against a Dockerfile in the current directory
docker run --rm -v $(pwd):/workspace dsize /workspace/Dockerfile
```

The command prints the estimated size in megabytes, e.g.:

```
Estimated image size: 140 MB
```

## How it works

The script parses the Dockerfile, counts relevant instructions, looks up the base image size (a small built‑in table), and applies the heuristics described above.

## Testing

Run the unit tests with:

```sh
python -m unittest discover -s tests
```

The tests are deterministic and do not require network access.
