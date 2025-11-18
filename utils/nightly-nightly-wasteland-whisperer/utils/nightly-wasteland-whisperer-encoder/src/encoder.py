import argparse

# Fixed substitution map for encoding
# This map is designed to be somewhat arbitrary but consistent.
# It maps lowercase letters and digits to other lowercase letters and digits.
ENCODE_MAP = {
    'a': 'q', 'b': 'w', 'c': 'e', 'd': 'r', 'e': 't', 'f': 'y', 'g': 'u', 'h': 'i', 'i': 'o', 'j': 'p',
    'k': 'a', 'l': 's', 'm': 'd', 'n': 'f', 'o': 'g', 'p': 'h', 'q': 'j', 'r': 'k', 's': 'l', 't': 'z',
    'u': 'x', 'v': 'c', 'w': 'v', 'x': 'b', 'y': 'n', 'z': 'm',
    '0': '5', '1': '6', '2': '7', '3': '8', '4': '9', '5': '0', '6': '1', '7': '2', '8': '3', '9': '4'
}

# Generate the decode map from the encode map
DECODE_MAP = {v: k for k, v in ENCODE_MAP.items()}

def transform_message(message: str, transform_map: dict) -> str:
    """Applies a substitution map to a message, preserving case and non-mapped characters."""
    transformed_chars = []
    for char in message:
        lower_char = char.lower()
        if lower_char in transform_map:
            transformed_char = transform_map[lower_char]
            # Preserve original case
            if char.isupper():
                transformed_chars.append(transformed_char.upper())
            else:
                transformed_chars.append(transformed_char)
        else:
            transformed_chars.append(char) # Keep non-mapped characters as they are
    return "".join(transformed_chars)

def encode(message: str) -> str:
    """Encodes a message using the fixed substitution cipher."""
    return transform_message(message, ENCODE_MAP)

def decode(message: str) -> str:
    """Decodes a message using the fixed substitution cipher."""
    return transform_message(message, DECODE_MAP)

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Whisperer Encoder: Encode or decode messages with a fixed substitution cipher."
    )
    parser.add_argument(
        "action",
        choices=["encode", "decode"],
        help="Action to perform: 'encode' or 'decode'."
    )
    parser.add_argument(
        "message",
        type=str,
        help="The message string to encode or decode."
    )

    args = parser.parse_args()

    if args.action == "encode":
        result = encode(args.message)
        print(result)
    elif args.action == "decode":
        result = decode(args.message)
        print(result)

if __name__ == "__main__":
    main()
