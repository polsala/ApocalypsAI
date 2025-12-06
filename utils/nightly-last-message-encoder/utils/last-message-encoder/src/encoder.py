import argparse
import string

def _generate_cipher_map(keyword: str) -> tuple[dict[str, str], dict[str, str]]:
    """
    Generates forward and reverse substitution cipher maps based on a keyword.
    The cipher alphabet is formed by the unique characters of the keyword
    followed by the remaining uppercase English letters in alphabetical order.
    """
    keyword = keyword.upper()
    standard_alphabet = string.ascii_uppercase
    
    # Build unique keyword characters
    cipher_alphabet_list = []
    for char in keyword:
        if char.isalpha() and char not in cipher_alphabet_list:
            cipher_alphabet_list.append(char)
            
    # Add remaining standard alphabet characters
    for char in standard_alphabet:
        if char not in cipher_alphabet_list:
            cipher_alphabet_list.append(char)
            
    cipher_alphabet = "".join(cipher_alphabet_list)
    
    if len(cipher_alphabet) != len(standard_alphabet):
        raise ValueError("Generated cipher alphabet length mismatch.")

    forward_map = {std_char: cipher_char for std_char, cipher_char in zip(standard_alphabet, cipher_alphabet)}
    reverse_map = {cipher_char: std_char for std_char, cipher_char in zip(standard_alphabet, cipher_alphabet)}
    
    return forward_map, reverse_map

def encode(message: str, keyword: str) -> str:
    """Encodes a message using a keyword-based substitution cipher."""
    forward_map, _ = _generate_cipher_map(keyword)
    encoded_message = []
    for char in message.upper():
        if char.isalpha():
            encoded_message.append(forward_map.get(char, char)) # Use char itself if not in map (e.g., non-alpha)
        else:
            encoded_message.append(char) # Keep non-alpha characters as is
    return "".join(encoded_message)

def decode(encoded_message: str, keyword: str) -> str:
    """Decodes an encoded message using a keyword-based substitution cipher."""
    _, reverse_map = _generate_cipher_map(keyword)
    decoded_message = []
    for char in encoded_message.upper():
        if char.isalpha():
            decoded_message.append(reverse_map.get(char, char)) # Use char itself if not in map
        else:
            decoded_message.append(char) # Keep non-alpha characters as is
    return "".join(decoded_message)

def main():
    parser = argparse.ArgumentParser(
        description="Encode or decode a message using a whimsical keyword-based substitution cipher.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("action", choices=["encode", "decode"], help="Action to perform: 'encode' or 'decode'.")
    parser.add_argument("message", help="The message string to process.")
    parser.add_argument("keyword", help="The keyword to use for generating the cipher map.")
    
    args = parser.parse_args()
    
    if args.action == "encode":
        result = encode(args.message, args.keyword)
        print(f"Original: {args.message}")
        print(f"Encoded:  {result}")
    elif args.action == "decode":
        result = decode(args.message, args.keyword)
        print(f"Original: {args.message}")
        print(f"Decoded:  {result}")

if __name__ == "__main__":
    main()
