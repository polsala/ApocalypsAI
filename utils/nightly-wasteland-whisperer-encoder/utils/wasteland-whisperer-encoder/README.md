# Wasteland Whisperer Encoder

A utility for encoding and decoding critical, short messages into a robust, low-bandwidth numeric format. Designed for scenarios where traditional communication channels are unreliable or compromised, this encoder helps ensure your vital dispatches get through, even if only partially.

## Philosophy

In the desolate future, every character counts. This encoder converts common alphanumeric characters and essential punctuation into a compact numeric sequence, augmented with a simple checksum for basic error detection. It's not about encryption, but about resilience and clarity under duress.

## How to Use

### Encoding a Message

To encode a message, run the `encoder.py` script with the `-e` or `--encode` flag followed by your message:

```bash
python src/encoder.py --encode "Hello World!"
```

This will output the numeric sequence representing your message, including a checksum.

### Decoding a Message

To decode a numeric sequence, run the `encoder.py` script with the `-d` or `--decode` flag followed by the encoded string:

```bash
python src/encoder.py --decode "08-05-12-12-15-37-23-15-18-12-04-40##189"
```

The script will attempt to decode the message and verify its checksum. If the checksum doesn't match, it will indicate a potential transmission error.

## Encoding Scheme

Each supported character is mapped to a two-digit number. Numbers are separated by a hyphen (`-`). A simple sum-of-digits checksum is appended at the end, separated by a double hash (`##`).

**Supported Characters & Mappings:**

| Char | Code | Char | Code | Char | Code |
| :--: | :--: | :--: | :--: | :--: | :--: |
| A-Z  | 01-26| 0-9  | 27-36| Space| 37   |
| .    | 38   | ,    | 39   | !    | 40   |
| ?    | 41   |      |      |      |      |

Unsupported characters are ignored during encoding.

## Examples

```bash
# Encode "SURVIVE"
python src/encoder.py --encode "SURVIVE"
# Output: Encoded: 19-21-18-22-09-22-05##116

# Decode "19-21-18-22-09-22-05##116"
python src/encoder.py --decode "19-21-18-22-09-22-05##116"
# Output: Decoded: SURVIVE (Checksum OK Expected 116, Got 116)

# Decode with a corrupted checksum
python src/encoder.py --decode "19-21-18-22-09-22-05##115"
# Output: Decoded: SURVIVE (Checksum MISMATCH! Expected 115, Got 116)
```
