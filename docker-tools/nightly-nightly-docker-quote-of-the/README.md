nightly-docker-quote-of-the-day

A tiny Dockerized utility that prints a random quote from a curated list each time it runs.

Usage

docker run --rm ghcr.io/your-org/nightly-docker-quote-of-the-day

You can also specify a deterministic quote by setting the QUOTE_INDEX environment variable:

docker run --rm -e QUOTE_INDEX=3 ghcr.io/your-org/nightly-docker-quote-of-the-day

The index is zero‑based and wraps around if out of range.

Building locally

docker build -t nightly-docker-quote-of-the-day .

License

MIT
