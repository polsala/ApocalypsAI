# Scavenger's Cipher Scribe

"Whispers in the wasteland, secrets in the dust."

This utility provides a basic, self-contained substitution cipher for encrypting and decrypting short messages. It's perfect for quick, clandestine communications between survivor groups without relying on complex infrastructure.

## Features

*   **Simple Substitution**: Each character in the defined alphabet is mapped to another unique character based on a provided key.
*   **Configurable**: Customize the alphabet and the substitution key to enhance security or adapt to specific communication needs.
*   **Offline & Self-Contained**: No external dependencies or network access required, making it robust for post-apocalyptic scenarios.

## Usage

The `cipher_scribe.py` script can be run directly from the command line.

```bash
python src/cipher_scribe.py --help
```

### Encrypting a message

To encrypt a message using the default alphabet and key:

```bash
python src/cipher_scribe.py --encrypt --message "Hello, survivor! Meet me at the old water tower tonight."
```

Output:

```
Encrypted message: 'Uqppc, 0v0o0vcr! Fqq0 fq 00 0uq cpd 800qr 0c8qr 0c000u.
'
```

### Decrypting a message

To decrypt a message using the default alphabet and key:

```bash
python src/cipher_scribe.py --decrypt --message "Uqppc, 0v0o0vcr! Fqq0 fq fq 0uq cpd 800qr 0c8qr 0c000u."
```

Output:

```
Decrypted message: 'Hello, survivor! Meet me at the old water tower tonight.
'
```

### Using a custom alphabet and key

You can specify your own alphabet and a corresponding key. The key must be a permutation of the alphabet and have the same length.

```bash
python src/cipher_scribe.py \
  --alphabet "abc" \
  --key "bca" \
  --encrypt \
  --message "cab"
```

Output:

```
Encrypted message: 'abc'
```

## How it Works

The utility creates a one-to-one mapping between characters in the `ALPHABET` and characters in the `KEY`. For encryption, it looks up each character of your message in the `ALPHABET` and replaces it with the character at the same position in the `KEY`. Decryption reverses this process.

**Important**: Keep your custom `ALPHABET` and `KEY` secret! Without them, messages are much harder to decrypt.
