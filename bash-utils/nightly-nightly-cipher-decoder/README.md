# nightly-cipher-decoder

A tiny Bash utility that decodes (or encodes) Caesar‑cipher text with any shift you specify.  By default it uses the classic ROT13 shift (13).

## Usage

```bash
# Decode a string with the default ROT13 shift
./src/decode.sh "Uryyb Jbeyq!"

# Decode with a custom shift (e.g., shift of 5)
./src/decode.sh 5 "fgh CDE"

# Pipe input from stdin (default shift)
echo "Uryyb Jbeyq!" | ./src/decode.sh
```

### Arguments

1. **shift** (optional) – Integer shift amount. Positive values shift forward, negative values shift backward. If omitted, defaults to `13` (ROT13).
2. **text** (optional) – The text to decode. If omitted, the script reads from `stdin`.

## How it works

The script builds a rotated alphabet for both upper‑ and lower‑case letters and then uses `tr` to translate the input. Non‑alphabetic characters are left untouched.

## Testing

Run the test suite with:

```bash
bash tests/test_decode.sh
```

All tests should pass.
