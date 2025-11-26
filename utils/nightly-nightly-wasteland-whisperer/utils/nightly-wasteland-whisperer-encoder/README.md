# Wasteland Whisperer Encoder

A discreet command-line utility for encoding and decoding messages using a simple, configurable Caesar cipher. Perfect for sending short, sensitive communications across the irradiated plains without attracting unwanted attention from raiders or rogue AI.

## Features

*   **Simple Caesar Cipher**: Shifts alphabetic characters by a specified amount.
*   **Case-Preserving**: Maintains original casing of letters.
*   **Non-Alphabetic Preservation**: Numbers, symbols, and spaces remain unchanged.
*   **CLI Interface**: Easy to use from the command line.

## Usage

### Encoding a Message

To encode a message, use the `--encode` flag, provide your message with `--text`, and specify a numeric `--shift` key.

```bash
python src/encoder.py --encode --text "Hello, Wasteland!" --shift 3
```

Output:
```
Khoor, Zdvwhodqg!
```

### Decoding a Message

To decode a message, use the `--decode` flag, provide the encoded text with `--text`, and the same numeric `--shift` key used for encoding.

```bash
python src/encoder.py --decode --text "Khoor, Zdvwhodqg!" --shift 3
```

Output:
```
Hello, Wasteland!
```

### Help

For more information on available commands:

```bash
python src/encoder.py --help
```
