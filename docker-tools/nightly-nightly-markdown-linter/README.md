# Nightly Markdown Linter

A lightweight Dockerized Markdown linter that checks heading hierarchy, image alt text, and link validity.

## Features
- Validates that heading levels increase by at most one level.
- Ensures all images have non‑empty alt text.
- Performs HTTP HEAD checks on all links and reports broken ones.

## Usage
```bash
# Build the image
docker build -t markdown-linter .

# Run the linter against a Markdown file
# The file is mounted into the container at /data
# Replace /path/to/README.md with the path to your file

docker run --rm -v $(pwd):/data markdown-linter /data/README.md
```

The linter prints a report of any issues found. If no issues are reported, the exit code is 0; otherwise it exits with code 1.

## Development
The source code is written in Go and can be built locally with:
```bash
go build -o markdown-linter
```

Run the tests with:
```bash
go test ./...
```
