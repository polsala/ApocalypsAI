# Nightly Emoji Logger

Adds a whimsical emoji prefix to each log line for fun readability.

## Usage

```bash
# From source
go run src/main.go path/to/logfile

# Or build
go build -o emoji-logger src/main.go
./emoji-logger path/to/logfile

# If no file is provided, reads from stdin
cat logfile | ./emoji-logger
```

The utility cycles through a predefined set of emojis, assigning one to each line in order.

## Testing

Run `go test ./...` to execute the bundled tests.

