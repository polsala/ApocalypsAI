# nightly-qr-glitch

**Generates an ASCII QR code with a whimsical glitch effect for any input string.**

## Usage

```bash
nightly-qr-glitch <text>
```

- If `<text>` is omitted, the utility reads from *stdin*.
- The output is an ASCII representation of a QR code, where most dark modules are rendered as `██` and every 7th dark module is rendered as `▓▓` to give a subtle "glitch" look.

## Examples

```bash
# Direct argument
nightly-qr-glitch "Hello, world!"

# Piped input
echo "ApocalypsAI" | nightly-qr-glitch
```

The command prints the QR code to standard output, which can be copied, displayed in a terminal, or piped into other tools.

## Building

```bash
cargo build --release
```

The compiled binary will be located at `target/release/nightly-qr-glitch`.

## Testing

```bash
cargo test
```

The test suite checks that the generated QR code contains the expected dark block characters.
