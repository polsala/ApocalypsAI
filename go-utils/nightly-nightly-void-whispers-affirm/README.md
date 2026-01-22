# nightly-void-whispers-affirmations

A lightweight Go service that delivers whimsical, void-themed affirmations via HTTP.

## Features

- Serves a random affirmation on request
- Optional void-themed styling via query parameter
- Lightweight and fast

## Usage

Start the server:

```bash
go run src/main.go
```

Fetch an affirmation:

```bash
curl http://localhost:8080/affirmation
```

Fetch with void styling:

```bash
curl http://localhost:8080/affirmation?void=true
```

## Tests

Run tests:

```bash
go test -v ./tests
```
