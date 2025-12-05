import argparse

def caesar_cipher(text: str, shift: int, mode: str = 'encode') -> str:
    """
    Applies a Caesar cipher to the given text.

    Args:
        text (str): The input string to encode or decode.
        shift (int): The numerical shift value.
        mode (str): 'encode' to encrypt, 'decode' to decrypt. Defaults to 'encode'.

    Returns:
        str: The processed string.
    """
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            start = ord('a')
            if mode == 'encode':
                shifted_char = chr(((ord(char) - start + shift) % 26) + start)
            else:  # decode
                shifted_char = chr(((ord(char) - start - shift + 26) % 26) + start)
            result.append(shifted_char)
        elif 'A' <= char <= 'Z':
            start = ord('A')
            if mode == 'encode':
                shifted_char = chr(((ord(char) - start + shift) % 26) + start)
            else:  # decode
                shifted_char = chr(((ord(char) - start - shift + 26) % 26) + start)
            result.append(shifted_char)
        else:
            result.append(char)
    return "".join(result)

def main():
    """
    Parses command-line arguments and performs Caesar cipher operations.
    """
    parser = argparse.ArgumentParser(
        description="Encode or decode messages using a Caesar cipher for wasteland communication."
    )
    parser.add_argument(
        "--message",
        "-m",
        type=str,
        required=True,
        help="The message to encode or decode."
    )
    parser.add_argument(
        "--shift",
        "-s",
        type=int,
        required=True,
        help="The numerical shift value (e.g., 3 for a Caesar cipher).
              Can be positive or negative."
    )
    parser.add_argument(
        "--mode",
        "-d",
        type=str,
        choices=['encode', 'decode'],
        default='encode',
        help="Operation mode: 'encode' (default) or 'decode'."
    )

    args = parser.parse_args()

    output_message = caesar_cipher(args.message, args.shift, args.mode)
    print(f"Original: {args.message}")
    print(f"Shift: {args.shift}")
    print(f"Mode: {args.mode}")
    print(f"Result: {output_message}")

if __name__ == "__main__":
    main()
