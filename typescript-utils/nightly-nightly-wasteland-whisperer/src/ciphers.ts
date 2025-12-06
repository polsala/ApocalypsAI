export type CipherType = 'caesar' | 'atbash';

/**
 * Decodes a message using the Caesar cipher.
 * @param text The text to decode.
 * @param shift The shift value (positive for right shift, negative for left shift).
 * @returns The decoded text.
 */
export function caesarCipher(text: string, shift: number): string {
  return text.split('').map(char => {
    const charCode = char.charCodeAt(0);
    // Handle uppercase letters
    if (charCode >= 65 && charCode <= 90) {
      return String.fromCharCode(((charCode - 65 - shift + 26) % 26) + 65);
    }
    // Handle lowercase letters
    if (charCode >= 97 && charCode <= 122) {
      return String.fromCharCode(((charCode - 97 - shift + 26) % 26) + 97);
    }
    // Return non-alphabetic characters as is
    return char;
  }).join('');
}

/**
 * Decodes a message using the Atbash cipher.
 * @param text The text to decode.
 * @returns The decoded text.
 */
export function atbashCipher(text: string): string {
  return text.split('').map(char => {
    const charCode = char.charCodeAt(0);
    // Handle uppercase letters
    if (charCode >= 65 && charCode <= 90) {
      return String.fromCharCode(90 - (charCode - 65));
    }
    // Handle lowercase letters
    if (charCode >= 97 && charCode <= 122) {
      return String.fromCharCode(122 - (charCode - 97));
    }
    // Return non-alphabetic characters as is
    return char;
  }).join('');
}

/**
 * Decodes a message based on the specified cipher type.
 * @param cipherType The type of cipher to use ('caesar' or 'atbash').
 * @param message The message string to decode.
 * @param shift Optional shift value for Caesar cipher.
 * @returns The decoded message.
 * @throws Error if an unknown cipher type is provided or required parameters are missing.
 */
export function decode(cipherType: CipherType, message: string, shift?: number): string {
  switch (cipherType) {
    case 'caesar':
      if (shift === undefined) {
        throw new Error('Caesar cipher requires a shift value.');
      }
      return caesarCipher(message, shift);
    case 'atbash':
      return atbashCipher(message);
    default:
      throw new Error(`Unknown cipher type: ${cipherType}`);
  }
}
