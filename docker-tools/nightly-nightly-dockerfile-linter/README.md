# Dockerfile Linter

A tiny Docker image that checks Dockerfiles for common pitfalls such as using the `latest` tag, missing `LABEL maintainer`, or running as root. It prints warnings to help you improve your images before building.

## Usage

```sh
# Build the linter image
docker build -t dockerfile-linter .

# Lint a Dockerfile
docker run --rm -v $(pwd)/Dockerfile:/Dockerfile dockerfile-linter /Dockerfile
```

## What it checks

- Avoid `FROM ...:latest`
- Presence of a `LABEL maintainer="..."` instruction
- Whether the Dockerfile switches away from the root user (`USER`)

## Exit codes

- `0` – No issues found
- `1` – One or more warnings detected
