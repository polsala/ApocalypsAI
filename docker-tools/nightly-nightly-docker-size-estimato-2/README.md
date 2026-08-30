# nightly-docker-size-estimator

Estimates the size of a Docker image from a Dockerfile using a tiny heuristic lookup. Useful for quick sanity checks before building large images.

## Usage

```sh
docker run --rm -v $(pwd)/Dockerfile:/Dockerfile \
    nightly-docker-size-estimator /Dockerfile
```

The tool prints the estimated size in MB.

## How it works

- Looks up the base image size from a built‑in table.
- Adds 10 MB for each `RUN` instruction.
- Adds 1 MB for each `COPY` or `ADD` instruction.
- Returns the sum.

## Example

Given a Dockerfile:

```Dockerfile
FROM alpine:3.18
RUN apk add --no-cache curl
COPY . /app
RUN echo "done"
```

The estimator outputs `26 MB`.

## Building the estimator image

```sh
docker build -t nightly-docker-size-estimator .
```
