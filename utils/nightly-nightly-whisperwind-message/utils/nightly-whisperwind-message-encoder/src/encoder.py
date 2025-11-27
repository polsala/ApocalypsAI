import argparse

# Define the standard alphabet and its reverse for the substitution cipher
ALPHABET_LOWER = 'abcdefghijklmnopqrstuvwxyz'
ALPHABET_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
CIPHER_ALPHABET_LOWER = 'zyxwuvtsrqponmlkjihgfedcba'
CIPHER_ALPHABET_UPPER = 'ZYXWVUTSRQPONMLKJIHGFEDCBA'

def _transform_char(char, source_lower, source_upper, target_lower, target_upper):
    """Helper to transform a single character based on source and target alphabets."""
    if char.islower() and char in source_lower:
        idx = source_lower.index(char)
        return target_lower[idx]
    elif char.isupper() and char in source_upper:
        idx = source_upper.index(char)
        return target_upper[idx]
    return char # Return non-alphabetic characters unchanged

def encode(text: str) -> str:
    """Encodes a given string using the Whisperwind substitution cipher."""
    encoded_chars = [
        _transform_char(char, ALPHABET_LOWER, ALPHABET_UPPER, CIPHER_ALPHABET_LOWER, CIPHER_ALPHABET_UPPER)
        for char in text
    ]
    return ''.join(encoded_chars)

def decode(text: str) -> str:
    """Decodes a given string using the Whisperwind substitution cipher."""
    decoded_chars = [
        _transform_char(char, CIPHER_ALPHABET_LOWER, CIPHER_ALPHABET_UPPER, ALPHABET_LOWER, ALPHABET_UPPER)
        for char in text
    ]
    return ''.join(decoded_chars)

def main():
    parser = argparse.ArgumentParser(
        description="Whisperwind Message Encoder: Encode or decode messages using a simple substitution cipher."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--encode", action="store_true", help="Encode the provided message.")
    group.add_argument("--decode", action="store_true", help="Decode the provided message.")
    parser.add_argument("message", type=str, help="The message to encode or decode.")

    args = parser.parse_args()

    if args.encode:
        result = encode(args.message)
        print(f"Encoded message: {result}")
    elif args.decode:
        result = decode(args.message)
        print(f"Decoded message: {result}")

if __name__ == "__main__":
    main()
