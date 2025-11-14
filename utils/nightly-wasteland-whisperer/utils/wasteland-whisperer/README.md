# Wasteland Whisperer

## Cryptic Communications for the End Times

The Wasteland Whisperer is a vital tool for survivors needing to send short, critical messages across hostile, interference-ridden landscapes. It encodes your plain text into resilient, cryptic formats, making it harder to intercept and easier to transmit with limited bandwidth or unreliable signals.

### Features

*   **Substitution Cipher**: A simple, fixed-shift cipher for quick, obfuscated messages.
*   **Morse Code**: Convert messages into standard International Morse Code (dots, dashes, spaces) for auditory or visual transmission.

### Usage

This utility is a standalone Python script. You can run it directly.

#### Encode a message using the Substitution Cipher (default):

```bash
python3 src/whisperer.py encode "Hello World 123!"
# Output: KHOOR ZRUOG 456!
```

#### Decode a message using the Substitution Cipher:

```bash
python3 src/whisperer.py decode "KHOOR ZRUOG 456!"
# Output: HELLO WORLD 123!
```

#### Encode a message to Morse Code:

```bash
python3 src/whisperer.py encode "SOS" --method morse
# Output: ... --- ...
```

#### Decode a message from Morse Code:

```bash
python3 src/whisperer.py decode "... --- ..." --method morse
# Output: SOS
```

### Methods

*   `substitution`: A Caesar cipher with a fixed shift of +3 for letters (A->D) and +3 for numbers (0->3). Non-alphanumeric characters are preserved.
*   `morse`: Standard International Morse Code. Words are separated by ` / ` and characters within a word by a single space. Non-mappable characters are ignored.

### Development

To run tests, navigate to the `utils/wasteland-whisperer/` directory and execute:

```bash
python3 -m pytest tests/
```
