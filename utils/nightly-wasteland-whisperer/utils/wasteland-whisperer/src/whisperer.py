import argparse

def _shift_char(char, shift, encode=True):
    """Helper to shift a single character, preserving case and non-alphabetic chars."""
    if 'a' <= char <= 'z':
        start = ord('a')
        shifted_char = chr(start + (ord(char) - start + (shift if encode else -shift)) % 26)
    elif 'A' <= char <= 'Z':
        start = ord('A')
        shifted_char = chr(start + (ord(char) - start + (shift if encode else -shift)) % 26)
    else:
        shifted_char = char  # Non-alphabetic characters remain unchanged
    return shifted_char

def encode(text: str, shift: int) -> str:
    """Encodes a string using a Caesar cipher with the given shift."""
    return "".join(_shift_char(char, shift, encode=True) for char in text)

def decode(text: str, shift: int) -> str:
    """Decodes a string using a Caesar cipher with the given shift."""
    return "".join(_shift_char(char, shift, encode=False) for char in text)

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Whisperer: Encode or decode messages using a Caesar cipher."
    )
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # Encode parser
    encode_parser = subparsers.add_parser('encode', help='Encode a message')
    encode_parser.add_argument('message', type=str, help='The message to encode')
    encode_parser.add_argument('shift', type=int, help='The integer shift value')

    # Decode parser
    decode_parser = subparsers.add_parser('decode', help='Decode a message')
    decode_parser.add_argument('message', type=str, help='The message to decode')
    decode_parser.add_argument('shift', type=int, help='The integer shift value')

    args = parser.parse_args()

    if args.command == 'encode':
        result = encode(args.message, args.shift)
        print(result)
    elif args.command == 'decode':
        result = decode(args.message, args.shift)
        print(result)

if __name__ == '__main__':
    main()
