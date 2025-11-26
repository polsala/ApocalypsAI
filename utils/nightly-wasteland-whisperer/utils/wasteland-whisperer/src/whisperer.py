import argparse

def _shift_char(char: str, scramble_factor: int, encode: bool) -> str:
    """Shifts a single alphabetic character by the scramble_factor."""
    if not char.isalpha():
        return char

    start = ord('a') if char.islower() else ord('A')
    offset = ord(char) - start

    if encode:
        shifted_offset = (offset + scramble_factor) % 26
    else:
        shifted_offset = (offset - scramble_factor) % 26

    return chr(start + shifted_offset)

def whisper(text: str, scramble_factor: int, mode: str = 'encode') -> str:
    """Encodes or decodes a message using a Caesar-like substitution cipher.

    Args:
        text (str): The message to process.
        scramble_factor (int): The integer shift amount.
        mode (str): 'encode' to encrypt, 'decode' to decrypt.

    Returns:
        str: The processed message.
    """
    if mode not in ['encode', 'decode']:
        raise ValueError("Mode must be 'encode' or 'decode'.")

    processed_chars = [
        _shift_char(char, scramble_factor, encode=(mode == 'encode'))
        for char in text
    ]
    return ''.join(processed_chars)

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Whisperer: Encode or decode messages for post-apocalyptic communication."
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=['encode', 'decode'],
        required=True,
        help="Operation mode: 'encode' to encrypt, 'decode' to decrypt."
    )
    parser.add_argument(
        "--text",
        type=str,
        required=True,
        help="The message string to process."
    )
    parser.add_argument(
        "--scramble-factor",
        type=int,
        required=True,
        help="The integer shift amount for the cipher."
    )

    args = parser.parse_args()

    try:
        result = whisper(args.text, args.scramble_factor, args.mode)
        print(result)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
