# Apocalypse Tips Docker Utility

A whimsical Docker container that prints a random post‑apocalyptic survival tip each time it runs.

## Usage

```sh
# Build the image
docker build -t apocalypse-tips .

# Run the container
docker run --rm apocalypse-tips
```

You can also run the compiled binary directly (requires Go):

```sh
go run src/main.go
```

## How it works

The container builds a tiny Go program that selects a tip from an embedded list at random and prints it to stdout.
