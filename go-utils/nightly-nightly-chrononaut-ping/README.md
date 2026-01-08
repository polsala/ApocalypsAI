# nightly-chrononaut-ping

Utility to concurrently ping a list of URLs and report their HTTP status codes as JSON.

## Usage

```sh
go run ./src/main.go https://example.com https://example.org
```

Outputs something like:

```json
{"https://example.com":200,"https://example.org":404}
```

## Build

```sh
go build -o chrononaut-ping ./src/main.go
```

## How it works

Spawns a goroutine per URL, uses `net/http` GET, collects status codes, and prints a JSON object mapping each URL to its HTTP status code.

## Testing

Run the test suite with:

```sh
go test ./tests
```

The tests spin up local HTTP servers to provide deterministic responses, ensuring offline, repeatable verification.
