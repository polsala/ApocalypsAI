# Wasteland Whisperer

## Clandestine Communications for the End Times

The `Wasteland Whisperer` is a simple, self-contained Python utility designed to help survivors encode and decode messages using a unique 'Scavenger's Shift' substitution cipher. Whether you're coordinating a supply run, sharing intel on mutant patrols, or just sending a love note across the irradiated plains, this tool ensures your messages remain cryptic to unwanted ears.

## How it Works

The 'Scavenger's Shift' cipher reorders the standard English alphabet based on a secret `keyword`. The keyword's unique letters form the beginning of the new cipher alphabet, followed by the remaining letters of the standard alphabet in their original order. This creates a unique substitution map for encoding and decoding.

**Example Cipher Alphabet Generation (Keyword: `APOCALYPSE`)**

1.  Unique letters from `APOCALYPSE` (in order of appearance): `A, P, O, C, L, Y, S, E`
2.  Remaining letters of standard alphabet (not in keyword): `B, D, F, G, H, I, J, K, M, N, Q, R, T, U, V, W, X, Z`
3.  Cipher Alphabet: `APOCLYSEBDFGHIJKMNQRTVWXZ`

## Usage

### Prerequisites

*   Python 3.11+

### Running the Utility

Navigate to the `utils/wasteland-whisperer/src/` directory and run `whisperer.py` directly.

```bash
python whisperer.py --help
```

```
usage: whisperer.py [-h] (--encode | --decode) --message MESSAGE --keyword KEYWORD

Clandestine Communications for the End Times

options:
  -h, --help            show this help message and exit
  --encode              Encode the message
  --decode              Decode the message
  --message MESSAGE     The message to encode or decode
  --keyword KEYWORD     The secret keyword for the cipher
```

### Examples

**1. Encoding a message:**

```bash
python whisperer.py --encode --message "Hello Survivor" --keyword "APOCALYPSE"
```

Output:

```
Encoded message: Hqffb Suxlxbx
```

**2. Decoding a message:**

```bash
python whisperer.py --decode --message "Hqffb Suxlxbx" --keyword "APOCALYPSE"
```

Output:

```
Decoded message: Hello Survivor
```

## Development

To run tests, navigate to the `utils/wasteland-whisperer/` directory and execute:

```bash
python -m unittest tests/test_whisperer.py
```
