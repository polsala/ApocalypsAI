# Whisperwind Message Encoder

## Overview
In the quiet aftermath, when every whisper carries weight, the Whisperwind Message Encoder helps you share your thoughts with a touch of mystery. This utility provides a simple substitution cipher to encode and decode text messages, making them just obscure enough to deter casual eavesdroppers but easy for your trusted allies to decipher.

It's a lightweight, self-contained Python script designed for quick command-line use.

## Features
- **Simple Substitution Cipher**: Uses a fixed, reversible alphabet substitution.
- **Case-Preserving**: Maintains the original casing of letters.
- **Non-Alphabetic Passthrough**: Numbers, symbols, and spaces are left unchanged.
- **Command-Line Interface**: Easy to use directly from your terminal.

## Installation
This utility is self-contained and requires no special installation beyond a Python 3.x environment.

```bash
# Navigate to the utility's directory
cd utils/nightly-whisperwind-message-encoder/src

# You can then run it directly
python encoder.py --help
```

## Usage

### Encoding a message
To encode a message, use the `--encode` flag followed by your message:

```bash
python encoder.py --encode "Hello, fellow survivor! Meet me at the old water tower tonight."
```

**Example Output:**
```
Encoded message: Svool, uvoolm hfiernref! Nvvg nv zg gsv old dzgvi gldvi glmrtsg.
```

### Decoding a message
To decode a message, use the `--decode` flag followed by the encoded text:

```bash
python encoder.py --decode "Svool, uvoolm hfiernref! Nvvg nv zg gsv old dzgvi gldvi glmrtsg."
```

**Example Output:**
```
Decoded message: Hello, fellow survivor! Meet me at the old water tower tonight.
```

## Cipher Details
The encoder uses a simple reverse alphabet substitution. For example, 'a' becomes 'z', 'b' becomes 'y', and so on. This ensures a consistent and easily reversible transformation.

## Development & Testing
To run the tests for this utility:

```bash
cd utils/nightly-whisperwind-message-encoder
python -m unittest tests/test_encoder.py
```
