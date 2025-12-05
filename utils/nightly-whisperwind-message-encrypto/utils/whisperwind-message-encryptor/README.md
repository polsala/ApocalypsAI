# Whisperwind Message Encryptor

## 🌬️ Keep Your Secrets Safe in the Shifting Sands 🌬️

In a world where communication is paramount but trust is scarce, the Whisperwind Message Encryptor offers a simple, robust way to secure your vital messages. Whether you're coordinating a scavenging run, sharing intel on a new mutant sighting, or just sending a heartfelt note to a loved one across the wastes, this utility ensures your words remain private.

It uses a keyword-based substitution cipher, easy to understand and implement, yet effective enough to deter casual eavesdroppers.

## Features

*   **Keyword-Based Encryption**: Generate a unique cipher based on a secret keyword.
*   **Simple & Effective**: A straightforward substitution cipher for quick encoding and decoding.
*   **Self-Contained**: No external dependencies, just pure Python.
*   **Case-Preserving**: Maintains original casing for readability (encrypted letters will match case of original).
*   **Non-Alphabetic Passthrough**: Numbers, symbols, and spaces are left untouched.

## Usage

### Command Line

```bash
# Encrypt a message
python src/encryptor.py encrypt "The supplies are at sector 7G. Beware the glowing fungi." "RAVENCLAW"

# Decrypt a message
python src/encryptor.py decrypt "Gvs ehhhwove zqv zg evxgdq 7P. Osvzqv gsv torldrmt uhmtw." "RAVENCLAW"
```

### As a Module

```python
from src.encryptor import encrypt, decrypt

keyword = "APOCALYPSE"
message = "Meet me at the old water tower tonight."

encrypted_message = encrypt(message, keyword)
print(f"Encrypted: {encrypted_message}")

decrypted_message = decrypt(encrypted_message, keyword)
print(f"Decrypted: {decrypted_message}")
```

## How it Works (The Cipher)

The utility constructs a unique cipher alphabet based on your chosen keyword.
1.  It takes the keyword and removes any duplicate letters.
2.  It appends the remaining letters of the standard English alphabet (A-Z) in order, ensuring all 26 letters are present.
3.  This new, shuffled alphabet becomes the substitution map for the original alphabet.

Example with keyword "ZOMBIE":
*   Original Alphabet: `ABCDEFGHIJKLMNOPQRSTUVWXYZ`
*   Keyword Unique: `ZOMBIE`
*   Cipher Alphabet: `ZOMBIEACDFGHJKLNPQRSTUVWXY` (Z, O, M, B, I, E, then A, C, D, F, G, H, J, K, L, N, P, Q, R, S, T, U, V, W, X, Y)

So, 'A' encrypts to 'Z', 'B' to 'O', 'C' to 'M', and so on.

## Development

To run tests:

```bash
python -m unittest tests/test_encryptor.py
```
