import sys
import string

def _generate_cipher_map(keyword: str) -> tuple[dict[str, str], dict[str, str]]:
    """
    Generates forward and reverse substitution maps based on a keyword.
    The keyword is used to create a shuffled alphabet.
    """
    keyword = keyword.upper()
    
    # Build the unique characters from the keyword
    cipher_alphabet_list = []
    for char in keyword:
        if char.isalpha() and char not in cipher_alphabet_list:
            cipher_alphabet_list.append(char)
    
    # Append remaining alphabet characters
    for char_code in range(ord('A'), ord('Z') + 1):
        char = chr(char_code)
        if char not in cipher_alphabet_list:
            cipher_alphabet_list.append(char)
            
    cipher_alphabet = "".join(cipher_alphabet_list)
    
    # Standard alphabet
    std_alphabet = string.ascii_uppercase
    
    if len(std_alphabet) != len(cipher_alphabet):
        raise ValueError("Cipher alphabet generation failed: lengths do not match standard alphabet.")

    forward_map = {std_alphabet[i]: cipher_alphabet[i] for i in range(26)}
    reverse_map = {cipher_alphabet[i]: std_alphabet[i] for i in range(26)}
    
    return forward_map, reverse_map

def encrypt(text: str, keyword: str) -> str:
    """
    Encrypts a message using a keyword-based substitution cipher.
    Non-alphabetic characters are preserved. Case is preserved for encrypted letters.
    """
    if not keyword:
        return text # No encryption if no keyword

    forward_map, _ = _generate_cipher_map(keyword)
    
    encrypted_chars = []
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            mapped_char = forward_map.get(char.upper(), char.upper()) # Fallback to original if not in map (shouldn't happen for A-Z)
            encrypted_chars.append(mapped_char if is_upper else mapped_char.lower())
        else:
            encrypted_chars.append(char)
            
    return "".join(encrypted_chars)

def decrypt(text: str, keyword: str) -> str:
    """
    Decrypts a message using a keyword-based substitution cipher.
    Non-alphabetic characters are preserved. Case is preserved for decrypted letters.
    """
    if not keyword:
        return text # No decryption if no keyword

    _, reverse_map = _generate_cipher_map(keyword)
    
    decrypted_chars = []
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            mapped_char = reverse_map.get(char.upper(), char.upper()) # Fallback to original if not in map
            decrypted_chars.append(mapped_char if is_upper else mapped_char.lower())
        else:
            decrypted_chars.append(char)
            
    return "".join(decrypted_chars)

def main():
    if len(sys.argv) < 4:
        print("Usage: python src/encryptor.py <encrypt|decrypt> <message> <keyword>")
        sys.exit(1)

    action = sys.argv[1].lower()
    message = sys.argv[2]
    keyword = sys.argv[3]

    if action == "encrypt":
        result = encrypt(message, keyword)
        print(result)
    elif action == "decrypt":
        result = decrypt(message, keyword)
        print(result)
    else:
        print(f"Invalid action: {action}. Must be 'encrypt' or 'decrypt'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
