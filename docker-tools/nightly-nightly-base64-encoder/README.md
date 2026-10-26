# nightly-base64-encoder

A minimal utility that reads data from **stdin**, encodes it to Base64, and writes the result to **stdout**. The tool is implemented in Go (standard library only) and distributed as a lightweight Docker image.

## Features
- Zero‑dependency Go binary (standard library only)
- Multi‑stage Docker build for a tiny final image (~5 MB)
- Works with any data stream (text, binary, files via redirection)

## Build the Docker image
```sh
docker build -t nightly-base64-encoder .
```

## Run the encoder
```sh
# Encode a short string
echo -n "hello world" | docker run -i nightly-base64-encoder
# => aGVsbG8gd29ybGQ=

# Encode a file
cat myfile.bin | docker run -i nightly-base64-encoder > myfile.b64
```

## Run the binary directly (without Docker)
```sh
# Build the Go binary
go build -o encoder src/main.go

# Use it
echo -n "test" | ./encoder
```

## Testing
The repository includes a Go test suite that validates the core encoding function.
```sh
go test ./tests
```
