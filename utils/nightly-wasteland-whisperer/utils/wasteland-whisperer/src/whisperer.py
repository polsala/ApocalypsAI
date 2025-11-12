import argparse
import string

def generate_cipher_alphabet(keyword: str) -> str:
    """
    Generates a substitution cipher alphabet based on a keyword.
    The keyword's unique letters come first, followed by the rest of the alphabet.
    Non-alphabetic characters in the keyword are ignored.
    """
    keyword = keyword.upper()
    standard_alphabet = string.ascii_uppercase
    
    # Collect unique letters from the keyword in order
    cipher_chars = []
    for char in keyword:
        if char.isalpha() and char not in cipher_chars:
            cipher_chars.append(char)
            
    # Add remaining letters from the standard alphabet
    for char in standard_alphabet:
        if char not in cipher_chars:
            cipher_chars.append(char)
            
    return "".join(cipher_chars)

def transform_message(message: str, keyword: str, mode: str) -> str:
    """
    Transforms a message (encode or decode) using the Scavenger's Shift cipher.
    Preserves case and leaves non-alphabetic characters unchanged.
    """
    if not keyword:
        raise ValueError("Keyword cannot be empty.")

    cipher_alphabet = generate_cipher_alphabet(keyword)
    standard_alphabet = string.ascii_uppercase
    
    if mode == "encode":
        # Map standard_alphabet chars to cipher_alphabet chars
        mapping = {std_char: cipher_char for std_char, cipher_char in zip(standard_alphabet, cipher_alphabet)}
    elif mode == "decode":
        # Map cipher_alphabet chars back to standard_alphabet chars
        mapping = {cipher_char: std_char for cipher_char, std_char in zip(cipher_alphabet, standard_alphabet)}
    else:
        raise ValueError("Mode must be 'encode' or 'decode'.")

    transformed_chars = []
    for char in message:
        if char.isalpha():
            is_upper = char.isupper()
            char_upper = char.upper()
            # Use .get() with fallback to handle cases where char_upper might not be in mapping
            # (though for standard English alphabet, it should always be found).
            transformed_char = mapping.get(char_upper, char_upper)
            transformed_chars.append(transformed_char if is_upper else transformed_char.lower())
        else:
            transformed_chars.append(char) # Non-alphabetic characters are unchanged
            
    return "".join(transformed_chars)

def encode(message: str, keyword: str) -> str:
    """
    Encodes a message using the Scavenger's Shift cipher.
    """
    return transform_message(message, keyword, "encode")

def decode(encoded_message: str, keyword: str) -> str:
    """
    Decodes an encoded message using the Scavenger's Shift cipher.
    """
    return transform_message(encoded_message, keyword, "decode")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clandestine Communications for the End Times")
    parser.add_argument("--encode", action="store_true", help="Encode the message")
    parser.add_argument("--decode", action="store_true", help="Decode the message")
    parser.add_argument("--message", type=str, required=True, help="The message to encode or decode")
    parser.add_argument("--keyword", type=str, required=True, help="The secret keyword for the cipher")

    args = parser.parse_args()

    if args.encode and args.decode:
        parser.error("Cannot specify both --encode and --decode. Choose one.")
    if not args.encode and not args.decode:
        parser.error("Must specify either --encode or --decode.")

    try:
        if args.encode:
            result = encode(args.message, args.keyword)
            print(f"Encoded message: {result}")
        elif args.decode:
            result = decode(args.message, args.keyword)
            print(f"Decoded message: {result}")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
