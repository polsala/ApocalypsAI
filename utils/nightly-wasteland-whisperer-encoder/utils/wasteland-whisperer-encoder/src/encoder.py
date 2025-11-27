import argparse

# Define the alphabet for substitution. Includes lowercase, uppercase, and numbers.
ALPHABET_ORIGINAL = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# Define the cipher alphabet by shifting the original alphabet by 13 positions.
# This creates a fixed, deterministic substitution (similar to ROT13, but for all alphanumeric).
SHIFT_AMOUNT = 13
ALPHABET_CIPHER = ALPHABET_ORIGINAL[SHIFT_AMOUNT:] + ALPHABET_ORIGINAL[:SHIFT_AMOUNT]

# Create mapping dictionaries for efficient lookup
ENCODE_MAP = {char: ALPHABET_CIPHER[ALPHABET_ORIGINAL.index(char)] for char in ALPHABET_ORIGINAL}
DECODE_MAP = {char: ALPHABET_ORIGINAL[ALPHABET_CIPHER.index(char)] for char in ALPHABET_ORIGINAL}

def encode(text: str) -> str:
    """Encodes a given string using the fixed substitution cipher."""
    encoded_chars = []
    for char in text:
        encoded_chars.append(ENCODE_MAP.get(char, char)) # Pass through non-alphanumeric chars
    return "".join(encoded_chars)

def decode(text: str) -> str:
    """Decodes a given string using the fixed substitution cipher."""
    decoded_chars = []
    for char in text:
        decoded_chars.append(DECODE_MAP.get(char, char)) # Pass through non-alphanumeric chars
    return "".join(decoded_chars)

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Whisperer Encoder: Encode or decode messages using a fixed substitution cipher."
    )
    parser.add_argument(
        "--encode",
        type=str,
        help="Message to encode."
    )
    parser.add_argument(
        "--decode",
        type=str,
        help="Message to decode."
    )

    args = parser.parse_args()

    if args.encode:
        result = encode(args.encode)
        print(result)
    elif args.decode:
        result = decode(args.decode)
        print(result)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
