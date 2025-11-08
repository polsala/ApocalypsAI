import re

# Define the dictionary for encoding common wasteland terms.
# Keys are full terms, values are 3-letter codes.
ENCODE_DICT = {
    "DANGER": "DGR", "WATER": "WTR", "FOOD": "FOD", "SAFE": "SAF", "HELP": "HLP",
    "BASE": "BAS", "NORTH": "NRT", "SOUTH": "SUT", "EAST": "EST", "WEST": "WST",
    "SCOUT": "SCT", "MESSAGE": "MSG", "OVER": "OVR", "OUT": "OUT", "SUPPLIES": "SPL",
    "ENEMY": "ENY", "FRIENDLY": "FRN", "RENDEZVOUS": "RDV", "LOCATION": "LOC",
    "RADIO": "RDO", "SIGNAL": "SGN", "CLEAR": "CLR", "UNKNOWN": "UKN", "WAIT": "WAI"
}

# Create the inverse dictionary for decoding.
DECODE_DICT = {v: k for k, v in ENCODE_DICT.items()}

def _normalize_message(message: str) -> str:
    """Normalizes the message by converting to uppercase and removing non-alphanumeric characters, except spaces."""
    message = message.upper()
    # Remove any character that is not a letter, number, or space
    message = re.sub(r'[^A-Z0-9\s]', '', message)
    # Replace multiple spaces with a single space
    message = re.sub(r'\s+', ' ', message).strip()
    return message

def encode_message(original_message: str) -> str:
    """Encodes a message using the Wasteland Whisperer dictionary.

    Args:
        original_message: The message string to encode.

    Returns:
        The encoded message string.
    """
    normalized_message = _normalize_message(original_message)
    if not normalized_message:
        return ""

    words = normalized_message.split()
    encoded_words = []
    for word in words:
        # Check if the word is in the dictionary
        encoded_words.append(ENCODE_DICT.get(word, word))

    return ' '.join(encoded_words)

def decode_message(encoded_message: str) -> str:
    """Decodes a message encoded with the Wasteland Whisperer dictionary.

    Args:
        encoded_message: The encoded message string to decode.

    Returns:
        The decoded message string.
    """
    normalized_message = _normalize_message(encoded_message)
    if not normalized_message:
        return ""

    words = normalized_message.split()
    decoded_words = []
    for word in words:
        decoded_words.append(DECODE_DICT.get(word, word))

    return ' '.join(decoded_words)

if __name__ == '__main__':
    print("--- Wasteland Whisperer Encoder Demo ---")

    # Example 1: Encoding
    msg1_orig = "DANGER! Enemy spotted near the WATER source. Proceed with caution to BASE NORTH."
    msg1_enc = encode_message(msg1_orig)
    print(f"\nOriginal:  {msg1_orig}")
    print(f"Encoded:   {msg1_enc}")
    msg1_dec = decode_message(msg1_enc)
    print(f"Decoded:   {msg1_dec}")
    assert msg1_dec == "DANGER ENEMY SPOTTED NEAR THE WATER SOURCE PROCEED WITH CAUTION TO BASE NORTH"

    # Example 2: Decoding
    msg2_enc = "HLP FRN SGN UKN LOC OVR"
    msg2_dec = decode_message(msg2_enc)
    print(f"\nEncoded:   {msg2_enc}")
    print(f"Decoded:   {msg2_dec}")
    msg2_orig = encode_message(msg2_dec)
    print(f"Re-encoded: {msg2_orig}")
    assert msg2_orig == "HLP FRN SGN UKN LOC OVR"

    # Example 3: Empty message
    msg3_orig = ""
    msg3_enc = encode_message(msg3_orig)
    print(f"\nOriginal:  '{msg3_orig}'")
    print(f"Encoded:   '{msg3_enc}'")
    assert msg3_enc == ""

    # Example 4: Message with only non-dictionary words
    msg4_orig = "HELLO WORLD THIS IS A TEST"
    msg4_enc = encode_message(msg4_orig)
    print(f"\nOriginal:  {msg4_orig}")
    print(f"Encoded:   {msg4_enc}")
    assert msg4_enc == "HELLO WORLD THIS IS A TEST"

    # Example 5: Message with mixed case and punctuation
    msg5_orig = "wAtEr sUpPlIeS lOw! rDv aT bAsE nOrTh."
    msg5_enc = encode_message(msg5_orig)
    print(f"\nOriginal:  {msg5_orig}")
    print(f"Encoded:   {msg5_enc}")
    assert msg5_enc == "WTR SPL LOW RDV AT BAS NRT"
    msg5_dec = decode_message(msg5_enc)
    print(f"Decoded:   {msg5_dec}")
    assert msg5_dec == "WATER SUPPLIES LOW RENDEZVOUS AT BASE NORTH"

    print("\nAll demo assertions passed!")
