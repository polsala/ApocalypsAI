# Docker Image Size Estimator

Estimates the size of a Docker image from its Dockerfile without actually building the image.

## Usage

```sh
docker build -t size-estimator .
docker run --rm -v $(pwd)/Dockerfile:/Dockerfile size-estimator /Dockerfile
```

The tool will output an estimated size like `16MB`.

## How it works

- Looks up a hard‑coded size for the base image.
- Adds 10 MB for each `RUN` instruction.
- Adds 1 MB for each `COPY` or `ADD` instruction.

The heuristics are simple but give a quick ballpark.
