# Whisperwind Cipher

A whimsical, lightweight command-line utility for encrypting and decrypting short messages using a custom substitution cipher based on a 'whisperwind' key phrase. Perfect for sharing secret notes in a post-apocalyptic world where strong cryptographic tools might be unavailable or overkill.

## How it Works

The cipher generates a unique substitution map based on a provided 'key phrase'. This key phrase acts as the seed for scrambling the alphabet, ensuring that only those who know the exact key phrase can encrypt or decrypt messages. Characters not present in the cipher's base alphabet (standard letters, numbers, punctuation, space) are left unchanged.

## Usage

### Prerequisites

*   Python 3.11+

### Encryption

To encrypt a message:

```bash
python src/cipher.py encrypt "Your secret message here." "my-apocalypse-key"
```

This will output the encrypted string to standard output.

### Decryption

To decrypt a message:

```bash
python src/cipher.py decrypt "Encrypted message here." "my-apocalypse-key"
```

This will output the original decrypted string to standard output.

## Examples

```bash
# Encrypt
python src/cipher.py encrypt "Hello, ApocalypsAI!" "nightly-integrator"
# Expected Output: "Lipps, HtqchzbsfHI!"

# Decrypt
python src/cipher.py decrypt "Lipps, HtqchzbsfHI!" "nightly-integrator"
# Expected Output: "Hello, ApocalypsAI!"

# With special characters not in base alphabet (left unchanged)
python src/cipher.py encrypt "Hello 👋 World!" "simple"
# Expected Output: "Ksvvo 👋 Zosrj!"
```
