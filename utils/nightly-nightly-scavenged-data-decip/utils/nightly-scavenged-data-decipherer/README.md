# Nightly Scavenged Data Decipherer

## Description
In the post-apocalyptic wasteland, data often comes in fragmented, corrupted, or encoded forms. The `nightly-scavenged-data-decipherer` is a crucial tool for making sense of these digital relics. It automatically attempts to detect and decode common data encodings such as Base64, URL encoding, and Hexadecimal from a given input string.

This utility is designed to be a first-pass attempt at cleaning up 'scavenged' data, providing a more readable output and indicating what encoding, if any, was successfully identified.

## Usage

Run the utility from the command line, providing the potentially encoded string as an argument:

```bash
python src/decipherer.py "<encoded_string>"
```

### Examples

```bash
python src/decipherer.py "SGVsbG8sIFdvcmxkIQ=="
# Output: Decoded (Base64): Hello, World!

python src/decipherer.py "Hello%2C%20World%21"
# Output: Decoded (URL): Hello, World!

python src/decipherer.py "48656c6c6f2c20576f726c6421"
# Output: Decoded (Hex): Hello, World!

python src/decipherer.py "This is plain text."
# Output: Original: This is plain text.

python src/decipherer.py "Not an encoding, just gibberish!@#"
# Output: Original: Not an encoding, just gibberish!@#
```

## How it Works
The utility attempts to decode the input string using a sequence of common decoding algorithms. It prioritizes decoders that are less likely to produce false positives for arbitrary text. The first successful and meaningful decode is returned.

Currently supported encodings:
- Base64
- URL Encoding
- Hexadecimal
