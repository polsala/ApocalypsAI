# nightly-rot13-base64-encoder

Utility that takes a string (argument or stdin), applies ROT13 cipher, then Base64 encodes the result. Handy for quick obfuscation or encoding pipelines.

## Usage

```sh
# Encode a string passed as argument
./src/main.sh "Hello World"

# Or pipe input
echo "Secret Message" | ./src/main.sh
```

## How it works

1. ROT13 is performed using `tr`.
2. The ROT13 output is piped to `base64` for encoding.

## Exit codes

- `0` on success
- `1` if no input is provided

## License

MIT
