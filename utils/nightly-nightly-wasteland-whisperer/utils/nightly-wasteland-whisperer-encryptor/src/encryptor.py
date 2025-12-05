import argparse

def caesar_cipher(text: str, shift: int, mode: str = 'encrypt') -> str:
    """
    Applies a Caesar cipher to the given text.

    Args:
        text (str): The input string to encrypt or decrypt.
        shift (int): The numerical shift value. Positive for right shift, negative for left shift.
        mode (str): 'encrypt' to encrypt, 'decrypt' to decrypt. Defaults to 'encrypt'.

    Returns:
        str: The processed string.
    """
    result = []
    # Adjust shift for decryption: to reverse a +N shift, we apply a -N shift.
    # The cipher function itself always applies a 'forward' shift, so for decryption
    # we effectively pass a negative shift to move characters backwards.
    if mode == 'decrypt':
        shift = -shift

    for char in text:
        if 'a' <= char <= 'z':
            start = ord('a')
            result.append(chr((ord(char) - start + shift) % 26 + start))
        elif 'A' <= char <= 'Z':
            start = ord('A')
            result.append(chr((ord(char) - start + shift) % 26 + start))
        else:
            result.append(char) # Non-alphabetic characters remain unchanged
    return ''.join(result)

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Whisperer: A simple Caesar cipher utility."
    )
    parser.add_argument(
        "--message",
        type=str,
        required=True,
        help="The message string to encrypt or decrypt."
    )
    parser.add_argument(
        "--shift",
        type=int,
        required=True,
        help="The numerical shift value. Positive for right shift, negative for left shift."
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=['encrypt', 'decrypt'],
        required=True,
        help="Operation mode: 'encrypt' or 'decrypt'."
    )

    args = parser.parse_args()

    processed_message = caesar_cipher(args.message, args.shift, args.mode)
    print(processed_message)

if __name__ == '__main__':
    main()
