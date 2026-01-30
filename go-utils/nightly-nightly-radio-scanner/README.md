# Nightly Radio Scanner

A whimsical yet useful Go utility that simulates scanning radio frequencies for encoded messages. Each line of input should be in the form:

```
SHIFT:<n>:<ciphertext>
```

where `<n>` is the Caesar cipher shift (0‑25) and `<ciphertext>` is the encoded text. The tool decodes the message concurrently and prints the plaintext.

## Usage

```sh
echo "SHIFT:3:KHOOR ZRUOG" | go run ./src
# Output: HELLO WORLD
```

## Building

```sh
go build -o radio-scanner ./src
```

## Testing

```sh
go test ./...
```
