# Last Message Encoder

A whimsical utility for encoding and decoding short, critical messages using a configurable, non-cryptographic substitution cipher. Perfect for sharing "last words" or simple notes in a "post-apocalyptic" scenario where complex technology might fail, but a shared simple key could persist.

## Philosophy

In the spirit of "Anarchy with discipline," this utility provides a simple, self-contained tool for basic text obfuscation. It's not for secure communication, but for the fun and utility of a shared secret code in a world where digital infrastructure is a distant memory.

## How it Works

The `last-message-encoder` uses a keyword-based substitution cipher.
1.  It constructs a unique cipher alphabet by taking the unique letters from your chosen `KEYWORD` first, followed by the remaining letters of the English alphabet in their standard order.
2.  It then maps the standard English alphabet to this new cipher alphabet.
3.  Encoding replaces each letter in your message with its corresponding letter from the cipher alphabet. Non-alphabetic characters (numbers, symbols, spaces) are left unchanged.
4.  Decoding reverses this process.

**Example Cipher Alphabet Generation (Keyword: `APOCALYPSE`)**

*   Unique letters from `APOCALYPSE`: `A, P, O, C, L, Y, S, E`
*   Remaining letters of the alphabet (in order, excluding those above): `B, D, F, G, H, I, J, K, M, N, Q, R, T, U, V, W, X, Z`
*   Resulting Cipher Alphabet: `APOCLYSEBDFGHIJKMNQRTUVWXZ`

## Installation

This utility is self-contained. Simply copy the `last-message-encoder` folder to your desired location. No external dependencies are required beyond a standard Python 3.11+ environment.

## Usage

Navigate into the `utils/last-message-encoder/src` directory and run `encoder.py` with the desired action, message, and keyword.

```bash
# To encode a message
python encoder.py encode "SURVIVE AND THRIVE" "APOCALYPSE"

# Expected Output:
# Original: SURVIVE AND THRIVE
# Encoded:  QTNUBUL AIC RNEBUL

# To decode a message
python encoder.py decode "QTNUBUL AIC RNEBUL" "APOCALYPSE"

# Expected Output:
# Original: QTNUBUL AIC RNEBUL
# Decoded:  SURVIVE AND THRIVE
```

### Command Line Arguments

*   `action`: `encode` or `decode` (required)
*   `message`: The string to be processed (required)
*   `keyword`: The keyword used to generate the cipher map (required)

## Tests

To run the tests, navigate to the `utils/last-message-encoder/tests` directory and execute:

```bash
python -m unittest test_encoder.py
```

All tests are deterministic and run offline, ensuring reliability without external network access.
