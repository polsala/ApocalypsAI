# nightly-qr-code-cli

A whimsical command‑line utility that turns any text into a simple QR‑like block pattern using Unicode full‑block characters. No external dependencies, just TypeScript/Node.

## Installation

```sh
npm install -g nightly-qr-code-cli
```

## Usage

```sh
npx nightly-qr-code-cli "Hello World"
```

If no argument is supplied, the utility reads from **STDIN**:

```sh
echo "Secret" | npx nightly-qr-code-cli
```

## How it works

Each character is converted to its 8‑bit binary representation; `1` → `█`, `0` → space. The rows are concatenated, producing a blocky pattern reminiscent of a QR code.

## Example

```text
$ npx nightly-qr-code-cli A
 █      █
```

## License

MIT
