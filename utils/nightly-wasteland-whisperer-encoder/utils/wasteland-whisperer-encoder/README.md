# Wasteland Whisperer Encoder

A simple, self-contained command-line utility for encoding and decoding messages using a fixed substitution cipher. Ideal for passing 'secure' notes between survivors when the internet is a distant memory.

## Features

*   **Fixed Substitution Cipher**: Uses a deterministic, non-random substitution for alphanumeric characters.
*   **Case-Preserving**: Maintains the case of letters.
*   **Number-Encoding**: Encodes numbers as well.
*   **Special Character Passthrough**: Non-alphanumeric characters are passed through unchanged.
*   **Command-Line Interface**: Easy to use from your terminal.

## Installation

This utility is self-contained. No special installation is required beyond having Python 3.11+ installed.

## Usage

To encode a message:

```bash
python3 src/encoder.py --encode "Hello, Survivor! The cache is at Sector 7, Grid 3."
# Output: Uryyb, Fheivibe! Gur pnpur vf ng Frpgbe k, Tevq g.
```

To decode a message:

```bash
python3 src/encoder.py --decode "Uryyb, Fheivibe! Gur pnpur vf ng Frpgbe k, Tevq g."
# Output: Hello, Survivor! The cache is at Sector 7, Grid 3.
```

### Examples

```bash
# Encode a simple message with numbers
python3 src/encoder.py --encode "Secret message 123"
# Output: Frperg zrffntr def

# Decode the message
python3 src/encoder.py --decode "Frperg zrffntr def"
# Output: Secret message 123

# Encode with special characters (they pass through unchanged)
python3 src/encoder.py --encode "@#$%^& *()_+"
# Output: @#$%^& *()_+
```
