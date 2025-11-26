import argparse
import sys

def caesar_cipher(text: str, shift: int, encode: bool = True) -> str:
    """
    Applies a Caesar cipher to the given text.
    Shifts alphabetic characters by the specified amount.
    Preserves case and non-alphabetic characters.
    """
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            start = ord('a')
            if not encode:
                shift = -shift
            result.append(chr((ord(char) - start + shift) % 26 + start))
        elif 'A' <= char <= 'Z':
            start = ord('A')
            if not encode:
                shift = -shift
            result.append(chr((ord(char) - start + shift) % 26 + start))
        else:
            result.append(char)
    return "".join(result)

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Whisperer Encoder: A simple Caesar cipher utility."
    )
    parser.add_argument(
        "--encode", action="store_true", help="Encode the provided text."
    )
    parser.add_argument(
        "--decode", action="store_true", help="Decode the provided text."
    )
    parser.add_argument(
        "--text", type=str, required=True, help="The message text to process."
    )
    parser.add_argument(
        "--shift", type=int, required=True, help="The numeric shift key (e.g., 3 for Caesar cipher)."
    )

    args = parser.parse_args()

    if args.encode and args.decode:
        print("Error: Cannot use both --encode and --decode simultaneously.", file=sys.stderr)
        sys.exit(1)
    elif not args.encode and not args.decode:
        print("Error: Must specify either --encode or --decode.", file=sys.stderr)
        sys.exit(1)

    if args.encode:
        processed_text = caesar_cipher(args.text, args.shift, encode=True)
        print(processed_text)
    elif args.decode:
        processed_text = caesar_cipher(args.text, args.shift, encode=False)
        print(processed_text)

if __name__ == "__main__":
    main()
