# nightly-emoji-encoder

Encode plain text into a whimsical sequence of emojis.

## Usage

```sh
# Encode a string passed as arguments
go run ./src/main.go "Hello World"

# Or pipe input via stdin
echo "Hello" | go run ./src/main.go
```

## Build

```sh
go build -o emoji-encoder ./src/main.go
```

## How it works

The tool maps letters, digits and space to a predefined set of emojis. Unknown characters are replaced with the ❓ emoji.
