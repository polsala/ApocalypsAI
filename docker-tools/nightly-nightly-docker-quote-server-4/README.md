# Nightly Docker Quote Server

A whimsical Dockerized Go HTTP service that returns a random quote.

## Usage

```sh
docker build -t nightly-quote-server .
docker run -p 8080:8080 nightly-quote-server
```

Then request a quote:

```sh
curl http://localhost:8080/quote
```

Typical response:

```json
{"quote":"The early bird gets the worm, but the second mouse gets the cheese."}
```

## How it works

The server picks a random quote from an embedded list each time `/quote` is requested. No external dependencies, perfect for quick morale boosts in CI pipelines or local dev sessions.
