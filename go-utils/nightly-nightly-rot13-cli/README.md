# nightly-rot13-cli

A tiny Go command‑line utility that applies the classic ROT13 cipher to any text. Perfect for secret messages, post‑apocalyptic notes, or just a bit of fun.

## Features

- Accepts input via command‑line arguments or STDIN.
- Works with Unicode letters (preserves case).
- No external dependencies; pure Go standard library.

## Installation

```sh
go build -o nightly-rot13-cli ./src/main.go
```

## Usage

```sh
# Encode a string
./nightly-rot13-cli "Hello, World!"
# => Uryyb, Jbeyq!

# Decode (ROT13 is symmetric)
echo "Uryyb, Jbeyq!" | ./nightly-rot13-cli
# => Hello, World!
```

## Testing

```sh
go test ./...
```

## License

MIT
