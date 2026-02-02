# nightly-void-whispers-affirmations

A lightweight Go service that delivers whimsical, post-apocalyptic affirmations via HTTP.

## Usage

Start the server:

```bash
go run src/main.go
```

Fetch an affirmation:

```bash
curl http://localhost:8080/affirmation
```

## Test

Run tests with:

```bash
go test -v ./tests
```
