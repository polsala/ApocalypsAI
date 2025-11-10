import argparse

# Character to numeric code mapping
CHAR_TO_CODE = {
    'A': '01', 'B': '02', 'C': '03', 'D': '04', 'E': '05',
    'F': '06', 'G': '07', 'H': '08', 'I': '09', 'J': '10',
    'K': '11', 'L': '12', 'M': '13', 'N': '14', 'O': '15',
    'P': '16', 'Q': '17', 'R': '18', 'S': '19', 'T': '20',
    'U': '21', 'V': '22', 'W': '23', 'X': '24', 'Y': '25',
    'Z': '26',
    '0': '27', '1': '28', '2': '29', '3': '30', '4': '31',
    '5': '32', '6': '33', '7': '34', '8': '35', '9': '36',
    ' ': '37', '.': '38', ',': '39', '!': '40', '?': '41'
}

# Numeric code to character mapping (inverse of CHAR_TO_CODE)
CODE_TO_CHAR = {v: k for k, v in CHAR_TO_CODE.items()}

DELIMITER = '-'
CHECKSUM_DELIMITER = '##'

def calculate_checksum(numeric_codes: list[str]) -> int:
    """Calculates a simple sum-of-digits checksum from a list of numeric codes."""
    total_sum = 0
    for code in numeric_codes:
        try:
            total_sum += int(code)
        except ValueError:
            # Ignore non-numeric parts, as they might be malformed or empty strings from split
            pass
    return total_sum

def encode_message(message: str) -> str:
    """Encodes a string message into a numeric sequence with a checksum."""
    encoded_parts = []
    for char in message.upper(): # Convert to uppercase to match mapping
        code = CHAR_TO_CODE.get(char)
        if code:
            encoded_parts.append(code)
    
    if not encoded_parts:
        return ""

    checksum = calculate_checksum(encoded_parts)
    return DELIMITER.join(encoded_parts) + CHECKSUM_DELIMITER + str(checksum)

def decode_message(encoded_string: str) -> tuple[str, bool, int, int]:
    """Decodes a numeric sequence and verifies its checksum.

    Returns: (decoded_message, is_checksum_ok, expected_checksum, actual_checksum)
    """
    parts_str = encoded_string
    expected_checksum = -1 # Default to -1 to indicate no checksum provided or invalid format
    actual_checksum = 0
    is_checksum_ok = False

    if CHECKSUM_DELIMITER in encoded_string:
        parts_str, checksum_str = encoded_string.split(CHECKSUM_DELIMITER, 1)
        try:
            expected_checksum = int(checksum_str)
        except ValueError:
            # Invalid checksum format, expected_checksum remains -1
            pass

    numeric_codes = parts_str.split(DELIMITER) if parts_str else []
    
    decoded_chars = []
    for code in numeric_codes:
        if not code: # Handle empty strings from split, e.g., "-01" or "01-"
            continue
        char = CODE_TO_CHAR.get(code)
        if char:
            decoded_chars.append(char)
        else:
            # If a code is unknown, represent it as a placeholder
            decoded_chars.append('[?]') 

    actual_checksum = calculate_checksum(numeric_codes)
    
    if expected_checksum != -1:
        is_checksum_ok = (expected_checksum == actual_checksum)
    
    return "".join(decoded_chars), is_checksum_ok, expected_checksum, actual_checksum

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Whisperer Encoder/Decoder for robust, low-bandwidth messages."
    )
    parser.add_argument(
        "-e", "--encode", type=str, help="Message to encode."
    )
    parser.add_argument(
        "-d", "--decode", type=str, help="Encoded string to decode."
    )

    args = parser.parse_args()

    if args.encode:
        encoded = encode_message(args.encode)
        print(f"Encoded: {encoded}")
    elif args.decode:
        decoded_msg, is_ok, expected_cs, actual_cs = decode_message(args.decode)
        status = "OK" if is_ok else "MISMATCH!"
        
        if expected_cs == -1 and CHECKSUM_DELIMITER not in args.decode:
            print(f"Decoded: {decoded_msg} (No checksum provided in encoded string)")
        elif expected_cs == -1:
            print(f"Decoded: {decoded_msg} (Invalid checksum format in encoded string)")
        else:
            print(f"Decoded: {decoded_msg} (Checksum {status} Expected {expected_cs}, Got {actual_cs})")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
