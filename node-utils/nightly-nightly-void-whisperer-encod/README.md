# nightly-void-whisperer-encoder

A Node.js utility to encode and decode secret messages using a whimsical void-inspired cipher.

## Usage

```bash
node src/index.js encode "hello world"
node src/index.js decode "svool dliow"
```

## Examples

Encoding:
```
$ node src/index.js encode "apocalypse"
zkxlkzsv
```

Decoding:
```
$ node src/index.js decode "zkxlkzsv"
apocalypse
```

## Tests

Run tests with:

```bash
node tests/test_index.js
```
