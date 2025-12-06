import argparse

def caesar_cipher(text: str, shift: int, encrypt: bool = True) -> str:
    """
    Applies a Caesar cipher to the given text.
    Non-alphabetic characters are ignored. Case is preserved.
    """
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            start = ord('a')
            if not encrypt:
                shift = -shift
            shifted_char = chr(((ord(char) - start + shift) % 26 + 26) % 26 + start)
            result.append(shifted_char)
        elif 'A' <= char <= 'Z':
            start = ord('A')
            if not encrypt:
                shift = -shift
            shifted_char = chr(((ord(char) - start + shift) % 26 + 26) % 26 + start)
            result.append(shifted_char)
        else:
            result.append(char)
    return "".join(result)

def main():
    parser = argparse.ArgumentParser(
        description="Scramble or unscramble messages using a Caesar cipher."
    )
    parser.add_argument("text", help="The message to scramble or unscramble.")
    parser.add_argument("shift", type=int, help="The shift value for the cipher.")
    parser.add_argument(
        "--decrypt",
        action="store_true",
        help="Decrypt the message instead of encrypting.",
    )

    args = parser.parse_args()

    if args.decrypt:
        output = caesar_cipher(args.text, args.shift, encrypt=False)
        print(f"Decrypted: {output}")
    else:
        output = caesar_cipher(args.text, args.shift, encrypt=True)
        print(f"Encrypted: {output}")

if __name__ == "__main__":
    main()
