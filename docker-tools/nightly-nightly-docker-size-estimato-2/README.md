# nightly-docker-size-estimator

Estimate the size of a Docker image from its Dockerfile without building it.

## Overview

The tool parses a Dockerfile, looks up the base image size from a small built‑in table and adds heuristic sizes for each `RUN`, `COPY` and `ADD` instruction. The result is an approximate size in megabytes (MB).

## Usage

```sh
# Build the estimator container
docker build -t size-estimator .

# Run it against a Dockerfile in the current directory
docker run --rm -v $(pwd)/Dockerfile:/Dockerfile size-estimator /Dockerfile
```

Or run locally with Python:

```sh
python -m src.size_estimator path/to/Dockerfile
```

## Example

Given a Dockerfile:

```
FROM python:3.11-slim
COPY . /app
RUN pip install -r requirements.txt
```

The estimator might output:

```
Estimated image size: 115 MB
```

## Limitations

- Only a few common base images are known.
- Heuristics are coarse; real size may differ.
