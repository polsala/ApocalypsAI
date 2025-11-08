import argparse

def _normalize_text(text):
    """Converts text to uppercase and filters out non-alphabetic characters."""
    return "".join(filter(str.isalpha, text)).upper()

def _vigenere_cipher(text, keyword, encrypt=True):
    """
    Applies the Vigenere cipher to the given text using the keyword.
    Non-alphabetic characters are preserved. Case of alphabetic characters is preserved.
    """
    normalized_keyword = _normalize_text(keyword)

    if not normalized_keyword:
        raise ValueError("Keyword must contain at least one alphabetic character.")

    result = []
    keyword_len = len(normalized_keyword)
    keyword_idx = 0

    for char in text:
        if 'A' <= char.upper() <= 'Z':
            is_lower = char.islower()
            text_char_val = ord(char.upper()) - ord('A')
            keyword_char_val = ord(normalized_keyword[keyword_idx % keyword_len]) - ord('A')

            if encrypt:
                shifted_val = (text_char_val + keyword_char_val) % 26
            else: # decrypt
                shifted_val = (text_char_val - keyword_char_val + 26) % 26

            new_char = chr(shifted_val + ord('A'))
            
            if is_lower:
                result.append(new_char.lower())
            else:
                result.append(new_char)
            
            keyword_idx += 1
        else:
            result.append(char) # Preserve non-alphabetic characters
            
    return "".join(result)

def encode(message, keyword):
    """Encodes a message using the Vigenere cipher."""
    return _vigenere_cipher(message, keyword, encrypt=True)

def decode(message, keyword):
    """Decodes a message using the Vigenere cipher."""
    return _vigenere_cipher(message, keyword, encrypt=False)

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Whisperer: A Vigenere cipher utility for cryptic communication."
    )
    parser.add_argument(
        "-e", "--encode", type=str, help="The message to encode."
    )
    parser.add_argument(
        "-d", "--decode", type=str, help="The message to decode."
    )
    parser.add_argument(
        "-k", "--keyword", type=str, required=True, help="The keyword for encryption/decryption."
    )

    args = parser.parse_args()

    if args.encode and args.decode:
        parser.error("Cannot use --encode and --decode simultaneously. Choose one.")
    elif args.encode:
        encoded_message = encode(args.encode, args.keyword)
        print(f"Original Message: {args.encode}")
        print(f"Keyword: {args.keyword}")
        print(f"Encoded Message: {encoded_message}")
    elif args.decode:
        decoded_message = decode(args.decode, args.keyword)
        print(f"Encoded Message: {args.decode}")
        print(f"Keyword: {args.keyword}")
        print(f"Decoded Message: {decoded_message}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
