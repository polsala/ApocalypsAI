import argparse
import sys

def caesar_cipher(text: str, shift: int, mode: str) -> str:
    """
    Applies a Caesar cipher to the given text.

    Args:
        text (str): The input string to encode or decode.
        shift (int): The number of positions to shift each character.
                     Positive for encoding, negative for decoding (or vice-versa
                     depending on how you define the mode).
        mode (str): 'encode' to shift forward, 'decode' to shift backward.

    Returns:
        str: The processed string.
    """
    result = []
    effective_shift = shift if mode == 'encode' else -shift

    for char in text:
        if 'a' <= char <= 'z':
            start = ord('a')
            shifted_char = chr(((ord(char) - start + effective_shift) % 26 + 26) % 26 + start)
            result.append(shifted_char)
        elif 'A' <= char <= 'Z':
            start = ord('A')
            shifted_char = chr(((ord(char) - start + effective_shift) % 26 + 26) % 26 + start)
            result.append(shifted_char)
        else:
            result.append(char)
    return "".join(result)

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Whisperer Encoder: Encode or decode messages using a Caesar cipher."
    )
    parser.add_argument(
        "--message",
        type=str,
        required=True,
        help="The message string to encode or decode."
    )
    parser.add_argument(
        "--shift",
        type=int,
        required=True,
        help="The integer value by which to shift characters."
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=['encode', 'decode'],
        required=True,
        help="The operation mode: 'encode' to shift forward, 'decode' to shift backward."
    )

    args = parser.parse_args()

    processed_message = caesar_cipher(args.message, args.shift, args.mode)
    print(processed_message)

if __name__ == "__main__":
    main()
