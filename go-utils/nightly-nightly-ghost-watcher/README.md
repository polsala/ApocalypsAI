# nightly-ghost-watcher

A whimsical Go CLI that watches a directory and prints a playful ghost message whenever a new file appears.

## Usage

```bash
go run . /path/to/watch
```

The program will poll the directory every 500ms and output:

```
👻 A new ghost has appeared: <filename>
```

## Features

- Simple polling-based watcher (no external dependencies)
- Thread-safe and concurrent
- Easy to embed in scripts or CI pipelines

## Testing

Run `go test ./...` to execute the deterministic tests.
