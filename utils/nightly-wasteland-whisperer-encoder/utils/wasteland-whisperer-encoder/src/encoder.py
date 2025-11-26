import argparse

def caesar_cipher(text: str, shift: int, encode: bool = True) -> str:
    """
    Applies a Caesar cipher to the given text.
    Non-alphabetic characters are ignored.
    """
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            start = ord('a')
            if not encode:
                shift = -shift
            shifted_char = chr(((ord(char) - start + shift) % 26) + start)
            result.append(shifted_char)
        elif 'A' <= char <= 'Z':
            start = ord('A')
            if not encode:
                shift = -shift
            shifted_char = chr(((ord(char) - start + shift) % 26) + start)
            result.append(shifted_char)
        else:
            result.append(char)
    return "".join(result)

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Whisperer Message Encoder/Decoder using Caesar cipher."
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Command to execute")

    # Encode subparser
    encode_parser = subparsers.add_parser("encode", help="Encode a message")
    encode_parser.add_argument("message", type=str, help="The message to encode")
    encode_parser.add_argument("--shift", type=int, default=3,
                               help="The shift value for the Caesar cipher (default: 3)")

    # Decode subparser
    decode_parser = subparsers.add_parser("decode", help="Decode a message")
    decode_parser.add_argument("message", type=str, help="The message to decode")
    decode_parser.add_argument("--shift", type=int, default=3,
                               help="The shift value for the Caesar cipher (default: 3)")

    args = parser.parse_args()

    if args.command == "encode":
        encoded_message = caesar_cipher(args.message, args.shift, encode=True)
        print(encoded_message)
    elif args.command == "decode":
        decoded_message = caesar_cipher(args.message, args.shift, encode=False)
        print(decoded_message)

if __name__ == "__main__":
    main()
