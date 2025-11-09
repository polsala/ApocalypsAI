import argparse

def caesar_cipher(text, shift, encode=True):
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            start = ord('a')
            shifted_char = chr(((ord(char) - start + shift * (1 if encode else -1)) % 26) + start)
            result.append(shifted_char)
        elif 'A' <= char <= 'Z':
            start = ord('A')
            shifted_char = chr(((ord(char) - start + shift * (1 if encode else -1)) % 26) + start)
            result.append(shifted_char)
        else:
            result.append(char) # Non-alphabetic characters are unchanged
    return "".join(result)

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Whisperer: Encode or decode messages using a simple Caesar cipher."
    )
    parser.add_argument("action", choices=["encode", "decode"], help="Action to perform: 'encode' or 'decode'.")
    parser.add_argument("message", help="The message to process.")
    parser.add_argument("shift", type=int, help="The integer shift key for the cipher.")

    args = parser.parse_args()

    if args.action == "encode":
        output = caesar_cipher(args.message, args.shift, encode=True)
        print(f"Encoded message: {output}")
    else: # decode
        output = caesar_cipher(args.message, args.shift, encode=False)
        print(f"Decoded message: {output}")

if __name__ == "__main__":
    main()
